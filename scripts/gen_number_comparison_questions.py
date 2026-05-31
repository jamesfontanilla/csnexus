"""
Generate 600 number comparison questions for the CSE reviewer.
200 Easy, 200 Medium, 200 Hard.

Question types:
- Are these numbers identical? (Yes/No)
- Which pair is identical?
- Which pair is NOT identical?
- How many pairs are identical/not identical?
- What type of error exists?
"""

import json
import random
import os

random.seed(43)

# --- Number Data ---

# Simple digit sequences of various lengths
SHORT_NUMBERS = [
    "1234", "5678", "9012", "3456", "7890",
    "2468", "1357", "8024", "6913", "4827",
    "5039", "7261", "8493", "1625", "3847",
    "9058", "2716", "4382", "6194", "8507",
    "1948", "3672", "5814", "7036", "9250",
    "4163", "6285", "8407", "2539", "7641",
    "3918", "5274", "8630", "1492", "7053",
    "2847", "6301", "9475", "4086", "5729",
    "8163", "3047", "6592", "1738", "9204",
    "4651", "7389", "2014", "5867", "8432",
    "3196", "6740", "9583", "1027", "4365",
    "7801", "2956", "5413", "8079", "6248",
]

MEDIUM_NUMBERS = [
    "12345", "67890", "24680", "13579", "80214",
    "48273", "91635", "57082", "36941", "72058",
    "48291", "63507", "19284", "75036", "82419",
    "56738", "30192", "64857", "97213", "41068",
    "28374", "50916", "73482", "16509", "89247",
    "34761", "62098", "45183", "78920", "10345",
    "59127", "83064", "27491", "60853", "14726",
    "93580", "46012", "71938", "25467", "80391",
    "37654", "52809", "68143", "94270", "15683",
    "42917", "76350", "81624", "39058", "64792",
    "20836", "57149", "93401", "18265", "45073",
    "72618", "86934", "31507", "69842", "54280",
]

LONG_NUMBERS = [
    "123456789", "987654321", "246813579", "135792468",
    "482739156", "917263548", "305816274", "648205193",
    "571930482", "829461037", "194728365", "736051928",
    "408192637", "562847193", "891034726", "273618405",
    "615927384", "948371062", "357204891", "780463215",
]

# Government-style formatted numbers
EMPLOYEE_IDS = [
    "2024-00135", "2024-00246", "2024-00357", "2024-00468",
    "2024-00579", "2023-01234", "2023-02345", "2023-03456",
    "2023-04567", "2023-05678", "2022-00891", "2022-01902",
]

VOUCHER_NUMBERS = [
    "DV-2024-03-0042", "DV-2024-03-0135", "DV-2024-04-0001",
    "DV-2024-05-0078", "DV-2023-12-0234", "DV-2023-11-0567",
    "DV-2024-01-0089", "DV-2024-02-0156", "DV-2024-06-0023",
    "DV-2024-07-0045", "DV-2023-09-0312", "DV-2023-10-0198",
]

CHECK_NUMBERS = [
    "0012345678", "0098765432", "0045678901", "0023456789",
    "0067890123", "0034567890", "0056789012", "0078901234",
    "0089012345", "0001234567", "0043218765", "0076543210",
]

TIN_NUMBERS = [
    "123-456-789-000", "234-567-890-001", "345-678-901-002",
    "456-789-012-003", "567-890-123-004", "678-901-234-005",
    "789-012-345-006", "890-123-456-007", "901-234-567-008",
    "012-345-678-009", "111-222-333-000", "444-555-666-001",
]

PHILHEALTH_IDS = [
    "01-234567890-1", "02-345678901-2", "03-456789012-3",
    "04-567890123-4", "05-678901234-5", "06-789012345-6",
    "07-890123456-7", "08-901234567-8", "09-012345678-9",
    "10-123456789-0", "11-234567890-1", "12-345678901-2",
]

SSS_NUMBERS = [
    "34-1234567-8", "34-2345678-9", "34-3456789-0",
    "33-4567890-1", "33-5678901-2", "33-6789012-3",
    "32-7890123-4", "32-8901234-5", "32-9012345-6",
    "31-0123456-7", "31-1234567-8", "31-2345678-9",
]

PAGIBIG_MIDS = [
    "1234-5678-9012", "2345-6789-0123", "3456-7890-1234",
    "4567-8901-2345", "5678-9012-3456", "6789-0123-4567",
    "7890-1234-5678", "8901-2345-6789", "9012-3456-7890",
    "0123-4567-8901", "1111-2222-3333", "4444-5555-6666",
]

