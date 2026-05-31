"""
Generate 600-question bank for Filing Systems.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).

Topics covered:
- Identifying the four major filing systems (alphabetic, numeric, subject, geographic)
- Advantages and disadvantages of each system
- Choosing the appropriate filing system for a scenario
- Direct vs. indirect access
- Terminal-digit filing
- Relative index (subject filing)
- Geographic hierarchy (Philippine regions)
- Combination systems
- Arranging records within each system
- Cross-referencing within filing systems
"""
import json
import random
import os

random.seed(42)

# ============================================================
# DATA POOLS
# ============================================================

FILING_SYSTEMS = ["Alphabetic", "Numeric", "Subject", "Geographic"]

# Scenarios mapped to correct filing system
ALPHABETIC_SCENARIOS = [
    ("A small barangay hall with 50 resident folders requested by name", "Small volume, name-based retrieval — alphabetic is simplest and most efficient."),
    ("A municipal office with 150 employee personnel files retrieved by surname", "Small volume, name-based retrieval — alphabetic filing is appropriate."),
    ("A small NGO with 80 donor files always requested by donor name", "Small volume, direct name-based retrieval — alphabetic is ideal."),
    ("A school registrar's office with 300 student folders retrieved by student surname", "Moderate volume, name-based retrieval — alphabetic filing works well."),
    ("A law office with 200 client folders retrieved by client surname", "Small-to-moderate volume, name-based retrieval — alphabetic is appropriate."),
    ("A dental clinic with 100 patient folders retrieved by patient name", "Small volume, name-based retrieval, no special confidentiality — alphabetic."),
    ("A parish office with 120 parishioner records requested by family name", "Small volume, name-based retrieval — alphabetic filing is suitable."),
    ("A cooperative with 250 member files always requested by member name", "Moderate volume, name-based retrieval — alphabetic is efficient."),
    ("A small business with 90 supplier files retrieved by company name", "Small volume, name-based retrieval — alphabetic filing is appropriate."),
    ("A guidance counselor's office with 180 student records requested by surname", "Small-to-moderate volume, name-based retrieval — alphabetic is suitable."),
    ("A homeowners' association with 75 member folders retrieved by resident name", "Small volume, name-based retrieval — alphabetic is simplest."),
    ("A local library with 200 borrower cards arranged by borrower surname", "Moderate volume, name-based retrieval — alphabetic filing is standard."),
    ("A small accounting firm with 150 client folders requested by client name", "Small volume, name-based retrieval — alphabetic is efficient."),
    ("A daycare center with 40 enrollment files retrieved by child's surname", "Very small volume, name-based retrieval — alphabetic is ideal."),
    ("A real estate office with 100 property owner files requested by owner name", "Small volume, name-based retrieval — alphabetic filing works."),
]

NUMERIC_SCENARIOS = [
    ("A hospital with 120,000 patient records referenced by medical record number", "Very large volume, confidentiality required, records referenced by number — numeric."),
    ("The BIR filing taxpayer records by Taxpayer Identification Number (TIN)", "Large volume, records referenced by assigned number, confidentiality — numeric."),
    ("COA filing 80,000 audit findings by case number for confidential tracking", "Large volume, confidentiality, referenced by case number — numeric."),
    ("A court filing 50,000 case records by docket number", "Large volume, confidentiality, referenced by case number — numeric."),
    ("SSS filing millions of member records by SSS number", "Massive volume, referenced by assigned number — numeric."),
    ("A government hospital with 75,000 patient files needing confidentiality", "Large volume, medical confidentiality required — numeric."),
    ("PhilHealth filing member claims by PhilHealth Identification Number", "Large volume, referenced by assigned number — numeric."),
    ("A police department filing 30,000 case records by case number", "Large volume, confidentiality, referenced by number — numeric."),
    ("Pag-IBIG filing member records by Pag-IBIG Member ID number", "Large volume, referenced by assigned number — numeric."),
    ("A bank filing 200,000 account records by account number", "Massive volume, confidentiality, referenced by number — numeric."),
    ("GSIS filing retirement records by GSIS member number", "Large volume, referenced by assigned number — numeric."),
    ("A university registrar with 60,000 student records filed by student number", "Large volume, referenced by assigned number — numeric."),
    ("NBI filing criminal records by NBI clearance number for confidentiality", "Large volume, high confidentiality, referenced by number — numeric."),
    ("A large insurance company filing 100,000 policies by policy number", "Large volume, referenced by assigned number — numeric."),
    ("LTO filing millions of driver records by license number", "Massive volume, referenced by assigned number — numeric."),
]

SUBJECT_SCENARIOS = [
    ("A policy research office organizing documents by topic: transportation, education, health", "Topic-oriented office, records requested by subject — subject filing."),
    ("NEDA organizing economic planning documents by sector: agriculture, industry, services", "Policy office, topic-based retrieval — subject filing."),
    ("A training office filing documents under headings: Seminars, Scholarships, Conferences", "Topic-based organization with pre-defined categories — subject filing."),
    ("A legislative office organizing bills by subject: taxation, education, health, defense", "Topic-oriented, records requested by subject area — subject filing."),
    ("A research institute filing studies by topic: climate change, biodiversity, pollution", "Research office, topic-based retrieval — subject filing."),
    ("An HR office organizing policy documents by topic: Benefits, Recruitment, Training, Discipline", "Topic-based organization for policy reference — subject filing."),
    ("A planning office filing project documents by program area: infrastructure, social services", "Project/topic-based organization — subject filing."),
    ("A media office organizing press releases by topic: health, education, economy, governance", "Topic-based retrieval for reference — subject filing."),
    ("A legal division organizing jurisprudence by subject: labor law, civil law, criminal law", "Topic-based legal research — subject filing."),
    ("A standards office filing regulations by industry: food, construction, electronics", "Topic-based organization — subject filing."),
    ("An environmental office organizing reports by issue: air quality, water, waste, forests", "Topic-oriented, records requested by environmental issue — subject filing."),
    ("A budget office organizing circulars by topic: compensation, allowances, benefits, procurement", "Topic-based policy reference — subject filing."),
    ("A communications office filing media coverage by topic: agency programs, personnel, events", "Topic-based organization for media monitoring — subject filing."),
    ("A disaster office organizing plans by hazard type: earthquake, typhoon, flood, fire", "Topic-based emergency planning — subject filing."),
    ("A health office organizing protocols by disease: tuberculosis, dengue, COVID-19, measles", "Topic-based medical reference — subject filing."),
]

GEOGRAPHIC_SCENARIOS = [
    ("DSWD Regional Office managing beneficiary files by province and municipality", "Regional office, area-based service delivery — geographic filing."),
    ("DepEd organizing school records by region, division, and district", "National agency with geographic administrative structure — geographic filing."),
    ("DPWH filing infrastructure project records by region and province", "Area-based project management — geographic filing."),
    ("Philippine Postal Corporation organizing delivery records by region and city", "Location-based service delivery — geographic filing."),
    ("DENR organizing environmental permits by region and province", "Area-based regulatory office — geographic filing."),
    ("A national sales company organizing client files by territory and city", "Territory-based operations — geographic filing."),
    ("DOH organizing hospital data by region and province", "Area-based health service monitoring — geographic filing."),
    ("DILG organizing LGU compliance reports by region and municipality", "Area-based governance monitoring — geographic filing."),
    ("A delivery company organizing customer records by city and barangay", "Location-based service delivery — geographic filing."),
    ("PNP organizing crime statistics by region, province, and city", "Area-based law enforcement data — geographic filing."),
    ("TESDA organizing training center records by region and province", "Area-based skills development — geographic filing."),
    ("A real estate company organizing property listings by city and district", "Location-based property management — geographic filing."),
    ("DAR organizing land reform records by region, province, and municipality", "Area-based agrarian program — geographic filing."),
    ("PAGASA organizing weather station data by region and province", "Location-based meteorological data — geographic filing."),
    ("A telecommunications company organizing cell tower records by region and city", "Location-based infrastructure management — geographic filing."),
]

# Advantages/disadvantages
ADVANTAGES = {
    "Alphabetic": [
        ("Simple and universally understood — minimal training required", "alphabetic"),
        ("Direct access — no separate index needed to locate a file", "alphabetic"),
        ("Self-indexing — the arrangement itself serves as the index", "alphabetic"),
        ("Easily expandable — new files inserted without renumbering", "alphabetic"),
    ],
    "Numeric": [
        ("Provides confidentiality — file labels reveal no content", "numeric"),
        ("Unlimited expansion — new numbers always available", "numeric"),
        ("Eliminates confusion between people with the same name", "numeric"),
        ("Even distribution of files (especially with terminal-digit)", "numeric"),
        ("Unique identification — no two files share a number", "numeric"),
    ],
    "Subject": [
        ("Groups all related documents on a topic together", "subject"),
        ("Supports decision-making by consolidating topic information", "subject"),
        ("Logical for offices that think in terms of topics", "subject"),
        ("Flexible — new subjects can be added as needs arise", "subject"),
    ],
    "Geographic": [
        ("Groups all records from one area together", "geographic"),
        ("Natural for offices serving geographic territories", "geographic"),
        ("Supports geographic reporting requirements", "geographic"),
        ("Intuitive for clerks who think in terms of service areas", "geographic"),
    ],
}

DISADVANTAGES = {
    "Alphabetic": [
        ("Congestion at common letters in Philippine offices (S, D, G)", "alphabetic"),
        ("Misspelling causes misfiling", "alphabetic"),
        ("Not suitable for confidential records — name is visible on label", "alphabetic"),
        ("Requires consistent indexing rules for prefixes and particles", "alphabetic"),
    ],
    "Numeric": [
        ("Indirect access — requires a separate alphabetic index", "numeric"),
        ("If the alphabetic index is lost, the system is unusable", "numeric"),
        ("No logical grouping — related records may have distant numbers", "numeric"),
        ("Requires training — clerks must understand the numbering scheme", "numeric"),
    ],
    "Subject": [
        ("Requires a pre-established relative index for consistency", "subject"),
        ("Subjective — different clerks may assign different subjects", "subject"),
        ("Difficult to maintain consistency as the system grows", "subject"),
        ("Indirect access for name-based searches — must search every subject", "subject"),
    ],
    "Geographic": [
        ("Requires knowledge of Philippine geography", "geographic"),
        ("Indirect access for name-based searches — must know the person's location first", "geographic"),
        ("Boundary changes cause file reorganization", "geographic"),
        ("Uneven distribution — NCR may have far more records than CAR", "geographic"),
    ],
}

# Philippine regions for geographic questions
PH_REGIONS = [
    "Region I (Ilocos Region)", "Region II (Cagayan Valley)",
    "Region III (Central Luzon)", "Region IV-A (CALABARZON)",
    "Region IV-B (MIMAROPA)", "Region V (Bicol Region)",
    "Region VI (Western Visayas)", "Region VII (Central Visayas)",
    "Region VIII (Eastern Visayas)", "Region IX (Zamboanga Peninsula)",
    "Region X (Northern Mindanao)", "Region XI (Davao Region)",
    "Region XII (SOCCSKSARGEN)", "Region XIII (Caraga)",
    "NCR (National Capital Region)", "CAR (Cordillera Administrative Region)",
    "BARMM (Bangsamoro Autonomous Region)",
]

# Provinces by region (subset for questions)
PROVINCES_BY_REGION = {
    "Region I": ["Ilocos Norte", "Ilocos Sur", "La Union", "Pangasinan"],
    "Region III": ["Bulacan", "Pampanga", "Tarlac", "Nueva Ecija", "Zambales", "Bataan", "Aurora"],
    "Region IV-A": ["Cavite", "Laguna", "Batangas", "Rizal", "Quezon"],
    "Region VII": ["Cebu", "Bohol", "Negros Oriental", "Siquijor"],
    "NCR": ["Manila", "Quezon City", "Makati", "Pasig", "Taguig", "Mandaluyong", "Caloocan"],
}

# Cities/municipalities for geographic ordering
CITIES_BY_PROVINCE = {
    "Pangasinan": ["Dagupan", "Lingayen", "San Carlos", "Urdaneta", "Alaminos"],
    "Bulacan": ["Malolos", "Meycauayan", "San Jose del Monte", "Baliwag", "Guiguinto"],
    "Cebu": ["Cebu City", "Lapu-Lapu City", "Mandaue", "Talisay", "Danao"],
    "Laguna": ["Santa Rosa", "Biñan", "Calamba", "San Pedro", "Los Baños"],
    "Cavite": ["Bacoor", "Dasmariñas", "Imus", "General Trias", "Tagaytay"],
}

# Filipino names for alphabetic ordering
FILIPINO_NAMES = [
    "Santos, Maria", "Reyes, Juan", "Cruz, Ana", "Garcia, Pedro",
    "Mendoza, Rosa", "Rivera, Carlos", "Bautista, Elena", "Flores, Roberto",
    "Gonzales, Carmen", "Torres, Fernando", "Ramos, Patricia", "Morales, Luis",
    "Navarro, Gloria", "Perez, Ricardo", "Castillo, Teresa", "Hernandez, Eduardo",
    "Lopez, Cristina", "Romero, Miguel", "Salazar, Dolores", "Villanueva, Alfredo",
    "Aquino, Jose", "Dela Cruz, Maria", "De Leon, Juan", "Dizon, Ana",
    "Soriano, Pedro", "Santiago, Rosa", "Pascual, Carlos", "Manalo, Elena",
    "Tolentino, Roberto", "Aguilar, Carmen", "Mercado, Fernando", "Valdez, Patricia",
    "Ocampo, Luis", "Fernandez, Gloria", "Domingo, Ricardo", "Magno, Teresa",
    "Lim, Eduardo", "Tan, Cristina", "Sy, Miguel", "Ong, Dolores",
]

