"""
Generate 400 additional business and office filing questions (IDs 201-600).
Covers: company names, acronyms, numeric names, government offices, The-rule, mixed filing.
"""
import json
import random
import itertools

random.seed(42)

questions = []
current_id = 201

# Data pools
COMPANIES = [
    ("Ayala Corporation", "Ayala"),
    ("Globe Telecom", "Globe"),
    ("Jollibee Foods Corporation", "Jollibee"),
    ("Manila Water", "Manila"),
    ("San Miguel Corporation", "San"),
    ("Cebu Pacific", "Cebu"),
    ("Metrobank", "Metrobank"),
    ("SM Investments", "SM"),
    ("PLDT", "PLDT"),
    ("BDO", "BDO"),
    ("Meralco", "Meralco"),
    ("Aboitiz Power", "Aboitiz"),
    ("Universal Robina Corporation", "Universal"),
    ("Petron Corporation", "Petron"),
    ("Shell Philippines", "Shell"),
    ("Toyota Motor Philippines", "Toyota"),
    ("Nestle Philippines", "Nestle"),
    ("Procter and Gamble Philippines", "Procter"),
    ("Unilever Philippines", "Unilever"),
    ("Bench", "Bench"),
    ("Mercury Drug", "Mercury"),
    ("Puregold", "Puregold"),
    ("Robinsons Land", "Robinsons"),
    ("Vista Land", "Vista"),
    ("Megaworld Corporation", "Megaworld"),
    ("Filinvest Land", "Filinvest"),
    ("Century Pacific Food", "Century"),
    ("Monde Nissin", "Monde"),
    ("Alaska Milk Corporation", "Alaska"),
    ("Del Monte Philippines", "Del"),
    ("Gardenia Bakeries Philippines", "Gardenia"),
    ("Lucky Me", "Lucky"),
    ("Oishi", "Oishi"),
    ("Rebisco", "Rebisco"),
    ("Liwayway Marketing", "Liwayway"),
    ("Splash Corporation", "Splash"),
    ("Lamoiyan Corporation", "Lamoiyan"),
    ("Emperador Inc", "Emperador"),
    ("Tanduay Distillers", "Tanduay"),
    ("Ginebra San Miguel", "Ginebra"),
    ("Asia Brewery", "Asia"),
    ("Pilipinas Shell", "Pilipinas"),
    ("Phoenix Petroleum", "Phoenix"),
    ("Caltex Philippines", "Caltex"),
    ("Total Philippines", "Total"),
    ("Converge ICT", "Converge"),
    ("DITO Telecommunity", "DITO"),
    ("Smart Communications", "Smart"),
    ("Sun Cellular", "Sun"),
    ("Cherry Mobile", "Cherry"),
]

THE_COMPANIES = [
    ("The Manila Hotel", "Manila Hotel"),
    ("The Philippine Star", "Philippine Star"),
    ("The Freeman", "Freeman"),
    ("The Manila Times", "Manila Times"),
    ("The Daily Tribune", "Daily Tribune"),
    ("The Philippine Daily Inquirer", "Philippine Daily Inquirer"),
    ("The Manila Bulletin", "Manila Bulletin"),
    ("The Palawan Express", "Palawan Express"),
    ("The Visayan Daily Star", "Visayan Daily Star"),
    ("The Mindanao Times", "Mindanao Times"),
    ("The Sunday Times", "Sunday Times"),
    ("The Evening Post", "Evening Post"),
    ("The Business Mirror", "Business Mirror"),
    ("The Standard", "Standard"),
    ("The Nation", "Nation"),
]

NUMERIC_NAMES = [
    ("7-Eleven", "Seven-Eleven", "S"),
    ("3M Philippines", "Three M Philippines", "T"),
    ("8th Wonder Cafe", "Eighth Wonder Cafe", "E"),
    ("1st Choice Printing", "First Choice Printing", "F"),
    ("24/7 Express", "Twentyfour Seven Express", "T"),
    ("100 Islands Resort", "One Hundred Islands Resort", "O"),
    ("9th Avenue Bistro", "Ninth Avenue Bistro", "N"),
    ("5th Avenue Salon", "Fifth Avenue Salon", "F"),
    ("2nd Street Bakery", "Second Street Bakery", "S"),
    ("4th Estate Publishing", "Fourth Estate Publishing", "F"),
    ("6th Sense Marketing", "Sixth Sense Marketing", "S"),
    ("10th Floor Cafe", "Tenth Floor Cafe", "T"),
    ("3rd Wave Coffee", "Third Wave Coffee", "T"),
    ("12 Monkeys Bar", "Twelve Monkeys Bar", "T"),
    ("21 Grams Cafe", "Twentyone Grams Cafe", "T"),
    ("50 Shades Salon", "Fifty Shades Salon", "F"),
    ("99 Ranch Market", "Ninetynine Ranch Market", "N"),
    ("4 Seasons Catering", "Four Seasons Catering", "F"),
    ("5 Star Printing", "Five Star Printing", "F"),
    ("2GO Travel", "Two GO Travel", "T"),
]