BUDGET_CODES = [
    "PS-101-2024-001", "PS-102-2024-002", "PS-103-2024-003",
    "MOOE-205-2024-001", "MOOE-206-2024-002", "MOOE-207-2024-003",
    "CO-301-2024-001", "CO-302-2024-002", "CO-303-2024-003",
    "PS-101-2023-045", "MOOE-205-2023-078", "CO-301-2023-012",
]

DOCUMENT_CODES = [
    "CSC-2024-03-0042", "CSC-2024-04-0135", "CSC-NCR-001",
    "COA-R3-045", "COA-R4-078", "COA-R5-012",
    "DILG-2024-001", "DILG-2024-002", "DILG-2024-003",
    "DBM-2024-0001", "DBM-2024-0002", "DBM-2024-0003",
]

PHONE_NUMBERS = [
    "09171234567", "09181234567", "09191234567",
    "09201234567", "09211234567", "09271234567",
    "09281234567", "09291234567", "09301234567",
    "09171112233", "09184445566", "09197778899",
]

FINANCIAL_AMOUNTS = [
    "12,345.67", "23,456.78", "34,567.89", "45,678.90",
    "56,789.01", "67,890.12", "78,901.23", "89,012.34",
    "1,234,567.89", "2,345,678.90", "3,456,789.01",
    "100,000.00", "250,000.00", "500,000.00", "1,000,000.00",
    "5,678.50", "9,876.25", "15,432.10", "87,654.32",
]

# --- Error Generation Functions ---