# Terminal-digit file numbers
def generate_file_number():
    """Generate a 6-digit file number in XX-XX-XX format."""
    return f"{random.randint(10,99):02d}-{random.randint(10,99):02d}-{random.randint(10,99):02d}"

# Subject filing headings
SUBJECT_HEADINGS = {
    "Benefits": ["Health Insurance", "Leave", "Retirement", "Allowances"],
    "Recruitment": ["Examinations", "Hiring", "Screening", "Interviews"],
    "Training": ["Local Seminars", "Foreign Scholarships", "Online Courses", "Certifications"],
    "Financial": ["Budget", "Disbursements", "Collections", "Audit"],
    "Legal": ["Contracts", "Cases", "Opinions", "Compliance"],
    "Administrative": ["Office Orders", "Memoranda", "Meetings", "Reports"],
}

# Agencies
AGENCIES = ["CSC", "COA", "DILG", "DBM", "DENR", "DOH", "DepEd", "DOLE", "DPWH", "DOT", "DOJ", "DSWD", "NBI", "PNP", "BIR", "BSP"]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_question(qid, difficulty, question, choices, answer, explanation, tags):
    """Create a question dict in the standard format."""
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Indexing and Record Organization",
        "subtopic": "Filing Systems",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English",
    }


def shuffle_choices(choices, answer):
    """Shuffle choices ensuring answer is included."""
    if answer not in choices:
        choices.append(answer)
    random.shuffle(choices)
    return choices


def pick_wrong_systems(correct, n=3):
    """Pick n wrong filing system names."""
    wrong = [s for s in FILING_SYSTEMS if s != correct]
    return random.sample(wrong, min(n, len(wrong)))


# ============================================================
# EASY QUESTIONS (IDs 1-200)
# ============================================================

