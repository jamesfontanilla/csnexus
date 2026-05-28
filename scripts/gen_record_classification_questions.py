"""
Generate 600-question bank for Record Classification.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).

Topics covered:
- Classifying documents into major record classes (Personnel, Administrative,
  Legal, Financial, Correspondence, Technical/Operational)
- Identifying classification schemes (subject, functional, numerical)
- Hierarchical classification (main class → subclass → specific topic)
- Odd-one-out (which document does NOT belong)
- Cross-referencing decisions
- Distinguishing classification from filing and indexing
- Decision flowchart application
- Numerical classification codes
"""
import json
import random
import os

random.seed(42)

# ============================================================
# DATA POOLS
# ============================================================

# Major record classes and their documents
PERSONNEL_DOCS = [
    ("CS Form 212 (Personal Data Sheet)", "It records personal information of an employee, making it a personnel record."),
    ("Statement of Assets, Liabilities, and Net Worth (SALN)", "SALN is part of an employee's 201 file, making it primarily a personnel record."),
    ("Appointment Paper", "An appointment paper records an employee's hiring or promotion — a personnel action."),
    ("Certificate of Employment", "It certifies an employee's service record, which is a personnel document."),
    ("Performance Evaluation Report", "It assesses an employee's work performance — a personnel record."),
    ("Leave Application", "A leave application is an employee benefit request — a personnel record."),
    ("Daily Time Record (DTR)", "DTR tracks employee attendance, making it a personnel record."),
    ("Service Record", "It documents an employee's history of government service — a personnel record."),
    ("Notice of Salary Adjustment", "It records a change in employee compensation — a personnel action."),
    ("Certificate of Training Completion", "Training certificates are part of an employee's development record — personnel."),
    ("Position Description Form", "It describes the duties of a position held by an employee — personnel."),
    ("Leave Card", "A leave card tracks an employee's leave credits — a personnel record."),
    ("Oath of Office", "It is executed upon assumption of duty — a personnel record."),
    ("Personal Data Sheet Update", "An update to employee personal information — personnel."),
    ("Certificate of Leave Credits", "It shows an employee's remaining leave balance — personnel."),
    ("Clearance Form", "Employee clearance upon separation from service — personnel."),
    ("Notice of Step Increment", "Records an employee's salary step increase — personnel."),
    ("Request for Transfer", "An employee's request to move to another office — personnel."),
    ("Medical Certificate for Sick Leave", "Supports an employee's sick leave application — personnel."),
    ("Employee Disciplinary Action Report", "Documents disciplinary proceedings against an employee — personnel."),
]

ADMINISTRATIVE_DOCS = [
    ("Office Order", "An office order is an internal directive for operations — administrative."),
    ("Office Memorandum", "A memorandum is an internal communication/directive — administrative."),
    ("Minutes of Meeting", "Minutes record internal proceedings — an administrative document."),
    ("Travel Order", "A travel order authorizes official travel — an administrative directive."),
    ("Special Order", "A special order designates or assigns duties — administrative."),
    ("Organizational Chart", "It shows the office structure — an administrative record."),
    ("Annual Report", "An annual report summarizes office operations — administrative."),
    ("Office Calendar of Activities", "It plans internal activities — administrative."),
    ("Inventory of Office Equipment", "Property inventory is an internal management record — administrative."),
    ("Resolution on Revised Office Structure", "Internal governance document — administrative."),
]

ADMINISTRATIVE_DOCS += [
    ("Attendance Monitoring Report", "It tracks office-wide attendance compliance — administrative."),
    ("Office Circular", "A circular disseminates internal policies — administrative."),
    ("Designation Order", "Designates an officer-in-charge — an administrative directive."),
    ("Authority to Travel", "Authorizes an employee's official trip — administrative."),
    ("Job Order for Maintenance", "Directs maintenance work — an administrative operational record."),
    ("Office Rules and Regulations", "Internal governance policies — administrative."),
    ("Committee Creation Order", "Creates an internal committee — administrative."),
    ("Flag Ceremony Schedule", "Internal scheduling document — administrative."),
    ("Building Access Policy", "Internal security policy — administrative."),
    ("Vehicle Trip Ticket", "Authorizes use of office vehicle — administrative."),
]

FINANCIAL_DOCS = [
    ("Disbursement Voucher", "A disbursement voucher authorizes payment — a financial record."),
    ("Purchase Order", "A purchase order commits funds for procurement — financial."),
    ("Payroll", "Payroll records salary payments — a financial document."),
    ("Annual Budget Proposal", "A budget proposal plans expenditures — financial."),
    ("Quarterly Financial Report", "Reports financial status — a financial record."),
    ("Statement of Allotments", "Tracks budget allocations — financial."),
    ("Annual Procurement Plan", "Plans purchases for the fiscal year — financial."),
    ("Obligation Request", "Commits funds for a specific expense — financial."),
    ("Liquidation Report", "Accounts for cash advances — a financial record."),
    ("Check Disbursement Journal", "Records check payments — financial."),
    ("Certificate of Availability of Funds", "Certifies budget availability — financial."),
    ("Abstract of Bids", "Summarizes procurement bids — financial."),
    ("Notice of Award to Supplier", "Awards a procurement contract — financial."),
    ("Petty Cash Voucher", "Records small cash disbursements — financial."),
    ("Tax Remittance Report", "Records tax payments to BIR — financial."),
    ("Collection Report", "Records revenue collected — financial."),
    ("Bank Reconciliation Statement", "Reconciles office and bank records — financial."),
    ("Request for Quotation", "Solicits price quotes for procurement — financial."),
    ("Audit Observation Memorandum", "COA audit finding on financial matters — financial."),
    ("Statement of Cash Flows", "Reports cash movement — financial."),
]

LEGAL_DOCS = [
    ("Memorandum of Agreement (MOA)", "A MOA is a binding agreement between parties — a legal document."),
    ("Service Contract", "A contract binds parties to obligations — legal."),
    ("Legal Opinion", "A legal opinion interprets law — a legal record."),
    ("Court Order", "A court order is a judicial directive — legal."),
    ("Deed of Donation", "A deed transfers property rights — legal."),
    ("Affidavit", "A sworn statement with legal force — legal."),
    ("Notarized Document", "Notarization gives legal validity — legal."),
    ("Memorandum of Understanding (MOU)", "An MOU establishes mutual commitments — legal."),
    ("Administrative Complaint", "A formal complaint initiating legal proceedings — legal."),
    ("Subpoena", "A legal order to appear or produce documents — legal."),
    ("Resolution of Adjudication", "A decision on a legal matter — legal."),
    ("Non-Disclosure Agreement", "A binding confidentiality agreement — legal."),
    ("Lease Contract", "A binding agreement for property use — legal."),
    ("Power of Attorney", "Authorizes legal representation — legal."),
    ("Cease and Desist Order", "A legal directive to stop an action — legal."),
]

CORRESPONDENCE_DOCS = [
    ("Incoming Letter from a Citizen", "External communication received — correspondence."),
    ("Outgoing Letter to Another Agency", "External communication sent — correspondence."),
    ("Endorsement Letter", "Forwards a document to another office — correspondence."),
    ("Letter of Inquiry from a Congressman", "External request for information — correspondence."),
    ("Reply Letter to a Client", "Response to external party — correspondence."),
    ("Invitation to a Conference", "External communication inviting participation — correspondence."),
    ("Thank You Letter from a Partner Agency", "External communication received — correspondence."),
    ("Request Letter from an NGO", "External organization's request — correspondence."),
    ("Referral Letter to Another Office", "Routes a matter to another agency — correspondence."),
    ("Acknowledgment Letter", "Confirms receipt of external communication — correspondence."),
    ("Complaint Letter from the Public", "External grievance received — correspondence."),
    ("Letter of Intent from a Supplier", "External business communication — correspondence."),
    ("Follow-up Letter to DILG", "External communication sent — correspondence."),
    ("Transmittal Letter", "Accompanies documents sent externally — correspondence."),
    ("Congratulatory Letter from the President", "External communication received — correspondence."),
]

TECHNICAL_DOCS = [
    ("Project Completion Report", "Documents project outcomes — technical/operational."),
    ("Program Implementation Plan", "Plans core service delivery — technical/operational."),
    ("Technical Specifications Document", "Details technical requirements — technical/operational."),
    ("Monitoring and Evaluation Report", "Assesses program effectiveness — technical/operational."),
    ("Research Study Report", "Documents research findings — technical/operational."),
    ("Field Inspection Report", "Records on-site findings — technical/operational."),
    ("Environmental Impact Assessment", "Technical study of environmental effects — technical/operational."),
    ("Engineering Design Plan", "Technical blueprint for construction — technical/operational."),
    ("Laboratory Test Results", "Scientific/technical findings — technical/operational."),
    ("Statistical Report on Service Delivery", "Operational data analysis — technical/operational."),
]