ACRONYMS = [
    ("CSC", "C-S-C"),
    ("NBI", "N-B-I"),
    ("BIR", "B-I-R"),
    ("SSS", "S-S-S"),
    ("GSIS", "G-S-I-S"),
    ("COA", "C-O-A"),
    ("BSP", "B-S-P"),
    ("DENR", "D-E-N-R"),
    ("DILG", "D-I-L-G"),
    ("DOLE", "D-O-L-E"),
    ("DOJ", "D-O-J"),
    ("DOT", "D-O-T"),
    ("DPWH", "D-P-W-H"),
    ("DSWD", "D-S-W-D"),
    ("TESDA", "T-E-S-D-A"),
    ("PAGASA", "P-A-G-A-S-A"),
    ("PNP", "P-N-P"),
    ("AFP", "A-F-P"),
    ("CHED", "C-H-E-D"),
    ("NAPOLCOM", "N-A-P-O-L-C-O-M"),
    ("PCSO", "P-C-S-O"),
    ("POEA", "P-O-E-A"),
    ("OWWA", "O-W-W-A"),
    ("LTO", "L-T-O"),
    ("LRA", "L-R-A"),
    ("PRC", "P-R-C"),
    ("SEC", "S-E-C"),
    ("DTI", "D-T-I"),
    ("BOC", "B-O-C"),
    ("NEDA", "N-E-D-A"),
    ("DICT", "D-I-C-T"),
    ("DOST", "D-O-S-T"),
    ("DAR", "D-A-R"),
    ("DA", "D-A"),
    ("DBM", "D-B-M"),
    ("DOH", "D-O-H"),
    ("DFA", "D-F-A"),
    ("DOE", "D-O-E"),
    ("DOTC", "D-O-T-C"),
    ("HUDCC", "H-U-D-C-C"),
]

GOVT_OFFICES = [
    ("Department of Education", "Education", "E"),
    ("Department of Health", "Health", "H"),
    ("Department of Justice", "Justice", "J"),
    ("Department of Finance", "Finance", "F"),
    ("Department of Tourism", "Tourism", "T"),
    ("Department of Agriculture", "Agriculture", "A"),
    ("Department of Trade and Industry", "Trade and Industry", "T"),
    ("Department of Labor and Employment", "Labor and Employment", "L"),
    ("Department of Budget and Management", "Budget and Management", "B"),
    ("Department of the Interior and Local Government", "Interior and Local Government", "I"),
    ("Department of Science and Technology", "Science and Technology", "S"),
    ("Department of Social Welfare and Development", "Social Welfare and Development", "S"),
    ("Department of Public Works and Highways", "Public Works and Highways", "P"),
    ("Department of National Defense", "National Defense", "N"),
    ("Department of Environment and Natural Resources", "Environment and Natural Resources", "E"),
    ("Department of Transportation", "Transportation", "T"),
    ("Department of Energy", "Energy", "E"),
    ("Department of Foreign Affairs", "Foreign Affairs", "F"),
    ("Department of Agrarian Reform", "Agrarian Reform", "A"),
    ("Department of Information and Communications Technology", "Information and Communications Technology", "I"),
    ("Bureau of Internal Revenue", "Internal Revenue", "I"),
    ("Bureau of Customs", "Customs", "C"),
    ("Bureau of Immigration", "Immigration", "I"),
    ("Bureau of Fire Protection", "Fire Protection", "F"),
    ("Bureau of Jail Management and Penology", "Jail Management and Penology", "J"),
    ("Bureau of Fisheries and Aquatic Resources", "Fisheries and Aquatic Resources", "F"),
    ("Office of the President", "President", "P"),
    ("Office of the Vice President", "Vice President", "V"),
    ("Office of the Ombudsman", "Ombudsman", "O"),
    ("Commission on Audit", "Audit", "A"),
    ("Commission on Elections", "Elections", "E"),
    ("Commission on Human Rights", "Human Rights", "H"),
    ("Commission on Higher Education", "Higher Education", "H"),
]


def get_filing_key(name):
    """Get the filing key for any entry."""
    # Check if it's a government office
    for orig, distinctive, _ in GOVT_OFFICES:
        if name == orig:
            return distinctive.lower()
    # Check if it starts with "The "
    for orig, filed in THE_COMPANIES:
        if name == orig:
            return filed.lower()
    # Check if it's a numeric name
    for orig, spelled, _ in NUMERIC_NAMES:
        if name == orig:
            return spelled.lower()
    # Otherwise file as written
    return name.lower()