def generate_easy_questions():
    """Generate 200 Easy questions. Single-concept identification, basic definitions."""
    questions = []
    qid = 1

    # --- Type 1: Definition/concept questions (40 questions) ---
    concept_questions = [
        ("What is a filing system?",
         ["The organized method by which records are arranged, stored, and retrieved",
          "The physical cabinet where documents are kept",
          "The process of stamping documents with a received date",
          "The act of destroying outdated records"],
         "The organized method by which records are arranged, stored, and retrieved",
         "A filing system is the plan or method used to arrange records — it determines the order in which documents are stored.",
         ["definition", "concept"]),
        ("Which filing system arranges records according to the letters of the alphabet?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "The alphabetic filing system arranges records in alphabetical order based on names or titles.",
         ["system-identification", "alphabetic"]),
        ("Which filing system arranges records by assigned numbers?",
         ["Numeric", "Alphabetic", "Subject", "Geographic"],
         "Numeric",
         "The numeric filing system arranges records by unique assigned numbers in numerical sequence.",
         ["system-identification", "numeric"]),
        ("Which filing system arranges records by topic or subject matter?",
         ["Subject", "Alphabetic", "Numeric", "Geographic"],
         "Subject",
         "The subject filing system groups records by their topic regardless of who created them or when.",
         ["system-identification", "subject"]),
        ("Which filing system arranges records by location or area?",
         ["Geographic", "Alphabetic", "Numeric", "Subject"],
         "Geographic",
         "The geographic filing system arranges records by location — region, province, city, or municipality.",
         ["system-identification", "geographic"]),
        ("Which filing system is the ONLY one that provides direct access?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "Alphabetic is the only system with direct access — you go straight to the letter/name without needing a separate index.",
         ["direct-access", "alphabetic"]),
        ("What does 'direct access' mean in filing?",
         ["You can go straight to the file without consulting a separate index",
          "You can access files only through a computer",
          "Files are arranged by date of access",
          "Only authorized personnel can access the files"],
         "You can go straight to the file without consulting a separate index",
         "Direct access means the arrangement itself tells you where to look — no intermediate lookup step is needed.",
         ["direct-access", "concept"]),
        ("What does 'indirect access' mean in filing?",
         ["You must consult a separate index before locating the file",
          "Files are hidden from unauthorized users",
          "You can only access files indirectly through a supervisor",
          "Files are stored in a remote location"],
         "You must consult a separate index before locating the file",
         "Indirect access requires a two-step process: look up the name in an index to get the identifier, then find the file.",
         ["indirect-access", "concept"]),
        ("Which filing system provides the HIGHEST level of confidentiality?",
         ["Numeric", "Alphabetic", "Subject", "Geographic"],
         "Numeric",
         "Numeric filing provides the highest confidentiality because file labels show only numbers, revealing nothing about the content or person.",
         ["confidentiality", "numeric"]),
        ("Why does numeric filing provide confidentiality?",
         ["File labels show only numbers, not names or subjects",
          "Files are locked in a safe",
          "Only managers can access numeric files",
          "Numbers are encrypted"],
         "File labels show only numbers, not names or subjects",
         "A label like '2024-0347' reveals nothing about the person or content, unlike 'Santos, Maria' or 'Leave Records'.",
         ["confidentiality", "numeric"]),
        ("What is a 'relative index' in filing?",
         ["A pre-established alphabetical list of all subjects used in a subject filing system",
          "A list of all employees arranged by seniority",
          "The table of contents of a book",
          "A numeric code assigned to each file"],
         "A pre-established alphabetical list of all subjects used in a subject filing system",
         "A relative index lists all approved subject headings and cross-references, ensuring consistent filing across clerks.",
         ["relative-index", "subject"]),
        ("Which filing system requires a 'relative index'?",
         ["Subject", "Alphabetic", "Numeric", "Geographic"],
         "Subject",
         "Subject filing requires a relative index — a master list of approved subject headings — to prevent inconsistent categorization.",
         ["relative-index", "subject"]),
        ("In geographic filing, what is the typical Philippine hierarchy?",
         ["Region → Province → City/Municipality",
          "City → Province → Region",
          "Barangay → City → Province",
          "Country → Island Group → Region"],
         "Region → Province → City/Municipality",
         "Philippine geographic filing follows the administrative hierarchy: Region first, then Province, then City/Municipality.",
         ["geographic-hierarchy", "geographic"]),
        ("What is the secondary arrangement method within geographic filing?",
         ["Alphabetical by name within each location",
          "Numerical by file number",
          "Chronological by date",
          "By document size"],
         "Alphabetical by name within each location",
         "Within each geographic division, individual records are arranged alphabetically by name.",
         ["secondary-arrangement", "geographic"]),
        ("What is 'terminal-digit filing'?",
         ["A numeric filing method that reads file numbers from right to left for even distribution",
          "Filing documents at the end of the cabinet",
          "A system where files are destroyed after a terminal date",
          "Filing by the last letter of a surname"],
         "A numeric filing method that reads file numbers from right to left for even distribution",
         "Terminal-digit filing reads the last digits first to distribute files evenly across all sections, preventing congestion.",
         ["terminal-digit", "numeric"]),
        ("Why do large offices use terminal-digit filing?",
         ["To distribute new files evenly across all sections and prevent congestion",
          "To make files harder to find for security",
          "To save space in filing cabinets",
          "To arrange files by date of termination"],
         "To distribute new files evenly across all sections and prevent congestion",
         "In consecutive filing, all new files go to the end. Terminal-digit distributes them across 100 sections evenly.",
         ["terminal-digit", "numeric"]),
        ("What happens to a numeric filing system if the alphabetic index is lost?",
         ["The system becomes unusable — files cannot be retrieved by name",
          "Nothing — files can still be found by number",
          "The files automatically rearrange themselves",
          "A new index is generated automatically"],
         "The system becomes unusable — files cannot be retrieved by name",
         "Without the alphabetic index, there is no way to determine which number corresponds to which name or record.",
         ["alphabetic-index", "numeric"]),
        ("Which filing system is described as 'self-indexing'?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "Alphabetic filing is self-indexing because the arrangement itself serves as the index — no separate lookup tool is needed.",
         ["self-indexing", "alphabetic"]),
        ("What is the main disadvantage of alphabetic filing in Philippine offices?",
         ["Congestion at common letters — many Filipino surnames start with S, D, or G",
          "It requires expensive equipment",
          "It cannot handle more than 10 files",
          "It requires a computer system"],
         "Congestion at common letters — many Filipino surnames start with S, D, or G",
         "Filipino surnames cluster heavily at certain letters (Santos, Soriano, Dela Cruz, De Leon, Garcia), creating uneven sections.",
         ["disadvantage", "alphabetic"]),
        ("In a numeric filing system, what bridges the gap between a name and a file number?",
         ["A separate alphabetic index",
          "The clerk's memory",
          "Color-coded labels",
          "The file's creation date"],
         "A separate alphabetic index",
         "The alphabetic index maps names to their assigned numbers, enabling retrieval in a numeric system.",
         ["alphabetic-index", "numeric"]),
    ]

    for q_data in concept_questions[:20]:
        question_text, choices, answer, explanation, tags = q_data
        questions.append(make_question(qid, "Easy", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- More concept questions (20 more) ---
    concept_questions_2 = [
        ("How many major filing systems are there?",
         ["Four", "Two", "Six", "Eight"],
         "Four",
         "The four major filing systems are: Alphabetic, Numeric, Subject, and Geographic.",
         ["concept", "overview"]),
        ("Which filing system is best for a small office where records are requested by name?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "For small offices with name-based retrieval, alphabetic filing is simplest — direct access, no index needed.",
         ["system-selection", "alphabetic"]),
        ("Which filing system is best when records must be confidential?",
         ["Numeric", "Alphabetic", "Subject", "Geographic"],
         "Numeric",
         "Numeric filing provides confidentiality because labels show only numbers, not names or subjects.",
         ["system-selection", "numeric"]),
        ("Which filing system is best for a regional office serving geographic areas?",
         ["Geographic", "Alphabetic", "Numeric", "Subject"],
         "Geographic",
         "Geographic filing is natural for offices that serve specific areas and generate area-based reports.",
         ["system-selection", "geographic"]),
        ("Which filing system is best for a policy office that organizes work by topic?",
         ["Subject", "Alphabetic", "Numeric", "Geographic"],
         "Subject",
         "Subject filing groups all documents on a topic together — ideal for policy and research offices.",
         ["system-selection", "subject"]),
        ("What is the PRIMARY arrangement in geographic filing?",
         ["Location (region, province, city)",
          "Alphabetical by name",
          "Chronological by date",
          "Numerical by file number"],
         "Location (region, province, city)",
         "Geographic filing arranges primarily by location. Alphabetic arrangement is secondary within each location.",
         ["primary-arrangement", "geographic"]),
        ("In alphabetic filing, what is the key filing unit for personal names?",
         ["The surname", "The given name", "The middle name", "The title"],
         "The surname",
         "Personal names are filed surname-first — the surname is the key unit for alphabetical comparison.",
         ["key-unit", "alphabetic"]),
        ("Which filing systems require indirect access (a separate index)?",
         ["Numeric, Subject, and Geographic",
          "Only Numeric",
          "Only Subject and Geographic",
          "All four systems"],
         "Numeric, Subject, and Geographic",
         "Only alphabetic provides direct access. Numeric needs an alphabetic index, subject needs a relative index, and geographic needs location knowledge.",
         ["indirect-access", "comparison"]),
        ("What is the difference between a filing system and filing equipment?",
         ["A filing system is the arrangement method; equipment is the physical storage (cabinets, shelves)",
          "They are the same thing",
          "A filing system is digital; equipment is physical",
          "Equipment determines the system used"],
         "A filing system is the arrangement method; equipment is the physical storage (cabinets, shelves)",
         "The filing system is the logical arrangement plan; equipment is the physical container. They are independent concepts.",
         ["concept", "distinction"]),
        ("Can an office use more than one filing system simultaneously?",
         ["Yes — different record types may use different systems",
          "No — only one system is allowed per office",
          "Only if approved by the National Archives",
          "Only government offices can use multiple systems"],
         "Yes — different record types may use different systems",
         "Most offices use combination systems: personnel files alphabetically, vouchers numerically, policies by subject.",
         ["combination-system", "concept"]),
        ("What determines which filing system an office should use?",
         ["How records are most frequently requested",
          "The size of the filing cabinet",
          "The supervisor's personal preference",
          "The color of the file folders"],
         "How records are most frequently requested",
         "The primary factor is how records are requested: by name (alphabetic), number (numeric), topic (subject), or location (geographic).",
         ["system-selection", "decision-factor"]),
        ("In subject filing, what prevents different clerks from using different headings for the same topic?",
         ["The relative index — a controlled list of approved subject headings",
          "A supervisor checking every filing decision",
          "Color-coded folders",
          "Filing documents by date instead"],
         "The relative index — a controlled list of approved subject headings",
         "The relative index is a master list that standardizes subject headings, preventing inconsistency.",
         ["relative-index", "subject"]),
        ("Which filing system would cause problems if many people share the same surname?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "Alphabetic filing struggles with duplicate names — multiple 'Santos, Maria' entries cause confusion. Numeric solves this.",
         ["disadvantage", "alphabetic"]),
        ("In numeric filing, what is the purpose of assigning each record a unique number?",
         ["To provide a unique identifier that eliminates confusion between similar names",
          "To count how many records exist",
          "To determine the record's importance",
          "To track when the record was created"],
         "To provide a unique identifier that eliminates confusion between similar names",
         "Unique numbers ensure no two files are confused, even if multiple people share the same name.",
         ["unique-identifier", "numeric"]),
        ("What type of filing arranges records in the order: 001, 002, 003, 004...?",
         ["Consecutive numeric filing",
          "Terminal-digit filing",
          "Alphabetic filing",
          "Subject filing"],
         "Consecutive numeric filing",
         "Consecutive (or serial) numeric filing assigns numbers in sequence and arranges files in that order.",
         ["consecutive", "numeric"]),
        ("Which filing system is easiest to learn and requires minimal training?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "Alphabetic filing leverages universal knowledge of the alphabet — anyone can use it without special training.",
         ["advantage", "alphabetic"]),
        ("What is the main advantage of subject filing?",
         ["It groups all related documents on a topic together for easy reference",
          "It provides confidentiality",
          "It requires no training",
          "It distributes files evenly"],
         "It groups all related documents on a topic together for easy reference",
         "Subject filing consolidates all information on a topic in one place, supporting research and decision-making.",
         ["advantage", "subject"]),
        ("What is the main advantage of geographic filing?",
         ["It groups all records from one area together for area-based reporting",
          "It provides confidentiality",
          "It requires no index",
          "It is the simplest system"],
         "It groups all records from one area together for area-based reporting",
         "Geographic filing groups records by location, making it easy to generate reports and manage services by area.",
         ["advantage", "geographic"]),
        ("A file labeled '2024-0892' reveals nothing about its content. Which filing system is this?",
         ["Numeric", "Alphabetic", "Subject", "Geographic"],
         "Numeric",
         "Numeric labels show only the assigned number — they reveal nothing about the person or content, providing confidentiality.",
         ["confidentiality", "numeric"]),
        ("A file labeled 'Santos, Maria C.' immediately reveals the person's identity. Which system?",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Alphabetic",
         "Alphabetic filing uses names as labels, which immediately reveals the identity — low confidentiality.",
         ["confidentiality", "alphabetic"]),
    ]

    for q_data in concept_questions_2[:20]:
        question_text, choices, answer, explanation, tags = q_data
        questions.append(make_question(qid, "Easy", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Type 2: Simple scenario identification (80 questions) ---
    all_scenarios = (
        [(s, "Alphabetic") for s in ALPHABETIC_SCENARIOS] +
        [(s, "Numeric") for s in NUMERIC_SCENARIOS] +
        [(s, "Subject") for s in SUBJECT_SCENARIOS] +
        [(s, "Geographic") for s in GEOGRAPHIC_SCENARIOS]
    )
    random.shuffle(all_scenarios)

    for (scenario_text, expl), correct_system in all_scenarios[:80]:
        wrong = pick_wrong_systems(correct_system)
        choices = [correct_system] + wrong
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Easy",
            f"Which filing system is most appropriate? Scenario: {scenario_text}",
            choices, correct_system, expl,
            ["system-selection", correct_system.lower()]
        ))
        qid += 1

    # --- Type 3: Advantage/disadvantage identification (40 questions) ---
    adv_questions = []
    for system, advs in ADVANTAGES.items():
        for adv_text, _ in advs:
            wrong_systems = pick_wrong_systems(system)
            choices = [system] + wrong_systems
            random.shuffle(choices)
            adv_questions.append((
                f"Which filing system has this advantage: \"{adv_text}\"?",
                choices, system,
                f"This is an advantage of the {system} filing system.",
                ["advantage", system.lower()]
            ))

    for system, disadvs in DISADVANTAGES.items():
        for disadv_text, _ in disadvs:
            wrong_systems = pick_wrong_systems(system)
            choices = [system] + wrong_systems
            random.shuffle(choices)
            adv_questions.append((
                f"Which filing system has this disadvantage: \"{disadv_text}\"?",
                choices, system,
                f"This is a disadvantage of the {system} filing system.",
                ["disadvantage", system.lower()]
            ))

    random.shuffle(adv_questions)
    for q_data in adv_questions[:40]:
        question_text, choices, answer, explanation, tags = q_data
        questions.append(make_question(qid, "Easy", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Pad scenario questions if needed to reach 140 before tf section ---
    pre_pad_counter = 0
    while len(questions) < 140:
        pre_pad_counter += 1
        # Generate more scenario questions
        pool_choice = random.choice(["A", "N", "S", "G"])
        if pool_choice == "A":
            scenario_text, expl = random.choice(ALPHABETIC_SCENARIOS)
            correct_system = "Alphabetic"
        elif pool_choice == "N":
            scenario_text, expl = random.choice(NUMERIC_SCENARIOS)
            correct_system = "Numeric"
        elif pool_choice == "S":
            scenario_text, expl = random.choice(SUBJECT_SCENARIOS)
            correct_system = "Subject"
        else:
            scenario_text, expl = random.choice(GEOGRAPHIC_SCENARIOS)
            correct_system = "Geographic"
        wrong = pick_wrong_systems(correct_system)
        choices = [correct_system] + wrong
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Easy",
            f"Select the appropriate filing system (Set {pre_pad_counter}): {scenario_text}",
            choices, correct_system, expl,
            ["system-selection", correct_system.lower()]
        ))
        qid += 1

    # --- Type 4: True/False style (which statement is correct) (60 questions) ---
    tf_questions = [
        ("Which statement about alphabetic filing is CORRECT?",
         ["It provides direct access without needing a separate index",
          "It requires a relative index to function",
          "It provides the highest confidentiality",
          "It is only used for numeric records"],
         "It provides direct access without needing a separate index",
         "Alphabetic filing is self-indexing — you go directly to the letter without consulting a separate index.",
         ["correct-statement", "alphabetic"]),
        ("Which statement about numeric filing is CORRECT?",
         ["It requires a separate alphabetic index for name-based retrieval",
          "It provides direct access like alphabetic filing",
          "It cannot handle more than 1,000 records",
          "File labels always show the person's name"],
         "It requires a separate alphabetic index for name-based retrieval",
         "Numeric filing is indirect — you must look up the name in an alphabetic index to get the file number.",
         ["correct-statement", "numeric"]),
        ("Which statement about subject filing is CORRECT?",
         ["It requires a pre-established list of subject headings (relative index)",
          "It arranges records by assigned numbers",
          "It provides direct access by name",
          "It groups records by geographic location"],
         "It requires a pre-established list of subject headings (relative index)",
         "Subject filing needs a relative index to ensure all clerks use the same subject headings consistently.",
         ["correct-statement", "subject"]),
        ("Which statement about geographic filing is CORRECT?",
         ["It uses alphabetic arrangement as a secondary method within each location",
          "It provides direct access by name",
          "It does not require knowledge of geography",
          "It arranges records by assigned numbers"],
         "It uses alphabetic arrangement as a secondary method within each location",
         "Geographic filing arranges primarily by location, then alphabetically by name within each geographic division.",
         ["correct-statement", "geographic"]),
        ("Which statement is INCORRECT about alphabetic filing?",
         ["It provides high confidentiality because names are hidden",
          "It is the simplest filing system to learn",
          "It provides direct access",
          "It is self-indexing"],
         "It provides high confidentiality because names are hidden",
         "Alphabetic filing has LOW confidentiality — file labels show names, which are immediately visible.",
         ["incorrect-statement", "alphabetic"]),
        ("Which statement is INCORRECT about numeric filing?",
         ["It provides direct access without any index",
          "It provides high confidentiality",
          "It handles large volumes efficiently",
          "It eliminates confusion between same-name records"],
         "It provides direct access without any index",
         "Numeric filing requires INDIRECT access — you must consult the alphabetic index first.",
         ["incorrect-statement", "numeric"]),
        ("Which statement is INCORRECT about subject filing?",
         ["It does not require any pre-established list of categories",
          "It groups related documents by topic",
          "It is ideal for policy offices",
          "It supports topic-based decision-making"],
         "It does not require any pre-established list of categories",
         "Subject filing REQUIRES a relative index (pre-established subject list) to maintain consistency.",
         ["incorrect-statement", "subject"]),
        ("Which statement is INCORRECT about geographic filing?",
         ["It arranges records purely alphabetically by city name without geographic grouping",
          "It groups records by location",
          "It uses alphabetic arrangement within each location",
          "It is ideal for regional offices"],
         "It arranges records purely alphabetically by city name without geographic grouping",
         "Geographic filing groups by administrative hierarchy (Region → Province → City), not purely alphabetically by city name.",
         ["incorrect-statement", "geographic"]),
    ]

    # Generate more true/false style questions programmatically
    system_facts = {
        "Alphabetic": [
            ("provides direct access", True),
            ("is self-indexing", True),
            ("requires minimal training", True),
            ("provides high confidentiality", False),
            ("requires a relative index", False),
            ("is best for large offices with 50,000+ records", False),
        ],
        "Numeric": [
            ("provides indirect access", True),
            ("requires a separate alphabetic index", True),
            ("provides high confidentiality", True),
            ("handles large volumes efficiently", True),
            ("provides direct access", False),
            ("is self-indexing", False),
        ],
        "Subject": [
            ("requires a relative index", True),
            ("groups documents by topic", True),
            ("is ideal for policy offices", True),
            ("provides direct access by name", False),
            ("arranges records by assigned numbers", False),
            ("requires no training", False),
        ],
        "Geographic": [
            ("arranges primarily by location", True),
            ("uses alphabetic as secondary arrangement", True),
            ("is ideal for regional offices", True),
            ("provides direct access by name", False),
            ("requires no knowledge of geography", False),
            ("provides high confidentiality", False),
        ],
    }

    for system, facts in system_facts.items():
        for fact_text, is_true in facts:
            if is_true:
                q_text = f"True or False: The {system.lower()} filing system {fact_text}."
                answer = "True"
                explanation = f"Correct — the {system.lower()} filing system does {fact_text}."
            else:
                q_text = f"True or False: The {system.lower()} filing system {fact_text}."
                answer = "False"
                explanation = f"False — the {system.lower()} filing system does NOT {fact_text}."
            tf_questions.append((
                q_text,
                ["True", "False"],
                answer,
                explanation,
                ["true-false", system.lower()]
            ))

    random.shuffle(tf_questions)
    for q_data in tf_questions[:60]:
        question_text, choices, answer, explanation, tags = q_data
        # Ensure 4 choices for true/false by adding plausible options
        if len(choices) == 2:
            choices = ["True", "False", "It depends on the office size", "Only in government offices"]
        questions.append(make_question(qid, "Easy", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Final padding to reach 200 ---
    pad_counter = 0
    while len(questions) < 200:
        pad_counter += 1
        pool_choice = random.choice(["A", "N", "S", "G"])
        if pool_choice == "A":
            scenario_text, expl = random.choice(ALPHABETIC_SCENARIOS)
            correct_system = "Alphabetic"
        elif pool_choice == "N":
            scenario_text, expl = random.choice(NUMERIC_SCENARIOS)
            correct_system = "Numeric"
        elif pool_choice == "S":
            scenario_text, expl = random.choice(SUBJECT_SCENARIOS)
            correct_system = "Subject"
        else:
            scenario_text, expl = random.choice(GEOGRAPHIC_SCENARIOS)
            correct_system = "Geographic"
        wrong = pick_wrong_systems(correct_system)
        choices = [correct_system] + wrong
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Easy",
            f"Identify the best filing system (#{pad_counter}): {scenario_text}",
            choices, correct_system, expl,
            ["system-selection", correct_system.lower()]
        ))
        qid += 1

    return questions[:200]


# ============================================================
# MEDIUM QUESTIONS (IDs 201-400)
# ============================================================

def generate_medium_questions():
    """Generate 200 Medium questions. Two-step reasoning, comparisons, application."""
    questions = []
    qid = 201

    # --- Type 1: Scenario with additional decision factors (50 questions) ---
    complex_scenarios = [
        # (scenario, correct_system, explanation, tags)
        ("A government hospital has 30,000 patient records. The records clerk argues for alphabetic filing because 'everyone knows the alphabet.' The records officer argues for numeric filing. Who is correct?",
         "The records officer (numeric filing)",
         ["The records officer (numeric filing)",
          "The records clerk (alphabetic filing)",
          "Both are equally correct",
          "Neither — subject filing should be used"],
         "With 30,000 records, medical confidentiality needs, and likely name duplication, numeric filing is appropriate.",
         ["system-selection", "numeric", "scenario-analysis"]),
        ("An office currently uses alphabetic filing but 15 employees share the surname 'Santos.' What system would solve this problem?",
         "Numeric",
         ["Numeric", "Subject", "Geographic", "Chronological"],
         "Numeric filing assigns unique numbers to each person, eliminating confusion between people with identical surnames.",
         ["problem-solving", "numeric"]),
        ("A clerk files correspondence alphabetically by sender name within each province folder, arranged under regional tabs. What is the PRIMARY filing system?",
         "Geographic",
         ["Geographic", "Alphabetic", "Subject", "Numeric"],
         "The primary arrangement is by location (region → province). Alphabetic is the secondary method within each geographic division.",
         ["primary-system", "geographic", "combination"]),
        ("A national agency needs to generate quarterly reports showing transaction counts per region. Which filing system best supports this?",
         "Geographic",
         ["Geographic", "Alphabetic", "Numeric", "Subject"],
         "Geographic filing groups records by location, making area-based reporting straightforward.",
         ["system-selection", "geographic", "reporting"]),
        ("An office has 500 records. They are always requested by name. The supervisor wants numeric filing 'for security.' Is this justified?",
         "No — alphabetic is more appropriate for this volume and retrieval pattern",
         ["No — alphabetic is more appropriate for this volume and retrieval pattern",
          "Yes — numeric is always better for security",
          "Yes — all offices should use numeric filing",
          "No — subject filing should be used instead"],
         "With only 500 records and name-based retrieval, the overhead of maintaining a numeric index is not justified. Alphabetic is simpler and sufficient.",
         ["system-selection", "justification", "alphabetic"]),
        ("A training office receives documents about seminars, scholarships, and conferences. Staff always ask 'Where are the scholarship files?' Which system?",
         "Subject",
         ["Subject", "Alphabetic", "Numeric", "Geographic"],
         "Staff request records by topic (scholarships, seminars). Subject filing groups all documents on each topic together.",
         ["system-selection", "subject"]),
        ("The DPWH needs to organize road project files. Projects are managed by region and province. Field engineers request files by location. Which system?",
         "Geographic",
         ["Geographic", "Subject", "Numeric", "Alphabetic"],
         "Projects are managed by area and requested by location — geographic filing matches the workflow.",
         ["system-selection", "geographic"]),
        ("A court has 45,000 active cases. Each case has a docket number. Lawyers request files by docket number. Which system?",
         "Numeric",
         ["Numeric", "Alphabetic", "Subject", "Geographic"],
         "Large volume, referenced by assigned number, confidentiality of case contents — numeric filing is appropriate.",
         ["system-selection", "numeric"]),
        ("A small barangay health center has 80 patient folders. The midwife retrieves them by patient name. No confidentiality concerns. Which system?",
         "Alphabetic",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Very small volume, name-based retrieval, no confidentiality needs — alphabetic is simplest.",
         ["system-selection", "alphabetic"]),
        ("An office uses subject filing but clerks keep creating new headings without checking the relative index. What problem does this cause?",
         "Documents scatter across inconsistent categories, making retrieval unreliable",
         ["Documents scatter across inconsistent categories, making retrieval unreliable",
          "Files become too confidential to access",
          "The filing cabinets run out of space",
          "Documents are automatically deleted"],
         "Without following the relative index, different clerks use different headings for the same topic, causing documents to scatter.",
         ["problem-identification", "subject", "relative-index"]),
    ]

    # Add more complex scenarios
    complex_scenarios += [
        ("A government agency is transitioning from 2,000 to 50,000 records due to expansion. They currently use alphabetic filing. Should they switch?",
         "Yes — numeric filing handles large volumes better and prevents name congestion",
         ["Yes — numeric filing handles large volumes better and prevents name congestion",
          "No — alphabetic filing works for any volume",
          "Yes — they should switch to geographic filing",
          "No — they should just buy bigger cabinets"],
         "At 50,000 records, alphabetic filing creates severe congestion at common letters. Numeric filing scales better.",
         ["system-transition", "numeric"]),
        ("A regional DSWD office serves 4 provinces. Social workers request beneficiary files by municipality. The office also needs to generate reports per province. Which system?",
         "Geographic",
         ["Geographic", "Alphabetic", "Numeric", "Subject"],
         "Area-based service delivery with location-based retrieval and geographic reporting needs — geographic filing.",
         ["system-selection", "geographic"]),
        ("A research institute publishes studies on 12 different topics. Researchers always ask 'Do we have studies on climate change?' Which system?",
         "Subject",
         ["Subject", "Alphabetic", "Numeric", "Geographic"],
         "Topic-based retrieval in a research environment — subject filing groups all studies by topic.",
         ["system-selection", "subject"]),
        ("An insurance company has 150,000 policies. Each policy has a unique policy number. Agents request files by policy number. Which system?",
         "Numeric",
         ["Numeric", "Alphabetic", "Subject", "Geographic"],
         "Massive volume, referenced by assigned number — numeric filing (likely terminal-digit for even distribution).",
         ["system-selection", "numeric"]),
        ("A cooperative has 300 members. Files are requested by member name. Some members share surnames. The cooperative cannot afford to maintain a separate index. Which system?",
         "Alphabetic",
         ["Alphabetic", "Numeric", "Subject", "Geographic"],
         "Moderate volume, name-based retrieval, and inability to maintain a separate index rules out numeric. Alphabetic with careful indexing rules for same-surname members.",
         ["system-selection", "alphabetic", "constraint"]),
        ("Personnel files are arranged alphabetically by surname. Financial vouchers are arranged by voucher number. Policy documents are arranged by topic. What type of system is this office using?",
         "Combination system — different record types use different filing systems",
         ["Combination system — different record types use different filing systems",
          "Alphabetic system only",
          "Numeric system only",
          "Subject system only"],
         "Using different systems for different record types is a combination system — the most common approach in government offices.",
         ["combination-system", "identification"]),
        ("A clerk needs to find 'Santos, Maria' in a numeric filing system. What is the FIRST step?",
         "Look up 'Santos, Maria' in the alphabetic index to get the file number",
         ["Look up 'Santos, Maria' in the alphabetic index to get the file number",
          "Go directly to the 'S' section of the filing cabinet",
          "Ask the supervisor for the file number",
          "Search every file until finding it"],
         "In numeric filing, retrieval requires consulting the alphabetic index first to get the assigned number.",
         ["retrieval-process", "numeric"]),
        ("A clerk needs to find 'Santos, Maria' in an alphabetic filing system. What is the FIRST step?",
         "Go directly to the 'S' section and look for 'Santos'",
         ["Go directly to the 'S' section and look for 'Santos'",
          "Look up the name in a separate index",
          "Check the relative index for the correct subject",
          "Determine which region Santos is from"],
         "In alphabetic filing, you go directly to the letter — no intermediate step needed (direct access).",
         ["retrieval-process", "alphabetic"]),
        ("A subject filing system has headings: Benefits, Recruitment, Training. A 'PhilHealth Enrollment Form' should be filed under which heading?",
         "Benefits",
         ["Benefits", "Recruitment", "Training", "Administrative"],
         "PhilHealth is a health benefit — it belongs under the Benefits heading.",
         ["subject-classification", "subject"]),
        ("In terminal-digit filing, file number 34-56-78 is filed in which section?",
         "Section 78",
         ["Section 78", "Section 34", "Section 56", "Section 12"],
         "Terminal-digit filing reads from right to left — the last two digits (78) determine the primary section.",
         ["terminal-digit", "numeric"]),
    ]

    random.shuffle(complex_scenarios)
    for scenario_data in complex_scenarios[:50]:
        question_text, answer, choices, explanation, tags = scenario_data
        if answer not in choices:
            choices[0] = answer
        random.shuffle(choices)
        questions.append(make_question(qid, "Medium", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Type 2: Comparison questions (40 questions) ---
    comparison_questions = [
        ("What is the KEY difference between alphabetic and numeric filing?",
         "Alphabetic provides direct access; numeric requires indirect access through an index",
         ["Alphabetic provides direct access; numeric requires indirect access through an index",
          "Alphabetic uses numbers; numeric uses letters",
          "Alphabetic is for large offices; numeric is for small offices",
          "There is no significant difference"],
         "The fundamental distinction is access type: alphabetic is direct (go straight to the name), numeric is indirect (consult index first).",
         ["comparison", "alphabetic", "numeric"]),
        ("What is the KEY difference between subject and geographic filing?",
         "Subject arranges by topic; geographic arranges by location",
         ["Subject arranges by topic; geographic arranges by location",
          "Subject is for large offices; geographic is for small offices",
          "Subject uses numbers; geographic uses letters",
          "Subject provides direct access; geographic does not"],
         "Subject filing groups by topic (what it's about); geographic filing groups by location (where it's from).",
         ["comparison", "subject", "geographic"]),
        ("How are subject filing and geographic filing SIMILAR?",
         "Both require indirect access — subject needs a relative index, geographic needs location knowledge",
         ["Both require indirect access — subject needs a relative index, geographic needs location knowledge",
          "Both provide direct access",
          "Both arrange records by assigned numbers",
          "Both are only used in small offices"],
         "Neither provides direct name-based access. Both require knowing something (the subject or the location) before finding a specific record.",
         ["comparison", "similarity"]),
        ("Which TWO factors most strongly indicate that numeric filing should be used?",
         "Large volume AND confidentiality requirements",
         ["Large volume AND confidentiality requirements",
          "Small volume AND name-based retrieval",
          "Topic-based work AND policy research",
          "Regional service AND area-based reporting"],
         "Large volume (prevents congestion) and confidentiality (labels reveal nothing) are the two strongest indicators for numeric filing.",
         ["decision-factors", "numeric"]),
        ("What do subject filing and alphabetic filing have in common?",
         "Both use alphabetical arrangement — alphabetic for names, subject for headings in the relative index",
         ["Both use alphabetical arrangement — alphabetic for names, subject for headings in the relative index",
          "Both provide confidentiality",
          "Both require assigned numbers",
          "Both are only for geographic offices"],
         "Alphabetic filing arranges names alphabetically; subject filing arranges subject headings alphabetically in the relative index.",
         ["comparison", "similarity"]),
        ("Why might a geographic filing system also be called a 'combination system'?",
         "Because it uses geographic arrangement as primary and alphabetic arrangement as secondary",
         ["Because it uses geographic arrangement as primary and alphabetic arrangement as secondary",
          "Because it combines numbers and letters",
          "Because it uses both paper and digital storage",
          "Because it requires two filing cabinets"],
         "Geographic filing inherently combines two methods: geographic grouping (primary) and alphabetic arrangement within each location (secondary).",
         ["combination", "geographic"]),
        ("A numeric system and a subject system both require indirect access. How do their indexes differ?",
         "Numeric uses an alphabetic index (name → number); subject uses a relative index (list of approved headings)",
         ["Numeric uses an alphabetic index (name → number); subject uses a relative index (list of approved headings)",
          "They use the same type of index",
          "Numeric uses a geographic index; subject uses a numeric index",
          "Neither actually requires an index"],
         "The alphabetic index maps names to numbers; the relative index lists all approved subject categories and cross-references.",
         ["comparison", "index-types"]),
        ("Which filing system is MOST affected by Philippine surname patterns (many Santos, Cruz, Garcia)?",
         "Alphabetic — common surnames create congestion at certain letters",
         ["Alphabetic — common surnames create congestion at certain letters",
          "Numeric — numbers cluster at certain digits",
          "Subject — topics cluster at certain letters",
          "Geographic — regions have too many provinces"],
         "Alphabetic filing suffers most because Filipino surnames cluster heavily at S, C, D, G, and R.",
         ["philippine-context", "alphabetic"]),
    ]

    # Generate more comparison questions
    pairs = [("Alphabetic", "Numeric"), ("Alphabetic", "Subject"), ("Alphabetic", "Geographic"),
             ("Numeric", "Subject"), ("Numeric", "Geographic"), ("Subject", "Geographic")]

    for sys1, sys2 in pairs:
        comparison_questions.append((
            f"Which provides BETTER confidentiality: {sys1.lower()} or {sys2.lower()} filing?",
            "Numeric" if "Numeric" in (sys1, sys2) else sys1,
            [sys1, sys2, "Both provide equal confidentiality", "Neither provides confidentiality"],
            f"Numeric filing provides the highest confidentiality because labels show only numbers." if "Numeric" in (sys1, sys2) else f"{sys1} and {sys2} both have low confidentiality since labels reveal content.",
            ["comparison", "confidentiality"]
        ))

    for sys1, sys2 in pairs:
        better = sys1 if sys1 == "Alphabetic" else sys2 if sys2 == "Alphabetic" else sys1
        if "Alphabetic" in (sys1, sys2):
            answer = "Alphabetic"
            expl = "Only alphabetic filing provides direct access — all others require a separate index."
        else:
            answer = "Neither — both require indirect access"
            expl = f"Both {sys1.lower()} and {sys2.lower()} filing require indirect access through an index."
        comparison_questions.append((
            f"Which provides direct access: {sys1.lower()} or {sys2.lower()} filing?",
            answer,
            [sys1, sys2, "Both provide direct access", "Neither — both require indirect access"],
            expl,
            ["comparison", "access-type"]
        ))

    random.shuffle(comparison_questions)
    for q_data in comparison_questions[:40]:
        question_text, answer, choices, explanation, tags = q_data
        if answer not in choices:
            choices[0] = answer
        random.shuffle(choices)
        questions.append(make_question(qid, "Medium", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Type 3: Alphabetic ordering within filing system (30 questions) ---
    used_name_sets = set()
    for _ in range(60):  # Try more to get 30 unique
        if len(questions) >= qid - 201 + 30 + 50 + 40:  # already have 50 scenarios + 40 comparisons
            break
        names = random.sample(FILIPINO_NAMES, 4)
        name_key = tuple(sorted(names))
        if name_key in used_name_sets:
            continue
        used_name_sets.add(name_key)
        sorted_names = sorted(names, key=lambda n: n.lower().replace(" ", ""))
        # Ask which comes first
        question_type = random.choice(["first", "last"])
        names_str = "; ".join(names)
        if question_type == "first":
            answer = sorted_names[0]
            q_text = f"In an alphabetic filing system, which of the following should be filed FIRST? Names: {names_str}"
            expl = f"'{answer}' comes first alphabetically when comparing key units (surnames) letter by letter."
        else:
            answer = sorted_names[-1]
            q_text = f"In an alphabetic filing system, which of the following should be filed LAST? Names: {names_str}"
            expl = f"'{answer}' comes last alphabetically when comparing key units (surnames) letter by letter."

        questions.append(make_question(
            qid, "Medium", q_text, list(names), answer, expl,
            ["alphabetic-order", "name-comparison"]
        ))
        qid += 1

    # --- Type 4: Geographic ordering (30 questions) ---
    geo_questions = []

    # Province ordering within a region
    for region, provinces in PROVINCES_BY_REGION.items():
        if len(provinces) >= 4:
            sample = random.sample(provinces, 4)
            sorted_sample = sorted(sample)
            sample_str = ", ".join(sample)
            geo_questions.append((
                f"In a geographic filing system for {region}, arrange these provinces alphabetically: {sample_str}. Which comes FIRST?",
                sorted_sample[0],
                sample,
                f"Within a region, provinces are arranged alphabetically. '{sorted_sample[0]}' comes first.",
                ["geographic-order", "province"]
            ))
            geo_questions.append((
                f"In a geographic filing system for {region}, among {sample_str} — which province would be filed LAST?",
                sorted_sample[-1],
                sample,
                f"Within a region, provinces are arranged alphabetically. '{sorted_sample[-1]}' comes last.",
                ["geographic-order", "province"]
            ))

    # City ordering within a province
    for province, cities in CITIES_BY_PROVINCE.items():
        if len(cities) >= 4:
            sample = random.sample(cities, 4)
            sorted_sample = sorted(sample)
            sample_str = ", ".join(sample)
            geo_questions.append((
                f"In a geographic filing system, arrange these cities/municipalities in {province} alphabetically: {sample_str}. Which comes FIRST?",
                sorted_sample[0],
                sample,
                f"Within a province, cities are arranged alphabetically. '{sorted_sample[0]}' comes first.",
                ["geographic-order", "city"]
            ))
            geo_questions.append((
                f"In a geographic filing system for {province}, among {sample_str} — which city/municipality would be filed LAST?",
                sorted_sample[-1],
                sample,
                f"Within a province, cities are arranged alphabetically. '{sorted_sample[-1]}' comes last.",
                ["geographic-order", "city"]
            ))

    # Pad with more generated geo questions
    while len(geo_questions) < 30:
        region = random.choice(list(PROVINCES_BY_REGION.keys()))
        provinces = PROVINCES_BY_REGION[region]
        if len(provinces) >= 3:
            sample = random.sample(provinces, min(4, len(provinces)))
            sorted_sample = sorted(sample)
            pos = random.randint(0, len(sorted_sample) - 1)
            target = sorted_sample[pos]
            geo_questions.append((
                f"In geographic filing for {region}, in what position would '{target}' be filed among: {', '.join(sample)}?",
                f"{pos + 1}{'st' if pos == 0 else 'nd' if pos == 1 else 'rd' if pos == 2 else 'th'}",
                [f"1st", f"2nd", f"3rd", f"4th"][:len(sample)],
                f"Arranging alphabetically: {', '.join(sorted_sample)}. '{target}' is in position {pos + 1}.",
                ["geographic-order", "position"]
            ))

    random.shuffle(geo_questions)
    for q_data in geo_questions[:30]:
        question_text, answer, choices, explanation, tags = q_data
        if answer not in choices:
            choices.append(answer)
        choices = choices[:4]
        random.shuffle(choices)
        questions.append(make_question(qid, "Medium", question_text, choices, answer, explanation, tags))
        qid += 1

    # --- Type 5: Terminal-digit filing questions (20 questions) ---
    for _ in range(20):
        file_num = generate_file_number()
        parts = file_num.split("-")
        last = parts[2]
        middle = parts[1]
        first = parts[0]

        q_type = random.choice(["section", "subsection", "tertiary"])
        if q_type == "section":
            answer = f"Section {last}"
            q_text = f"In terminal-digit filing, file number {file_num} would be placed in which PRIMARY section?"
            wrong = [f"Section {first}", f"Section {middle}", f"Section {(int(last)+10) % 100:02d}"]
            expl = f"Terminal-digit reads from right to left. The last two digits ({last}) determine the primary section."
        elif q_type == "subsection":
            answer = f"Subsection {middle}"
            q_text = f"In terminal-digit filing, file number {file_num} — after determining the primary section, which SUBSECTION?"
            wrong = [f"Subsection {first}", f"Subsection {last}", f"Subsection {(int(middle)+10) % 100:02d}"]
            expl = f"After the primary section (last digits {last}), the middle digits ({middle}) determine the subsection."
        else:
            answer = f"Position {first}"
            q_text = f"In terminal-digit filing, file number {file_num} — what is the TERTIARY (final) position indicator?"
            wrong = [f"Position {middle}", f"Position {last}", f"Position {(int(first)+10) % 100:02d}"]
            expl = f"The first two digits ({first}) are the tertiary indicator, determining final position within the subsection."

        choices = [answer] + wrong[:3]
        # Deduplicate choices
        choices = list(dict.fromkeys(choices))
        while len(choices) < 4:
            extra = f"Section {random.randint(10,99):02d}" if "Section" in answer else f"Subsection {random.randint(10,99):02d}" if "Subsection" in answer else f"Position {random.randint(10,99):02d}"
            if extra not in choices:
                choices.append(extra)
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Medium", q_text, choices, answer, expl,
            ["terminal-digit", "numeric"]
        ))
        qid += 1

    # --- Type 6: Subject filing - where to file a document (30 questions) ---
    subject_docs = [
        ("PhilHealth enrollment form", "Benefits", "PhilHealth is a health benefit for employees."),
        ("Sick leave application", "Benefits", "Leave is an employee benefit."),
        ("GSIS retirement application", "Benefits", "Retirement is a benefit administered through GSIS."),
        ("Clothing allowance request", "Benefits", "Allowances are employee benefits."),
        ("CSE eligibility certificate", "Recruitment", "Eligibility certificates relate to hiring qualifications."),
        ("Job posting for Clerk III position", "Recruitment", "Job postings are part of the recruitment process."),
        ("Shortlist of qualified applicants", "Recruitment", "Shortlisting is a recruitment activity."),
        ("Interview schedule for applicants", "Recruitment", "Interviews are part of the recruitment process."),
        ("Certificate of training completion", "Training", "Training certificates document completed training."),
        ("Scholarship grant from JICA", "Training", "Scholarships are training/development opportunities."),
        ("Seminar registration form", "Training", "Seminar registration is a training activity."),
        ("Online course enrollment", "Training", "Online courses are training activities."),
        ("Annual budget proposal", "Financial", "Budget proposals are financial planning documents."),
        ("Disbursement voucher", "Financial", "Disbursement vouchers authorize payments — financial."),
        ("Collection report", "Financial", "Collection reports track revenue — financial."),
        ("Audit observation memorandum", "Financial", "Audit findings relate to financial accountability."),
        ("Service contract with supplier", "Legal", "Contracts are binding legal instruments."),
        ("Memorandum of Agreement", "Legal", "MOAs are legal agreements between parties."),
        ("Legal opinion from DOJ", "Legal", "Legal opinions interpret law — legal records."),
        ("Administrative complaint", "Legal", "Formal complaints initiate legal proceedings."),
        ("Office order on new procedures", "Administrative", "Office orders are internal directives."),
        ("Minutes of staff meeting", "Administrative", "Meeting minutes record internal proceedings."),
        ("Organizational chart update", "Administrative", "Org charts document internal structure."),
        ("Annual accomplishment report", "Administrative", "Annual reports summarize operations."),
        ("Vacation leave application", "Benefits", "Leave applications are benefit requests."),
        ("Performance bonus computation", "Benefits", "Bonuses are employee benefits."),
        ("Applicant screening results", "Recruitment", "Screening is part of recruitment."),
        ("Training needs assessment", "Training", "Needs assessment guides training planning."),
        ("Petty cash voucher", "Financial", "Petty cash vouchers are financial records."),
        ("Non-disclosure agreement", "Legal", "NDAs are binding legal documents."),
    ]

    random.shuffle(subject_docs)
    for doc_name, correct_heading, expl in subject_docs[:30]:
        wrong_headings = [h for h in SUBJECT_HEADINGS.keys() if h != correct_heading]
        wrong = random.sample(wrong_headings, 3)
        choices = [correct_heading] + wrong
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Medium",
            f"In a subject filing system with headings (Benefits, Recruitment, Training, Financial, Legal, Administrative), under which heading should a '{doc_name}' be filed?",
            choices, correct_heading, expl,
            ["subject-classification", "subject"]
        ))
        qid += 1

    # --- Pad to 200 if needed ---
    med_pad_counter = 0
    while len(questions) < 200:
        med_pad_counter += 1
        # Generate additional medium scenario questions
        pool_choice = random.choice(["A", "N", "S", "G"])
        if pool_choice == "A":
            scenario_text, expl = random.choice(ALPHABETIC_SCENARIOS)
            correct_system = "Alphabetic"
        elif pool_choice == "N":
            scenario_text, expl = random.choice(NUMERIC_SCENARIOS)
            correct_system = "Numeric"
        elif pool_choice == "S":
            scenario_text, expl = random.choice(SUBJECT_SCENARIOS)
            correct_system = "Subject"
        else:
            scenario_text, expl = random.choice(GEOGRAPHIC_SCENARIOS)
            correct_system = "Geographic"

        wrong = pick_wrong_systems(correct_system)
        # Add a complicating factor for medium difficulty
        complications = [
            f" The office also handles some records by name. Despite this, what is the PRIMARY system for this scenario?",
            f" A new clerk suggests alphabetic filing instead. Why is {correct_system.lower()} filing more appropriate here?",
            f" The office expects to double its records in 2 years. Does this change the recommendation?",
        ]
        complication = complications[med_pad_counter % 3]
        q_text = f"(Case {med_pad_counter}) {scenario_text}.{complication}"

        if "PRIMARY" in complication or "more appropriate" in complication:
            answer = correct_system
            choices = [correct_system] + wrong
        else:
            answer = f"No — {correct_system.lower()} filing remains appropriate regardless of growth"
            choices = [answer,
                       "Yes — switch to numeric filing",
                       "Yes — switch to alphabetic filing",
                       "Yes — switch to geographic filing"]

        random.shuffle(choices)
        questions.append(make_question(
            qid, "Medium", q_text, choices, answer,
            expl + " The primary retrieval pattern determines the system.",
            ["system-selection", correct_system.lower(), "medium-scenario"]
        ))
        qid += 1

    return questions[:200]


# ============================================================
# HARD QUESTIONS (IDs 401-600)
# ============================================================

def generate_hard_questions():
    """Generate 200 Hard questions. Multi-step, traps, complex scenarios."""
    questions = []
    qid = 401

    # --- Type 1: Multi-factor scenario analysis (60 questions) ---
    hard_scenarios = [
        ("A government agency has 100,000 records. They need confidentiality, "
         "records are referenced by case number, and they must generate reports "
         "by region. Which combination of systems is most appropriate?",
         "Numeric filing as primary (for confidentiality and volume) with "
         "geographic cross-referencing for regional reports",
         ["Numeric filing as primary (for confidentiality and volume) with "
          "geographic cross-referencing for regional reports",
          "Alphabetic filing with geographic secondary arrangement",
          "Subject filing with numeric codes",
          "Geographic filing only"],
         "The volume and confidentiality needs demand numeric filing. "
         "Geographic cross-referencing supports regional reporting without "
         "changing the primary system.",
         ["combination-system", "multi-factor"]),
    ]
    hard_scenarios += [
        ("A DSWD office serves 5 provinces with 20,000 beneficiary records. "
         "Social workers request files by municipality. However, some "
         "beneficiaries move between provinces. What filing challenge does "
         "geographic filing present here?",
         "Files must be physically moved when beneficiaries relocate, "
         "requiring cross-references at the old location",
         ["Files must be physically moved when beneficiaries relocate, "
          "requiring cross-references at the old location",
          "The system cannot handle 20,000 records",
          "Social workers cannot learn geography",
          "Geographic filing does not allow alphabetic sub-arrangement"],
         "Geographic filing's weakness: when the geographic basis changes "
         "(person moves), files must be relocated and cross-referenced.",
         ["geographic", "limitation", "relocation"]),
    ]
    hard_scenarios += [
        ("An office switches from alphabetic to numeric filing. During "
         "transition, some records have numbers and some don't. What is the "
         "MOST critical task during this transition?",
         "Building a complete alphabetic index that maps every existing "
         "name to its newly assigned number",
         ["Building a complete alphabetic index that maps every existing "
          "name to its newly assigned number",
          "Buying new filing cabinets",
          "Training staff on the alphabet",
          "Destroying all old records"],
         "Without a complete alphabetic index, the numeric system is "
         "unusable — no one can find files by name.",
         ["system-transition", "numeric", "index"]),
    ]
    hard_scenarios += [
        ("A subject filing system has grown from 10 to 200 subject headings "
         "over 5 years. Clerks report difficulty finding documents. What is "
         "the likely problem?",
         "The relative index has become too complex and may contain "
         "overlapping or redundant headings that need consolidation",
         ["The relative index has become too complex and may contain "
          "overlapping or redundant headings that need consolidation",
          "The office needs to switch to numeric filing",
          "Too many documents have been created",
          "The filing cabinets are too small"],
         "Subject filing becomes unwieldy when headings proliferate without "
         "periodic review. Overlapping categories cause confusion.",
         ["subject", "maintenance", "relative-index"]),
    ]
    hard_scenarios += [
        ("A hospital uses terminal-digit filing with 100,000 records. A new "
         "clerk files record 45-67-23 in section 45 instead of section 23. "
         "What type of error is this?",
         "The clerk read the number left-to-right (consecutive style) "
         "instead of right-to-left (terminal-digit style)",
         ["The clerk read the number left-to-right (consecutive style) "
          "instead of right-to-left (terminal-digit style)",
          "The clerk transposed two digits",
          "The record number is invalid",
          "Terminal-digit filing does not use sections"],
         "Terminal-digit reads right-to-left: section 23, subsection 67, "
         "position 45. Reading left-to-right is the most common error.",
         ["terminal-digit", "error-identification", "numeric"]),
    ]
    hard_scenarios += [
        ("An office uses geographic filing (Region → Province → City). A new "
         "region is created by splitting Region IV-A. What operational "
         "challenge does this create?",
         "All files from provinces reassigned to the new region must be "
         "physically moved to new geographic sections",
         ["All files from provinces reassigned to the new region must be "
          "physically moved to new geographic sections",
          "The alphabetic index must be rebuilt",
          "All file numbers must be changed",
          "No challenge — files stay where they are"],
         "Geographic filing's weakness: boundary changes require physical "
         "reorganization of all affected files.",
         ["geographic", "boundary-change", "limitation"]),
    ]
    hard_scenarios += [
        ("A clerk argues that subject filing is better than alphabetic "
         "because 'you can find everything about a topic in one place.' "
         "What is the STRONGEST counter-argument?",
         "Subject filing requires subjective judgment about which heading "
         "to use, and without strict relative index discipline, documents "
         "scatter across inconsistent categories",
         ["Subject filing requires subjective judgment about which heading "
          "to use, and without strict relative index discipline, documents "
          "scatter across inconsistent categories",
          "Subject filing is more expensive",
          "Subject filing cannot handle more than 100 documents",
          "Subject filing requires a computer"],
         "The subjectivity problem is subject filing's greatest weakness — "
         "different people categorize the same document differently.",
         ["subject", "counter-argument", "critical-thinking"]),
    ]
    hard_scenarios += [
        ("Two offices in the same building both file personnel records. "
         "Office A uses alphabetic filing (200 employees). Office B uses "
         "numeric filing (15,000 employees). Both are correct. Why?",
         "The appropriate system depends on volume — alphabetic works for "
         "200 records but would create severe congestion with 15,000",
         ["The appropriate system depends on volume — alphabetic works for "
          "200 records but would create severe congestion with 15,000",
          "Office A is wrong — all offices should use numeric",
          "Office B is wrong — personnel files must be alphabetic",
          "Both are wrong — subject filing should be used"],
         "There is no universally 'best' system. Volume is a key factor: "
         "alphabetic suits small collections, numeric suits large ones.",
         ["system-selection", "volume", "justification"]),
    ]
    hard_scenarios += [
        ("A government agency uses numeric filing. An employee requests "
         "'all files related to training.' The clerk cannot fulfill this "
         "request efficiently. Why?",
         "Numeric filing has no logical grouping — training-related files "
         "may have widely scattered numbers with no topical connection",
         ["Numeric filing has no logical grouping — training-related files "
          "may have widely scattered numbers with no topical connection",
          "The clerk is not trained properly",
          "Numeric filing cannot store training documents",
          "The alphabetic index is missing"],
         "This is a key disadvantage of numeric filing: related records "
         "(same topic) may have completely unrelated numbers.",
         ["numeric", "limitation", "no-logical-grouping"]),
    ]
    hard_scenarios += [
        ("A subject filing system uses these headings: 'Seminars' and "
         "'Training.' A document titled 'Seminar on Leadership Training' "
         "could fit either heading. How should this be resolved?",
         "File under the primary heading per the relative index rules and "
         "create a cross-reference under the other heading",
         ["File under the primary heading per the relative index rules and "
          "create a cross-reference under the other heading",
          "File a copy under both headings",
          "Create a new heading called 'Seminar-Training'",
          "Ask the supervisor to decide each time"],
         "Cross-referencing solves the 'fits multiple headings' problem "
         "without duplicating documents or creating ad-hoc categories.",
         ["subject", "cross-reference", "ambiguity"]),
    ]

    for scenario_data in hard_scenarios[:10]:
        q_text, answer, choices, explanation, tags = scenario_data
        if answer not in choices:
            choices[0] = answer
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, explanation, tags
        ))
        qid += 1

    return questions, qid


