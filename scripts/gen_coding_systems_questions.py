"""
Generate 600-question bank for Coding Systems.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).

Topics covered:
- Numeric codes (sequential, block, significant-digit)
- Alphabetic codes (mnemonic, substitution/shifted alphabet)
- Alphanumeric codes (structured multi-segment government codes)
- Classification codes (hierarchical numeric)
- Encoding (information → code)
- Decoding (code → information)
- Error detection in coded data
- Code type identification
"""
import json
import random
import os
import string

random.seed(42)

# ============================================================
# DATA POOLS
# ============================================================

# Division codes for alphanumeric encoding/decoding
DIVISIONS = {
    "ADM": "Administrative Division",
    "FIN": "Finance Division",
    "HRD": "Human Resources Division",
    "OPS": "Operations Division",
    "LEG": "Legal Division",
    "PRO": "Procurement Division",
    "REC": "Records Division",
    "ICT": "ICT Division",
    "PLN": "Planning Division",
    "GAD": "Gender and Development Division",
}

# Action/document type codes
ACTIONS = {
    "IC": "Incoming Correspondence",
    "OC": "Outgoing Correspondence",
    "MO": "Memorandum Order",
    "AP": "Appointment",
    "DV": "Disbursement Voucher",
    "PO": "Purchase Order",
    "SO": "Special Order",
    "OO": "Office Order",
    "TO": "Travel Order",
    "LR": "Leave Request",
}

# Agency codes
AGENCIES = {
    "CSC": "Civil Service Commission",
    "COA": "Commission on Audit",
    "DBM": "Department of Budget and Management",
    "DILG": "Department of the Interior and Local Government",
    "DOH": "Department of Health",
    "DOLE": "Department of Labor and Employment",
    "DPWH": "Department of Public Works and Highways",
    "DepEd": "Department of Education",
    "DOJ": "Department of Justice",
    "DSWD": "Department of Social Welfare and Development",
}

# Document type codes (for agency-level coding)
DOC_TYPES = {
    "MC": "Memorandum Circular",
    "EO": "Executive Order",
    "AO": "Administrative Order",
    "SO": "Special Order",
    "OO": "Office Order",
    "DO": "Department Order",
    "MO": "Memorandum Order",
    "JC": "Joint Circular",
}

# Classification scheme (hierarchical numeric)
CLASSIFICATION_SCHEME = {
    "100": "Administrative Records",
    "110": "Organization and Management",
    "111": "Office Orders",
    "112": "Memoranda",
    "113": "Organizational Charts",
    "114": "Minutes of Meetings",
    "120": "Personnel Administration",
    "121": "Appointments",
    "122": "Leave Records",
    "123": "Training Records",
    "124": "Performance Evaluations",
    "125": "Service Records",
    "130": "Property and Supply",
    "131": "Equipment Inventory",
    "132": "Supply Requisitions",
    "200": "Financial Records",
    "210": "Budget",
    "211": "Annual Budget Proposals",
    "212": "Allotment Releases",
    "213": "Supplemental Budgets",
    "220": "Disbursements",
    "221": "Salary Vouchers",
    "222": "Travel Vouchers",
    "223": "Petty Cash Vouchers",
    "224": "Utility Payments",
    "230": "Collections and Revenue",
    "231": "Collection Reports",
    "232": "Revenue Summaries",
    "300": "Legal Records",
    "310": "Contracts and Agreements",
    "311": "Service Contracts",
    "312": "MOAs and MOUs",
    "313": "Lease Contracts",
    "320": "Cases and Opinions",
    "321": "Administrative Cases",
    "322": "Legal Opinions",
    "400": "Correspondence",
    "410": "Incoming Communications",
    "411": "Letters from Citizens",
    "412": "Letters from Agencies",
    "420": "Outgoing Communications",
    "421": "Reply Letters",
    "422": "Endorsement Letters",
}

# Block numeric ranges for employee IDs
BLOCK_RANGES = [
    ((1000, 1999), "Administrative Division"),
    ((2000, 2999), "Finance Division"),
    ((3000, 3999), "Operations Division"),
    ((4000, 4999), "Legal Division"),
    ((5000, 5999), "Human Resources Division"),
    ((6000, 6999), "ICT Division"),
    ((7000, 7999), "Planning Division"),
    ((8000, 8999), "Procurement Division"),
]

# Significant-digit code structures
FUND_SOURCES = {1: "General Fund", 2: "Special Fund", 3: "Trust Fund", 4: "Revolving Fund"}
SIG_DIVISIONS = {1: "Administrative", 2: "Finance", 3: "Operations", 4: "Legal", 5: "HR"}
EXPENSE_CATS = {1: "Personnel Services", 2: "MOOE", 3: "Capital Outlay"}

# Employment status codes (letter-based significant positions)
EMPLOYMENT_TYPE = {"R": "Regular", "C": "Contractual", "J": "Job Order", "E": "Elected"}
SCHEDULE_TYPE = {"F": "Full-time", "H": "Half-time", "P": "Part-time"}
TENURE_TYPE = {"P": "Permanent", "T": "Temporary", "C": "Coterminous"}

# Priority codes
PRIORITY_CODES = {"A": "Urgent", "B": "Normal", "C": "Low", "D": "Routine"}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_question(qid, difficulty, question, choices, answer, explanation, tags):
    """Create a question dict in the standard format."""
    # Ensure no duplicate choices while maintaining answer
    seen = set()
    unique_choices = []
    for c in choices:
        if c not in seen:
            seen.add(c)
            unique_choices.append(c)
    if answer not in seen:
        unique_choices.insert(0, answer)
        seen.add(answer)
    # If we lost choices due to dedup, generate filler alternatives
    filler_idx = 1
    while len(unique_choices) < 4:
        # Create a distinct filler that won't match the answer
        filler = f"None of the above ({filler_idx})" if filler_idx > 1 else "None of the above"
        if filler not in seen:
            unique_choices.append(filler)
            seen.add(filler)
        filler_idx += 1
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Indexing and Record Organization",
        "subtopic": "Coding Systems",
        "difficulty": difficulty,
        "question": question,
        "choices": unique_choices[:4],
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English",
    }


def shift_letter(ch, shift):
    """Shift a letter by n positions (wraps around Z→A)."""
    if ch.upper() in string.ascii_uppercase:
        base = ord('A')
        return chr((ord(ch.upper()) - base + shift) % 26 + base)
    return ch


def shift_word(word, shift):
    """Shift all letters in a word."""
    return "".join(shift_letter(c, shift) for c in word)


def reverse_alphabet(ch):
    """Reverse alphabet substitution: A↔Z, B↔Y, etc."""
    if ch.upper() in string.ascii_uppercase:
        return chr(ord('Z') - (ord(ch.upper()) - ord('A')))
    return ch


def reverse_word(word):
    """Apply reverse alphabet to all letters."""
    return "".join(reverse_alphabet(c) for c in word)