def sort_entries(entries):
    """Sort entries by their filing keys."""
    return sorted(entries, key=lambda x: get_filing_key(x))


def make_question(qid, difficulty, question_text, choices, answer, explanation, tags):
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Alphabetical Filing",
        "subtopic": "Business and Office Filing",
        "difficulty": difficulty,
        "question": question_text,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English"
    }


# ============================================================
# EASY QUESTIONS (IDs 201-330, ~130 questions)
# ============================================================

# --- Type 1: "Which should be filed FIRST?" with company names only ---
def gen_easy_company_first():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 25 and attempts < 200:
        attempts += 1
        sample = random.sample(COMPANIES, 4)
        names = [s[0] for s in sample]
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[0]
        first_units = [s[1] for s in sample]
        explanation = (
            f"Company names are filed as written. Comparing first units: "
            f"{', '.join(f'{s[1]} ({s[1][0]})' for s in sample)}. "
            f"'{answer.split()[0]}' comes first alphabetically."
        )
        questions.append(make_question(
            current_id, "Easy",
            "Which of the following should be filed FIRST?",
            names, answer, explanation,
            ["company-name"]
        ))
        current_id += 1
        count += 1

gen_easy_company_first()


# --- Type 2: "Which should be filed LAST?" with company names only ---
def gen_easy_company_last():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 20 and attempts < 200:
        attempts += 1
        sample = random.sample(COMPANIES, 4)
        names = [s[0] for s in sample]
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[-1]
        explanation = (
            f"Company names are filed as written. Comparing first units: "
            f"{', '.join(f'{s[1]} ({s[1][0]})' for s in sample)}. "
            f"'{answer.split()[0]}' comes last alphabetically."
        )
        questions.append(make_question(
            current_id, "Easy",
            "Which of the following should be filed LAST?",
            names, answer, explanation,
            ["company-name"]
        ))
        current_id += 1
        count += 1

gen_easy_company_last()


# --- Type 3: "Which should be filed FIRST?" with acronyms only ---
def gen_easy_acronym_first():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 20 and attempts < 200:
        attempts += 1
        sample = random.sample(ACRONYMS, 4)
        names = [s[0] for s in sample]
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[0]
        explanation = (
            f"Acronyms are filed letter by letter. "
            f"Comparing: {', '.join(f'{s[0]} ({s[1]})' for s in sample)}. "
            f"{answer} comes first alphabetically."
        )
        questions.append(make_question(
            current_id, "Easy",
            "Which of the following should be filed FIRST?",
            names, answer, explanation,
            ["acronym"]
        ))
        current_id += 1
        count += 1

gen_easy_acronym_first()

# --- Type 4: "Which should be filed LAST?" with acronyms only ---
def gen_easy_acronym_last():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 20 and attempts < 200:
        attempts += 1
        sample = random.sample(ACRONYMS, 4)
        names = [s[0] for s in sample]
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[-1]
        explanation = (
            f"Acronyms are filed letter by letter. "
            f"Comparing: {', '.join(f'{s[0]} ({s[1]})' for s in sample)}. "
            f"{answer} comes last alphabetically."
        )
        questions.append(make_question(
            current_id, "Easy",
            "Which of the following should be filed LAST?",
            names, answer, explanation,
            ["acronym"]
        ))
        current_id += 1
        count += 1

gen_easy_acronym_last()


# --- Type 5: "Under which letter would X be filed?" for government offices ---
def gen_easy_govt_letter():
    global current_id
    used = set()
    for govt in GOVT_OFFICES:
        if current_id > 290:
            break
        orig, distinctive, letter = govt
        if orig in used:
            continue
        used.add(orig)
        # Generate wrong choices
        wrong_letters = ["D", "O", "B", "C", "T", "N", "F", "A", "E", "H", "S", "L", "P"]
        wrong_letters = [l for l in wrong_letters if l != letter]
        random.shuffle(wrong_letters)
        choices = [letter] + wrong_letters[:3]
        random.shuffle(choices)
        explanation = (
            f"Government offices are filed by the distinctive word. "
            f"'{orig}' is filed as '{distinctive}, {orig.split()[0]} of' — under {letter}."
        )
        questions.append(make_question(
            current_id, "Easy",
            f"Under which letter would '{orig}' be filed?",
            choices, letter, explanation,
            ["government-office"]
        ))
        current_id += 1

gen_easy_govt_letter()