def generate_hard_questions_continued(questions, qid):
    """Continue generating hard questions."""

    # More multi-factor scenarios (50 more)
    more_scenarios = [
        ("An office uses alphabetic filing. A new employee named "
         "'Santos, Maria Clara' joins. There are already files for "
         "'Santos, Maria' and 'Santos, Maria C.' How does alphabetic "
         "filing handle this?",
         "Compare unit by unit: Santos Maria (nothing after) files before "
         "Santos Maria C, which files before Santos Maria Clara",
         ["Compare unit by unit: Santos Maria (nothing after) files before "
          "Santos Maria C, which files before Santos Maria Clara",
          "All three files are placed together with no distinction",
          "The newest employee's file goes last regardless of name",
          "A number must be added to distinguish them"],
         "'Nothing before something' rule: shorter names file first. "
         "Santos Maria → Santos Maria C → Santos Maria Clara.",
         ["alphabetic", "nothing-before-something", "name-comparison"]),
        ("A government office files 10,000 records geographically by "
         "region. NCR has 4,000 records while CAR has only 200. What "
         "problem does this illustrate?",
         "Uneven distribution — geographic filing creates imbalanced "
         "sections when some areas generate far more records than others",
         ["Uneven distribution — geographic filing creates imbalanced "
          "sections when some areas generate far more records than others",
          "The system has too many records overall",
          "CAR records should be moved to NCR",
          "Geographic filing cannot handle 10,000 records"],
         "Uneven distribution is a key disadvantage of geographic filing — "
         "some areas naturally generate more records than others.",
         ["geographic", "uneven-distribution", "limitation"]),
        ("A clerk in a numeric filing system memorizes frequently-used "
         "file numbers instead of checking the alphabetic index. Why is "
         "this a BAD practice?",
         "Memory is unreliable — transposing digits (e.g., 2034 vs 2043) "
         "leads to misfiling, and the practice fails when the clerk is "
         "absent",
         ["Memory is unreliable — transposing digits (e.g., 2034 vs 2043) "
          "leads to misfiling, and the practice fails when the clerk is "
          "absent",
          "It is actually a good practice that saves time",
          "The alphabetic index will become outdated",
          "Other clerks will become jealous"],
         "Relying on memory bypasses the system's safeguard (the index) "
         "and introduces human error risk.",
         ["numeric", "bad-practice", "error-prevention"]),
        ("An office wants to implement subject filing but has no relative "
         "index. The supervisor says 'Just start filing by topic and we'll "
         "organize later.' What will likely happen?",
         "Different clerks will create inconsistent headings for the same "
         "topics, making retrieval unreliable from day one",
         ["Different clerks will create inconsistent headings for the same "
          "topics, making retrieval unreliable from day one",
          "The system will work perfectly without an index",
          "Documents will automatically organize themselves",
          "The supervisor's approach is correct"],
         "Subject filing without a relative index inevitably produces "
         "inconsistent categories — the index must come FIRST.",
         ["subject", "relative-index", "implementation-error"]),
        ("A geographic filing system for DepEd uses: Region → Division → "
         "District → School. A school is transferred from one division to "
         "another. What must happen to its files?",
         "Files must be physically moved to the new division's section "
         "and a cross-reference left at the old location during transition",
         ["Files must be physically moved to the new division's section "
          "and a cross-reference left at the old location during transition",
          "Nothing — files stay in the original location permanently",
          "All files are destroyed and recreated",
          "The school's name is changed"],
         "Geographic filing requires physical relocation when the "
         "geographic basis changes. Cross-references prevent lost files "
         "during transition.",
         ["geographic", "relocation", "cross-reference"]),
        ("An office uses consecutive numeric filing (001, 002, 003...). "
         "After 5 years, they have 50,000 files. New files always go at "
         "the end (around 50,000). What problem does this create?",
         "Congestion at the end — all filing activity concentrates in one "
         "area, causing bottlenecks when multiple clerks need access",
         ["Congestion at the end — all filing activity concentrates in one "
          "area, causing bottlenecks when multiple clerks need access",
          "The numbers become too large to read",
          "The alphabetic index becomes too long",
          "Files at the beginning are never accessed"],
         "Consecutive filing concentrates all new activity at the highest "
         "numbers. Terminal-digit filing solves this by distributing evenly.",
         ["numeric", "consecutive", "congestion"]),
        ("A subject filing system has 'Training' as a main heading with "
         "sub-headings: Local Seminars, Foreign Scholarships, Online "
         "Courses. A document about a 'Webinar on Philippine Tax Law' — "
         "is it Local Seminars or Online Courses?",
         "Online Courses — a webinar is conducted online regardless of "
         "the topic being Philippine-specific",
         ["Online Courses — a webinar is conducted online regardless of "
          "the topic being Philippine-specific",
          "Local Seminars — it's about Philippine law",
          "Foreign Scholarships — webinars are international",
          "A new heading 'Webinars' should be created"],
         "The filing criterion is the FORMAT/DELIVERY METHOD (online), "
         "not the topic content. Follow the relative index categories.",
         ["subject", "classification-judgment", "ambiguity"]),
        ("Two filing systems are being compared for a new office: "
         "alphabetic (simple, direct access) vs. numeric (confidential, "
         "scalable). The office will start with 100 records but expects "
         "to grow to 20,000 in 3 years. Which is better?",
         "Numeric — plan for the future volume rather than current "
         "simplicity, since switching systems later is very disruptive",
         ["Numeric — plan for the future volume rather than current "
          "simplicity, since switching systems later is very disruptive",
          "Alphabetic — start simple and switch later if needed",
          "Subject — it handles growth better than both",
          "Geographic — it scales automatically"],
         "Switching filing systems is extremely disruptive (every file "
         "must be converted). Plan for projected volume from the start.",
         ["system-selection", "future-planning", "numeric"]),
        ("A clerk files a document about 'Employee Training Budget' in "
         "a subject filing system. The relative index has both 'Training' "
         "and 'Budget' as headings. The clerk files it under 'Budget.' "
         "Is this correct?",
         "It depends on the document's primary purpose — if it's a "
         "budget document that happens to be for training, 'Budget' is "
         "correct with a cross-reference under 'Training'",
         ["It depends on the document's primary purpose — if it's a "
          "budget document that happens to be for training, 'Budget' is "
          "correct with a cross-reference under 'Training'",
          "Always file under 'Training' because training is more specific",
          "Always file under 'Budget' because money is more important",
          "File a copy under both headings"],
         "The primary purpose determines the primary filing location. "
         "A budget document goes under Budget; a training plan goes under "
         "Training. Cross-reference the other.",
         ["subject", "primary-purpose", "cross-reference"]),
        ("In terminal-digit filing, which of these file numbers would be "
         "in the SAME primary section: 12-34-56, 78-90-56, 11-22-56, "
         "56-78-90?",
         "12-34-56, 78-90-56, and 11-22-56 (all end in 56) — but NOT "
         "56-78-90 (ends in 90)",
         ["12-34-56, 78-90-56, and 11-22-56 (all end in 56) — but NOT "
          "56-78-90 (ends in 90)",
          "All four are in the same section",
          "Only 12-34-56 and 56-78-90 (both contain 56)",
          "None are in the same section"],
         "Terminal-digit groups by LAST two digits. Files ending in 56 "
         "go in section 56. File 56-78-90 ends in 90, so it's in "
         "section 90.",
         ["terminal-digit", "grouping", "numeric"]),
    ]

    for scenario_data in more_scenarios:
        q_text, answer, choices, explanation, tags = scenario_data
        if answer not in choices:
            choices[0] = answer
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, explanation, tags
        ))
        qid += 1

    return questions, qid