# Category labels
CATEGORIES = {
    "Personnel": PERSONNEL_DOCS,
    "Administrative": ADMINISTRATIVE_DOCS,
    "Financial": FINANCIAL_DOCS,
    "Legal": LEGAL_DOCS,
    "Correspondence": CORRESPONDENCE_DOCS,
    "Technical/Operational": TECHNICAL_DOCS,
}

CATEGORY_NAMES = list(CATEGORIES.keys())

# Numerical classification scheme
NUMERICAL_SCHEME = {
    "100": "Administrative Records",
    "110": "Organization and Management",
    "111": "Office Orders",
    "112": "Memoranda",
    "113": "Organizational Charts",
    "114": "Minutes of Meetings",
    "115": "Annual Reports",
    "120": "Personnel Records",
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
    "220": "Disbursements",
    "221": "Salary Vouchers",
    "222": "Travel Reimbursements",
    "223": "Petty Cash",
    "230": "Collections and Revenue",
    "231": "Collection Reports",
    "232": "Revenue Summaries",
    "300": "Legal Records",
    "310": "Contracts and Agreements",
    "311": "Service Contracts",
    "312": "MOAs and MOUs",
    "320": "Cases",
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

# Classification schemes
SCHEMES = [
    ("Subject Classification", "groups documents by topic or subject matter"),
    ("Functional Classification", "groups documents by business function or activity"),
    ("Numerical Classification", "assigns numeric codes representing categories"),
]

# Concepts for definition questions
CONCEPTS = [
    ("Record classification", "assigning a document to a predetermined category based on content or purpose", "filing"),
    ("Filing", "placing a document in its correct position within a category", "classification"),
    ("Indexing", "creating finding aids to locate documents", "classification"),
    ("Cross-referencing", "creating pointers from secondary categories to the primary file location", "filing"),
    ("Rule of Specificity", "classifying at the most specific subcategory level available", "classifying at the broadest level"),
    ("Primary classification", "the main category where the original document is filed", "the only category a document can belong to"),
]

# Decision flowchart order
FLOWCHART_ORDER = ["Personnel", "Financial", "Legal", "Administrative", "Correspondence", "Technical/Operational"]

# Agencies for context
AGENCIES = ["CSC", "COA", "DILG", "DBM", "DENR", "DOH", "DepEd", "DOLE", "DPWH", "DOT", "DOJ", "DSWD"]

# Employee names for context
EMPLOYEE_NAMES = [
    "Maria Santos", "Juan Reyes", "Ana Cruz", "Pedro Garcia", "Rosa Mendoza",
    "Carlos Rivera", "Elena Bautista", "Roberto Flores", "Carmen Gonzales",
    "Fernando Torres", "Patricia Ramos", "Luis Morales", "Gloria Navarro",
    "Ricardo Perez", "Teresa Castillo", "Eduardo Hernandez", "Cristina Lopez",
    "Miguel Romero", "Dolores Salazar", "Alfredo Villanueva",
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def make_question(qid, difficulty, question, choices, answer, explanation, tags):
    """Create a question dict in the standard format."""
    return {
        "id": qid,
        "subtest": "Clerical Ability",
        "module": "Indexing and Record Organization",
        "subtopic": "Record Classification",
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": ["Sub-Professional"],
        "language": "English",
    }


def pick_doc(category):
    """Pick a random document from a category, return (doc_name, explanation)."""
    return random.choice(CATEGORIES[category])


def pick_wrong_categories(correct, n=3):
    """Pick n wrong category names."""
    wrong = [c for c in CATEGORY_NAMES if c != correct]
    return random.sample(wrong, min(n, len(wrong)))


def shuffle_choices_with_answer(choices, answer):
    """Shuffle choices ensuring answer is included."""
    if answer not in choices:
        choices.append(answer)
    random.shuffle(choices)
    return choices


# ============================================================
# EASY QUESTIONS (IDs 1-200)
# ============================================================

def generate_easy_questions():
    """Generate 200 Easy questions. Single-category identification, basic concepts."""
    questions = []
    used_docs = set()
    qid = 1

    # --- Type 1: "Which category does this document belong to?" (80 questions) ---
    all_docs_with_cat = []
    for cat, docs in CATEGORIES.items():
        for doc_name, expl in docs:
            all_docs_with_cat.append((doc_name, cat, expl))
    random.shuffle(all_docs_with_cat)

    for doc_name, correct_cat, expl in all_docs_with_cat:
        if len(questions) >= 80:
            break
        if doc_name in used_docs:
            continue
        used_docs.add(doc_name)

        wrong = pick_wrong_categories(correct_cat, 3)
        choices = [correct_cat] + wrong
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Easy",
            f'Under which major record class should a "{doc_name}" be classified?',
            choices, correct_cat, expl,
            ["document-classification", "major-record-class"]
        ))
        qid += 1

    # --- Type 2: "Which of these is a [Category] record?" (40 questions) ---
    type2_used = set()
    for _ in range(80):
        if len(questions) >= 120:
            break
        correct_cat = random.choice(CATEGORY_NAMES)
        correct_doc, expl = pick_doc(correct_cat)

        # Avoid reusing the same correct_doc
        if correct_doc in type2_used:
            continue
        type2_used.add(correct_doc)

        # Pick 3 wrong docs from other categories
        wrong_cats = [c for c in CATEGORY_NAMES if c != correct_cat]
        wrong_docs = []
        for wc in random.sample(wrong_cats, 3):
            wd, _ = pick_doc(wc)
            wrong_docs.append(wd)

        choices = [correct_doc] + wrong_docs
        random.shuffle(choices)

        # Use unique question text by listing the choices in the stem
        choices_str = "; ".join(choices)
        questions.append(make_question(
            qid, "Easy",
            f"Given these documents: {choices_str} — which one is classified as a {correct_cat} record?",
            choices, correct_doc, expl,
            ["document-classification", "identify-category-member"]
        ))
        qid += 1

    # --- Type 3: Definition/concept questions (30 questions) ---
    concept_questions = [
        ("What is record classification?",
         ["Assigning a document to a predetermined category based on its content or purpose",
          "Arranging documents alphabetically within a folder",
          "Creating an index card for every document",
          "Stamping a document with a received date"],
         "Assigning a document to a predetermined category based on its content or purpose",
         "Record classification is the act of assigning a document to a category — it determines WHAT group a document belongs to.",
         ["definition", "concept"]),
        ("What is the difference between classification and filing?",
         ["Classification determines the category; filing determines the position within that category",
          "Classification and filing are the same process",
          "Filing determines the category; classification determines the position",
          "Classification is for digital records; filing is for paper records"],
         "Classification determines the category; filing determines the position within that category",
         "Classification answers 'what group?' while filing answers 'where within the group?'",
         ["definition", "classification-vs-filing"]),
        ("What does the Rule of Specificity require?",
         ["Classify at the most specific subcategory level available",
          "Always use the broadest category possible",
          "Create a new category for every document",
          "File documents by date rather than subject"],
         "Classify at the most specific subcategory level available",
         "The Rule of Specificity requires classifying at the narrowest matching level, not leaving documents in broad parent categories.",
         ["rule-of-specificity", "concept"]),
        ("What is a cross-reference in records management?",
         ["A pointer from a secondary category to the primary file location",
          "A copy of the document placed in every relevant folder",
          "The document's tracking number",
          "A stamp indicating the document has been reviewed"],
         "A pointer from a secondary category to the primary file location",
         "A cross-reference is a pointer (not a copy) that directs users from a secondary category to where the original is filed.",
         ["cross-reference", "concept"]),
        ("Which classification scheme groups documents by topic or subject matter?",
         ["Subject Classification", "Functional Classification", "Numerical Classification", "Chronological Classification"],
         "Subject Classification",
         "Subject classification organizes records by their topic, regardless of who created them or when.",
         ["classification-scheme", "subject"]),
        ("Which classification scheme assigns numeric codes to represent categories?",
         ["Numerical Classification", "Subject Classification", "Functional Classification", "Alphabetical Classification"],
         "Numerical Classification",
         "Numerical classification uses codes (like 100, 110, 111) where each number represents a specific category in the hierarchy.",
         ["classification-scheme", "numerical"]),
        ("Which classification scheme groups documents by business function or activity?",
         ["Functional Classification", "Subject Classification", "Numerical Classification", "Topical Classification"],
         "Functional Classification",
         "Functional classification organizes records by the business function they support (e.g., procurement, oversight, administration).",
         ["classification-scheme", "functional"]),
        ("What is the primary classification of a document?",
         ["The main category where the original document is filed",
          "The first category listed in the classification scheme",
          "The category assigned by the supervisor",
          "The broadest possible category"],
         "The main category where the original document is filed",
         "Primary classification is where the original is stored — determined by the document's main purpose.",
         ["primary-classification", "concept"]),
        ("What question does record classification answer?",
         ["What group does this document belong to?",
          "Where exactly should this document be placed?",
          "How can this document be found later?",
          "When was this document created?"],
         "What group does this document belong to?",
         "Classification answers 'what category?' — filing answers 'where within it?' and indexing answers 'how to find it?'",
         ["definition", "concept"]),
        ("In the Philippine government, which body mandates records management standards?",
         ["National Archives of the Philippines (NAP)",
          "Commission on Audit (COA)",
          "Civil Service Commission (CSC)",
          "Department of Budget and Management (DBM)"],
         "National Archives of the Philippines (NAP)",
         "The NAP sets records management standards including classification schemes and disposition schedules for all government agencies.",
         ["philippine-context", "concept"]),
    ]

    # Add more concept questions
    concept_questions += [
        ("What does indexing do in records management?",
         ["Creates finding aids to locate documents",
          "Assigns documents to categories",
          "Arranges documents in alphabetical order",
          "Destroys outdated records"],
         "Creates finding aids to locate documents",
         "Indexing creates search aids (like index cards or database entries) that help users find documents — it answers 'how can this be found?'",
         ["definition", "indexing"]),
        ("Which major record class includes office orders and memoranda?",
         ["Administrative", "Personnel", "Financial", "Legal"],
         "Administrative",
         "Office orders and memoranda are internal directives/communications — they belong to Administrative records.",
         ["major-record-class", "administrative"]),
        ("Which major record class includes disbursement vouchers and payroll?",
         ["Financial", "Administrative", "Personnel", "Legal"],
         "Financial",
         "Disbursement vouchers and payroll involve money transactions — they are Financial records.",
         ["major-record-class", "financial"]),
        ("Which major record class includes appointment papers and leave records?",
         ["Personnel", "Administrative", "Financial", "Correspondence"],
         "Personnel",
         "Appointment papers and leave records relate to employee status and benefits — they are Personnel records.",
         ["major-record-class", "personnel"]),
        ("Which major record class includes contracts and MOAs?",
         ["Legal", "Administrative", "Financial", "Correspondence"],
         "Legal",
         "Contracts and MOAs are binding agreements between parties — they are Legal records.",
         ["major-record-class", "legal"]),
        ("Which major record class includes incoming and outgoing letters?",
         ["Correspondence", "Administrative", "Legal", "Technical/Operational"],
         "Correspondence",
         "Incoming and outgoing letters are external communications — they belong to Correspondence.",
         ["major-record-class", "correspondence"]),
        ("What is a 201 file in Philippine government offices?",
         ["An employee's complete personnel record folder",
          "A financial ledger",
          "A legal case file",
          "An administrative policy manual"],
         "An employee's complete personnel record folder",
         "A 201 file contains all personnel documents of an individual employee — from appointment to separation.",
         ["philippine-context", "personnel"]),
        ("How many major record classes are commonly used in Philippine government offices?",
         ["Six", "Three", "Four", "Ten"],
         "Six",
         "The six classes are: Personnel, Administrative, Legal, Financial, Correspondence, and Technical/Operational.",
         ["major-record-class", "concept"]),
        ("What determines the primary classification when a document fits multiple categories?",
         ["The document's main purpose",
          "The sender's preference",
          "The date it was received",
          "The document's physical format"],
         "The document's main purpose",
         "The Purpose Rule states: classify by the document's primary purpose. Secondary categories get cross-references.",
         ["primary-classification", "purpose-rule"]),
        ("In numerical classification, what does a code like '122' represent?",
         ["A specific category in the classification hierarchy",
          "The document's sequence number",
          "The date the document was created",
          "The number of pages in the document"],
         "A specific category in the classification hierarchy",
         "In numerical classification, codes represent categories (e.g., 122 = Personnel → Leave Records), not sequence numbers or dates.",
         ["numerical-classification", "concept"]),
    ]

    for q_data in concept_questions[:30]:
        question_text, choices, answer, explanation, tags = q_data
        questions.append(make_question(
            qid, "Easy", question_text, choices, answer, explanation, tags
        ))
        qid += 1

    # --- Type 4: "Which does NOT belong?" - obvious cases (50 questions) ---
    while len(questions) < 200:
        # Pick a majority category and one outlier
        majority_cat = random.choice(CATEGORY_NAMES)
        outlier_cat = random.choice([c for c in CATEGORY_NAMES if c != majority_cat])

        majority_docs_pool = CATEGORIES[majority_cat][:]
        random.shuffle(majority_docs_pool)
        outlier_doc, outlier_expl = pick_doc(outlier_cat)

        # Pick 3 docs from majority
        majority_picks = random.sample(majority_docs_pool, min(3, len(majority_docs_pool)))
        majority_names = [d[0] for d in majority_picks]

        choices = majority_names + [outlier_doc]
        random.shuffle(choices)

        explanation = f"'{outlier_doc}' is a {outlier_cat} record, while the others are all {majority_cat} records."

        # Include choices in question text to make each unique
        choices_str = "; ".join(choices)
        questions.append(make_question(
            qid, "Easy",
            f"Which of the following does NOT belong to the {majority_cat} record class? Documents: {choices_str}",
            choices, outlier_doc, explanation,
            ["odd-one-out", "major-record-class"]
        ))
        qid += 1

    return questions[:200]