# --- Type 6: "Under which letter would X be filed?" for numeric names ---
def gen_easy_numeric_letter():
    global current_id
    for num in NUMERIC_NAMES:
        if current_id > 310:
            break
        orig, spelled, letter = num
        wrong_letters = list(set(["E", "S", "T", "N", "F", "O", "1", "2", "3", "7", "8", "9"]) - {letter})
        random.shuffle(wrong_letters)
        choices = [letter] + wrong_letters[:3]
        random.shuffle(choices)
        explanation = (
            f"Numbers in business names are spelled out for filing. "
            f"'{orig}' becomes '{spelled}', which files under {letter}."
        )
        questions.append(make_question(
            current_id, "Easy",
            f"Under which letter would '{orig}' be filed?",
            choices, letter, explanation,
            ["numeric-name"]
        ))
        current_id += 1

gen_easy_numeric_letter()

# --- Type 7: "Under which letter would X be filed?" for The-rule ---
def gen_easy_the_letter():
    global current_id
    for the_co in THE_COMPANIES:
        if current_id > 325:
            break
        orig, filed = the_co
        letter = filed[0]
        wrong_letters = ["T", "A", "S", "M", "P", "D", "B", "N", "F", "V"]
        wrong_letters = [l for l in wrong_letters if l != letter]
        random.shuffle(wrong_letters)
        choices = [letter] + wrong_letters[:3]
        random.shuffle(choices)
        explanation = (
            f"When 'The' begins a business name, move it to the end. "
            f"Filed as '{filed} (The)' — under {letter}."
        )
        questions.append(make_question(
            current_id, "Easy",
            f"Under which letter would '{orig}' be filed?",
            choices, letter, explanation,
            ["the-rule", "company-name"]
        ))
        current_id += 1

gen_easy_the_letter()


# --- Type 8: "Which should be filed FIRST?" with government offices ---
def gen_easy_govt_first():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 15 and attempts < 200:
        attempts += 1
        sample = random.sample(GOVT_OFFICES, 4)
        names = [s[0] for s in sample]
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[0]
        # Find distinctive word for answer
        answer_distinctive = next(s[1] for s in sample if s[0] == answer)
        explanation = (
            f"Government offices are filed by the distinctive word. "
            f"Distinctive words: {', '.join(f'{s[1]} ({s[2]})' for s in sample)}. "
            f"'{answer_distinctive}' ({answer_distinctive[0]}) comes first alphabetically."
        )
        questions.append(make_question(
            current_id, "Easy",
            "Which of the following should be filed FIRST?",
            names, answer, explanation,
            ["government-office"]
        ))
        current_id += 1
        count += 1

gen_easy_govt_first()

# Pad easy section to reach ~130 easy questions
def gen_easy_the_first():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 10 and attempts < 200:
        attempts += 1
        sample = random.sample(THE_COMPANIES, 4)
        names = [s[0] for s in sample]
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[0]
        answer_filed = next(s[1] for s in sample if s[0] == answer)
        explanation = (
            f"When 'The' begins a business name, move it to the end. "
            f"Filed as: {', '.join(f'{s[1]} (The)' for s in sample)}. "
            f"'{answer_filed}' ({answer_filed[0]}) comes first alphabetically."
        )
        questions.append(make_question(
            current_id, "Easy",
            "Which of the following should be filed FIRST?",
            names, answer, explanation,
            ["the-rule", "company-name"]
        ))
        current_id += 1
        count += 1

gen_easy_the_first()


# ============================================================
# MEDIUM QUESTIONS (IDs ~331-465, ~135 questions)
# ============================================================

# --- Type 1: Mixed company + acronym, filed FIRST ---
def gen_medium_mixed_first():
    global current_id
    used = set()
    count = 0
    attempts = 0
    while count < 25 and attempts < 300:
        attempts += 1
        co_sample = random.sample(COMPANIES, 2)
        ac_sample = random.sample(ACRONYMS, 2)
        names = [c[0] for c in co_sample] + [a[0] for a in ac_sample]
        random.shuffle(names)
        key = tuple(sorted(names))
        if key in used:
            continue
        used.add(key)
        sorted_names = sort_entries(names)
        answer = sorted_names[0]
        explanation = (
            f"Company names and acronyms are filed as written. "
            f"Comparing first units/letters: {', '.join(f'{n} ({get_filing_key(n)[0].upper()})' for n in names)}. "
            f"'{answer}' comes first alphabetically."
        )
        questions.append(make_question(
            current_id, "Medium",
            "Which of the following should be filed FIRST?",
            names, answer, explanation,
            ["company-name", "acronym", "mixed-filing"]
        ))
        current_id += 1
        count += 1

gen_medium_mixed_first()