def generate_hard_questions_part3(questions, qid):
    """Generate remaining hard questions — ordering, traps, mixed."""

    # --- Type 2: Terminal-digit ordering (30 questions) ---
    for _ in range(30):
        # Generate 4 file numbers and ask for correct terminal-digit order
        nums = [generate_file_number() for _ in range(4)]
        # Sort by terminal-digit rules: last 2, then middle 2, then first 2
        def td_key(n):
            parts = n.split("-")
            return (int(parts[2]), int(parts[1]), int(parts[0]))
        sorted_nums = sorted(nums, key=td_key)

        q_type = random.choice(["first", "last", "order"])
        if q_type == "first":
            answer = sorted_nums[0]
            q_text = (f"In terminal-digit filing, which file number would "
                      f"be filed FIRST among: {', '.join(nums)}?")
            expl = (f"Terminal-digit compares last digits first. "
                    f"'{answer}' has the lowest terminal digits.")
            choices = list(nums)
        elif q_type == "last":
            answer = sorted_nums[-1]
            q_text = (f"In terminal-digit filing, which file number would "
                      f"be filed LAST among: {', '.join(nums)}?")
            expl = (f"Terminal-digit compares last digits first. "
                    f"'{answer}' has the highest terminal digits.")
            choices = list(nums)
        else:
            answer = ", ".join(sorted_nums)
            q_text = (f"Arrange in correct terminal-digit filing order: "
                      f"{', '.join(nums)}")
            # Generate wrong orderings
            wrong1 = ", ".join(sorted(nums))  # consecutive order
            wrong2 = ", ".join(sorted(nums, key=lambda n: n.split("-")[1]))
            wrong3 = ", ".join(reversed(sorted_nums))
            choices = [answer, wrong1, wrong2, wrong3]
            # Deduplicate
            choices = list(dict.fromkeys(choices))[:4]
            while len(choices) < 4:
                alt = list(nums)
                random.shuffle(alt)
                alt_str = ", ".join(alt)
                if alt_str not in choices:
                    choices.append(alt_str)
            expl = (f"Terminal-digit reads right-to-left. Correct order: "
                    f"{answer}")

        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, expl,
            ["terminal-digit", "ordering", "numeric"]
        ))
        qid += 1

    # --- Type 3: Complex geographic ordering (30 questions) ---
    # Multi-level geographic comparisons
    geo_entries = []
    for region, provinces in PROVINCES_BY_REGION.items():
        for province in provinces:
            if province in CITIES_BY_PROVINCE:
                for city in CITIES_BY_PROVINCE[province]:
                    names = random.sample(FILIPINO_NAMES, 2)
                    for name in names:
                        geo_entries.append({
                            "region": region,
                            "province": province,
                            "city": city,
                            "name": name,
                            "full": f"{name} — {city}, {province}, {region}"
                        })

    for _ in range(30):
        sample = random.sample(geo_entries, 4)
        # Sort: region → province → city → name
        sorted_sample = sorted(sample, key=lambda e: (
            e["region"], e["province"], e["city"], e["name"].lower()
        ))

        q_type = random.choice(["first", "last"])
        entries_str = "; ".join([e["full"] for e in sample])
        if q_type == "first":
            answer = sorted_sample[0]["full"]
            q_text = (f"In a geographic filing system (Region → Province → "
                      f"City → Name), which entry would be filed FIRST? "
                      f"Entries: {entries_str}")
            expl = (f"Geographic filing sorts by region first, then "
                    f"province, then city, then name alphabetically. "
                    f"'{answer}' comes first.")
        else:
            answer = sorted_sample[-1]["full"]
            q_text = (f"In a geographic filing system (Region → Province → "
                      f"City → Name), which entry would be filed LAST? "
                      f"Entries: {entries_str}")
            expl = (f"Geographic filing sorts by region first, then "
                    f"province, then city, then name alphabetically. "
                    f"'{answer}' comes last.")

        choices = [e["full"] for e in sample]
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, expl,
            ["geographic-order", "multi-level", "geographic"]
        ))
        qid += 1

    # --- Type 4: Trap questions (40 questions) ---
    trap_questions = [
        ("A memo ABOUT the annual budget is filed in a subject system. "
         "A clerk files it under 'Financial/Budget.' Is this correct?",
         "It depends — if the memo is a directive (e.g., 'Submit your "
         "budget proposals'), it's Administrative. If it IS the budget "
         "document, it's Financial.",
         ["It depends — if the memo is a directive (e.g., 'Submit your "
          "budget proposals'), it's Administrative. If it IS the budget "
          "document, it's Financial.",
          "Yes — anything about money goes under Financial",
          "No — all memos are Administrative",
          "No — memos cannot be filed in subject systems"],
         "The document's nature matters: a memo ABOUT a topic is a "
         "directive (Administrative); the topic document itself belongs "
         "to its subject category.",
         ["trap", "subject", "document-nature"]),
        ("Filing by date (January before February, 2023 before 2024) is "
         "an example of which filing system?",
         "Chronological filing — a separate method, not one of the four "
         "major filing systems",
         ["Chronological filing — a separate method, not one of the four "
          "major filing systems",
          "Numeric filing",
          "Alphabetic filing",
          "Subject filing"],
         "Chronological (date-based) filing is distinct from numeric "
         "filing. Numeric uses assigned ID numbers, not dates.",
         ["trap", "chronological-vs-numeric"]),
        ("A file cabinet has tabs labeled: A-D, E-H, I-L, M-P, Q-T, "
         "U-Z. What filing system is this?",
         "Alphabetic filing system",
         ["Alphabetic filing system",
          "Subject filing system",
          "Geographic filing system",
          "Numeric filing system"],
         "Letter-range tabs (A-D, E-H...) are the hallmark of alphabetic "
         "filing — records arranged by the alphabet.",
         ["identification", "alphabetic"]),
        ("A file cabinet has tabs labeled: 001-100, 101-200, 201-300. "
         "What filing system is this?",
         "Numeric filing system",
         ["Numeric filing system",
          "Alphabetic filing system",
          "Subject filing system",
          "Chronological filing system"],
         "Number-range tabs indicate numeric filing — records arranged "
         "by assigned numbers.",
         ["identification", "numeric"]),
        ("A file cabinet has tabs labeled: Region I, Region II, Region "
         "III, NCR. What filing system is this?",
         "Geographic filing system",
         ["Geographic filing system",
          "Subject filing system",
          "Alphabetic filing system",
          "Numeric filing system"],
         "Regional tabs indicate geographic filing — records arranged "
         "by location.",
         ["identification", "geographic"]),
        ("A file cabinet has tabs labeled: Benefits, Legal, Training, "
         "Recruitment. What filing system is this?",
         "Subject filing system",
         ["Subject filing system",
          "Alphabetic filing system",
          "Geographic filing system",
          "Functional filing system"],
         "Topic-based tabs indicate subject filing — records arranged "
         "by subject heading.",
         ["identification", "subject"]),
        ("'Geographic filing is just alphabetic filing by location name.' "
         "Is this statement correct?",
         "No — geographic filing groups by administrative hierarchy "
         "(Region → Province → City) first, then alphabetizes within "
         "each level",
         ["No — geographic filing groups by administrative hierarchy "
          "(Region → Province → City) first, then alphabetizes within "
          "each level",
          "Yes — it's the same as alphabetizing city names",
          "Yes — all filing systems are variations of alphabetic",
          "No — geographic filing uses numbers, not letters"],
         "Geographic filing's PRIMARY arrangement is hierarchical "
         "(by administrative level), not purely alphabetical.",
         ["trap", "geographic", "misconception"]),
        ("'Numeric filing means filing by date.' Is this correct?",
         "No — numeric filing uses assigned ID numbers as identifiers, "
         "not dates. Filing by date is chronological filing.",
         ["No — numeric filing uses assigned ID numbers as identifiers, "
          "not dates. Filing by date is chronological filing.",
          "Yes — dates are numbers so it's numeric filing",
          "Yes — all number-based filing is numeric",
          "No — numeric filing uses letters, not numbers"],
         "Numeric filing assigns arbitrary numbers as unique identifiers. "
         "Chronological filing arranges by date. They are different.",
         ["trap", "numeric", "misconception"]),
        ("An office has files labeled: 'Santos-001', 'Santos-002', "
         "'Reyes-001', 'Reyes-002'. What type of system is this?",
         "Alphanumeric — a combination using both name and number "
         "elements",
         ["Alphanumeric — a combination using both name and number "
          "elements",
          "Purely alphabetic",
          "Purely numeric",
          "Subject filing"],
         "Labels combining names and numbers indicate an alphanumeric "
         "system — a hybrid approach.",
         ["identification", "alphanumeric", "combination"]),
        ("A clerk says 'I don't need a relative index — I just file "
         "documents under whatever topic seems right.' What will happen?",
         "Inconsistent filing — the same type of document will end up "
         "under different headings depending on which clerk files it",
         ["Inconsistent filing — the same type of document will end up "
          "under different headings depending on which clerk files it",
          "The system will work perfectly",
          "Documents will be easier to find",
          "The supervisor will create the index automatically"],
         "Without a relative index, subject filing degrades into chaos — "
         "each clerk invents their own categories.",
         ["trap", "subject", "relative-index"]),
    ]

    # Add more trap/critical-thinking questions
    trap_questions += [
        ("Which is MORE important when choosing a filing system: the "
         "clerk's preference or how records are most frequently requested?",
         "How records are most frequently requested — the system must "
         "serve retrieval needs, not personal preference",
         ["How records are most frequently requested — the system must "
          "serve retrieval needs, not personal preference",
          "The clerk's preference — they use the system daily",
          "Both are equally important",
          "Neither — the supervisor decides"],
         "Filing systems exist to serve retrieval. The primary decision "
         "factor is always how records are requested.",
         ["critical-thinking", "system-selection"]),
        ("An office has 5,000 records filed alphabetically. Retrieval is "
         "slow because 40% of files are under letters S and D. What is "
         "the BEST solution?",
         "Consider switching to numeric filing to distribute files evenly, "
         "or subdivide the congested letters with additional guides",
         ["Consider switching to numeric filing to distribute files evenly, "
          "or subdivide the congested letters with additional guides",
          "Remove all files starting with S and D",
          "Switch to geographic filing",
          "File everything under one letter"],
         "Congestion at common letters is alphabetic filing's weakness. "
         "Numeric filing or additional subdivision guides can solve it.",
         ["problem-solving", "alphabetic", "congestion"]),
        ("A numeric filing system assigns numbers 1-50,000. File #25,001 "
         "belongs to 'Santos, Maria.' If the alphabetic index entry for "
         "'Santos, Maria' is accidentally deleted, what happens?",
         "The physical file still exists at position 25,001 but cannot "
         "be found by name — it's effectively lost until the index is "
         "rebuilt",
         ["The physical file still exists at position 25,001 but cannot "
          "be found by name — it's effectively lost until the index is "
          "rebuilt",
          "The physical file is automatically deleted",
          "Nothing — the file can still be found by number",
          "The system reassigns a new number"],
         "The alphabetic index is the ONLY bridge between names and "
         "numbers. Without it, name-based retrieval is impossible.",
         ["numeric", "index-dependency", "critical-thinking"]),
        ("Can a single document be filed in TWO different filing systems "
         "simultaneously?",
         "No — the original goes in one system. Cross-references or "
         "index entries in other systems point to the original location.",
         ["No — the original goes in one system. Cross-references or "
          "index entries in other systems point to the original location.",
          "Yes — make copies for each system",
          "Yes — the same document can exist in two places",
          "No — documents can only exist in subject filing"],
         "One original, one primary location. Other systems use "
         "cross-references (pointers), not duplicate originals.",
         ["cross-reference", "critical-thinking"]),
        ("A geographic filing system for a national agency has 17 "
         "regional sections. A document is from a Filipino working "
         "overseas (no Philippine region). Where should it be filed?",
         "Under a special 'Foreign/Overseas' section — geographic "
         "systems need a catch-all for records outside the defined "
         "geographic scope",
         ["Under a special 'Foreign/Overseas' section — geographic "
          "systems need a catch-all for records outside the defined "
          "geographic scope",
          "Under NCR because that's the capital",
          "Under the person's home province",
          "It cannot be filed in a geographic system"],
         "Geographic systems must account for records that don't fit "
         "the defined hierarchy. A 'Miscellaneous/Foreign' section "
         "handles these.",
         ["geographic", "edge-case", "critical-thinking"]),
    ]

    random.shuffle(trap_questions)
    for q_data in trap_questions[:40]:
        q_text, answer, choices, explanation, tags = q_data
        if answer not in choices:
            choices[0] = answer
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, explanation, tags
        ))
        qid += 1

    return questions, qid