# ============================================================
# MEDIUM QUESTIONS (IDs 201-400)
# ============================================================

def generate_medium_questions():
    """Generate 200 Medium questions. Two-step reasoning, ambiguous docs, scheme identification."""
    questions = []
    qid = 201

    # --- Type 1: Ambiguous documents requiring decision flowchart (50 questions) ---
    ambiguous_docs = [
        ("Memorandum directing all employees to submit updated SALN",
         "Administrative",
         "The memo itself is an internal directive (Administrative). The SALNs submitted in response are Personnel records.",
         ["decision-flowchart", "directive-vs-content"]),
        ("Memorandum directing the Finance Division to release training funds",
         "Administrative",
         "The memo is a directive (Administrative). The actual disbursement voucher created in response is Financial.",
         ["decision-flowchart", "directive-vs-content"]),
        ("Office Order creating a committee to review procurement policies",
         "Administrative",
         "An office order is an internal directive — Administrative. The procurement policies themselves may be Financial.",
         ["decision-flowchart", "directive-vs-content"]),
        ("Letter from COA regarding audit findings on payroll",
         "Correspondence",
         "It is an external communication received from another agency — Correspondence. Cross-reference: Financial.",
         ["decision-flowchart", "correspondence-vs-financial"]),
        ("Notice of Salary Adjustment for Clerk III Maria Santos",
         "Personnel",
         "It records a change in an employee's compensation status — Personnel. The payroll reflecting it is Financial.",
         ["decision-flowchart", "personnel-vs-financial"]),
        ("Resolution approving the annual budget for employee training",
         "Financial",
         "The resolution commits funds (budget approval) — Financial. Cross-reference: Personnel (training).",
         ["decision-flowchart", "financial-vs-personnel"]),
        ("Endorsement letter forwarding a citizen complaint to the Legal Division",
         "Correspondence",
         "The endorsement is a routing communication — Correspondence. The complaint itself may be cross-referenced under Legal.",
         ["decision-flowchart", "correspondence-vs-legal"]),
        ("Special Order granting authority to sign financial documents",
         "Administrative",
         "A special order is an internal directive delegating authority — Administrative, not Financial.",
         ["decision-flowchart", "directive-vs-content"]),
        ("Report on the implementation of the Gender and Development program",
         "Technical/Operational",
         "A program implementation report documents core function delivery — Technical/Operational.",
         ["decision-flowchart", "technical"]),
        ("Memorandum of Agreement for employee health insurance coverage",
         "Legal",
         "A MOA is a binding agreement between parties — Legal. Cross-reference: Personnel (employee benefit).",
         ["decision-flowchart", "legal-vs-personnel"]),
        ("Travel reimbursement claim of Director Reyes",
         "Financial",
         "A reimbursement claim involves money (payment request) — Financial, not Administrative.",
         ["decision-flowchart", "financial-vs-administrative"]),
        ("Certificate of Appearance for a court hearing",
         "Legal",
         "It relates to legal proceedings (court hearing) — Legal.",
         ["decision-flowchart", "legal"]),
        ("Invitation from DepEd to attend a national conference",
         "Correspondence",
         "An invitation from an external agency is incoming correspondence — Correspondence.",
         ["decision-flowchart", "correspondence"]),
        ("Office Order designating Juan Reyes as Officer-in-Charge",
         "Administrative",
         "An office order is an internal directive — Administrative. It affects an employee but the document itself is a directive.",
         ["decision-flowchart", "administrative-vs-personnel"]),
        ("Request for Quotation sent to three suppliers",
         "Financial",
         "An RFQ is part of the procurement process (committing funds) — Financial.",
         ["decision-flowchart", "financial"]),
        ("Complaint filed by an employee against a co-worker",
         "Personnel",
         "An internal employee complaint is a personnel/disciplinary matter — Personnel. If it escalates to formal charges, cross-reference Legal.",
         ["decision-flowchart", "personnel-vs-legal"]),
        ("Board Resolution approving a new organizational structure",
         "Administrative",
         "A resolution on organizational structure is internal governance — Administrative.",
         ["decision-flowchart", "administrative"]),
        ("Certification of available funds for a construction project",
         "Financial",
         "Certifying fund availability is a financial action — Financial.",
         ["decision-flowchart", "financial"]),
        ("Letter to the Office of the Ombudsman submitting required documents",
         "Correspondence",
         "A letter sent to an external body is outgoing correspondence — Correspondence. Cross-reference: Legal.",
         ["decision-flowchart", "correspondence-vs-legal"]),
        ("Daily Time Record summary for the month of March",
         "Personnel",
         "DTR tracks employee attendance — Personnel, even though it may be used for payroll computation.",
         ["decision-flowchart", "personnel-vs-financial"]),
        ("Audit report on the agency's procurement activities",
         "Financial",
         "An audit report on procurement examines financial transactions — Financial.",
         ["decision-flowchart", "financial"]),
        ("Memorandum requiring all staff to attend a fire drill",
         "Administrative",
         "A memo directing staff action (fire drill) is an internal directive — Administrative.",
         ["decision-flowchart", "administrative"]),
        ("Contract of Service for a janitorial company",
         "Legal",
         "A contract is a binding agreement — Legal. Cross-reference: Financial (involves payment).",
         ["decision-flowchart", "legal-vs-financial"]),
        ("Performance bonus computation for FY 2024",
         "Financial",
         "Bonus computation involves money calculation — Financial. Cross-reference: Personnel.",
         ["decision-flowchart", "financial-vs-personnel"]),
        ("Reply letter to a senator's inquiry about agency programs",
         "Correspondence",
         "A reply to an external party is outgoing correspondence — Correspondence.",
         ["decision-flowchart", "correspondence"]),
    ]

    # Generate questions from ambiguous docs
    for doc_text, correct_cat, expl, tags in ambiguous_docs[:50]:
        wrong = pick_wrong_categories(correct_cat, 3)
        choices = [correct_cat] + wrong
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f'Under which major record class should the following be classified: "{doc_text}"?',
            choices, correct_cat, expl, tags
        ))
        qid += 1

    # Pad to 50 if needed with more ambiguous scenarios
    while len(questions) < 50:
        cat = random.choice(CATEGORY_NAMES)
        doc, expl = pick_doc(cat)
        employee = random.choice(EMPLOYEE_NAMES)
        agency = random.choice(AGENCIES)

        wrong = pick_wrong_categories(cat, 3)
        choices = [cat] + wrong
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f'A document titled "{doc}" from {agency} regarding {employee} should be classified under which record class?',
            choices, cat, expl,
            ["document-classification", "context-application"]
        ))
        qid += 1

    # --- Type 2: Numerical classification code assignment (40 questions) ---
    code_items = list(NUMERICAL_SCHEME.items())
    # Only use specific codes (3 digits) for questions
    specific_codes = [(code, desc) for code, desc in code_items if len(code) == 3]
    random.shuffle(specific_codes)

    for code, desc in specific_codes[:40]:
        # Create wrong choices from other codes at same level
        parent = code[:2]
        siblings = [c for c, d in code_items if c != code and len(c) == 3]
        wrong_codes = random.sample(siblings, min(3, len(siblings)))

        choices = [code] + wrong_codes
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f'Using a numerical classification scheme, which code should be assigned to "{desc}"?',
            choices, code,
            f"Code {code} represents '{desc}' in the numerical classification hierarchy.",
            ["numerical-classification", "code-assignment"]
        ))
        qid += 1

    # --- Type 3: "Which does NOT belong?" with less obvious outliers (40 questions) ---
    while len(questions) < 130 + (201 - 1):
        majority_cat = random.choice(CATEGORY_NAMES)
        # Pick an outlier from a RELATED category (harder to distinguish)
        related_map = {
            "Personnel": ["Administrative", "Financial"],
            "Administrative": ["Personnel", "Correspondence"],
            "Financial": ["Administrative", "Legal"],
            "Legal": ["Administrative", "Correspondence"],
            "Correspondence": ["Administrative", "Legal"],
            "Technical/Operational": ["Administrative", "Financial"],
        }
        outlier_cat = random.choice(related_map.get(majority_cat, ["Administrative"]))

        majority_docs_pool = CATEGORIES[majority_cat][:]
        random.shuffle(majority_docs_pool)
        outlier_doc, _ = pick_doc(outlier_cat)

        majority_picks = random.sample(majority_docs_pool, min(3, len(majority_docs_pool)))
        majority_names = [d[0] for d in majority_picks]

        choices = majority_names + [outlier_doc]
        random.shuffle(choices)

        explanation = f"'{outlier_doc}' is a {outlier_cat} record. The others are all {majority_cat} records."

        # Include choices in question text to make each unique
        choices_str = "; ".join(choices)
        questions.append(make_question(
            qid, "Medium",
            f"Which of the following does NOT belong in the same record class as the others? Documents: {choices_str}",
            choices, outlier_doc, explanation,
            ["odd-one-out", "related-categories"]
        ))
        qid += 1

    # --- Type 4: Hierarchical classification - determine correct level (35 questions) ---
    hierarchy_questions = [
        ("A vacation leave application from Ana Cruz",
         "Personnel → Leave Records → Vacation Leave",
         ["Personnel", "Personnel → Leave Records", "Personnel → Leave Records → Vacation Leave", "Administrative → Leave"],
         "The Rule of Specificity requires classifying at the most specific level: Personnel → Leave Records → Vacation Leave."),
        ("An office order reassigning a clerk to the Records Section",
         "Administrative → Organization and Management → Office Orders",
         ["Administrative", "Administrative → Organization and Management", "Administrative → Organization and Management → Office Orders", "Personnel → Appointments"],
         "An office order is an internal directive. Most specific level: Administrative → Organization and Management → Office Orders."),
        ("A disbursement voucher for salary payment",
         "Financial → Disbursements → Salary Vouchers",
         ["Financial", "Financial → Disbursements", "Financial → Disbursements → Salary Vouchers", "Personnel → Payroll"],
         "A salary DV is a disbursement. Most specific: Financial → Disbursements → Salary Vouchers."),
        ("An annual budget proposal for FY 2025",
         "Financial → Budget → Annual Budget Proposals",
         ["Financial", "Financial → Budget", "Financial → Budget → Annual Budget Proposals", "Administrative → Planning"],
         "Most specific level: Financial → Budget → Annual Budget Proposals."),
        ("A service contract with ABC Consulting",
         "Legal → Contracts and Agreements → Service Contracts",
         ["Legal", "Legal → Contracts and Agreements", "Legal → Contracts and Agreements → Service Contracts", "Financial → Procurement"],
         "A service contract is a binding agreement. Most specific: Legal → Contracts and Agreements → Service Contracts."),
        ("Minutes of the management committee meeting",
         "Administrative → Organization and Management → Minutes of Meetings",
         ["Administrative", "Administrative → Organization and Management", "Administrative → Organization and Management → Minutes of Meetings", "Correspondence"],
         "Minutes record internal proceedings. Most specific: Administrative → Organization and Management → Minutes of Meetings."),
        ("A sick leave application from Pedro Garcia",
         "Personnel → Leave Records → Sick Leave",
         ["Personnel", "Personnel → Leave Records", "Personnel → Leave Records → Sick Leave", "Administrative"],
         "Most specific: Personnel → Leave Records → Sick Leave."),
        ("A petty cash voucher for office supplies",
         "Financial → Disbursements → Petty Cash",
         ["Financial", "Financial → Disbursements", "Financial → Disbursements → Petty Cash", "Administrative → Supply"],
         "Petty cash is a disbursement type. Most specific: Financial → Disbursements → Petty Cash."),
        ("A letter from a citizen requesting certification",
         "Correspondence → Incoming Communications → Letters from Citizens",
         ["Correspondence", "Correspondence → Incoming Communications", "Correspondence → Incoming Communications → Letters from Citizens", "Administrative"],
         "Most specific: Correspondence → Incoming Communications → Letters from Citizens."),
        ("A performance evaluation report for Juan Reyes",
         "Personnel → Performance Evaluations",
         ["Personnel", "Personnel → Performance Evaluations", "Administrative → Reports", "Financial"],
         "Performance evaluations are personnel records. Most specific available: Personnel → Performance Evaluations."),
        ("An equipment inventory list",
         "Administrative → Property and Supply → Equipment Inventory",
         ["Administrative", "Administrative → Property and Supply", "Administrative → Property and Supply → Equipment Inventory", "Financial → Assets"],
         "Equipment inventory is property management. Most specific: Administrative → Property and Supply → Equipment Inventory."),
        ("A MOA between CSC and a training provider",
         "Legal → Contracts and Agreements → MOAs and MOUs",
         ["Legal", "Legal → Contracts and Agreements", "Legal → Contracts and Agreements → MOAs and MOUs", "Administrative"],
         "A MOA is a binding agreement. Most specific: Legal → Contracts and Agreements → MOAs and MOUs."),
        ("A collection report for fees received",
         "Financial → Collections and Revenue → Collection Reports",
         ["Financial", "Financial → Collections and Revenue", "Financial → Collections and Revenue → Collection Reports", "Administrative → Reports"],
         "Collection reports track revenue. Most specific: Financial → Collections and Revenue → Collection Reports."),
        ("An endorsement letter forwarding documents to DILG",
         "Correspondence → Outgoing Communications → Endorsement Letters",
         ["Correspondence", "Correspondence → Outgoing Communications", "Correspondence → Outgoing Communications → Endorsement Letters", "Administrative"],
         "An endorsement is outgoing correspondence. Most specific: Correspondence → Outgoing Communications → Endorsement Letters."),
        ("A training completion certificate for leadership seminar",
         "Personnel → Training Records",
         ["Personnel", "Personnel → Training Records", "Administrative → Training", "Legal → Certificates"],
         "Training certificates are part of employee development records. Most specific: Personnel → Training Records."),
    ]

    for doc_desc, correct_level, choices, expl in hierarchy_questions[:35]:
        questions.append(make_question(
            qid, "Medium",
            f'What is the most specific classification for: "{doc_desc}"?',
            choices, correct_level, expl,
            ["rule-of-specificity", "hierarchical-classification"]
        ))
        qid += 1

    # Pad hierarchy questions if needed
    extra_hierarchy = [
        ("A supply requisition form",
         "Administrative → Property and Supply → Supply Requisitions",
         ["Administrative", "Administrative → Property and Supply", "Administrative → Property and Supply → Supply Requisitions", "Financial → Procurement"],
         "Supply requisitions are property/supply management. Most specific: Administrative → Property and Supply → Supply Requisitions."),
        ("An administrative case decision",
         "Legal → Cases → Administrative Cases",
         ["Legal", "Legal → Cases", "Legal → Cases → Administrative Cases", "Administrative"],
         "Administrative cases are legal proceedings. Most specific: Legal → Cases → Administrative Cases."),
        ("A legal opinion on procurement rules",
         "Legal → Cases → Legal Opinions",
         ["Legal", "Legal → Cases", "Legal → Cases → Legal Opinions", "Financial → Procurement"],
         "Legal opinions interpret law. Most specific: Legal → Cases → Legal Opinions."),
        ("An allotment release order",
         "Financial → Budget → Allotment Releases",
         ["Financial", "Financial → Budget", "Financial → Budget → Allotment Releases", "Administrative → Orders"],
         "Allotment releases are budget actions. Most specific: Financial → Budget → Allotment Releases."),
        ("A reply letter to a partner agency",
         "Correspondence → Outgoing Communications → Reply Letters",
         ["Correspondence", "Correspondence → Outgoing Communications", "Correspondence → Outgoing Communications → Reply Letters", "Administrative"],
         "A reply to an external party is outgoing correspondence. Most specific: Correspondence → Outgoing Communications → Reply Letters."),
    ]

    for doc_desc, correct_level, choices, expl in extra_hierarchy:
        if len(questions) >= 165 + (201 - 1):
            break
        questions.append(make_question(
            qid, "Medium",
            f'What is the most specific classification for: "{doc_desc}"?',
            choices, correct_level, expl,
            ["rule-of-specificity", "hierarchical-classification"]
        ))
        qid += 1

    # --- Type 5: Classification scheme identification (35 questions) ---
    scheme_scenarios = [
        ("A small barangay office where the clerk searches for documents by topic (leave, budget, correspondence)",
         "Subject Classification",
         "Subject classification is best for small offices where users search by topic.",
         ["classification-scheme", "subject"]),
        ("A large agency with separate divisions for HR, finance, procurement, and legal",
         "Functional Classification",
         "Functional classification matches offices organized by division/function.",
         ["classification-scheme", "functional"]),
        ("An audit team tracking thousands of findings by code number for quick reference",
         "Numerical Classification",
         "Numerical classification uses codes for high-volume, code-based tracking.",
         ["classification-scheme", "numerical"]),
        ("An investigation unit that needs file labels to not reveal document content",
         "Numerical Classification",
         "Numerical codes maintain confidentiality — they don't reveal content to unauthorized viewers.",
         ["classification-scheme", "numerical"]),
        ("A general administrative office handling diverse topics from multiple sources",
         "Subject Classification",
         "Subject classification works best when diverse topics come from multiple sources and users think by topic.",
         ["classification-scheme", "subject"]),
        ("A records center where the same subject (e.g., training) appears in HR, finance, and operations files",
         "Functional Classification",
         "When the same subject crosses multiple functions, functional classification prevents confusion.",
         ["classification-scheme", "functional"]),
        ("A municipal office where citizens ask for documents by subject (birth certificates, permits, complaints)",
         "Subject Classification",
         "Subject classification aligns with how citizens naturally search — by topic.",
         ["classification-scheme", "subject"]),
        ("A warehouse managing inventory with codes like INV-001, INV-002 for tracking",
         "Numerical Classification",
         "Numerical codes enable systematic tracking of high-volume items.",
         ["classification-scheme", "numerical"]),
        ("A regional office with separate sections for administration, operations, and finance",
         "Functional Classification",
         "Functional classification mirrors the organizational structure of sectioned offices.",
         ["classification-scheme", "functional"]),
        ("A legal office where cases are assigned docket numbers for court reference",
         "Numerical Classification",
         "Docket numbers are a form of numerical classification for legal case tracking.",
         ["classification-scheme", "numerical"]),
    ]

    # Repeat with variations to reach 35
    for scenario, correct, expl, tags in scheme_scenarios:
        if len(questions) >= 200:
            break
        wrong_schemes = [s[0] for s in SCHEMES if s[0] != correct]
        extra_wrong = "Chronological Classification"
        choices = [correct] + wrong_schemes + [extra_wrong]
        choices = choices[:4]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f"Which classification scheme is most appropriate for this scenario: \"{scenario}\"?",
            choices, correct, expl, tags
        ))
        qid += 1

    # Fill remaining with cross-reference questions
    cross_ref_questions = [
        ("A service contract with a training provider for employee development",
         "Legal", ["Personnel", "Financial"],
         "Primary: Legal (binding agreement). Cross-references: Personnel (employee training) and Financial (payment)."),
        ("A budget allocation for office renovation",
         "Financial", ["Administrative"],
         "Primary: Financial (budget/money). Cross-reference: Administrative (office management)."),
        ("An employee's SALN",
         "Personnel", ["Legal"],
         "Primary: Personnel (part of 201 file). Cross-reference: Legal (required by law)."),
        ("A disciplinary action report against an employee",
         "Personnel", ["Legal"],
         "Primary: Personnel (employee matter). Cross-reference: Legal (may involve formal charges)."),
        ("A purchase order for training materials",
         "Financial", ["Personnel"],
         "Primary: Financial (procurement/payment). Cross-reference: Personnel (training-related)."),
    ]

    for doc_desc, primary, cross_refs, expl in cross_ref_questions:
        if len(questions) >= 200:
            break
        wrong_primary = [c for c in CATEGORY_NAMES if c != primary and c not in cross_refs]
        choices = [primary] + random.sample(wrong_primary, min(3, len(wrong_primary)))
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f'What is the PRIMARY classification for: "{doc_desc}"?',
            choices, primary, expl,
            ["primary-classification", "cross-reference"]
        ))
        qid += 1

    # Fill any remaining spots
    medium_fill_used = set()
    while len(questions) < 200:
        cat = random.choice(CATEGORY_NAMES)
        doc, expl = pick_doc(cat)
        if doc in medium_fill_used:
            continue
        medium_fill_used.add(doc)
        wrong = pick_wrong_categories(cat, 3)
        choices = [cat] + wrong
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Medium",
            f'Under which record class should "{doc}" be primarily classified?',
            choices, cat, expl,
            ["document-classification", "primary-classification"]
        ))
        qid += 1

    return questions[:200]