# Words suitable for encoding/decoding exercises
ENCODE_WORDS_3 = ["ACE", "AID", "BAD", "BIG", "CAB", "COP", "DIG", "DIM", "ELF",
                  "FIG", "FIN", "GAP", "GEM", "HID", "HOP", "ICE", "INK", "JAM",
                  "JOB", "KEY", "KIN", "LAP", "LOG", "MAP", "MIX", "NAP", "NET",
                  "OAK", "ODD", "PAN", "PIG", "RAG", "RIM", "SAP", "SIP", "TAP",
                  "TIN", "VAN", "VET", "WAR", "WIG", "YAM", "ZAP", "ZIP", "COD"]

ENCODE_WORDS_4 = ["AIDE", "BACK", "BAND", "CAGE", "CARD", "DARE", "DESK", "EDIT",
                  "FACE", "FILE", "FORM", "GAIN", "GRID", "HALF", "HAND", "IDEA",
                  "ITEM", "JACK", "JUMP", "KEEP", "KING", "LAMP", "LAND", "MAIL",
                  "MARK", "NAME", "NODE", "OPEN", "PACK", "PAGE", "RANK", "RISK",
                  "SAFE", "SEAL", "SIGN", "TASK", "TERM", "UNIT", "VAST", "VOTE",
                  "WAGE", "WARD", "WORK", "YEAR", "ZONE", "MEMO", "CODE", "PLAN"]

ENCODE_WORDS_5 = ["BADGE", "BRIEF", "CHAIR", "CLAIM", "CLERK", "COVER", "DRAFT",
                  "ENTRY", "FILED", "FORMS", "GRANT", "INDEX", "JUDGE", "LABOR",
                  "LEGAL", "MERIT", "NOTED", "ORDER", "PANEL", "PRINT", "QUOTA",
                  "RANGE", "STAMP", "TRACK", "VALID", "WRITE", "AUDIT", "BOARD",
                  "CHIEF", "FUNDS", "LEAVE", "MINOR", "OFFER", "PRIME", "RULES",
                  "SCORE", "SHIFT", "STAFF", "TERMS", "UNION", "VALUE", "WORKS"]


# ============================================================
# EASY QUESTIONS (IDs 1-200)
# ============================================================