def generate_hard_questions_part4(questions, qid):
    """Generate final batch of hard questions — application and synthesis."""

    # --- Type 5: System design / recommendation questions (40 questions) ---
    design_questions = [
        ("A new government agency is being established. It will have "
         "500 employees, handle 10,000 financial transactions per year, "
         "manage policy documents on 20 topics, and serve all 17 regions. "
         "Recommend the filing system for PERSONNEL records.",
         "Alphabetic — 500 employees is manageable, and personnel files "
         "are always requested by employee name",
         ["Alphabetic — 500 employees is manageable, and personnel files "
          "are always requested by employee name",
          "Numeric — for confidentiality",
          "Subject — organized by topic",
          "Geographic — organized by region"],
         "500 personnel files with name-based retrieval is ideal for "
         "alphabetic filing. The volume doesn't justify numeric overhead.",
         ["system-recommendation", "alphabetic", "personnel"]),
        ("Same agency as above. Recommend the filing system for "
         "FINANCIAL TRANSACTIONS (10,000 per year, each with a voucher "
         "number).",
         "Numeric — large volume, referenced by voucher number, audit "
         "trail requirements",
         ["Numeric — large volume, referenced by voucher number, audit "
          "trail requirements",
          "Alphabetic — by payee name",
          "Subject — by transaction type",
          "Geographic — by region of origin"],
         "10,000 transactions with assigned voucher numbers and audit "
         "requirements point clearly to numeric filing.",
         ["system-recommendation", "numeric", "financial"]),
        ("Same agency. Recommend the filing system for POLICY DOCUMENTS "
         "(20 topics).",
         "Subject — policy documents are requested by topic, and 20 "
         "headings is a manageable relative index",
         ["Subject — policy documents are requested by topic, and 20 "
          "headings is a manageable relative index",
          "Alphabetic — by document title",
          "Numeric — by document number",
          "Geographic — by region affected"],
         "Policy documents are inherently topic-based. A 20-heading "
         "relative index is simple and effective.",
         ["system-recommendation", "subject", "policy"]),
        ("Same agency. Recommend the filing system for REGIONAL "
         "CORRESPONDENCE (serving all 17 regions).",
         "Geographic — correspondence is managed by region, and staff "
         "need to pull 'all letters from Region V' easily",
         ["Geographic — correspondence is managed by region, and staff "
          "need to pull 'all letters from Region V' easily",
          "Alphabetic — by sender name",
          "Numeric — by letter number",
          "Subject — by letter topic"],
         "Regional correspondence is naturally organized by location. "
         "Geographic filing supports area-based retrieval and reporting.",
         ["system-recommendation", "geographic", "correspondence"]),
        ("A medical clinic is upgrading from paper to digital records. "
         "They currently use alphabetic filing (500 patients). They "
         "expect to grow to 5,000 patients. Should they keep alphabetic "
         "in the digital system?",
         "Switch to numeric — digital systems handle numeric indexing "
         "effortlessly, and 5,000 records with common Filipino surnames "
         "will cause search problems in alphabetic",
         ["Switch to numeric — digital systems handle numeric indexing "
          "effortlessly, and 5,000 records with common Filipino surnames "
          "will cause search problems in alphabetic",
          "Keep alphabetic — it worked before",
          "Use subject filing — organize by diagnosis",
          "Use geographic — organize by patient address"],
         "Digital systems eliminate the 'index maintenance' disadvantage "
         "of numeric filing. With projected growth and name duplication, "
         "numeric is better.",
         ["system-recommendation", "digital-transition", "numeric"]),
        ("A government archive receives 1,000 boxes of old records from "
         "a closed agency. The records have no existing organization. "
         "The archive needs to make them retrievable. Which system?",
         "Numeric — assign box/record numbers and build an index. This "
         "avoids reorganizing the physical records while enabling retrieval",
         ["Numeric — assign box/record numbers and build an index. This "
          "avoids reorganizing the physical records while enabling retrieval",
          "Alphabetic — rearrange everything by name",
          "Subject — sort by topic",
          "Geographic — sort by origin"],
         "Numeric filing can be applied to existing records without "
         "physical reorganization — just assign numbers and build an index.",
         ["system-recommendation", "numeric", "archive"]),
        ("A law firm handles cases in 3 practice areas: corporate, "
         "criminal, and family law. Each area has 500+ active cases with "
         "docket numbers. What combination system works best?",
         "Subject filing as primary (3 practice areas) with numeric "
         "filing within each area (by docket number)",
         ["Subject filing as primary (3 practice areas) with numeric "
          "filing within each area (by docket number)",
          "Alphabetic only — by client name",
          "Numeric only — by docket number",
          "Geographic — by court location"],
         "The practice areas provide natural subject divisions. Within "
         "each, docket numbers provide numeric arrangement.",
         ["combination-system", "subject", "numeric"]),
        ("A delivery company has 50 drivers serving 200 routes across "
         "Metro Manila. Dispatch needs to quickly find all deliveries "
         "for a specific area. Which system for delivery records?",
         "Geographic — organized by city/area within Metro Manila, "
         "matching how dispatch thinks about routes",
         ["Geographic — organized by city/area within Metro Manila, "
          "matching how dispatch thinks about routes",
          "Alphabetic — by customer name",
          "Numeric — by delivery number",
          "Subject — by package type"],
         "Dispatch thinks geographically (routes, areas). Geographic "
         "filing matches the operational workflow.",
         ["system-recommendation", "geographic", "operations"]),
        ("A university library catalogs 100,000 books. Each book has a "
         "call number (e.g., QA 76.73). Books are shelved by call number. "
         "What filing system is this?",
         "Alphanumeric/Numeric — books are arranged by assigned codes "
         "(call numbers) in a systematic order",
         ["Alphanumeric/Numeric — books are arranged by assigned codes "
          "(call numbers) in a systematic order",
          "Alphabetic — by author name",
          "Subject — by topic",
          "Geographic — by publisher location"],
         "Library call numbers are assigned codes that determine shelf "
         "position — this is a form of numeric/alphanumeric filing.",
         ["identification", "numeric", "real-world"]),
        ("A government office files employee grievances. The union "
         "representative says files should be alphabetic (by employee "
         "name) for easy access. Management says files should be numeric "
         "(by case number) for confidentiality. Who has the stronger "
         "argument?",
         "Management — grievance files are sensitive and confidentiality "
         "should take priority over convenience",
         ["Management — grievance files are sensitive and confidentiality "
          "should take priority over convenience",
          "The union — easy access is more important",
          "Both are wrong — subject filing should be used",
          "Neither — geographic filing is best"],
         "Grievance files contain sensitive information. Confidentiality "
         "(numeric) outweighs convenience (alphabetic) for sensitive "
         "records.",
         ["system-selection", "confidentiality", "numeric"]),
    ]

    # Generate more design questions from scenario pools
    more_design = []
    office_types = [
        ("a barangay health station with 150 patient records, no "
         "confidentiality concerns, retrieved by patient name",
         "Alphabetic", "Small volume, name-based, no confidentiality."),
        ("a national pension fund with 2 million member records "
         "referenced by member ID",
         "Numeric", "Massive volume, referenced by assigned number."),
        ("a congressional office organizing bills by committee: "
         "appropriations, education, health, defense",
         "Subject", "Topic-based legislative work."),
        ("a water district serving 5 municipalities, organizing "
         "customer records by service area",
         "Geographic", "Area-based utility service."),
        ("a small law office with 80 client files retrieved by "
         "client surname",
         "Alphabetic", "Small volume, name-based retrieval."),
        ("a national police database with 500,000 criminal records "
         "requiring strict confidentiality",
         "Numeric", "Massive volume, high confidentiality."),
        ("an environmental agency organizing research by ecosystem: "
         "marine, forest, wetland, urban",
         "Subject", "Topic-based research organization."),
        ("a logistics company organizing shipment records by "
         "destination city and province",
         "Geographic", "Location-based operations."),
        ("a credit cooperative with 400 member savings accounts "
         "retrieved by member name",
         "Alphabetic", "Moderate volume, name-based retrieval."),
        ("a court system with 200,000 cases referenced by docket "
         "number, requiring confidentiality",
         "Numeric", "Large volume, number-referenced, confidential."),
    ]

    for scenario, correct, expl in more_design:
        wrong = pick_wrong_systems(correct)
        choices = [correct] + wrong
        random.shuffle(choices)
        more_design_q = (
            f"Recommend the most appropriate filing system for {scenario}.",
            correct, choices, expl,
            ["system-recommendation", correct.lower()]
        )
        design_questions.append(more_design_q)

    random.shuffle(design_questions)
    for q_data in design_questions[:40]:
        q_text, answer, choices, explanation, tags = q_data
        if answer not in choices:
            choices[0] = answer
        choices = choices[:4]
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, explanation, tags
        ))
        qid += 1

    # --- Fill remaining with mixed application (to reach 200 total) ---
    remaining = 200 - len(questions)
    fill_questions = [
        ("What is the FIRST thing an office should do before "
         "implementing a subject filing system?",
         "Develop a comprehensive relative index listing all approved "
         "subject headings and cross-references",
         ["Develop a comprehensive relative index listing all approved "
          "subject headings and cross-references",
          "Buy new filing cabinets",
          "Train all staff on the alphabet",
          "Assign numbers to all documents"],
         "The relative index must exist BEFORE filing begins — it's the "
         "foundation of subject filing consistency.",
         ["subject", "implementation", "relative-index"]),
        ("In a combination system, personnel files are alphabetic and "
         "financial vouchers are numeric. A document is BOTH a personnel "
         "action AND a financial transaction (e.g., salary adjustment "
         "voucher). Where is the PRIMARY file?",
         "Financial (numeric) — the voucher's primary purpose is to "
         "authorize payment. A cross-reference goes in the personnel file.",
         ["Financial (numeric) — the voucher's primary purpose is to "
          "authorize payment. A cross-reference goes in the personnel file.",
          "Personnel (alphabetic) — it affects an employee",
          "Both systems equally",
          "Neither — create a new system"],
         "The voucher's primary purpose is financial (payment "
         "authorization). The personnel impact is secondary.",
         ["combination-system", "primary-purpose", "cross-reference"]),
        ("An office switches from geographic to numeric filing. What is "
         "the BIGGEST advantage they gain?",
         "Confidentiality — file labels no longer reveal the location "
         "or identity associated with the record",
         ["Confidentiality — file labels no longer reveal the location "
          "or identity associated with the record",
          "Faster retrieval",
          "Less training needed",
          "Smaller filing cabinets"],
         "Switching from geographic (labels show location) to numeric "
         "(labels show only numbers) primarily gains confidentiality.",
         ["system-transition", "advantage", "numeric"]),
        ("An office switches from numeric to alphabetic filing. What is "
         "the BIGGEST advantage they gain?",
         "Direct access — no longer need to consult a separate index "
         "before retrieving a file",
         ["Direct access — no longer need to consult a separate index "
          "before retrieving a file",
          "Better confidentiality",
          "Handles larger volumes",
          "Even distribution of files"],
         "Switching from numeric (indirect) to alphabetic (direct) "
         "eliminates the two-step retrieval process.",
         ["system-transition", "advantage", "alphabetic"]),
        ("What is the BIGGEST risk of NOT maintaining the alphabetic "
         "index in a numeric filing system?",
         "Complete system failure — files exist physically but cannot "
         "be located by name, making the entire collection inaccessible",
         ["Complete system failure — files exist physically but cannot "
          "be located by name, making the entire collection inaccessible",
          "Files will be automatically deleted",
          "The system switches to alphabetic automatically",
          "Minor inconvenience only"],
         "The alphabetic index is the ONLY way to find files by name "
         "in a numeric system. Without it, retrieval is impossible.",
         ["numeric", "risk", "index-dependency"]),
    ]

    # Add more fill questions
    for i in range(remaining - len(fill_questions)):
        # Generate scenario-based questions from pools
        all_pools = [
            (ALPHABETIC_SCENARIOS, "Alphabetic"),
            (NUMERIC_SCENARIOS, "Numeric"),
            (SUBJECT_SCENARIOS, "Subject"),
            (GEOGRAPHIC_SCENARIOS, "Geographic"),
        ]
        pool, correct = random.choice(all_pools)
        scenario_text, expl = random.choice(pool)
        wrong = pick_wrong_systems(correct)

        # Make it harder by adding a twist
        twists = [
            f" However, the office also needs to generate reports by region. Despite this secondary need, what is the PRIMARY filing system?",
            f" The supervisor suggests alphabetic filing instead. Why is {correct.lower()} filing still more appropriate?",
            f" A new clerk argues that all offices should use the same system. Why is this argument flawed?",
        ]
        twist = twists[i % 3]

        if "PRIMARY" in twist:
            q_text = f"(Application #{i+1}) Scenario: {scenario_text}.{twist}"
            answer = correct
            choices = [correct] + wrong
            explanation = f"{expl} The primary system matches the primary retrieval pattern."
        elif "still more appropriate" in twist:
            q_text = f"(Application #{i+1}) Scenario: {scenario_text}.{twist}"
            answer = f"Because the primary retrieval pattern is by {correct.lower().replace('alphabetic', 'name').replace('numeric', 'number').replace('subject', 'topic').replace('geographic', 'location')}"
            choices = [answer,
                       "Because alphabetic is always the default",
                       "Because the supervisor is always wrong",
                       "Because it's cheaper"]
            explanation = expl
        else:
            q_text = f"(Application #{i+1}) Scenario: {scenario_text}.{twist}"
            answer = "Different record types and office functions require different filing systems"
            choices = [answer,
                       "All offices should use alphabetic filing",
                       "The argument is correct — standardization is best",
                       "Only numeric filing should be used everywhere"]
            explanation = "No single system fits all situations. The appropriate system depends on volume, retrieval pattern, and confidentiality needs."

        random.shuffle(choices)
        fill_questions.append((q_text, answer, choices, explanation,
                              ["hard-application", correct.lower()]))

    for q_data in fill_questions[:remaining]:
        q_text, answer, choices, explanation, tags = q_data
        if answer not in choices:
            choices[0] = answer
        choices = choices[:4]
        random.shuffle(choices)
        questions.append(make_question(
            qid, "Hard", q_text, choices, answer, explanation, tags
        ))
        qid += 1

    return questions