def substitute_digit(number: str) -> str:
    """Replace one digit with a different digit."""
    positions = [i for i, c in enumerate(number) if c.isdigit()]
    if not positions:
        return number
    pos = random.choice(positions)
    original = number[pos]
    # Pick a visually similar digit when possible
    similar = {
        '0': ['8', '6', '9'],
        '1': ['7', '4'],
        '2': ['7', '3'],
        '3': ['8', '5'],
        '4': ['9', '1'],
        '5': ['6', '3'],
        '6': ['8', '0', '5'],
        '7': ['1', '2'],
        '8': ['6', '3', '0'],
        '9': ['4', '6', '0'],
    }
    choices = similar.get(original, ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    choices = [c for c in choices if c != original]
    replacement = random.choice(choices)
    return number[:pos] + replacement + number[pos + 1:]


def transpose_digits(number: str) -> str:
    """Swap two adjacent digits."""
    positions = [i for i in range(len(number) - 1)
                 if number[i].isdigit() and number[i + 1].isdigit()
                 and number[i] != number[i + 1]]
    if not positions:
        return substitute_digit(number)
    pos = random.choice(positions)
    return number[:pos] + number[pos + 1] + number[pos] + number[pos + 2:]


def omit_digit(number: str) -> str:
    """Remove one digit (preferring repeated digits)."""
    # Prefer removing from repeated digits
    for i in range(len(number) - 1):
        if number[i] == number[i + 1] and number[i].isdigit():
            return number[:i] + number[i + 1:]
    # Otherwise remove a random digit (not first or last for readability)
    positions = [i for i, c in enumerate(number) if c.isdigit()]
    if len(positions) < 3:
        return substitute_digit(number)
    pos = random.choice(positions[1:-1])
    return number[:pos] + number[pos + 1:]


def add_digit(number: str) -> str:
    """Insert a duplicate of an adjacent digit."""
    positions = [i for i, c in enumerate(number) if c.isdigit()]
    if not positions:
        return number
    pos = random.choice(positions)
    return number[:pos] + number[pos] + number[pos:]


def change_separator(number: str) -> str:
    """Change a separator character (hyphen, comma, period, slash)."""
    separators = {'-': '.', '.': '-', ',': '', '/': '-'}
    for sep, replacement in separators.items():
        if sep in number:
            pos = number.index(sep)
            return number[:pos] + replacement + number[pos + 1:]
    return substitute_digit(number)


def change_leading_zero(number: str) -> str:
    """Add or remove a leading zero in a segment."""
    # Find segments separated by non-digits
    import re
    segments = re.split(r'([^0-9])', number)
    # Find a segment with leading zeros
    for i, seg in enumerate(segments):
        if seg.isdigit() and len(seg) > 1 and seg[0] == '0':
            segments[i] = seg[1:]  # Remove one leading zero
            return ''.join(segments)
    # If no leading zeros, add one to a segment
    for i, seg in enumerate(segments):
        if seg.isdigit() and len(seg) >= 1:
            segments[i] = '0' + seg
            return ''.join(segments)
    return substitute_digit(number)


def digit_letter_swap(number: str) -> str:
    """Swap a digit with a visually similar letter (0→O, 1→l, 5→S)."""
    swaps = {'0': 'O', '1': 'l', '5': 'S'}
    positions = [i for i, c in enumerate(number) if c in swaps]
    if not positions:
        # Try reverse: letter to digit
        reverse_swaps = {'O': '0', 'l': '1', 'S': '5', 'I': '1'}
        positions = [i for i, c in enumerate(number) if c in reverse_swaps]
        if not positions:
            return substitute_digit(number)
        pos = random.choice(positions)
        return number[:pos] + reverse_swaps[number[pos]] + number[pos + 1:]
    pos = random.choice(positions)
    return number[:pos] + swaps[number[pos]] + number[pos + 1:]

# --- Helper Functions ---

def make_error(number: str, error_type: str) -> str:
    """Apply a specific error type to a number."""
    if error_type == "substitution":
        return substitute_digit(number)
    elif error_type == "transposition":
        return transpose_digits(number)
    elif error_type == "omission":
        return omit_digit(number)
    elif error_type == "addition":
        return add_digit(number)
    elif error_type == "separator":
        return change_separator(number)
    elif error_type == "leading_zero":
        return change_leading_zero(number)
    elif error_type == "digit_letter":
        return digit_letter_swap(number)
    else:
        return substitute_digit(number)


def get_error_explanation(num_a: str, num_b: str, error_type: str) -> str:
    """Generate explanation for the error."""
    explanations = {
        "substitution": f"'{num_a}' and '{num_b}' differ by one digit substitution.",
        "transposition": f"'{num_a}' and '{num_b}' have two adjacent digits swapped.",
        "omission": f"'{num_b}' is missing a digit that appears in '{num_a}'.",
        "addition": f"'{num_b}' has an extra digit not present in '{num_a}'.",
        "separator": f"'{num_a}' and '{num_b}' differ in separator formatting.",
        "leading_zero": f"'{num_a}' and '{num_b}' differ in leading zeros.",
        "digit_letter": f"'{num_a}' and '{num_b}' differ — digit vs. letter confusion (e.g., 0 vs. O).",
    }
    return explanations.get(error_type, f"The numbers differ: '{num_a}' vs '{num_b}'.")


def generate_random_number(length: int) -> str:
    """Generate a random digit string of given length."""
    first = random.choice("123456789")
    rest = ''.join(random.choices("0123456789", k=length - 1))
    return first + rest


def generate_formatted_number() -> str:
    """Generate a random formatted government-style number."""
    formats = [
        EMPLOYEE_IDS, VOUCHER_NUMBERS, CHECK_NUMBERS, TIN_NUMBERS,
        PHILHEALTH_IDS, SSS_NUMBERS, PAGIBIG_MIDS, BUDGET_CODES,
        DOCUMENT_CODES, PHONE_NUMBERS,
    ]
    pool = random.choice(formats)
    base = random.choice(pool)
    # Add variation by randomly tweaking digits to create more unique numbers
    if random.random() < 0.5:
        # Modify a random digit to create a new valid number
        positions = [i for i, c in enumerate(base) if c.isdigit()]
        if positions:
            pos = random.choice(positions)
            new_digit = str(random.randint(0, 9))
            base = base[:pos] + new_digit + base[pos + 1:]
    return base


def generate_financial_amount() -> str:
    """Generate a random financial amount string."""
    return "₱" + random.choice(FINANCIAL_AMOUNTS)


def ensure_different(original: str, modified: str, error_type: str) -> str:
    """Ensure the modified version is actually different from original."""
    attempts = 0
    while modified == original and attempts < 15:
        modified = make_error(original, error_type)
        attempts += 1
    if modified == original:
        modified = substitute_digit(original)
    if modified == original:
        # Last resort: flip a digit manually
        for i, c in enumerate(original):
            if c.isdigit():
                new_d = str((int(c) + 1) % 10)
                return original[:i] + new_d + original[i + 1:]
    return modified

# --- Easy Questions (IDs 1-200) ---
# Short numbers (4-5 digits), no formatting or simple formatting
# Single obvious difference or identical pairs
# Question types: "Are these identical?" and "Which pair is identical/not identical?"

def generate_easy_questions() -> list:
    questions = []
    qid = 1
    used_questions = set()  # Track question text to avoid duplicates

    easy_errors = ["substitution", "transposition", "omission", "addition"]
    all_short_medium = SHORT_NUMBERS + MEDIUM_NUMBERS

    # Type 1: Are these numbers identical? (50 identical, 50 different)
    used_numbers = set()
    for i in range(50):
        # Pick a number not yet used for identical pairs
        available = [n for n in all_short_medium if n not in used_numbers]
        if not available:
            available = all_short_medium
        number = random.choice(available)
        used_numbers.add(number)

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Easy",
            "question": f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {number}",
            "choices": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, they differ in length",
                "No, they differ in formatting"
            ],
            "answer": "Yes, they are identical",
            "explanation": f"Both numbers are exactly '{number}' — all digits match.",
            "tags": ["identical-pair", "short-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        used_questions.add(q["question"])
        questions.append(q)
        qid += 1

    for i in range(50):
        # Generate unique different-pair questions
        for _ in range(20):
            number = random.choice(all_short_medium)
            error_type = random.choice(easy_errors)
            modified = ensure_different(number, make_error(number, error_type), error_type)
            q_text = f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}"
            if q_text not in used_questions:
                break

        if len(modified) != len(number):
            correct_answer = "No, they differ in length"
        else:
            correct_answer = "No, they differ by one digit"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Easy",
            "question": q_text,
            "choices": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, they differ in length",
                "No, they differ in formatting"
            ],
            "answer": correct_answer,
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "short-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        used_questions.add(q["question"])
        questions.append(q)
        qid += 1

    # Type 2: Which pair is identical? (50 questions)
    for i in range(50):
        for _ in range(20):
            identical_pos = random.randint(0, 3)
            pairs = []
            for j in range(4):
                number = random.choice(all_short_medium)
                if j == identical_pos:
                    pairs.append((number, number))
                else:
                    error_type = random.choice(easy_errors)
                    modified = ensure_different(number, make_error(number, error_type), error_type)
                    pairs.append((number, modified))

            labels = ["A", "B", "C", "D"]
            pair_display = "; ".join([f"{labels[k]}. {a} vs. {b}" for k, (a, b) in enumerate(pairs)])
            q_text = f"Which of the following pairs contains numbers that are IDENTICAL?\n\n{pair_display}"
            if q_text not in used_questions:
                break

        choices_text = [f"{a} / {b}" for a, b in pairs]

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices_text,
            "answer": choices_text[identical_pos],
            "explanation": f"Only '{pairs[identical_pos][0]}' / '{pairs[identical_pos][1]}' are identical. The other pairs each contain a digit difference.",
            "tags": ["which-identical", "short-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        used_questions.add(q["question"])
        questions.append(q)
        qid += 1

    # Type 3: Which pair is NOT identical? (50 questions)
    for i in range(50):
        for _ in range(20):
            different_pos = random.randint(0, 3)
            pairs = []
            error_type = random.choice(easy_errors)
            for j in range(4):
                number = random.choice(all_short_medium)
                if j == different_pos:
                    modified = ensure_different(number, make_error(number, error_type), error_type)
                    pairs.append((number, modified))
                else:
                    pairs.append((number, number))

            labels = ["A", "B", "C", "D"]
            pair_display = "; ".join([f"{labels[k]}. {a} vs. {b}" for k, (a, b) in enumerate(pairs)])
            q_text = f"Which of the following pairs contains numbers that are NOT identical?\n\n{pair_display}"
            if q_text not in used_questions:
                break

        choices_text = [f"{a} / {b}" for a, b in pairs]

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Easy",
            "question": q_text,
            "choices": choices_text,
            "answer": choices_text[different_pos],
            "explanation": f"'{pairs[different_pos][0]}' and '{pairs[different_pos][1]}' differ ({error_type} error). All other pairs are identical.",
            "tags": ["which-not-identical", "short-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        used_questions.add(q["question"])
        questions.append(q)
        qid += 1

    return questions[:200]

# --- Medium Questions (IDs 201-400) ---
# Formatted numbers (government codes, financial amounts)
# May include separator differences, leading zeros
# Differences can be in any segment

def generate_medium_questions() -> list:
    questions = []
    qid = 201
    used_questions = set()

    medium_errors = ["substitution", "transposition", "omission", "addition", "separator", "leading_zero"]

    # Type 1: Are these formatted numbers identical? (30 identical, 30 different)
    for i in range(30):
        for _ in range(20):
            number = generate_formatted_number()
            q_text = f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {number}"
            if q_text not in used_questions:
                break
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": q_text,
            "choices": [
                "Yes, they are identical",
                "No, they differ in digits",
                "No, they differ in formatting",
                "No, they differ in length"
            ],
            "answer": "Yes, they are identical",
            "explanation": f"Both numbers are exactly '{number}' — all characters, digits, and separators match.",
            "tags": ["identical-pair", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        used_questions.add(q["question"])
        questions.append(q)
        qid += 1

    for i in range(30):
        for _ in range(20):
            number = generate_formatted_number()
            error_type = random.choice(medium_errors)
            modified = ensure_different(number, make_error(number, error_type), error_type)
            q_text = f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}"
            if q_text not in used_questions:
                break

        if error_type in ("separator", "leading_zero"):
            if len(modified) != len(number):
                correct_answer = "No, they differ in length"
            else:
                correct_answer = "No, they differ in formatting"
        elif len(modified) != len(number):
            correct_answer = "No, they differ in length"
        else:
            correct_answer = "No, they differ in digits"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, they differ in digits",
                "No, they differ in formatting",
                "No, they differ in length"
            ],
            "answer": correct_answer,
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 2: Which pair is identical? (formatted numbers) - 40 questions
    for i in range(40):
        identical_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            number = generate_formatted_number()
            if j == identical_pos:
                pairs.append((number, number))
            else:
                error_type = random.choice(medium_errors)
                modified = ensure_different(number, make_error(number, error_type), error_type)
                pairs.append((number, modified))

        choices_text = [f"{a} / {b}" for a, b in pairs]
        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[k]}. {a} vs. {b}" for k, (a, b) in enumerate(pairs)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"Which of the following pairs contains IDENTICAL numbers?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[identical_pos],
            "explanation": f"Only the pair '{pairs[identical_pos][0]}' is repeated identically. The other pairs each contain a discrepancy.",
            "tags": ["which-identical", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 3: What type of error? - 30 questions
    error_type_choices = ["Substitution", "Transposition", "Omission", "Addition"]
    error_types_map = ["substitution", "transposition", "omission", "addition"]
    for i in range(30):
        number = random.choice(SHORT_NUMBERS + MEDIUM_NUMBERS + LONG_NUMBERS)
        error_idx = random.randint(0, 3)
        error_type = error_types_map[error_idx]
        modified = ensure_different(number, make_error(number, error_type), error_type)

        # Verify the error type matches reality
        if len(modified) < len(number):
            error_idx = 2  # omission
        elif len(modified) > len(number):
            error_idx = 3  # addition

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"What type of error exists between these numbers?\n\nNumber A: {number}\nNumber B: {modified}",
            "choices": error_type_choices,
            "answer": error_type_choices[error_idx],
            "explanation": f"'{number}' vs '{modified}' — {error_type_choices[error_idx].lower()} error: {get_error_explanation(number, modified, error_type)}",
            "tags": ["error-type-identification", error_type],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 4: Financial amount comparison - 30 questions (15 identical, 15 different)
    for i in range(15):
        amount = generate_financial_amount()
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"Are the following amounts identical?\n\nAmount A: {amount}\nAmount B: {amount}",
            "choices": [
                "Yes, they are identical",
                "No, they differ in the peso amount",
                "No, they differ in the centavo amount",
                "No, they differ in formatting"
            ],
            "answer": "Yes, they are identical",
            "explanation": f"Both amounts are exactly '{amount}' — all digits, commas, and decimal match.",
            "tags": ["identical-pair", "financial-amount"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    for i in range(15):
        amount = generate_financial_amount()
        # Apply transposition to centavo portion if possible
        if '.' in amount:
            parts = amount.rsplit('.', 1)
            if len(parts[1]) == 2 and parts[1][0] != parts[1][1]:
                modified = parts[0] + '.' + parts[1][1] + parts[1][0]
                correct_answer = "No, they differ in the centavo amount"
                error_type = "transposition"
            else:
                error_type = "substitution"
                modified = ensure_different(amount, substitute_digit(amount), "substitution")
                correct_answer = "No, they differ in the peso amount"
        else:
            error_type = "substitution"
            modified = ensure_different(amount, substitute_digit(amount), "substitution")
            correct_answer = "No, they differ in the peso amount"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"Are the following amounts identical?\n\nAmount A: {amount}\nAmount B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, they differ in the peso amount",
                "No, they differ in the centavo amount",
                "No, they differ in formatting"
            ],
            "answer": correct_answer,
            "explanation": get_error_explanation(amount, modified, error_type),
            "tags": [f"{error_type}-error", "financial-amount"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 5: Which pair is NOT identical? (formatted) - 20 questions
    for i in range(20):
        different_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            number = generate_formatted_number()
            if j == different_pos:
                error_type = random.choice(medium_errors)
                modified = ensure_different(number, make_error(number, error_type), error_type)
                pairs.append((number, modified))
            else:
                pairs.append((number, number))

        choices_text = [f"{a} / {b}" for a, b in pairs]
        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[k]}. {a} vs. {b}" for k, (a, b) in enumerate(pairs)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"Which of the following pairs contains numbers that are NOT identical?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[different_pos],
            "explanation": f"'{pairs[different_pos][0]}' and '{pairs[different_pos][1]}' differ. All other pairs are identical.",
            "tags": ["which-not-identical", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Fill remaining to reach 200
    while len(questions) < 200:
        number = generate_formatted_number()
        error_type = random.choice(medium_errors)
        modified = ensure_different(number, make_error(number, error_type), error_type)

        if len(modified) != len(number):
            correct_answer = "No, they differ in length"
        elif error_type == "separator":
            correct_answer = "No, they differ in formatting"
        else:
            correct_answer = "No, they differ in digits"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Medium",
            "question": f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, they differ in digits",
                "No, they differ in formatting",
                "No, they differ in length"
            ],
            "answer": correct_answer,
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    return questions[:200]

# --- Hard Questions (IDs 401-600) ---
# Long numbers, mixed alphanumeric codes, financial amounts
# Multiple traps: digit/letter confusion, subtle transpositions
# Count-based questions, multi-pair analysis

def generate_hard_questions() -> list:
    questions = []
    qid = 401

    hard_errors = ["substitution", "transposition", "omission", "addition",
                   "separator", "leading_zero", "digit_letter"]

    # Type 1: Long number comparison (20 identical, 20 different)
    for i in range(20):
        number = random.choice(LONG_NUMBERS)
        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {number}",
            "choices": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, two adjacent digits are transposed",
                "No, a digit is missing or added"
            ],
            "answer": "Yes, they are identical",
            "explanation": f"Both numbers are exactly '{number}' — all 9 digits match position by position.",
            "tags": ["identical-pair", "long-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    for i in range(20):
        number = random.choice(LONG_NUMBERS)
        error_type = random.choice(["substitution", "transposition"])
        modified = ensure_different(number, make_error(number, error_type), error_type)

        if error_type == "transposition":
            correct_answer = "No, two adjacent digits are transposed"
        else:
            correct_answer = "No, they differ by one digit"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, two adjacent digits are transposed",
                "No, a digit is missing or added"
            ],
            "answer": correct_answer,
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "long-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 2: Alphanumeric code comparison with digit/letter traps - 30 questions
    for i in range(30):
        number = random.choice(BUDGET_CODES + DOCUMENT_CODES + VOUCHER_NUMBERS)
        if random.random() < 0.5:
            error_type = "digit_letter"
        else:
            error_type = random.choice(["substitution", "transposition"])
        modified = ensure_different(number, make_error(number, error_type), error_type)

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"Are the following codes identical?\n\nCode A: {number}\nCode B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, a digit is replaced by a similar-looking letter",
                "No, digits are transposed",
                "No, a digit is substituted with a different digit"
            ],
            "answer": (
                "No, a digit is replaced by a similar-looking letter" if error_type == "digit_letter"
                else "No, digits are transposed" if error_type == "transposition"
                else "No, a digit is substituted with a different digit"
            ),
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "alphanumeric-code"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 3: How many pairs are identical? (count questions) - 30 questions
    for i in range(30):
        num_pairs = 5
        num_identical = random.randint(1, 4)
        identical_positions = random.sample(range(num_pairs), num_identical)

        pair_lines = []
        for j in range(num_pairs):
            number = generate_formatted_number()
            if j in identical_positions:
                pair_lines.append((number, number))
            else:
                error_type = random.choice(hard_errors[:4])
                modified = ensure_different(number, make_error(number, error_type), error_type)
                pair_lines.append((number, modified))

        pair_display = "\n".join([f"{j+1}. {a}    {b}" for j, (a, b) in enumerate(pair_lines)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"How many of the following pairs are EXACTLY identical?\n\n{pair_display}",
            "choices": ["1", "2", "3", "4"],
            "answer": str(num_identical),
            "explanation": f"{num_identical} pair(s) are identical (pairs at positions {', '.join(str(p+1) for p in sorted(identical_positions))}). The rest contain digit discrepancies.",
            "tags": ["count-identical", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 4: Financial amount with subtle differences - 30 questions
    for i in range(30):
        amount = generate_financial_amount()
        error_type = random.choice(["substitution", "transposition"])
        modified = ensure_different(amount, make_error(amount, error_type), error_type)

        # Determine where the difference is
        if '.' in amount and '.' in modified:
            peso_a = amount.split('.')[0]
            peso_b = modified.split('.')[0]
            cent_a = amount.split('.')[1]
            cent_b = modified.split('.')[1]
            if peso_a != peso_b:
                location = "in the peso digits"
            elif cent_a != cent_b:
                location = "in the centavo digits"
            else:
                location = "in the number"
        else:
            location = "in the number"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"Are the following financial amounts identical?\n\nAmount A: {amount}\nAmount B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, they differ in the peso digits",
                "No, they differ in the centavo digits",
                "No, they differ in formatting (commas/decimal)"
            ],
            "answer": (
                "Yes, they are identical" if amount == modified
                else f"No, they differ {location}".replace("in the peso digits", "in the peso digits").replace("in the centavo digits", "in the centavo digits").replace("in the number", "in the peso digits")
            ),
            "explanation": get_error_explanation(amount, modified, error_type),
            "tags": [f"{error_type}-error", "financial-amount"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        # Fix the answer field
        if amount == modified:
            q["answer"] = "Yes, they are identical"
        elif location == "in the centavo digits":
            q["answer"] = "No, they differ in the centavo digits"
        else:
            q["answer"] = "No, they differ in the peso digits"

        questions.append(q)
        qid += 1

    # Type 5: Which pair is identical among complex codes - 30 questions
    for i in range(30):
        identical_pos = random.randint(0, 3)
        pairs = []
        for j in range(4):
            # Mix of different formatted types
            pool_choice = random.randint(0, 2)
            if pool_choice == 0:
                number = generate_formatted_number()
            elif pool_choice == 1:
                number = generate_financial_amount()
            else:
                number = random.choice(LONG_NUMBERS)

            if j == identical_pos:
                pairs.append((number, number))
            else:
                error_type = random.choice(hard_errors[:5])
                modified = ensure_different(number, make_error(number, error_type), error_type)
                pairs.append((number, modified))

        choices_text = [f"{a} / {b}" for a, b in pairs]
        labels = ["A", "B", "C", "D"]
        pair_display = "; ".join([f"{labels[k]}. {a} vs. {b}" for k, (a, b) in enumerate(pairs)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"Which of the following pairs contains numbers that are EXACTLY identical?\n\n{pair_display}",
            "choices": choices_text,
            "answer": choices_text[identical_pos],
            "explanation": f"Only '{pairs[identical_pos][0]}' is repeated identically. The other pairs each contain a subtle discrepancy.",
            "tags": ["which-identical", "mixed-format"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Type 6: How many pairs are NOT identical? - 20 questions
    for i in range(20):
        num_pairs = 5
        num_different = random.randint(2, 4)
        different_positions = random.sample(range(num_pairs), num_different)

        pair_lines = []
        for j in range(num_pairs):
            number = generate_formatted_number()
            if j in different_positions:
                error_type = random.choice(hard_errors[:4])
                modified = ensure_different(number, make_error(number, error_type), error_type)
                pair_lines.append((number, modified))
            else:
                pair_lines.append((number, number))

        pair_display = "\n".join([f"{j+1}. {a}    {b}" for j, (a, b) in enumerate(pair_lines)])

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"How many of the following pairs are NOT identical?\n\n{pair_display}",
            "choices": ["1", "2", "3", "4"],
            "answer": str(num_different),
            "explanation": f"{num_different} pair(s) are not identical (pairs at positions {', '.join(str(p+1) for p in sorted(different_positions))}). The rest are identical.",
            "tags": ["count-not-identical", "formatted-number"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        questions.append(q)
        qid += 1

    # Fill remaining to reach 200
    while len(questions) < 200:
        number = random.choice(LONG_NUMBERS + PHONE_NUMBERS)
        error_type = random.choice(["substitution", "transposition"])
        modified = ensure_different(number, make_error(number, error_type), error_type)

        if error_type == "transposition":
            correct_answer = "No, two adjacent digits are transposed"
        else:
            correct_answer = "No, they differ by one digit"

        q = {
            "id": qid,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": "Hard",
            "question": f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}",
            "choices": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, two adjacent digits are transposed",
                "No, a digit is missing or added"
            ],
            "answer": correct_answer,
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "long-number"],
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

    all_questions = easy + medium + hard

    # Reassign IDs sequentially
    for i, q in enumerate(all_questions):
        q["id"] = i + 1

    # Deduplicate: replace duplicate questions with fresh ones
    seen_texts = {}
    duplicates = []
    for i, q in enumerate(all_questions):
        if q["question"] in seen_texts:
            duplicates.append(i)
        else:
            seen_texts[q["question"]] = i

    # Regenerate duplicates with fresh random numbers
    for idx in duplicates:
        q = all_questions[idx]
        difficulty = q["difficulty"]
        # Generate a fresh unique question
        for attempt in range(50):
            if difficulty == "Easy":
                number = generate_random_number(random.choice([4, 5]))
            elif difficulty == "Medium":
                number = generate_formatted_number()
            else:
                number = generate_random_number(random.choice([8, 9, 10]))

            error_type = random.choice(["substitution", "transposition"])
            modified = ensure_different(number, make_error(number, error_type), error_type)
            q_text = f"Are the following numbers identical?\n\nNumber A: {number}\nNumber B: {modified}"
            if q_text not in seen_texts:
                break

        if len(modified) != len(number):
            correct_answer = "No, they differ in length" if difficulty != "Hard" else "No, a digit is missing or added"
        elif error_type == "transposition" and difficulty == "Hard":
            correct_answer = "No, two adjacent digits are transposed"
        elif error_type == "transposition" and difficulty == "Easy":
            correct_answer = "No, they differ by one digit"
        elif difficulty == "Medium":
            correct_answer = "No, they differ in digits"
        else:
            correct_answer = "No, they differ by one digit"

        choices_map = {
            "Easy": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, they differ in length",
                "No, they differ in formatting"
            ],
            "Medium": [
                "Yes, they are identical",
                "No, they differ in digits",
                "No, they differ in formatting",
                "No, they differ in length"
            ],
            "Hard": [
                "Yes, they are identical",
                "No, they differ by one digit",
                "No, two adjacent digits are transposed",
                "No, a digit is missing or added"
            ],
        }

        all_questions[idx] = {
            "id": idx + 1,
            "subtest": "Clerical Ability",
            "module": "Name and Number Comparison",
            "subtopic": "Number Comparison",
            "difficulty": difficulty,
            "question": q_text,
            "choices": choices_map[difficulty],
            "answer": correct_answer,
            "explanation": get_error_explanation(number, modified, error_type),
            "tags": [f"{error_type}-error", "dedup-replacement"],
            "category": ["Sub-Professional"],
            "language": "English"
        }
        seen_texts[q_text] = idx

    # Re-assign IDs after dedup
    for i, q in enumerate(all_questions):
        q["id"] = i + 1

    # Validate
    assert len(all_questions) == 600, f"Expected 600 questions, got {len(all_questions)}"
    assert all(q["difficulty"] == "Easy" for q in all_questions[:200])
    assert all(q["difficulty"] == "Medium" for q in all_questions[200:400])
    assert all(q["difficulty"] == "Hard" for q in all_questions[400:600])

    # Verify all answers are in choices
    for q in all_questions:
        assert q["answer"] in q["choices"], (
            f"Question {q['id']}: answer '{q['answer']}' not in choices {q['choices']}"
        )

    # Final duplicate check
    final_texts = [q["question"] for q in all_questions]
    final_dupes = len(final_texts) - len(set(final_texts))
    if final_dupes > 0:
        print(f"WARNING: {final_dupes} duplicates remain after dedup pass")

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability",
        "name-and-number-comparison", "number-comparison"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Generated {len(all_questions)} questions")
    print(f"  Easy: {sum(1 for q in all_questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in all_questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in all_questions if q['difficulty'] == 'Hard')}")
    print(f"  Duplicates fixed: {len(duplicates)}")
    print(f"Output: {output_path}")


if __name__ == "__main__":
    main()