# ============================================================
# HARD QUESTIONS (IDs 401-600)
# ============================================================

def generate_hard_questions():
    """Generate 200 Hard questions. Multi-step reasoning, traps, mixed scenarios."""
    questions = []
    qid = 401

    # --- Type 1: Directive ABOUT a topic vs document OF that topic (40 questions) ---
    directive_traps = [
        ("Memorandum directing the Accounting Division to prepare the annual budget",
         "Administrative",
         "The memo is a directive (Administrative). The annual budget prepared in response is Financial.",
         "Financial"),
        ("Office Order requiring all employees to update their Personal Data Sheets",
         "Administrative",
         "The office order is a directive (Administrative). The PDS forms submitted are Personnel records.",
         "Personnel"),
        ("Memorandum instructing the Legal Division to draft a new service contract",
         "Administrative",
         "The memo is a directive (Administrative). The contract drafted in response is Legal.",
         "Legal"),
        ("Special Order directing the HR Division to process all pending leave applications",
         "Administrative",
         "The special order is a directive (Administrative). The leave applications themselves are Personnel.",
         "Personnel"),
        ("Office Circular reminding staff about the deadline for SALN submission",
         "Administrative",
         "The circular is an internal communication/directive (Administrative). The SALNs are Personnel records.",
         "Personnel"),
        ("Memorandum to the Finance Division regarding release of performance bonuses",
         "Administrative",
         "The memo is a directive about releasing funds (Administrative). The actual disbursement voucher is Financial.",
         "Financial"),
        ("Office Order creating a committee to investigate a complaint against an employee",
         "Administrative",
         "The office order is a directive (Administrative). The investigation report may be Personnel or Legal.",
         "Personnel"),
        ("Memorandum requiring submission of quarterly financial reports",
         "Administrative",
         "The memo is a directive (Administrative). The financial reports submitted are Financial records.",
         "Financial"),
        ("Special Order designating a lawyer to handle an administrative case",
         "Administrative",
         "The special order is a directive (Administrative). The case documents are Legal records.",
         "Legal"),
        ("Office Circular on the new procurement procedures",
         "Administrative",
         "The circular communicates internal policy (Administrative). Actual procurement documents are Financial.",
         "Financial"),
        ("Memorandum directing all divisions to submit accomplishment reports",
         "Administrative",
         "The memo is a directive (Administrative). The accomplishment reports are Technical/Operational.",
         "Technical/Operational"),
        ("Office Order on the schedule of flag ceremony duties",
         "Administrative",
         "An office order on scheduling is an internal directive — Administrative.",
         "Personnel"),
        ("Memorandum informing staff about changes to the leave policy",
         "Administrative",
         "The memo communicates policy (Administrative). Leave applications under the new policy are Personnel.",
         "Personnel"),
        ("Special Order authorizing the cashier to disburse petty cash",
         "Administrative",
         "The special order is a directive delegating authority (Administrative). Petty cash vouchers are Financial.",
         "Financial"),
        ("Office Circular on the filing of income tax returns",
         "Administrative",
         "The circular is an internal directive (Administrative). The actual tax documents are Financial.",
         "Financial"),
        ("Memorandum to Legal Division to review the draft MOA",
         "Administrative",
         "The memo is a directive (Administrative). The MOA itself is a Legal document.",
         "Legal"),
        ("Office Order on the conduct of mid-year performance review",
         "Administrative",
         "The office order directs an activity (Administrative). The performance reviews are Personnel records.",
         "Personnel"),
        ("Memorandum requiring all divisions to submit budget proposals for next FY",
         "Administrative",
         "The memo is a directive (Administrative). The budget proposals submitted are Financial records.",
         "Financial"),
        ("Special Order assigning staff to attend a court hearing",
         "Administrative",
         "The special order is a directive (Administrative). Court-related documents are Legal.",
         "Legal"),
        ("Office Circular announcing the new records classification system",
         "Administrative",
         "The circular announces internal policy (Administrative). The classification system itself is a tool, not a record class.",
         "Technical/Operational"),
    ]

    for doc_text, correct_cat, expl, trap_cat in directive_traps[:40]:
        # The trap category is what examinees commonly but incorrectly choose
        wrong_cats = [trap_cat]
        remaining = [c for c in CATEGORY_NAMES if c != correct_cat and c != trap_cat]
        wrong_cats += random.sample(remaining, 2)
        choices = [correct_cat] + wrong_cats
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f'Under which major record class should the following document be classified: "{doc_text}"?',
            choices, correct_cat, expl,
            ["directive-vs-content", "trap-question", "decision-flowchart"]
        ))
        qid += 1

    # --- Type 2: Multi-document classification (group all correctly) (35 questions) ---
    multi_doc_sets = []
    for _ in range(35):
        # Pick 4 documents, ask which grouping is correct
        cats_to_use = random.sample(CATEGORY_NAMES, 4)
        docs_picked = []
        for cat in cats_to_use:
            doc, _ = pick_doc(cat)
            docs_picked.append((doc, cat))

        # Ask about one specific document from the set
        target_idx = random.randint(0, 3)
        target_doc, target_cat = docs_picked[target_idx]

        wrong = pick_wrong_categories(target_cat, 3)
        choices = [target_cat] + wrong
        random.shuffle(choices)

        all_docs_str = ", ".join([d[0] for d in docs_picked])
        explanation = f"'{target_doc}' is a {target_cat} record based on its primary purpose."

        multi_doc_sets.append(make_question(
            qid, "Hard",
            f'Given these documents: {all_docs_str}. Under which record class does "{target_doc}" belong?',
            choices, target_cat, explanation,
            ["multi-document", "mixed-classification"]
        ))
        qid += 1

    questions += multi_doc_sets

    # --- Type 3: Cross-reference identification (35 questions) ---
    cross_ref_hard = [
        ("Service Contract between DepEd and ABC Training Corp for employee leadership seminar",
         "Legal",
         "Personnel",
         "Primary: Legal (binding contract). The most relevant cross-reference is Personnel (employee training), not Financial.",
         ["Financial", "Administrative"]),
        ("Budget allocation for the construction of a new records storage facility",
         "Financial",
         "Administrative",
         "Primary: Financial (budget/money). Cross-reference: Administrative (facility management).",
         ["Legal", "Technical/Operational"]),
        ("SALN of a department director under investigation for unexplained wealth",
         "Personnel",
         "Legal",
         "Primary: Personnel (part of 201 file). Cross-reference: Legal (used in investigation).",
         ["Financial", "Administrative"]),
        ("Purchase order for medicines for the agency clinic",
         "Financial",
         "Personnel",
         "Primary: Financial (procurement). Cross-reference: Personnel (employee health benefit).",
         ["Legal", "Administrative"]),
        ("Memorandum of Agreement with GSIS for employee loan program",
         "Legal",
         "Personnel",
         "Primary: Legal (binding agreement). Cross-reference: Personnel (employee benefit).",
         ["Financial", "Administrative"]),
        ("Audit report finding irregularities in employee overtime pay",
         "Financial",
         "Personnel",
         "Primary: Financial (audit of payments). Cross-reference: Personnel (employee compensation).",
         ["Legal", "Administrative"]),
        ("Contract for security services including guard deployment schedule",
         "Legal",
         "Administrative",
         "Primary: Legal (binding contract). Cross-reference: Administrative (office operations).",
         ["Personnel", "Financial"]),
        ("Training budget proposal for the HR Development Plan",
         "Financial",
         "Personnel",
         "Primary: Financial (budget). Cross-reference: Personnel (training/development).",
         ["Administrative", "Legal"]),
        ("Letter from the Ombudsman requesting employee records for investigation",
         "Correspondence",
         "Legal",
         "Primary: Correspondence (external communication). Cross-reference: Legal (investigation) and Personnel.",
         ["Administrative", "Financial"]),
        ("Resolution approving hazard pay for frontline workers",
         "Administrative",
         "Personnel",
         "Primary: Administrative (internal resolution/directive). Cross-reference: Personnel (employee benefit) and Financial.",
         ["Legal", "Technical/Operational"]),
    ]

    for doc_desc, primary, cross_ref, expl, wrong_options in cross_ref_hard:
        if len(questions) >= 110 + (401 - 1):
            break
        # Ask what the cross-reference should be
        choices = [cross_ref] + wrong_options + [primary]
        # Remove primary from choices (it's the primary, not cross-ref)
        choices = [c for c in choices if c != primary]
        # Ensure we have exactly 4 choices
        if len(choices) < 4:
            extra = [c for c in CATEGORY_NAMES if c not in choices and c != primary]
            choices += extra[:4 - len(choices)]
        choices = choices[:4]
        if cross_ref not in choices:
            choices[0] = cross_ref
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f'The document "{doc_desc}" is primarily classified as {primary}. Which category should receive a cross-reference?',
            choices, cross_ref, expl,
            ["cross-reference", "multi-category"]
        ))
        qid += 1

    # Generate more cross-reference questions
    more_cross_refs = [
        ("Employee disciplinary case that resulted in suspension",
         "Personnel", "Legal",
         "Primary: Personnel (employee matter). Cross-reference: Legal (formal disciplinary action).",
         ["Administrative", "Financial"]),
        ("Travel reimbursement claim with attached travel order",
         "Financial", "Administrative",
         "Primary: Financial (reimbursement/payment). Cross-reference: Administrative (travel order).",
         ["Personnel", "Legal"]),
        ("Contract renewal for office space lease",
         "Legal", "Financial",
         "Primary: Legal (binding contract). Cross-reference: Financial (involves rental payments).",
         ["Administrative", "Personnel"]),
        ("Letter from BIR regarding tax deficiency assessment",
         "Correspondence", "Financial",
         "Primary: Correspondence (external communication from BIR). Cross-reference: Financial (tax matter).",
         ["Legal", "Administrative"]),
        ("Board resolution approving salary standardization",
         "Administrative", "Financial",
         "Primary: Administrative (internal governance resolution). Cross-reference: Financial (salary/budget impact).",
         ["Personnel", "Legal"]),
        ("Certification of leave credits for retiring employee",
         "Personnel", "Financial",
         "Primary: Personnel (employee record). Cross-reference: Financial (monetization of leave credits).",
         ["Administrative", "Legal"]),
        ("MOA with a university for internship program",
         "Legal", "Personnel",
         "Primary: Legal (binding agreement). Cross-reference: Personnel (involves staff/interns).",
         ["Financial", "Administrative"]),
        ("Audit observation on non-compliance with procurement law",
         "Financial", "Legal",
         "Primary: Financial (procurement audit). Cross-reference: Legal (law compliance issue).",
         ["Administrative", "Personnel"]),
        ("Request from court for certified copies of employee records",
         "Correspondence", "Legal",
         "Primary: Correspondence (external request). Cross-reference: Legal (court proceeding) and Personnel.",
         ["Administrative", "Financial"]),
        ("Budget for construction of evacuation center",
         "Financial", "Technical/Operational",
         "Primary: Financial (budget allocation). Cross-reference: Technical/Operational (project implementation).",
         ["Administrative", "Legal"]),
    ]

    for doc_desc, primary, cross_ref, expl, wrong_options in more_cross_refs:
        if len(questions) >= 120 + (401 - 1):
            break
        choices = [cross_ref] + wrong_options
        if len(choices) < 4:
            extra = [c for c in CATEGORY_NAMES if c not in choices and c != primary]
            choices += extra[:4 - len(choices)]
        choices = choices[:4]
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f'The document "{doc_desc}" is primarily classified as {primary}. Which category should receive a cross-reference?',
            choices, cross_ref, expl,
            ["cross-reference", "multi-category"]
        ))
        qid += 1

    # --- Type 4: Scenario-based - "What should the clerk do?" (30 questions) ---
    scenario_questions = [
        ("A clerk receives a memorandum about budget cuts. The memo is from the Director to all division chiefs. Where should it be classified?",
         "Administrative",
         "The memo is an internal directive from the Director — Administrative. The budget documents it references are Financial.",
         ["scenario", "directive-vs-content"]),
        ("A citizen submits a complaint letter about a government employee. The clerk must classify this document. What is the primary classification?",
         "Correspondence",
         "A letter from an external party (citizen) is incoming correspondence. Cross-reference: Personnel (about an employee).",
         ["scenario", "correspondence"]),
        ("The office receives a court subpoena requiring production of financial records. How should the subpoena itself be classified?",
         "Legal",
         "A subpoena is a legal order — Legal. The financial records it requests are separately classified as Financial.",
         ["scenario", "legal"]),
        ("An employee submits both a leave application and a medical certificate. Should they be classified together or separately?",
         "They should be filed together under Personnel → Leave Records",
         "Supporting documents (medical certificate) are filed with the primary document (leave application) in the same classification.",
         ["scenario", "supporting-documents"]),
        ("A document titled 'Annual Report on Gender and Development Activities' arrives. Is this Administrative or Technical/Operational?",
         "Technical/Operational",
         "A report on program implementation (GAD activities) is Technical/Operational — it documents core function delivery.",
         ["scenario", "technical-vs-administrative"]),
        ("The Finance Division sends a memo to HR requesting employee data for payroll processing. Where does HR classify this memo?",
         "Correspondence",
         "An internal memo from another division requesting information is treated as internal correspondence by the receiving office.",
         ["scenario", "internal-correspondence"]),
        ("A clerk finds a document that could be either Personnel or Legal. The document is a formal charge sheet against an employee. What is the primary classification?",
         "Legal",
         "A formal charge sheet initiates legal/quasi-judicial proceedings — Legal. Cross-reference: Personnel.",
         ["scenario", "legal-vs-personnel"]),
        ("An office receives an invitation from a private company to attend a product demonstration. Classification?",
         "Correspondence",
         "An invitation from an external party is incoming correspondence — Correspondence.",
         ["scenario", "correspondence"]),
        ("A clerk must classify a 'Certificate of Availability of Funds' that was issued to support a purchase order. Primary classification?",
         "Financial",
         "A certificate of fund availability is a financial certification supporting procurement — Financial.",
         ["scenario", "financial"]),
        ("The office has a document titled 'Implementing Rules and Regulations of RA 11032.' Is this Legal or Administrative?",
         "Legal",
         "Implementing rules of a law are legal instruments — Legal. They have the force of law.",
         ["scenario", "legal-vs-administrative"]),
    ]

    # More scenario questions
    scenario_questions += [
        ("A travel order is issued, then a travel reimbursement is filed after the trip. Are they classified the same?",
         "No — Travel Order is Administrative; Travel Reimbursement is Financial",
         "The travel order authorizes travel (Administrative directive). The reimbursement requests payment (Financial).",
         ["scenario", "related-documents-different-class"]),
        ("An employee's appointment paper and the board resolution approving it arrive together. Same classification?",
         "No — Appointment Paper is Personnel; Board Resolution is Administrative",
         "The appointment paper is an employee record (Personnel). The resolution is a governance action (Administrative).",
         ["scenario", "related-documents-different-class"]),
        ("A clerk receives a notarized affidavit from an employee denying misconduct charges. Classification?",
         "Legal",
         "A notarized affidavit is a sworn legal document — Legal. Cross-reference: Personnel (employee matter).",
         ["scenario", "legal"]),
        ("The office receives an audit observation memorandum from COA. Is this Financial or Correspondence?",
         "Correspondence",
         "A document received from an external agency (COA) is incoming correspondence. Cross-reference: Financial (audit findings).",
         ["scenario", "correspondence-vs-financial"]),
        ("A 'Notice of Disallowance' from COA regarding irregular disbursements. Classification?",
         "Financial",
         "A notice of disallowance directly concerns financial transactions — Financial. If received as a letter, the transmittal is Correspondence.",
         ["scenario", "financial"]),
    ]

    for scenario_text, correct, expl, tags in scenario_questions[:30]:
        if len(questions) >= 150 + (401 - 1):
            break

        # For yes/no type answers, create appropriate choices
        if correct.startswith("No —") or correct.startswith("They should"):
            choices = [
                correct,
                "Yes — both are Administrative records",
                "Yes — both are Personnel records",
                "Yes — both are Financial records",
            ]
        else:
            wrong = pick_wrong_categories(correct, 3)
            choices = [correct] + wrong

        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            scenario_text,
            choices, correct, expl, tags
        ))
        qid += 1

    # --- Type 5: Numerical code hierarchy questions (25 questions) ---
    code_hierarchy_qs = [
        ("If code 200 represents 'Financial Records' and 220 represents 'Disbursements', what would code 221 most likely represent?",
         "Salary Vouchers",
         ["Salary Vouchers", "Annual Budget", "Collection Reports", "Office Orders"],
         "In numerical classification, 221 is a specific type under 220 (Disbursements). Salary vouchers are a disbursement type."),
        ("If code 120 represents 'Personnel Records' and 122 represents 'Leave Records', what level is code 120?",
         "Subclass level",
         ["Subclass level", "Main class level", "Specific topic level", "Document number"],
         "Code 120 is a two-digit subclass under main class 100. Three-digit codes (122) are specific topics."),
        ("In a numerical scheme where 100=Administrative, 200=Financial, 300=Legal, what code range would Personnel records likely use?",
         "400 series",
         ["400 series", "100 series", "200 series", "Any available number"],
         "Each main class gets its own hundred series. If 100-300 are taken, Personnel would logically be 400."),
        ("Code 311 represents 'Service Contracts' under 310 'Contracts and Agreements' under 300 'Legal Records'. How many hierarchical levels does this represent?",
         "Three levels (main class → subclass → specific topic)",
         ["Three levels (main class → subclass → specific topic)", "Two levels", "Four levels", "One level"],
         "300 is main class, 310 is subclass, 311 is specific topic — three hierarchical levels."),
        ("A document is assigned code 222. In the standard scheme, this means:",
         "Financial → Disbursements → Travel Reimbursements",
         ["Financial → Disbursements → Travel Reimbursements", "Personnel → Leave → Sick Leave", "Administrative → Correspondence → Outgoing", "Legal → Cases → Administrative Cases"],
         "Code 222 = 200 (Financial) → 220 (Disbursements) → 222 (Travel Reimbursements)."),
        ("What is the advantage of numerical classification over subject classification for confidential records?",
         "Numeric codes do not reveal document content to unauthorized viewers",
         ["Numeric codes do not reveal document content to unauthorized viewers", "Numbers are easier to remember than words", "Numerical systems are always faster", "Numbers prevent misfiling"],
         "A code like '321' reveals nothing about content, while a label like 'Administrative Cases' does."),
        ("If a new subcategory 'Maternity Leave' needs to be added under 'Leave Records' (code 122), what code should it receive?",
         "A new code like 123 or 122.1",
         ["A new code like 123 or 122.1", "Code 122 (same as Leave Records)", "Code 200", "Code 100"],
         "New specific topics get the next available number in the sequence under their parent subclass."),
        ("Code 410 represents 'Incoming Communications.' A letter from a citizen would be coded as:",
         "411",
         ["411", "410", "420", "400"],
         "411 is the specific code for 'Letters from Citizens' under 410 (Incoming Communications)."),
    ]

    for q_text, correct, choices, expl in code_hierarchy_qs[:25]:
        if len(questions) >= 175 + (401 - 1):
            break
        random.shuffle(choices)
        # Ensure correct answer is in choices
        if correct not in choices:
            choices[0] = correct
            random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            q_text,
            choices, correct, expl,
            ["numerical-classification", "hierarchy-reasoning"]
        ))
        qid += 1

    # --- Type 6: Complex odd-one-out with subtle differences (25+ questions) ---
    subtle_odd_out = [
        (["Office Memorandum", "Office Order", "Office Circular", "Memorandum of Agreement"],
         "Memorandum of Agreement",
         "A MOA is a Legal document (binding agreement). The others are all Administrative (internal directives/communications)."),
        (["Disbursement Voucher", "Purchase Order", "Travel Order", "Obligation Request"],
         "Travel Order",
         "A Travel Order is Administrative (authorizes travel). The others are all Financial (involve money/procurement)."),
        (["Leave Application", "Performance Evaluation", "Payroll", "Service Record"],
         "Payroll",
         "Payroll is Financial (salary payment). The others are all Personnel (employee records)."),
        (["Service Contract", "MOA", "Legal Opinion", "Office Order"],
         "Office Order",
         "An Office Order is Administrative (internal directive). The others are all Legal documents."),
        (["Incoming Letter", "Endorsement Letter", "Transmittal Letter", "Office Memorandum"],
         "Office Memorandum",
         "An Office Memorandum is Administrative (internal). The others are all Correspondence (external communications or routing)."),
        (["Annual Budget Proposal", "Quarterly Financial Report", "Annual Report", "Statement of Allotments"],
         "Annual Report",
         "An Annual Report is Administrative (summarizes operations). The others are all Financial records."),
        (["Appointment Paper", "Certificate of Employment", "Certificate of Availability of Funds", "Leave Card"],
         "Certificate of Availability of Funds",
         "Certificate of Availability of Funds is Financial. The others are all Personnel records."),
        (["Minutes of Meeting", "Organizational Chart", "Travel Order", "Subpoena"],
         "Subpoena",
         "A Subpoena is Legal (court order). The others are all Administrative records."),
        (["Project Completion Report", "Monitoring Report", "Field Inspection Report", "Audit Observation Memorandum"],
         "Audit Observation Memorandum",
         "An Audit Observation Memorandum is Financial (audit finding). The others are Technical/Operational (program delivery)."),
        (["Complaint Letter from Public", "Reply Letter to Client", "Invitation to Conference", "Office Circular"],
         "Office Circular",
         "An Office Circular is Administrative (internal policy). The others are all Correspondence (external communications)."),
        (["Deed of Donation", "Affidavit", "Non-Disclosure Agreement", "Disbursement Voucher"],
         "Disbursement Voucher",
         "A Disbursement Voucher is Financial. The others are all Legal documents."),
        (["CS Form 212", "SALN", "Daily Time Record", "Purchase Order"],
         "Purchase Order",
         "A Purchase Order is Financial (procurement). The others are all Personnel records."),
        (["Collection Report", "Bank Reconciliation", "Tax Remittance Report", "Endorsement Letter"],
         "Endorsement Letter",
         "An Endorsement Letter is Correspondence. The others are all Financial records."),
        (["Research Study Report", "Engineering Design Plan", "Laboratory Test Results", "Office Memorandum"],
         "Office Memorandum",
         "An Office Memorandum is Administrative. The others are all Technical/Operational records."),
        (["Lease Contract", "Power of Attorney", "Cease and Desist Order", "Special Order"],
         "Special Order",
         "A Special Order is Administrative (internal directive). The others are all Legal documents."),
    ]

    hard_odd_phrasings = [
        "Which of the following does NOT belong in the same record class as the others?",
        "One of these documents is classified under a different major record class. Identify it.",
        "Which document below does NOT share the same classification as the rest?",
        "Three of these belong to the same record class. Which is the outlier?",
        "Identify the document that breaks the classification pattern of the group.",
    ]
    hard_odd_counter = 0
    for choices_list, correct, expl in subtle_odd_out:
        if len(questions) >= 200:
            break
        choices = choices_list[:]
        random.shuffle(choices)

        choices_str = "; ".join(choices)
        phrasing = hard_odd_phrasings[hard_odd_counter % len(hard_odd_phrasings)]
        hard_odd_counter += 1

        questions.append(make_question(
            qid, "Hard",
            f"{phrasing} Documents: {choices_str}",
            choices, correct, expl,
            ["odd-one-out", "subtle-differences", "trap-question"]
        ))
        qid += 1

    # Fill remaining with more complex scenarios
    hard_fill_used = set()
    while len(questions) < 200:
        # Generate "what is the correct classification sequence" questions
        cat = random.choice(CATEGORY_NAMES)
        doc, expl = pick_doc(cat)
        employee = random.choice(EMPLOYEE_NAMES)
        agency = random.choice(AGENCIES)

        # Ensure unique question text
        key = (doc, agency, employee)
        if key in hard_fill_used:
            continue
        hard_fill_used.add(key)

        wrong = pick_wrong_categories(cat, 3)
        choices = [cat] + wrong
        random.shuffle(choices)

        questions.append(make_question(
            qid, "Hard",
            f'A document titled "{doc}" is found in the incoming mail of {agency}. '
            f'The document pertains to {employee}. What is its primary classification?',
            choices, cat,
            f"Regardless of context, '{doc}' is classified by its content/purpose: {expl}",
            ["context-independence", "primary-classification"]
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

    all_questions = easy + medium + hard

    # Reassign IDs sequentially
    for i, q in enumerate(all_questions, start=1):
        q["id"] = i

    # Verify counts
    easy_count = sum(1 for q in all_questions if q["difficulty"] == "Easy")
    medium_count = sum(1 for q in all_questions if q["difficulty"] == "Medium")
    hard_count = sum(1 for q in all_questions if q["difficulty"] == "Hard")

    print(f"Generated {len(all_questions)} questions total:")
    print(f"  Easy: {easy_count}")
    print(f"  Medium: {medium_count}")
    print(f"  Hard: {hard_count}")

    # Write output
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data", "seed", "questions", "clerical-ability",
        "indexing-and-record-organization", "record-classification"
    )
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "questions.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, indent=2, ensure_ascii=False)

    print(f"Written to: {output_path}")


if __name__ == "__main__":
    main()