def generate_easy_questions():
    """Generate 200 Easy questions. Single-step encoding/decoding, basic concepts."""
    questions = []
    qid = 1

    # --- Type 1: Concept/definition questions (30 questions) ---
    concept_qs = [
        ("What is a coding system in records management?",
         ["A set of rules that maps information to symbols for standardized representation",
          "A method of encrypting classified documents",
          "A way to arrange files alphabetically",
          "A system for counting documents in an office"],
         "A set of rules that maps information to symbols for standardized representation",
         "A coding system assigns symbols (numbers, letters, or both) to represent information in condensed, standardized form.",
         ["definition", "concept"]),
        ("What is encoding in a coding system?",
         ["Converting information into coded form using a code key",
          "Converting coded form back into information",
          "Creating a new code key from scratch",
          "Memorizing all possible codes"],
         "Converting information into coded form using a code key",
         "Encoding is the process of converting plain information INTO a code using the code key.",
         ["definition", "encoding"]),
        ("What is decoding in a coding system?",
         ["Converting coded form back into information using a code key",
          "Converting information into coded form",
          "Destroying coded documents",
          "Creating a backup of coded data"],
         "Converting coded form back into information using a code key",
         "Decoding is the process of converting a code BACK into its original information using the code key.",
         ["definition", "decoding"]),
        ("What is a code key?",
         ["A reference table that defines what each symbol represents",
          "A physical key that unlocks a filing cabinet",
          "The first document in a filing system",
          "A password for accessing digital records"],
         "A reference table that defines what each symbol represents",
         "A code key is the reference table showing the mapping between symbols and the information they represent.",
         ["definition", "code-key"]),
        ("Which type of code uses only digits (0-9)?",
         ["Numeric code", "Alphabetic code", "Alphanumeric code", "Classification code"],
         "Numeric code",
         "Numeric codes use only digits (0-9) to represent information.",
         ["code-type", "numeric"]),
        ("Which type of code uses only letters (A-Z)?",
         ["Alphabetic code", "Numeric code", "Alphanumeric code", "Sequential code"],
         "Alphabetic code",
         "Alphabetic codes use only letters (A-Z) to represent information.",
         ["code-type", "alphabetic"]),
        ("Which type of code combines letters and numbers?",
         ["Alphanumeric code", "Numeric code", "Alphabetic code", "Binary code"],
         "Alphanumeric code",
         "Alphanumeric codes combine letters (for categories) and numbers (for specifics).",
         ["code-type", "alphanumeric"]),
        ("What type of numeric code assigns numbers in order (0001, 0002, 0003...)?",
         ["Sequential numeric code", "Block numeric code", "Significant-digit code", "Classification code"],
         "Sequential numeric code",
         "Sequential codes assign numbers in order as items are added — the number carries no category meaning.",
         ["code-type", "sequential"]),
        ("What type of numeric code reserves number ranges for categories?",
         ["Block numeric code", "Sequential numeric code", "Significant-digit code", "Mnemonic code"],
         "Block numeric code",
         "Block codes reserve ranges (e.g., 1000-1999 = Admin, 2000-2999 = Finance) for categories.",
         ["code-type", "block"]),
        ("In a significant-digit code, what does each digit position represent?",
         ["A specific category or attribute",
          "A quantity or amount",
          "The document's page number",
          "The order in which it was filed"],
         "A specific category or attribute",
         "In significant-digit codes, each position encodes a category identifier, not a quantity.",
         ["code-type", "significant-digit"]),
        ("What is the relationship between encoding and decoding?",
         ["They are inverse operations — decoding reverses encoding",
          "They are the same operation applied twice",
          "Encoding is faster than decoding",
          "Decoding creates a new code"],
         "They are inverse operations — decoding reverses encoding",
         "Encoding and decoding are inverses: if encoding shifts +3, decoding shifts -3.",
         ["concept", "inverse-operations"]),
        ("What does 'ADM' typically represent in Philippine government codes?",
         ["Administrative Division", "Admissions Office", "Advanced Management", "Audit Department"],
         "Administrative Division",
         "ADM is the standard mnemonic abbreviation for Administrative Division in government coding.",
         ["philippine-context", "mnemonic"]),
        ("What does 'FIN' typically represent in government office codes?",
         ["Finance Division", "Final Report", "Finding Section", "First Notice"],
         "Finance Division",
         "FIN is the standard mnemonic abbreviation for Finance Division.",
         ["philippine-context", "mnemonic"]),
        ("What does 'MC' stand for in Philippine government document codes?",
         ["Memorandum Circular", "Management Committee", "Monthly Calendar", "Main Copy"],
         "Memorandum Circular",
         "MC is the standard code for Memorandum Circular in Philippine government documents.",
         ["philippine-context", "document-type"]),
        ("What is CS Form 212?",
         ["Personal Data Sheet", "Daily Time Record", "Leave Application", "Travel Order"],
         "Personal Data Sheet",
         "CS Form 212 is the Personal Data Sheet used in Philippine government personnel records.",
         ["philippine-context", "cs-forms"]),
        ("What is CS Form 48?",
         ["Daily Time Record", "Personal Data Sheet", "Appointment Form", "Leave Application"],
         "Daily Time Record",
         "CS Form 48 is the Daily Time Record (DTR) used to track employee attendance.",
         ["philippine-context", "cs-forms"]),
        ("What is CS Form 6?",
         ["Application for Leave", "Personal Data Sheet", "Daily Time Record", "Performance Rating"],
         "Application for Leave",
         "CS Form 6 is the standard Application for Leave form in Philippine government.",
         ["philippine-context", "cs-forms"]),
        ("In the code 'ADM-IC-2024-0153', what does the hyphen serve as?",
         ["A separator between code segments",
          "A minus sign indicating subtraction",
          "A placeholder for missing data",
          "An indicator of confidential status"],
         "A separator between code segments",
         "Hyphens in alphanumeric codes separate distinct segments that are decoded independently.",
         ["alphanumeric", "structure"]),
        ("How many segments does the code 'FIN-DV-2024-0321' have?",
         ["Four", "Three", "Five", "Two"],
         "Four",
         "The code has four segments separated by hyphens: FIN, DV, 2024, and 0321.",
         ["alphanumeric", "structure"]),
        ("What does a mnemonic alphabetic code use to aid memory?",
         ["Letters that abbreviate or hint at what they represent",
          "Random letter combinations",
          "Only vowels",
          "Letters arranged in reverse alphabetical order"],
         "Letters that abbreviate or hint at what they represent",
         "Mnemonic codes use letters that remind the user of their meaning (e.g., ADM = Administrative).",
         ["code-type", "mnemonic"]),
    ]

    for q_data in concept_qs[:20]:
        question_text, choices, answer, explanation, tags = q_data
        questions.append(make_question(qid, "Easy", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Type 2: Simple alphanumeric decoding (40 questions) ---
    div_keys = list(DIVISIONS.keys())
    act_keys = list(ACTIONS.keys())
    for _ in range(40):
        div_code = random.choice(div_keys)
        act_code = random.choice(act_keys)
        year = random.choice([2023, 2024, 2025])
        seq = random.randint(1, 500)
        full_code = f"{div_code}-{act_code}-{year}-{seq:04d}"

        correct = f"{DIVISIONS[div_code]}, {ACTIONS[act_code]}, Year {year}, Document #{seq}"

        # Generate wrong answers
        wrong_divs = [d for d in div_keys if d != div_code]
        wrong_acts = [a for a in act_keys if a != act_code]
        wrong1 = f"{DIVISIONS[random.choice(wrong_divs)]}, {ACTIONS[act_code]}, Year {year}, Document #{seq}"
        wrong2 = f"{DIVISIONS[div_code]}, {ACTIONS[random.choice(wrong_acts)]}, Year {year}, Document #{seq}"
        wrong3 = f"{DIVISIONS[random.choice(wrong_divs)]}, {ACTIONS[random.choice(wrong_acts)]}, Year {year}, Document #{seq}"

        choices = [correct, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f"Using the standard government code key, decode: {full_code}",
            choices, correct,
            f"{div_code} = {DIVISIONS[div_code]}, {act_code} = {ACTIONS[act_code]}, {year} = Year {year}, {seq:04d} = Document #{seq}.",
            ["alphanumeric", "decoding"]
        ))
        qid += 1

    # --- Type 3: Simple alphanumeric encoding (40 questions) ---
    for _ in range(40):
        div_code = random.choice(div_keys)
        act_code = random.choice(act_keys)
        year = random.choice([2023, 2024, 2025])
        seq = random.randint(1, 500)

        description = f"{DIVISIONS[div_code]}, {ACTIONS[act_code]}, Year {year}, Document #{seq}"
        correct_code = f"{div_code}-{act_code}-{year}-{seq:04d}"

        # Wrong codes
        wrong_divs = [d for d in div_keys if d != div_code]
        wrong_acts = [a for a in act_keys if a != act_code]
        wrong1 = f"{random.choice(wrong_divs)}-{act_code}-{year}-{seq:04d}"
        wrong2 = f"{div_code}-{random.choice(wrong_acts)}-{year}-{seq:04d}"
        wrong3 = f"{random.choice(wrong_divs)}-{random.choice(wrong_acts)}-{year}-{seq:04d}"

        choices = [correct_code, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f"Encode the following using the standard code structure [Division]-[Action]-[Year]-[Sequence]: {description}",
            choices, correct_code,
            f"{DIVISIONS[div_code]} = {div_code}, {ACTIONS[act_code]} = {act_code}, Year {year}, Document #{seq} = {seq:04d}.",
            ["alphanumeric", "encoding"]
        ))
        qid += 1

    # --- Type 4: Block numeric code identification (30 questions) ---
    for _ in range(30):
        range_info, division = random.choice(BLOCK_RANGES)
        emp_id = random.randint(range_info[0], range_info[1])

        wrong_divisions = [d for _, d in BLOCK_RANGES if d != division]
        wrong_choices = random.sample(wrong_divisions, 3)

        choices = [division] + wrong_choices
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f"In a block numeric coding system where ranges are assigned to divisions, employee ID {emp_id} (range {range_info[0]}-{range_info[1]}) belongs to which division?",
            choices, division,
            f"Employee ID {emp_id} falls in the {range_info[0]}-{range_info[1]} range, which is assigned to {division}.",
            ["block-numeric", "decoding"]
        ))
        qid += 1

    # --- Type 5: Simple classification code decoding (30 questions) ---
    three_digit_codes = [k for k in CLASSIFICATION_SCHEME.keys() if len(k) == 3 and k[2] != '0']
    for _ in range(30):
        code = random.choice(three_digit_codes)
        correct_name = CLASSIFICATION_SCHEME[code]

        # Get parent for explanation
        parent_code = code[:2] + "0"
        grandparent_code = code[0] + "00"
        parent_name = CLASSIFICATION_SCHEME.get(parent_code, "")
        grandparent_name = CLASSIFICATION_SCHEME.get(grandparent_code, "")

        # Wrong answers from same level
        wrong_codes = [k for k in three_digit_codes if k != code]
        wrong_names = [CLASSIFICATION_SCHEME[k] for k in random.sample(wrong_codes, min(3, len(wrong_codes)))]

        choices = [correct_name] + wrong_names[:3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f"In the Records Disposition Schedule, what does classification code '{code}' represent?",
            choices, correct_name,
            f"Code {code}: {grandparent_name} ({grandparent_code}) → {parent_name} ({parent_code}) → {correct_name} ({code}).",
            ["classification-code", "decoding"]
        ))
        qid += 1

    # --- Type 6: Simple letter shift encoding (30 questions) ---
    for _ in range(30):
        shift = random.choice([1, 2, 3])
        word = random.choice(ENCODE_WORDS_3)
        encoded = shift_word(word, shift)

        # Wrong answers with different shifts
        wrong1 = shift_word(word, shift + 1)
        wrong2 = shift_word(word, shift - 1) if shift > 1 else shift_word(word, shift + 2)
        wrong3 = shift_word(word, shift + 2)

        choices = [encoded, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f"Using a +{shift} letter shift, encode the word: {word}",
            choices, encoded,
            f"Each letter shifts forward by {shift}: {' → '.join(f'{c}→{shift_letter(c, shift)}' for c in word)} = {encoded}.",
            ["letter-shift", "encoding"]
        ))
        qid += 1

    # --- Type 7: Simple letter shift decoding with small shifts (10 questions) ---
    for _ in range(10):
        shift = random.choice([1, 2, 3])
        word = random.choice(ENCODE_WORDS_3)
        encoded = shift_word(word, shift)

        # Wrong answers
        wrong1 = shift_word(encoded, -shift + 1) if shift > 1 else shift_word(encoded, -2)
        wrong2 = shift_word(encoded, -shift - 1)
        wrong3 = shift_word(encoded, shift)  # common mistake: shift forward again

        choices = list(set([word, wrong1, wrong2, wrong3]))
        while len(choices) < 4:
            choices.append(shift_word(encoded, -random.randint(1, 5)))
            choices = list(set(choices))
        choices = choices[:4]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f"Using a +{shift} letter shift for encoding, decode: {encoded}",
            choices, word,
            f"To decode, shift each letter BACK by {shift}: {' → '.join(f'{c}→{shift_letter(c, -shift)}' for c in encoded)} = {word}.",
            ["letter-shift", "decoding"]
        ))
        qid += 1

    return questions[:200]