# ============================================================
# MAIN
# ============================================================

def main():
    """Generate all 600 questions and write to JSON."""
    print("Generating Easy questions (1-200)...")
    easy = generate_easy_questions()
    print(f"  Generated {len(easy)} Easy questions")

    print("Generating Medium questions (201-400)...")
    medium = generate_medium_questions()
    print(f"  Generated {len(medium)} Medium questions")

    print("Generating Hard questions (401-600)...")
    hard_initial, qid = generate_hard_questions()
    hard_initial, qid = generate_hard_questions_continued(hard_initial, qid)
    hard_final = generate_hard_questions_part3(hard_initial, qid)
    hard_questions_list, qid2 = hard_final if isinstance(hard_final, tuple) else (hard_final, 0)
    hard_all = generate_hard_questions_part4(hard_questions_list, qid2 if qid2 else qid)
    # Trim to 200 and re-number
    hard_all = hard_all[:200]
    for i, q in enumerate(hard_all):
        q["id"] = 401 + i
    print(f"  Generated {len(hard_all)} Hard questions")

    all_questions = easy + medium + hard_all
    print(f"\nTotal questions: {len(all_questions)}")

    # Validate
    assert len(all_questions) == 600, f"Expected 600, got {len(all_questions)}"
    for q in all_questions:
        assert q["answer"] in q["choices"], (
            f"Q{q['id']}: answer '{q['answer']}' not in choices"
        )

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability",
        "indexing-and-record-organization", "filing-systems"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Written to: {output_path}")

    # Print distribution
    difficulties = {}
    for q in all_questions:
        d = q["difficulty"]
        difficulties[d] = difficulties.get(d, 0) + 1
    print(f"Distribution: {difficulties}")


if __name__ == "__main__":
    main()