# ============================================================
# MEDIUM QUESTIONS (IDs 201-400)
# ============================================================

def generate_medium_questions():
    """Generate 200 Medium questions. Two-step reasoning, longer codes, shift decoding."""
    questions = []
    qid = 201

    # --- Type 1: Letter shift DECODING (40 questions) ---
    for _ in range(40):
        shift = random.choice([2, 3, 4, 5])
        word = random.choice(ENCODE_WORDS_4)
        encoded = shift_word(word, shift)

        # Wrong answers: decode with wrong shift
        wrong1 = shift_word(encoded, -shift + 1)  # off by 1
        wrong2 = shift_word(encoded, -shift - 1)  # off by 1 other direction
        wrong3 = shift_word(encoded, shift)  # applied encoding again instead of decoding

        choices = [word, wrong1, wrong2, wrong3]
        # Ensure uniqueness
        choices = list(set(choices))
        while len(choices) < 4:
            extra_shift = random.choice([s for s in range(1, 7) if s != shift])
            choices.append(shift_word(encoded, -extra_shift))
            choices = list(set(choices))
        choices = choices[:4]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f"Using a +{shift} letter shift for encoding, decode: {encoded}",
            choices, word,
            f"Decoding reverses the shift: each letter moves back {shift} positions. {encoded} → {word}.",
            ["letter-shift", "decoding"]
        ))
        qid += 1

    # --- Type 2: Significant-digit encoding (30 questions) ---
    for _ in range(30):
        fund = random.choice(list(FUND_SOURCES.keys()))
        div = random.choice(list(SIG_DIVISIONS.keys()))
        exp = random.choice(list(EXPENSE_CATS.keys()))
        item = random.randint(1, 50)

        correct_code = f"{fund}{div}{exp}{item:02d}"
        description = f"{FUND_SOURCES[fund]}, {SIG_DIVISIONS[div]} Division, {EXPENSE_CATS[exp]}, Item #{item}"

        # Wrong codes
        wrong_fund = random.choice([f for f in FUND_SOURCES.keys() if f != fund])
        wrong_div = random.choice([d for d in SIG_DIVISIONS.keys() if d != div])
        wrong_exp = random.choice([e for e in EXPENSE_CATS.keys() if e != exp])

        wrong1 = f"{wrong_fund}{div}{exp}{item:02d}"
        wrong2 = f"{fund}{wrong_div}{exp}{item:02d}"
        wrong3 = f"{fund}{div}{wrong_exp}{item:02d}"

        choices = [correct_code, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f"Using the budget code structure [Fund Source][Division][Expense Category][Item##], encode: {description}",
            choices, correct_code,
            f"Fund: {FUND_SOURCES[fund]}={fund}, Division: {SIG_DIVISIONS[div]}={div}, Expense: {EXPENSE_CATS[exp]}={exp}, Item #{item}={item:02d}.",
            ["significant-digit", "encoding"]
        ))
        qid += 1

    # --- Type 3: Significant-digit decoding (30 questions) ---
    for _ in range(30):
        fund = random.choice(list(FUND_SOURCES.keys()))
        div = random.choice(list(SIG_DIVISIONS.keys()))
        exp = random.choice(list(EXPENSE_CATS.keys()))
        item = random.randint(1, 50)

        code = f"{fund}{div}{exp}{item:02d}"
        correct_desc = f"{FUND_SOURCES[fund]}, {SIG_DIVISIONS[div]} Division, {EXPENSE_CATS[exp]}, Item #{item}"

        # Wrong descriptions
        wrong_fund = random.choice([f for f in FUND_SOURCES.keys() if f != fund])
        wrong_div = random.choice([d for d in SIG_DIVISIONS.keys() if d != div])
        wrong_exp = random.choice([e for e in EXPENSE_CATS.keys() if e != exp])

        wrong1 = f"{FUND_SOURCES[wrong_fund]}, {SIG_DIVISIONS[div]} Division, {EXPENSE_CATS[exp]}, Item #{item}"
        wrong2 = f"{FUND_SOURCES[fund]}, {SIG_DIVISIONS[wrong_div]} Division, {EXPENSE_CATS[exp]}, Item #{item}"
        wrong3 = f"{FUND_SOURCES[fund]}, {SIG_DIVISIONS[div]} Division, {EXPENSE_CATS[wrong_exp]}, Item #{item}"

        choices = [correct_desc, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f"Decode the budget code '{code}' using structure [Fund][Division][Expense][Item##]:",
            choices, correct_desc,
            f"Position 1: {fund}={FUND_SOURCES[fund]}, Position 2: {div}={SIG_DIVISIONS[div]}, Position 3: {exp}={EXPENSE_CATS[exp]}, Positions 4-5: {item:02d}=Item #{item}.",
            ["significant-digit", "decoding"]
        ))
        qid += 1

    # --- Type 4: Classification code encoding (25 questions) ---
    # Given a document description, find the correct classification code
    doc_to_code = [
        ("Office Orders", "111"), ("Memoranda", "112"), ("Organizational Charts", "113"),
        ("Minutes of Meetings", "114"), ("Appointments", "121"), ("Leave Records", "122"),
        ("Training Records", "123"), ("Performance Evaluations", "124"),
        ("Service Records", "125"), ("Equipment Inventory", "131"),
        ("Supply Requisitions", "132"), ("Annual Budget Proposals", "211"),
        ("Allotment Releases", "212"), ("Supplemental Budgets", "213"),
        ("Salary Vouchers", "221"), ("Travel Vouchers", "222"),
        ("Petty Cash Vouchers", "223"), ("Utility Payments", "224"),
        ("Collection Reports", "231"), ("Revenue Summaries", "232"),
        ("Service Contracts", "311"), ("MOAs and MOUs", "312"),
        ("Lease Contracts", "313"), ("Administrative Cases", "321"),
        ("Legal Opinions", "322"), ("Letters from Citizens", "411"),
        ("Letters from Agencies", "412"), ("Reply Letters", "421"),
        ("Endorsement Letters", "422"),
    ]
    random.shuffle(doc_to_code)

    for doc_name, correct_code in doc_to_code[:25]:
        # Wrong codes from same level
        all_codes = [c for _, c in doc_to_code if c != correct_code]
        wrong_codes = random.sample(all_codes, 3)

        choices = [correct_code, wrong_codes[0], wrong_codes[1], wrong_codes[2]]
        random.shuffle(choices)

        parent = CLASSIFICATION_SCHEME.get(correct_code[:2] + "0", "")
        grandparent = CLASSIFICATION_SCHEME.get(correct_code[0] + "00", "")

        questions.append(make_question(
            qid, "Medium",
            f"Using the Records Disposition Schedule, what is the classification code for '{doc_name}'?",
            choices, correct_code,
            f"{doc_name} falls under {grandparent} → {parent} → code {correct_code}.",
            ["classification-code", "encoding"]
        ))
        qid += 1

    # --- Type 5: Code type identification (25 questions) ---
    code_type_scenarios = [
        ("Employee IDs 1000-1999 are assigned to Admin, 2000-2999 to Finance, 3000-3999 to Operations.",
         "Block numeric code", "Number ranges are reserved for specific categories.",
         ["Sequential numeric code", "Significant-digit code", "Alphanumeric code"]),
        ("Documents are numbered 0001, 0002, 0003... in the order received.",
         "Sequential numeric code", "Numbers are assigned in order with no inherent category meaning.",
         ["Block numeric code", "Significant-digit code", "Classification code"]),
        ("Code 'FIN-DV-2024-0321' represents Finance Division, Disbursement Voucher, Year 2024, #321.",
         "Alphanumeric code", "It combines mnemonic letters with numeric identifiers in structured segments.",
         ["Numeric code", "Alphabetic code", "Classification code"]),
        ("Each letter is replaced by the letter 3 positions ahead in the alphabet.",
         "Alphabetic substitution code", "Letters are systematically replaced by other letters according to a fixed shift rule.",
         ["Numeric code", "Alphanumeric code", "Classification code"]),
        ("Code '222' means Financial Records → Disbursements → Travel Vouchers.",
         "Hierarchical classification code", "Each digit position represents a level in the category hierarchy.",
         ["Sequential numeric code", "Block numeric code", "Alphanumeric code"]),
        ("ADM stands for Administrative, FIN for Finance, HRD for Human Resources.",
         "Mnemonic alphabetic code", "Letters are chosen to abbreviate and remind users of what they represent.",
         ["Substitution code", "Sequential code", "Classification code"]),
        ("Position 1 = Fund Source, Position 2 = Division, Position 3 = Expense Category.",
         "Significant-digit code", "Each digit position has a specific assigned meaning.",
         ["Sequential numeric code", "Block numeric code", "Mnemonic code"]),
        ("A=Z, B=Y, C=X... each letter maps to its reverse-alphabet counterpart.",
         "Reverse-alphabet substitution code", "Letters are replaced by their mirror position in the alphabet.",
         ["Shift code", "Numeric code", "Classification code"]),
        ("CSC-MC-2024-005 represents Civil Service Commission, Memorandum Circular #5, Year 2024.",
         "Alphanumeric code", "It uses agency abbreviation + document type + year + sequence number.",
         ["Numeric code", "Alphabetic code", "Block code"]),
        ("Letters A=1, B=2, C=3... Z=26 convert names into numeric form.",
         "Positional numeric substitution code", "Letters are mapped to their position number in the alphabet.",
         ["Shift code", "Block code", "Classification code"]),
    ]

    used_scenarios = set()
    for scenario, correct, explanation, wrong_choices in code_type_scenarios:
        if len(questions) >= 125 + (qid - 201):
            break
        choices = [correct] + wrong_choices
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Medium",
            f"What type of coding system is described? \"{scenario}\"",
            choices, correct, explanation,
            ["code-type-identification"]
        ))
        qid += 1

    # Repeat with variations to fill 25
    more_scenarios = [
        ("Budget codes where the first digit means fund source and the second means division.",
         "Significant-digit code", "Each digit position independently encodes a category.",
         ["Block numeric code", "Sequential code", "Mnemonic code"]),
        ("All documents in the Legal Division get IDs in the 4000-4999 range.",
         "Block numeric code", "A specific number range is reserved for one category.",
         ["Significant-digit code", "Sequential code", "Classification code"]),
        ("The code 'RFP' stands for 'Regular, Full-time, Permanent' where each letter position has meaning.",
         "Significant-position alphabetic code", "Each letter position encodes a different attribute.",
         ["Mnemonic code", "Substitution code", "Sequential code"]),
        ("Documents get codes 100, 110, 111 where each digit level narrows the category.",
         "Hierarchical classification code", "The code structure mirrors a category tree with increasing specificity.",
         ["Block numeric code", "Sequential code", "Alphanumeric code"]),
        ("Each word is encoded by shifting every letter forward by 5 positions.",
         "Shifted-alphabet code", "A fixed shift is applied uniformly to all letters.",
         ["Reverse-alphabet code", "Block code", "Classification code"]),
        ("The code 'HRD-AP-2024-0087' uses abbreviations for division and action type.",
         "Structured alphanumeric code", "It combines mnemonic letter segments with numeric year and sequence.",
         ["Pure numeric code", "Alphabetic substitution code", "Block code"]),
        ("Receipts are numbered R-0001, R-0002, R-0003 in order of issuance.",
         "Sequential alphanumeric code", "A prefix identifies the type, and numbers increment sequentially.",
         ["Block code", "Significant-digit code", "Classification code"]),
        ("Code 'A-2-03' means Administrative → Personnel → Appointments.",
         "Alphanumeric classification code", "Letters identify main class, numbers identify subclass and item.",
         ["Sequential code", "Block code", "Substitution code"]),
    ]

    for scenario, correct, explanation, wrong_choices in more_scenarios:
        if qid > 325:
            break
        choices = [correct] + wrong_choices
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Medium",
            f"Identify the coding system type: \"{scenario}\"",
            choices, correct, explanation,
            ["code-type-identification"]
        ))
        qid += 1

    # --- Type 6: Reverse-alphabet encoding/decoding (25 questions) ---
    for i in range(25):
        word = random.choice(ENCODE_WORDS_4 if i < 15 else ENCODE_WORDS_3)
        encoded = reverse_word(word)

        if i % 2 == 0:
            # Encoding question
            wrong1 = shift_word(word, 1)
            wrong2 = shift_word(word, -1)
            wrong3 = reverse_word(shift_word(word, 1))
            choices = list(set([encoded, wrong1, wrong2, wrong3]))
            while len(choices) < 4:
                choices.append(shift_word(word, random.randint(2, 5)))
                choices = list(set(choices))
            choices = choices[:4]
            random.shuffle(choices)
            questions.append(make_question(
                qid, "Medium",
                f"Using reverse-alphabet substitution (A=Z, B=Y, C=X...), encode: {word}",
                choices, encoded,
                f"Each letter maps to its reverse: {' → '.join(f'{c}→{reverse_alphabet(c)}' for c in word)} = {encoded}.",
                ["reverse-alphabet", "encoding"]
            ))
        else:
            # Decoding question
            wrong1 = shift_word(encoded, 1)
            wrong2 = shift_word(encoded, -1)
            wrong3 = reverse_word(shift_word(word, 1))
            choices = list(set([word, wrong1, wrong2, wrong3]))
            while len(choices) < 4:
                choices.append(shift_word(word, random.randint(1, 4)))
                choices = list(set(choices))
            choices = choices[:4]
            random.shuffle(choices)
            questions.append(make_question(
                qid, "Medium",
                f"Using reverse-alphabet substitution (A=Z, B=Y, C=X...), decode: {encoded}",
                choices, word,
                f"Reverse-alphabet is its own inverse: {' → '.join(f'{c}→{reverse_alphabet(c)}' for c in encoded)} = {word}.",
                ["reverse-alphabet", "decoding"]
            ))
        qid += 1

    # --- Type 7: Letter-to-number substitution (25 questions) ---
    for _ in range(25):
        # Create a random letter-to-number mapping for 10 letters
        letters = random.sample(string.ascii_uppercase[:10], 10)
        numbers = list(range(10))
        random.shuffle(numbers)
        mapping = dict(zip(letters[:10], numbers))

        # Pick a 4-5 letter word from available letters
        word_len = random.choice([3, 4, 5])
        available = [l for l in letters[:10]]
        word_letters = [random.choice(available) for _ in range(word_len)]
        word = "".join(word_letters)
        encoded_num = "".join(str(mapping[l]) for l in word_letters)

        # Build the key display
        key_display = " | ".join(f"{l}={mapping[l]}" for l in sorted(mapping.keys()))

        if random.random() < 0.5:
            # Encode question
            wrong1 = "".join(str((mapping[l] + 1) % 10) for l in word_letters)
            wrong2 = "".join(str((mapping[l] - 1) % 10) for l in word_letters)
            wrong3 = encoded_num[::-1]  # reversed
            choices = list(set([encoded_num, wrong1, wrong2, wrong3]))
            while len(choices) < 4:
                choices.append("".join(str(random.randint(0, 9)) for _ in range(word_len)))
                choices = list(set(choices))
            choices = choices[:4]
            random.shuffle(choices)
            questions.append(make_question(
                qid, "Medium",
                f"Using this code key ({key_display}), encode: {word}",
                choices, encoded_num,
                f"Look up each letter: {' '.join(f'{l}={mapping[l]}' for l in word_letters)} → {encoded_num}.",
                ["letter-number-substitution", "encoding"]
            ))
        else:
            # Decode question
            rev_mapping = {v: k for k, v in mapping.items()}
            wrong1 = "".join(rev_mapping.get((int(d) + 1) % 10, "?") for d in encoded_num)
            wrong2 = "".join(rev_mapping.get((int(d) - 1) % 10, "?") for d in encoded_num)
            wrong3 = word[::-1]
            choices = list(set([word, wrong1, wrong2, wrong3]))
            while len(choices) < 4:
                choices.append("".join(random.choice(available) for _ in range(word_len)))
                choices = list(set(choices))
            choices = choices[:4]
            random.shuffle(choices)
            questions.append(make_question(
                qid, "Medium",
                f"Using this code key ({key_display}), decode: {encoded_num}",
                choices, word,
                "Reverse lookup: " + " ".join(f"{d}={rev_mapping.get(int(d), '?')}" for d in encoded_num) + f" → {word}.",
                ["letter-number-substitution", "decoding"]
            ))
        qid += 1

    # --- Type 8: Employment status code encoding/decoding (20 questions) ---
    while len(questions) < 200:
        emp = random.choice(list(EMPLOYMENT_TYPE.keys()))
        sched = random.choice(list(SCHEDULE_TYPE.keys()))
        ten = random.choice(list(TENURE_TYPE.keys()))

        code = f"{emp}{sched}{ten}"
        description = f"{EMPLOYMENT_TYPE[emp]}, {SCHEDULE_TYPE[sched]}, {TENURE_TYPE[ten]}"

        if random.random() < 0.5:
            # Encode
            wrong_emp = random.choice([e for e in EMPLOYMENT_TYPE.keys() if e != emp])
            wrong_sched = random.choice([s for s in SCHEDULE_TYPE.keys() if s != sched])
            wrong_ten = random.choice([t for t in TENURE_TYPE.keys() if t != ten])
            wrong1 = f"{wrong_emp}{sched}{ten}"
            wrong2 = f"{emp}{wrong_sched}{ten}"
            wrong3 = f"{emp}{sched}{wrong_ten}"
            choices = [code, wrong1, wrong2, wrong3]
            random.shuffle(choices)
            questions.append(make_question(
                qid, "Medium",
                f"Using the employment status code [Type][Schedule][Tenure], encode: {description}",
                choices, code,
                f"{EMPLOYMENT_TYPE[emp]}={emp}, {SCHEDULE_TYPE[sched]}={sched}, {TENURE_TYPE[ten]}={ten} → {code}.",
                ["positional-alpha", "encoding"]
            ))
        else:
            # Decode
            wrong_emp = random.choice([e for e in EMPLOYMENT_TYPE.keys() if e != emp])
            wrong_sched = random.choice([s for s in SCHEDULE_TYPE.keys() if s != sched])
            wrong1 = f"{EMPLOYMENT_TYPE[wrong_emp]}, {SCHEDULE_TYPE[sched]}, {TENURE_TYPE[ten]}"
            wrong2 = f"{EMPLOYMENT_TYPE[emp]}, {SCHEDULE_TYPE[wrong_sched]}, {TENURE_TYPE[ten]}"
            wrong3 = f"{EMPLOYMENT_TYPE[wrong_emp]}, {SCHEDULE_TYPE[wrong_sched]}, {TENURE_TYPE[ten]}"
            choices = [description, wrong1, wrong2, wrong3]
            random.shuffle(choices)
            questions.append(make_question(
                qid, "Medium",
                f"Decode the employment status code '{code}' using structure [Type][Schedule][Tenure]:",
                choices, description,
                f"Position 1: {emp}={EMPLOYMENT_TYPE[emp]}, Position 2: {sched}={SCHEDULE_TYPE[sched]}, Position 3: {ten}={TENURE_TYPE[ten]}.",
                ["positional-alpha", "decoding"]
            ))
        qid += 1

    return questions[:200]


# ============================================================
# HARD QUESTIONS (IDs 401-600)
# ============================================================

def generate_hard_questions():
    """Generate 200 Hard questions. Multi-step, error detection, complex codes, traps."""
    questions = []
    qid = 401

    # --- Type 1: Error detection in alphanumeric codes (40 questions) ---
    for _ in range(40):
        # Generate 4 codes, one with an error
        div_keys_list = list(DIVISIONS.keys())
        act_keys_list = list(ACTIONS.keys())

        correct_codes = []
        for _ in range(3):
            d = random.choice(div_keys_list)
            a = random.choice(act_keys_list)
            y = random.choice([2023, 2024, 2025])
            s = random.randint(1, 999)
            correct_codes.append(f"{d}-{a}-{y}-{s:04d}")

        # Create one with an error
        error_type = random.choice(["wrong_div", "wrong_act", "short_year", "short_seq", "missing_segment"])
        d = random.choice(div_keys_list)
        a = random.choice(act_keys_list)
        y = random.choice([2023, 2024, 2025])
        s = random.randint(1, 999)

        if error_type == "wrong_div":
            # Use invalid division code
            invalid_divs = ["ADN", "FNI", "HRR", "OPP", "LGE", "HR", "AD", "FN"]
            bad_div = random.choice(invalid_divs)
            error_code = f"{bad_div}-{a}-{y}-{s:04d}"
            error_explanation = f"'{bad_div}' is not a valid division code. Valid codes include ADM, FIN, HRD, OPS, LEG, etc."
        elif error_type == "wrong_act":
            invalid_acts = ["XX", "AB", "ZZ", "QQ", "EX", "IN"]
            bad_act = random.choice(invalid_acts)
            error_code = f"{d}-{bad_act}-{y}-{s:04d}"
            error_explanation = f"'{bad_act}' is not a valid action code. Valid codes include IC, OC, MO, AP, DV, etc."
        elif error_type == "short_year":
            error_code = f"{d}-{a}-{str(y)[2:]}-{s:04d}"
            error_explanation = f"The year segment '{str(y)[2:]}' has only 2 digits; it should be 4 digits ({y})."
        elif error_type == "short_seq":
            error_code = f"{d}-{a}-{y}-{s:02d}" if s < 100 else f"{d}-{a}-{y}-{s:03d}"
            error_explanation = f"The sequence number should be 4 digits (zero-padded), not {len(str(s))} digits."
        else:  # missing_segment
            error_code = f"{d}-{y}-{s:04d}"
            error_explanation = f"The code is missing the action segment. Expected format: [Division]-[Action]-[Year]-[Sequence]."

        all_codes = correct_codes + [error_code]
        random.shuffle(all_codes)

        choices = all_codes
        questions.append(make_question(
            qid, "Hard",
            f"Which of the following codes contains an error? Structure: [Division]-[Action]-[4-digit Year]-[4-digit Sequence]",
            choices, error_code,
            error_explanation,
            ["error-detection", "alphanumeric"]
        ))
        qid += 1

    # --- Type 2: Complex letter shift with 5-letter words (30 questions) ---
    for _ in range(30):
        shift = random.choice([4, 5, 6, 7])
        word = random.choice(ENCODE_WORDS_5)
        encoded = shift_word(word, shift)

        # Decoding question with tricky distractors
        wrong1 = shift_word(encoded, -(shift - 1))  # off by 1
        wrong2 = shift_word(encoded, -(shift + 1))  # off by 1 other way
        wrong3 = shift_word(encoded, shift)  # encoded again (common mistake)

        choices = list(set([word, wrong1, wrong2, wrong3]))
        while len(choices) < 4:
            extra = shift_word(encoded, -random.choice([s for s in range(1, 10) if s != shift]))
            choices.append(extra)
            choices = list(set(choices))
        choices = choices[:4]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f"A message was encoded using a +{shift} letter shift. Decode: {encoded}",
            choices, word,
            f"To decode, shift each letter BACK by {shift}: {' → '.join(f'{c}→{shift_letter(c, -shift)}' for c in encoded)} = {word}.",
            ["letter-shift", "decoding", "multi-step"]
        ))
        qid += 1

    # --- Type 3: Multi-segment code construction from description (30 questions) ---
    for _ in range(30):
        agency_code = random.choice(list(AGENCIES.keys()))
        doc_type = random.choice(list(DOC_TYPES.keys()))
        year = random.choice([2023, 2024, 2025])
        num = random.randint(1, 200)

        correct_code = f"{agency_code}-{doc_type}-{year}-{num:03d}"
        description = f"{AGENCIES[agency_code]}, {DOC_TYPES[doc_type]} #{num}, Year {year}"

        # Tricky wrong answers
        wrong_agency = random.choice([a for a in AGENCIES.keys() if a != agency_code])
        wrong_doc = random.choice([d for d in DOC_TYPES.keys() if d != doc_type])

        # Common errors: swapped segments, wrong padding, wrong agency
        wrong1 = f"{wrong_agency}-{doc_type}-{year}-{num:03d}"
        wrong2 = f"{agency_code}-{wrong_doc}-{year}-{num:03d}"
        wrong3 = f"{agency_code}-{doc_type}-{year}-{num:04d}"  # wrong padding

        choices = [correct_code, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f"Encode using structure [Agency]-[DocType]-[Year]-[3-digit Number]: {description}",
            choices, correct_code,
            f"{AGENCIES[agency_code]}={agency_code}, {DOC_TYPES[doc_type]}={doc_type}, Year {year}, #{num}={num:03d}.",
            ["alphanumeric", "encoding", "multi-segment"]
        ))
        qid += 1

    # --- Type 4: Decode and verify logic (25 questions) ---
    # Questions where the decoded result must be checked for logical consistency
    illogical_combos = [
        ("HRD-DV-2024-0015", "Human Resources Division processing a Disbursement Voucher",
         "Disbursement Vouchers are typically processed by the Finance Division, not HR.",
         "Which decoded result reveals a LOGICALLY INCONSISTENT code?"),
        ("LEG-AP-2024-0033", "Legal Division processing an Appointment",
         "Appointments are typically processed by the Human Resources Division, not Legal.",
         "Which decoded result reveals a LOGICALLY INCONSISTENT code?"),
        ("FIN-TO-2024-0088", "Finance Division issuing a Travel Order",
         "Travel Orders are typically issued by the Administrative Division, not Finance.",
         "Which decoded result reveals a LOGICALLY INCONSISTENT code?"),
        ("OPS-LR-2024-0012", "Operations Division processing a Leave Request",
         "Leave Requests are typically processed by Human Resources, not Operations.",
         "Which decoded result reveals a LOGICALLY INCONSISTENT code?"),
        ("ICT-PO-2024-0045", "ICT Division issuing a Purchase Order",
         "Purchase Orders are typically issued by the Procurement Division, not ICT.",
         "Which decoded result reveals a LOGICALLY INCONSISTENT code?"),
    ]

    for _ in range(25):
        # Pick one illogical and three logical
        illogical = random.choice(illogical_combos)
        illogical_code = illogical[0]

        # Generate logical codes
        logical_pairs = [
            ("FIN", "DV"), ("HRD", "AP"), ("ADM", "TO"), ("ADM", "MO"),
            ("HRD", "LR"), ("PRO", "PO"), ("LEG", "SO"), ("ADM", "OO"),
        ]
        logical_codes = []
        for div, act in random.sample(logical_pairs, 3):
            y = random.choice([2023, 2024, 2025])
            s = random.randint(1, 200)
            logical_codes.append(f"{div}-{act}-{y}-{s:04d}")

        choices = logical_codes + [illogical_code]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f"After decoding these codes, which one represents a LOGICALLY INCONSISTENT combination (wrong division for the action type)?",
            choices, illogical_code,
            illogical[2],
            ["error-detection", "logic-check"]
        ))
        qid += 1

    # --- Type 5: Infer the coding rule from examples (25 questions) ---
    for _ in range(25):
        shift = random.choice([2, 3, 4, 5, 6])
        # Give two encoded examples, ask to encode a third
        word1 = random.choice(ENCODE_WORDS_3)
        word2 = random.choice([w for w in ENCODE_WORDS_3 if w != word1])
        word3 = random.choice([w for w in ENCODE_WORDS_3 if w != word1 and w != word2])

        enc1 = shift_word(word1, shift)
        enc2 = shift_word(word2, shift)
        enc3 = shift_word(word3, shift)

        # Wrong answers for word3
        wrong1 = shift_word(word3, shift + 1)
        wrong2 = shift_word(word3, shift - 1)
        wrong3 = shift_word(word3, shift + 2)

        choices = list(set([enc3, wrong1, wrong2, wrong3]))
        while len(choices) < 4:
            choices.append(shift_word(word3, random.choice([s for s in range(1, 8) if s != shift])))
            choices = list(set(choices))
        choices = choices[:4]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f"If '{word1}' is coded as '{enc1}' and '{word2}' is coded as '{enc2}', how is '{word3}' coded?",
            choices, enc3,
            f"The rule is a +{shift} letter shift. Applying the same shift to '{word3}': {enc3}.",
            ["infer-rule", "letter-shift"]
        ))
        qid += 1

    # --- Type 6: Complex classification code with decimal expansion (25 questions) ---
    expanded_scheme = {
        "221.1": "Regular Salary Vouchers",
        "221.2": "Overtime Pay Vouchers",
        "221.3": "Hazard Pay Vouchers",
        "222.1": "Domestic Travel Vouchers",
        "222.2": "International Travel Vouchers",
        "222.3": "Local Travel Vouchers",
        "311.1": "Janitorial Service Contracts",
        "311.2": "Security Service Contracts",
        "311.3": "IT Service Contracts",
        "312.1": "Inter-Agency MOAs",
        "312.2": "MOAs with Private Sector",
        "312.3": "International MOUs",
        "121.1": "Original Appointments",
        "121.2": "Promotional Appointments",
        "121.3": "Transfer Appointments",
        "122.1": "Vacation Leave Records",
        "122.2": "Sick Leave Records",
        "122.3": "Maternity/Paternity Leave Records",
    }

    expanded_keys = list(expanded_scheme.keys())
    for _ in range(25):
        code = random.choice(expanded_keys)
        correct_name = expanded_scheme[code]

        # Wrong answers from same parent or nearby
        parent = code[:3]
        siblings = [k for k in expanded_keys if k[:3] == parent and k != code]
        cousins = [k for k in expanded_keys if k[:3] != parent]

        wrong_names = []
        if siblings:
            wrong_names.append(expanded_scheme[random.choice(siblings)])
        wrong_names += [expanded_scheme[random.choice(cousins)] for _ in range(3 - len(wrong_names))]

        choices = [correct_name] + wrong_names[:3]
        random.shuffle(choices)

        base_name = CLASSIFICATION_SCHEME.get(code[:3], "")
        parent_name = CLASSIFICATION_SCHEME.get(code[:2] + "0", "")

        questions.append(make_question(
            qid, "Hard",
            f"In an expanded classification scheme, what does code '{code}' represent?",
            choices, correct_name,
            f"Code {code}: {parent_name} → {base_name} → {correct_name} (decimal expansion for specificity).",
            ["classification-code", "expanded", "decoding"]
        ))
        qid += 1

    # --- Type 7: Mixed encoding with multiple code systems (25 questions) ---
    for _ in range(25):
        # Combine division code + priority + classification + sequence
        div = random.choice(list(DIVISIONS.keys()))
        priority = random.choice(list(PRIORITY_CODES.keys()))
        class_code = random.choice([k for k in CLASSIFICATION_SCHEME.keys() if len(k) == 3 and k[2] != '0'])
        seq = random.randint(1, 99)

        full_code = f"{div}-{priority}-{class_code}-{seq:02d}"
        correct_desc = f"{DIVISIONS[div]}, {PRIORITY_CODES[priority]} priority, {CLASSIFICATION_SCHEME[class_code]}, Item #{seq}"

        # Wrong descriptions
        wrong_div = random.choice([d for d in DIVISIONS.keys() if d != div])
        wrong_pri = random.choice([p for p in PRIORITY_CODES.keys() if p != priority])
        wrong_class = random.choice([c for c in CLASSIFICATION_SCHEME.keys() if len(c) == 3 and c[2] != '0' and c != class_code])

        wrong1 = f"{DIVISIONS[wrong_div]}, {PRIORITY_CODES[priority]} priority, {CLASSIFICATION_SCHEME[class_code]}, Item #{seq}"
        wrong2 = f"{DIVISIONS[div]}, {PRIORITY_CODES[wrong_pri]} priority, {CLASSIFICATION_SCHEME[class_code]}, Item #{seq}"
        wrong3 = f"{DIVISIONS[div]}, {PRIORITY_CODES[priority]} priority, {CLASSIFICATION_SCHEME[wrong_class]}, Item #{seq}"

        choices = [correct_desc, wrong1, wrong2, wrong3]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f"Decode the compound code '{full_code}' using structure [Division]-[Priority]-[ClassCode]-[Seq##]:",
            choices, correct_desc,
            f"{div}={DIVISIONS[div]}, {priority}={PRIORITY_CODES[priority]}, {class_code}={CLASSIFICATION_SCHEME[class_code]}, {seq:02d}=Item #{seq}.",
            ["compound-code", "decoding", "multi-system"]
        ))
        qid += 1

    return questions[:200]


# ============================================================
# MAIN
# ============================================================

def main():
    easy = generate_easy_questions()
    medium = generate_medium_questions()
    hard = generate_hard_questions()

    # Reassign IDs to ensure sequential ordering
    all_questions = []
    for i, q in enumerate(easy, start=1):
        q["id"] = i
        all_questions.append(q)
    for i, q in enumerate(medium, start=201):
        q["id"] = i
        all_questions.append(q)
    for i, q in enumerate(hard, start=401):
        q["id"] = i
        all_questions.append(q)

    # Validate
    print(f"Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")
    assert len(all_questions) == 600, f"Expected 600, got {len(all_questions)}"
    for q in all_questions:
        assert q["answer"] in q["choices"], f"ID {q['id']}: answer not in choices"
        assert len(q["choices"]) >= 3, f"ID {q['id']}: fewer than 3 choices"
        i = q["id"]
        if i <= 200:
            assert q["difficulty"] == "Easy", f"ID {i} should be Easy"
        elif i <= 400:
            assert q["difficulty"] == "Medium", f"ID {i} should be Medium"
        else:
            assert q["difficulty"] == "Hard", f"ID {i} should be Hard"

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability",
        "indexing-and-record-organization", "coding-systems"
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
