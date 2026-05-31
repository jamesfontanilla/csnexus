"""Generate 600-question bank for Record Retrieval.
200 Easy (IDs 1-200), 200 Medium (IDs 201-400), 200 Hard (IDs 401-600).
"""
import json
import random
import os

random.seed(42)

NAMES = [
    "Maria Santos", "Juan Reyes", "Ana Cruz", "Pedro Garcia", "Rosa Mendoza",
    "Carlos Rivera", "Elena Bautista", "Roberto Flores", "Carmen Gonzales",
    "Fernando Torres", "Patricia Ramos", "Luis Morales", "Gloria Navarro",
    "Ricardo Perez", "Teresa Castillo", "Eduardo Hernandez", "Cristina Lopez",
    "Miguel Romero", "Dolores Salazar", "Alfredo Villanueva",
    "Josefina Aquino", "Manuel Dela Cruz", "Lourdes Tan", "Antonio Lim",
    "Beatriz Ocampo", "Rodrigo Pascual", "Imelda Soriano", "Gregorio Valdez",
    "Consuelo Aguilar", "Ernesto Dizon", "Margarita Enriquez", "Danilo Francisco",
]
DIVS = ["HR Division", "Finance Division", "Records Section", "Legal Division",
        "Administrative Division", "Planning Division", "Accounting Section",
        "Procurement Unit", "General Services", "IT Division"]
DOCS = ["201 file", "leave application", "disbursement voucher", "appointment paper",
        "performance evaluation", "travel order", "office memorandum", "service contract",
        "payroll record", "CS Form 212", "SALN", "certificate of employment",
        "purchase order", "annual budget proposal", "minutes of meeting", "office order",
        "training certificate", "audit report", "leave card", "service record"]
AGENCIES = ["CSC", "COA", "DILG", "DBM", "DENR", "DOH", "DepEd", "DOLE", "DPWH", "DOT"]
REGIONS = [("NCR", ["Manila", "Quezon City", "Makati", "Taguig", "Pasig"]),
           ("Region III", ["San Fernando", "Angeles", "Olongapo", "Malolos"]),
           ("Region IV-A", ["Antipolo", "Calamba", "Batangas City", "Lucena"]),
           ("Region VII", ["Cebu City", "Mandaue", "Lapu-Lapu", "Talisay"]),
           ("Region XI", ["Davao City", "Tagum", "Panabo", "Digos"]),
           ("CAR", ["Baguio", "La Trinidad", "Tabuk", "Bontoc"])]
SUBJECTS = [("Employee Training", "Personnel Development > Capacity Building > Training Programs"),
            ("Office Supplies", "Administrative Services > Procurement > Supplies and Materials"),
            ("Budget Proposals", "Financial Records > Planning > Annual Budget"),
            ("Leave Applications", "Personnel Records > Benefits > Leave Management"),
            ("Audit Findings", "Oversight > Audit > Observation Memoranda"),
            ("Travel Expenses", "Financial Records > Disbursements > Travel Reimbursements"),
            ("Hiring Documents", "Personnel Records > Recruitment > Appointments"),
            ("Building Maintenance", "Administrative Services > General Services > Facilities"),
            ("Legal Opinions", "Legal Records > Advisory > Opinions and Interpretations"),
            ("Citizen Complaints", "Correspondence > Incoming > Public Grievances")]
SYSTEMS = {"Alphabetic": ("Direct", "Name (surname as key unit)", False),
           "Numeric": ("Indirect", "Alphabetic index lookup", True),
           "Subject": ("Indirect", "Relative index lookup", True),
           "Geographic": ("Direct", "Location (region/city)", False)}
OCAC = [("OUT guide", "Check if the file has been charged out to another user"),
        ("Cross-references", "Check if filed under an alternative name or heading"),
        ("Adjacent files", "Check files immediately before and after the expected position"),
        ("Catch-all tray", "Check the to-be-filed tray or pending area")]
STEPS5 = ["Receive the request", "Determine the search path",
          "Locate and extract", "Charge-out", "Follow-up and return"]
CHARGEOUT = [("OUT guide", "A card placed in the file position to show it is borrowed"),
             ("Charge-out register", "A logbook recording all borrowed files with borrower details"),
             ("Requisition slip", "A written request from the borrower authorizing file removal"),
             ("Follow-up tickler", "A date-organized reminder system for tracking overdue files")]
MISFILES = [("Transposition", "Two adjacent files were swapped"),
            ("Wrong unit", "Filed by given name instead of surname"),
            ("Wrong level", "Filed in parent category instead of subcategory"),
            ("Variant spelling", "Filed under alternate spelling"),
            ("Wrong section", "Filed in the wrong major division")]


def make_q(qid, diff, question, choices, answer, explanation, tags):
    return {"id": qid, "subtest": "Clerical Ability",
            "module": "Indexing and Record Organization", "subtopic": "Record Retrieval",
            "difficulty": diff, "question": question, "choices": choices,
            "answer": answer, "explanation": explanation, "tags": tags,
            "category": ["Sub-Professional"], "language": "English"}

def shuf(items, correct):
    result = list(items)
    if correct not in result:
        result.append(correct)
    random.shuffle(result)
    # Ensure correct answer is always in the final 4
    if correct not in result[:4]:
        result[random.randint(0, 3)] = correct
    return result[:4]

def rn(): return random.choice(NAMES)
def rs(): return rn().split()[-1]
def rd(): return random.choice(DIVS)
def rdc(): return random.choice(DOCS)
def ra(): return random.choice(AGENCIES)
def rrg():
    r, cs = random.choice(REGIONS)
    return r, random.choice(cs)
def rsub(): return random.choice(SUBJECTS)
def rsys(): return random.choice(list(SYSTEMS.keys()))


def gen_easy():
    qs = []
    D = [
        ("What is record retrieval?", "Locating and extracting a document from a filing system",
         ["Filing documents", "Creating index cards", "Destroying records"]),
        ("What is direct retrieval?", "Going straight to the file without consulting an index",
         ["Consulting an index first", "Searching sequentially", "Asking a colleague"]),
        ("What is indirect retrieval?", "Consulting an index first to find the location",
         ["Going directly without lookup", "Searching randomly", "Filing a new document"]),
        ("What is an OUT guide?", "A card placed where a borrowed file was to show who has it",
         ["A building exit guide", "A cabinet label", "A destruction form"]),
        ("What is a charge-out system?", "A system tracking who borrowed files and when due back",
         ["A fee-charging system", "A classification method", "A supply system"]),
        ("What is a relative index?", "A master list mapping common terms to official subject headings",
         ["A list of relatives", "A date-based index", "A temporary index"]),
        ("What is a cross-reference?", "A pointer redirecting from an alternative name to the primary location",
         ["A copy in multiple folders", "A tracking number", "A review stamp"]),
        ("What is the 3-Minute Rule?", "Any record should be retrievable within 3 minutes",
         ["Files must return in 3 min", "File in 3 min", "Index updates every 3 min"]),
        ("What is a follow-up tickler?", "A date-organized reminder for tracking overdue files",
         ["A new-file organizer", "A citizen letter", "An employee checklist"]),
        ("What is a charge-out register?", "A logbook recording all borrowed files with dates",
         ["A cash register", "A list of filers", "A document register"]),
        ("How many steps in the retrieval procedure?", "Five",
         ["Three", "Four", "Seven"]),
        ("First step in retrieval?", "Receive the request",
         ["Search the cabinet", "Place an OUT guide", "Consult the index"]),
        ("Last step in retrieval?", "Follow-up and return",
         ["Charge-out", "Locate and extract", "Determine search path"]),
        ("Before releasing a file, you must:", "Record the borrowing and place an OUT guide",
         ["Photocopy every page", "Get supervisor signature", "Stamp every page"]),
        ("When a file is returned:", "Remove OUT guide and refile correctly",
         ["Place on top of cabinet", "Assign new number", "Send to archives"]),
        ("Retrieval failure usually indicates:", "An error in indexing, classification, or filing",
         ["Cabinet is broken", "Clerk is slow", "Document never created"]),
        ("Purpose of file guides?", "Mark sections and speed navigation",
         ["Prevent files falling", "Lock cabinet", "Mark for destruction"]),
        ("What is a requisition slip?", "A written request authorizing file removal",
         ["A position marker", "A supply receipt", "A cabinet form"]),
        ("Retrieval answers which question?", "Where IS this document now?",
         ["What category?", "How to label?", "When created?"]),
        ("Relationship between retrieval and filing?", "Retrieval is the reverse of filing",
         ["Same process", "Retrieval before filing", "Filing more important"]),
        ("Which systems use DIRECT retrieval?", "Alphabetic and Geographic",
         ["Numeric and Subject", "Alphabetic and Numeric", "Subject and Geographic"]),
        ("Which systems use INDIRECT retrieval?", "Numeric and Subject",
         ["Alphabetic and Geographic", "Alphabetic and Numeric", "Geographic and Subject"]),
        ("Numeric system requires which index?", "Alphabetic index",
         ["Relative index", "Geographic index", "No index"]),
        ("Subject system requires which index?", "Relative index",
         ["Alphabetic index", "Numeric index", "No index"]),
        ("No file leaves without:", "An OUT guide in its position",
         ["A photocopy first", "Verbal approval", "Red ink stamp"]),
        ("What triggers follow-up action?", "File exceeds its return date",
         ["New file added", "Cabinet full", "Clerk on leave"]),
        ("Typical max loan period?", "3-5 working days",
         ["1 hour", "30 days", "Indefinite"]),
        ("If needed file is charged out?", "Contact borrower for return or photocopy",
         ["Report as lost", "Create new file", "Wait indefinitely"]),
        ("OUT guide must contain:", "Document description, borrower name, date, due date",
         ["Only title", "Only borrower name", "Only date"]),
        ("Report file missing only after:", "Checking OUT guide, cross-refs, adjacent files, and catch-all tray",
         ["Immediately", "After OUT guide only", "Never"]),
    ]
    for i, (q, a, w) in enumerate(D):
        qs.append(make_q(i+1, "Easy", q, shuf([a]+w, a), a, a+".", ["definition","concept"]))

    qid = len(D) + 1
    # Access type questions (40) - use index to ensure unique questions
    syskeys = list(SYSTEMS.keys())
    for i in range(40):
        sys = syskeys[i % 4]
        acc, entry, needs = SYSTEMS[sys]
        v = (i // 4) % 3
        name = NAMES[i % len(NAMES)]; doc = DOCS[i % len(DOCS)]
        if v == 0:
            q = f"A clerk needs to retrieve {name}'s {doc}. The {sys} system uses which access type?"
            a = acc
            choices = shuf(["Direct", "Indirect", "Sequential", "Random"], a)
            expl = f"{sys} uses {acc.lower()} access."
        elif v == 1:
            q = f"To find {name}'s {doc} in a {sys} system, the entry point is:"
            a = entry
            wrong = [v2[1] for k, v2 in SYSTEMS.items() if k != sys]
            choices = shuf([a] + wrong, a)
            expl = f"{sys} entry point: {entry}."
        else:
            if needs:
                idx = "alphabetic index" if sys == "Numeric" else "relative index"
                q = f"Before retrieving {name}'s {doc} from a {sys} system, consult:"
                a = f"The {idx}"
                choices = shuf([a, "Nothing - go directly", "Geographic guide", "Charge-out register"], a)
            else:
                q = f"Retrieving {name}'s {doc} from a {sys} system requires an index?"
                a = "No - go directly to the location"
                choices = shuf([a, "Yes - alphabetic index", "Yes - relative index", "Yes - numeric index"], a)
            expl = f"{sys} uses {acc.lower()} retrieval."
        qs.append(make_q(qid, "Easy", q, choices, a, expl, ["access-type", sys.lower()]))
        qid += 1

    # OCAC questions (30) - unique by incorporating names/docs
    pos = ["first", "second", "third", "fourth"]
    for rep in range(30):
        i = rep % 4
        step, desc = OCAC[i]
        others = [s[0] for s in OCAC if s[0] != step]
        name = NAMES[rep % len(NAMES)]; doc = DOCS[rep % len(DOCS)]
        if rep < 16:
            q = f"Searching for {name}'s {doc}, file not found. The {pos[i]} OCAC check is:"
            a = step
            choices = shuf([a] + others + ["Report lost"], a)
            expl = f"OCAC step {i+1}: {step}."
        else:
            q = f"While looking for {name}'s {doc}, OCAC step '{step}' means:"
            a = desc
            wrong = [s[1] for s in OCAC if s[0] != step]
            choices = shuf([a] + wrong + ["Reorganize cabinet"], a)
            expl = f"'{step}' means: {desc}."
        qs.append(make_q(qid, "Easy", q, choices, a, expl, ["not-found", "ocac"]))
        qid += 1

    # Procedure steps (30) - unique by incorporating names/docs
    for rep in range(30):
        i = rep % 5
        step = STEPS5[i]
        others = [s for s in STEPS5 if s != step]
        pw = ["first", "second", "third", "fourth", "fifth"][i]
        name = NAMES[(rep+10) % len(NAMES)]; doc = DOCS[(rep+5) % len(DOCS)]
        if rep < 10:
            q = f"When retrieving {name}'s {doc}, the {pw} step is:"
            a = step
            choices = shuf([a] + random.sample(others, 3), a)
            expl = f"Step {i+1}: {step}."
        elif rep < 20 and i < 4:
            nxt = STEPS5[i+1]
            q = f"After '{step}' when retrieving {name}'s {doc}, next is:"
            a = nxt
            choices = shuf([a] + random.sample([s for s in others if s != nxt], 3), a)
            expl = f"After '{step}' comes '{nxt}'."
        else:
            if i > 0:
                prev = STEPS5[i-1]
                q = f"Before '{step}' when retrieving {name}'s {doc}, the prior step is:"
                a = prev
                choices = shuf([a] + random.sample([s for s in others if s != prev], 3), a)
                expl = f"Before '{step}' comes '{prev}'."
            else:
                q = f"When retrieving {name}'s {doc}, '{step}' is step number:"
                a = "First step"
                choices = shuf([a, "Second", "Third", "Fifth"], a)
                expl = f"'{step}' is step 1."
        qs.append(make_q(qid, "Easy", q, choices, a, expl, ["retrieval-procedure"]))
        qid += 1

    # Retrieval path (70)
    for _ in range(70):
        name = rn(); surname = name.split()[-1]; doc = rdc(); sys = rsys()
        acc, entry, needs = SYSTEMS[sys]
        if sys == "Alphabetic":
            a = f"Go directly to '{surname[0]}' section, find '{surname}' alphabetically"
            wrong = ["Consult alphabetic index for number", "Consult relative index", "Go to geographic section"]
        elif sys == "Numeric":
            a = "Look up name in alphabetic index to get file number, then go to that position"
            wrong = [f"Go to '{surname[0]}' section directly", "Search from 001 sequentially", "Consult relative index"]
        elif sys == "Subject":
            a = "Consult relative index for official subject heading, then go to that section"
            wrong = ["Go directly to guessed folder", "Consult alphabetic index for number", "Search every folder"]
        else:
            region, city = rrg()
            a = f"Go to {region} section, find {city} within it"
            wrong = [f"Go to '{city[0]}' alphabetically", "Consult numeric index", "Consult relative index"]
        q = f"Retrieve the {doc} of {name} from a {sys} system. Correct path?"
        choices = shuf([a] + wrong, a)
        qs.append(make_q(qid, "Easy", q, choices, a, f"{sys}: {acc.lower()} retrieval via {entry.lower()}.",
                         ["retrieval-path", sys.lower()]))
        qid += 1

    return qs[:200]


def gen_medium():
    qs = []; qid = 201
    # Scenario retrieval paths (60)
    for _ in range(60):
        name=rn(); surname=name.split()[-1]; doc=rdc(); div=rd(); sys=rsys()
        acc,entry,needs=SYSTEMS[sys]
        if sys=="Alphabetic":
            q=f"Clerk in {div} needs {doc} of {name}. Alphabetic system. First action?"
            a=f"Go to '{surname[0]}' section directly"
            wrong=["Consult alphabetic index","Check charge-out register","Consult relative index"]
            expl=f"Alphabetic=direct. Go to '{surname[0]}' section."
        elif sys=="Numeric":
            q=f"Supervisor needs {doc} of {name}. Numeric system, number unknown. First action?"
            a="Consult alphabetic index for the file number"
            wrong=["Search from 001","Go to surname letter","Ask supervisor for number"]
            expl="Numeric=indirect. Must look up name in alphabetic index first."
        elif sys=="Subject":
            term,heading=rsub()
            q=f"Need docs about '{term}'. Subject system, no folder with that label. Action?"
            a="Consult relative index for official heading"
            wrong=["Create new folder","Report as missing","Search every folder"]
            expl=f"Subject=indirect. Relative index maps '{term}' to official heading."
        else:
            region,city=rrg()
            q=f"Need records for {city}, {region}. Geographic system. Sequence?"
            a=f"Go to {region} section, then find {city}"
            wrong=[f"Go to '{city[0]}' alphabetically","Consult numeric index","Search by office name"]
            expl=f"Geographic=direct. {region} > {city} > alphabetical."
        qs.append(make_q(qid,"Medium",q,shuf([a]+wrong,a),a,expl,["retrieval-path","scenario",sys.lower()]))
        qid+=1
    # Charge-out scenarios (40)
    months=["January","February","March","April","May","June"]
    for _ in range(40):
        borrower=rn(); bdiv=rd(); target=rn(); doc=rdc()
        due=random.randint(5,25); overdue=random.randint(0,10); today=due+overdue
        month=random.choice(months)
        if overdue==0:
            q=f"Need {doc} of {target}. OUT guide: '{borrower}, {bdiv}, due {month} {due}.' Today is {month} {due}. Status?"
            a="Charged out, due back today - not overdue"
            wrong=["Overdue","Lost","Never borrowed"]
        elif overdue<=3:
            q=f"OUT guide: '{borrower}, {bdiv}, due {month} {due}.' Today {month} {today}. Action?"
            a=f"Contact {borrower} in {bdiv} - file is {overdue} day(s) overdue"
            wrong=["Report as lost","Create new file","Wait indefinitely"]
        else:
            q=f"File charged to {borrower}, {bdiv}, {overdue} days overdue. Action?"
            a="Send formal follow-up notice and request immediate return"
            wrong=["Report as lost","Ignore it","Remove OUT guide"]
        expl=f"{'Not overdue yet.' if overdue==0 else f'File is {overdue} day(s) overdue. Contact borrower.'}"
        qs.append(make_q(qid,"Medium",q,shuf([a]+wrong,a),a,expl,["charge-out","scenario"]))
        qid+=1
    # Not-found troubleshooting (35)
    for rep in range(35):
        name=rn(); doc=rdc(); i=rep%5
        if i==0:
            q=f"Search for {doc} of {name}, find card with borrower info in its place. What happened?"
            a="File is charged out - the card is an OUT guide"
            wrong=["Permanently removed","Misfiled","Destroyed"]
        elif i==1:
            q=f"Searching for {name}'s file, find card saying 'See: [other location]'. Meaning?"
            a="File is at a different location - follow the cross-reference"
            wrong=["File destroyed","Never created","System reorganized"]
        elif i==2:
            q=f"{doc} of {name} not at expected position. No OUT guide, no cross-ref. Next?"
            a="Check files immediately before and after for misfiling"
            wrong=["Report as lost","Reorganize cabinet","Create replacement"]
        elif i==3:
            q=f"After OUT guide, cross-refs, adjacent files all negative. Last check before reporting missing?"
            a="The to-be-filed tray or pending area"
            wrong=["Supervisor's desk","Recycling bin","Other building"]
        else:
            mf=random.choice(MISFILES)
            q=f"File of {name} found because: {mf[1].lower()}. Error type?"
            a=mf[0]
            wrong=[m[0] for m in MISFILES if m[0]!=mf[0]][:3]
        expl=a+"."
        qs.append(make_q(qid,"Medium",q,shuf([a]+wrong,a),a,expl,["not-found","scenario"]))
        qid+=1
    # Efficiency (30)
    E=[("PRIMARY factor for retrieval speed?","Knowledge of filing system rules",
        ["Physical fitness","Cabinet size","Folder color"]),
       ("Retrieval over 3 min consistently indicates?","System needs reorganization",
        ["Replace clerk","More cabinets","Documents too old"]),
       ("FASTEST retrieval for finding by name?","Direct retrieval in alphabetic system",
        ["Indirect in numeric","Sequential scanning","Random searching"]),
       ("Numeric: fast refile but slow retrieval because?","Numbers need index lookup for retrieval",
        ["Numbers hard to read","Cabinets larger","Numbers change often"]),
       ("Well-maintained system means?","Current indexes, consistent filing, proper guides, charge-out discipline",
        ["Expensive cabinets","Many clerks","Date-only filing"]),
       ("Clerk searches randomly. Problem?","Does not understand the retrieval path",
        ["Cabinet too full","Docs too old","Random is fastest"]),
       ("Which does NOT affect retrieval speed?","Color of file folders",
        ["Index currency","Filing accuracy","Charge-out discipline"]),
       ("File guides improve speed because?","Let clerks jump to sections instead of scanning from start",
        ["Look organized","Prevent falling","Required by law"]),
       ("Alphabetic advantage over numeric for name retrieval?","Direct access - no index step needed",
        ["Smaller cabinets","More confidential","Less paper"]),
       ("When reorganize filing system?","When retrieval consistently exceeds 3-minute benchmark",
        ["Every month","Only when ordered","Never"])]
    for q,a,w in E:
        qs.append(make_q(qid,"Medium",q,shuf([a]+w,a),a,a+".",["efficiency"]))
        qid+=1
    for _ in range(20):
        sys=rsys(); acc,entry,_=SYSTEMS[sys]
        if random.random()<0.5:
            q=f"In {sys} system, what determines retrieval speed?"
            a=f"Knowing the {entry.lower()} and following correct path"
            wrong=["Cabinet size","Number of clerks","Document age"]
        else:
            q=f"New clerk slow at {sys} retrieval. Most likely cause?"
            a=f"Does not understand {sys} retrieval path"
            wrong=["Physically slow","Cabinet too far","Documents heavy"]
        qs.append(make_q(qid,"Medium",q,shuf([a]+wrong,a),a,a+".",["efficiency",sys.lower()]))
        qid+=1
    # Authorization (35)
    A=[("Which records need WRITTEN authorization?","Personnel records (201 files)",
        ["General admin records","Office circulars","Meeting schedules"]),
       ("Who can retrieve a 201 file?","HR staff, the employee, and authorized supervisors",
        ["Any staff","Only office head","Only auditors"]),
       ("Unsure if requester is authorized for confidential file?","Escalate to Records Officer",
        ["Release and ask later","Deny without explanation","Give photocopy"]),
       ("Authorization for general admin records?","Verbal request from any staff",
        ["Written from head","Court order","Notarized request"]),
       ("Authorization for records under COA audit?","Written request with audit authority reference",
        ["Verbal from any clerk","None needed","Presidential directive"]),
       ("Releasing personnel file without authorization?","Administrative liability",
        ["Nothing - public records","File becomes invalid","Clerk gets promoted"]),
       ("Before retrieval, verify about requester?","Whether authorized for that record type",
        ["Wearing proper attire","Employed 1+ year","Filed own docs recently"])]
    for q,a,w in A:
        qs.append(make_q(qid,"Medium",q,shuf([a]+w,a),a,a+".",["authorization"]))
        qid+=1
    recs=[("confidential records","Written authorization from head of office"),
          ("personnel records","Written requisition from authorized personnel"),
          ("financial records under audit","Written request with audit authority"),
          ("general administrative records","Verbal request from office staff"),
          ("legal case files","Court order or head of office authorization")]
    for _ in range(28):
        name=rn(); div=rd(); rt,auth=random.choice(recs)
        q=f"{name} from {div} requests {rt}. Authorization needed?"
        a=auth
        wrong=[r[1] for r in recs if r[1]!=auth]
        qs.append(make_q(qid,"Medium",q,shuf([a]+random.sample(wrong,3),a),a,
                         f"{rt.capitalize()} require {auth.lower()}.",["authorization","scenario"]))
        qid+=1
    return qs[:200]

def gen_hard():
    qs = []; qid = 401
    VP = [("Dela Cruz","Cruz, Maria Dela","DelaCruz, Maria"),
          ("De Leon","Leon, Jose De","DeLeon, Jose"),
          ("Delos Santos","Santos, Ana Delos","DelosSantos, Ana"),
          ("San Juan","Juan, Pedro San","SanJuan, Pedro"),
          ("De Guzman","Guzman, Carlos De","DeGuzman, Carlos")]
    # Multi-step (60)
    for rep in range(60):
        name=rn(); surname=name.split()[-1]; doc=rdc(); div=rd(); agency=ra()
        v=rep%6
        if v==0:
            q=f"Urgent: {agency} Director needs {doc} of {name}. Numeric system. Name NOT in alphabetic index. Action?"
            a="Check variant spellings, nicknames, or maiden names in the index"
            wrong=["Search from 001","Report as non-existent","Create new file"]
            expl="If name not in index, check variants before concluding non-existent."
            tags=["multi-step","numeric","variant-name"]
        elif v==1:
            term,heading=rsub()
            q=f"Relative index points '{term}' to '{heading}'. Go there but document missing. Next?"
            a="Check for OUT guide at that position - document may be charged out"
            wrong=["Conclude never filed","Create from scratch","File complaint"]
            expl="Even at correct heading, document might be charged out. Check OUT guide."
            tags=["multi-step","subject","charge-out"]
        elif v==2:
            region,city=rrg()
            q=f"Need records for {city} but unsure which region. Geographic system. Best approach?"
            a="Consult geographic index to identify correct region"
            wrong=["Search every region","Assume NCR","Ask supervisor"]
            expl=f"Geographic index maps cities to regions. {city} is in {region}."
            tags=["multi-step","geographic"]
        elif v==3:
            pf,wf,cf=random.choice(VP)
            q=f"Cannot find '{wf}' in alphabetic system. Name has prefix '{pf}'. Where to look?"
            a=f"Under '{cf}' - prefixes combine with surname"
            wrong=[f"Under '{wf[0]}' only","Miscellaneous section","Numeric system"]
            expl=f"Prefix '{pf}' combines with surname. Key unit: '{cf.split(',')[0]}'."
            tags=["multi-step","alphabetic","prefix-rule"]
        elif v==4:
            borrower=rn(); bdiv=rd()
            q=f"{doc} of {name} urgently needed by {agency} Director. OUT guide: {borrower}, {bdiv}, 3 days ago (not overdue). Action?"
            a=f"Contact {borrower} in {bdiv}, explain urgency, request early return or photocopy"
            wrong=["Wait until due date","Report as lost","Remove OUT guide"]
            expl="Urgent requests justify contacting borrower for early return even if not overdue."
            tags=["multi-step","charge-out","urgent"]
        else:
            r1=rn(); r2=rn()
            q=f"Both {r1} and {r2} need same {doc} simultaneously. File is in cabinet. Procedure?"
            a="Release original to first requester with charge-out; photocopy for second"
            wrong=["Give to higher rank","Tell both to wait","Split pages between them"]
            expl="One original with charge-out; photocopy serves additional requesters."
            tags=["multi-step","charge-out","multiple-requesters"]
        qs.append(make_q(qid,"Hard",q,shuf([a]+wrong,a),a,expl,tags))
        qid+=1
    # Complex not-found (40)
    for rep in range(40):
        name=rn(); surname=name.split()[-1]; doc=rdc(); v=rep%8
        if v==0:
            q="File returned yesterday not in cabinet. No OUT guide, no cross-ref. Most likely?"
            a="In the to-be-filed tray awaiting refiling"
            wrong=["Stolen","Destroyed","Never returned"]
        elif v==1:
            q="Frequently-requested file missing, NO OUT guide. Most likely cause?"
            a="Someone removed it without following charge-out procedures"
            wrong=["Destroyed by policy","Never existed","Cabinet reorganized"]
        elif v==2:
            q=f"Search for 'Dela Cruz, Maria' between 'Cruz' and 'Diaz' - nothing. Most likely?"
            a="Filed as 'DelaCruz, Maria' (prefix combined) - check further in 'D' section"
            wrong=["Filed under 'M' for Maria","Destroyed","Never created"]
        elif v==3:
            q=f"{name}'s file found ONE position after correct spot. Error type?"
            a="Transposition - two adjacent files swapped"
            wrong=["Wrong unit","Wrong section","Variant spelling"]
        elif v==4:
            q=f"{doc} not under '{surname}'. Found filed under given name. Error type?"
            a="Wrong unit - filed by given name instead of surname"
            wrong=["Transposition","Wrong level","Wrong section"]
        elif v==5:
            q="Leave application filed under 'Personnel' instead of 'Personnel > Leave > Vacation'. Error?"
            a="Wrong level - filed in parent category instead of specific subcategory"
            wrong=["Transposition","Wrong unit","Wrong section"]
        elif v==6:
            q="After ALL OCAC steps (OUT guide, cross-refs, adjacent, catch-all) - all negative. Now what?"
            a="Report as missing to Records Officer, documenting all search steps taken"
            wrong=["Check OUT guide again","Search building randomly","Assume it will appear"]
        else:
            q=f"Two '{surname}' files exist. Clerk pulled wrong one. What step was skipped?"
            a="Verification - did not confirm full name/employee number matched request"
            wrong=["Checking OUT guide","Consulting relative index","Filing requisition slip"]
        expl=a+"."
        qs.append(make_q(qid,"Hard",q,shuf([a]+wrong,a),a,expl,["not-found","complex"]))
        qid+=1
    # System comparison & judgment (50)
    for rep in range(50):
        v=rep%10; name=rn(); doc=rdc(); div=rd()
        if v==0:
            q="Office with 10,000 personnel files, retrieval by name most common. Fastest system?"
            a="Alphabetic - direct access by name without index lookup"
            wrong=["Numeric - numbers simpler","Subject - topics intuitive","Geographic - locations easy"]
        elif v==1:
            q="Need max confidentiality - labels should not reveal content. Best system and tradeoff?"
            a="Numeric - labels reveal nothing, but retrieval requires index lookup (slower)"
            wrong=["Alphabetic - names confidential","Subject - headings coded","Geographic - hides content"]
        elif v==2:
            q="Clerk retrieves from numeric system by memorized number (no index check). Correct?"
            a="Risky - if memory fails, must know to use alphabetic index as fallback"
            wrong=["Perfect procedure","Must always use index","Numeric doesn't allow fast retrieval"]
        elif v==3:
            region,city=rrg()
            q=f"Clerk goes to '{city[0]}' alphabetically instead of geographic section. Error?"
            a="Wrong path - geographic requires region first, not alphabetic by city"
            wrong=["Correct approach","File doesn't exist","Should use numeric index"]
        elif v==4:
            q="Subject system has NO relative index. New clerk can't find docs. Root cause?"
            a="System lacks required finding aid - relative index is mandatory for subject systems"
            wrong=["Clerk incompetent","Subject systems don't need indexes","Docs never filed"]
        elif v==5:
            q=f"Clerk retrieves file but it belongs to different person with same surname. Step skipped?"
            a="Verification - did not confirm full name/employee number matched"
            wrong=["Charge-out","Consulting index","Checking OUT guide"]
        elif v==6:
            q="Office transitions physical to digital records. Which principle stays the SAME?"
            a="Correct indexing at entry is still required - garbage in, garbage out"
            wrong=["Physical misfiling still possible","OUT guides still needed","Sequential scanning primary"]
        elif v==7:
            q="Three clerks: one uses index, one asks colleagues, one searches randomly. Numeric system. Who is correct?"
            a="The one using the index - numeric requires alphabetic index for retrieval"
            wrong=["Asking colleagues - teamwork","Random searcher - finds eventually","All equally valid"]
        elif v==8:
            q="Retrieval averaging 8 minutes. Best combination to improve?"
            a="Update indexes, add file guides, retrain clerks on retrieval paths"
            wrong=["Buy new cabinets","Hire more clerks","Switch to red folders"]
        else:
            q="File needed by COA auditor (proper authority). Currently charged out to Finance (not overdue). Action?"
            a="Contact Finance for immediate return citing audit authority, or provide certified copy"
            wrong=["Tell auditor to wait","Report as missing","Create new file"]
        expl=a+"."
        qs.append(make_q(qid,"Hard",q,shuf([a]+wrong,a),a,expl,["complex","judgment"]))
        qid+=1
    # Procedure traps (50)
    for rep in range(50):
        v=rep%10; name=rn(); doc=rdc(); div=rd()
        if v==0:
            q=f"Clerk retrieves {doc} of {name}, hands to requester WITHOUT OUT guide. Consequence?"
            a="File becomes untraceable - next searcher finds empty space with no explanation"
            wrong=["Nothing - OUT guides optional","File auto-returns","System self-corrects"]
        elif v==1:
            q="Clerk in NUMERIC system goes directly to position without checking index. Finds right file. Correct?"
            a="Worked by luck - proper procedure requires index verification to avoid wrong files"
            wrong=["Perfect - speed matters","Must use relative index","Numeric has no cabinets"]
        elif v==2:
            borrower=rn(); bdiv=rd()
            q=f"OUT guide: {borrower} borrowed file 2 weeks ago (7 days overdue). Follow-up sent 5 days ago, no response. Next?"
            a="Escalate to Records Officer or borrower's supervisor for formal recovery"
            wrong=["Send another notice","Remove OUT guide","Wait 2 more weeks"]
        elif v==3:
            q=f"Supervisor asks for 'all {surname} files.' Cabinet has 12 different {surname}s. Action?"
            a="Ask clarifying questions: which one, what document type, what date range"
            wrong=["Pull all 12","Pull first one only","Refuse as too vague"]
        elif v==4:
            q="File found THREE positions away from correct spot. Systemic problem?"
            a="File guides/dividers may be missing or poorly placed"
            wrong=["Alphabet changed","Cabinet too small","File deliberately hidden"]
        elif v==5:
            term,heading=rsub()
            q=f"Clerk creates NEW folder '{term}' because couldn't find it. Relative index maps to '{heading}'. Error?"
            a="Skipped relative index, created duplicate location - violates system"
            wrong=["Correctly expanded system","Relative index outdated","Unlimited new folders allowed"]
        elif v==6:
            q="Digital system shows file last accessed by someone 3 days ago. Physical equivalent info source?"
            a="Charge-out register or OUT guide - records who last borrowed the file"
            wrong=["File creation date","Cabinet lock log","Attendance record"]
        elif v==7:
            q="Records Section closed for lunch. Clerk takes file without charge-out, plans to record later. Correct?"
            a="Incorrect - no file leaves without immediate charge-out, no exceptions"
            wrong=["OK if recorded same day","OK during emergencies","Lunch breaks are exceptions"]
        elif v==8:
            q="Office has alphabetic (personnel) AND numeric (financial) systems. Need disbursement voucher. Path?"
            a="Numeric path: consult alphabetic index for file number, then go to position"
            wrong=["Alphabetic: go to surname","Either system works","Subject: consult relative index"]
        else:
            q="After retrieval, document inside doesn't match folder label. Action?"
            a="Do NOT release - report discrepancy to Records Officer for correction"
            wrong=["Release anyway - label matters","Throw away wrong doc","Refile without telling"]
        expl=a+"."
        qs.append(make_q(qid,"Hard",q,shuf([a]+wrong,a),a,expl,["procedure","trap"]))
        qid+=1
    return qs[:200]


def main():
    easy = gen_easy()
    medium = gen_medium()
    hard = gen_hard()
    all_q = easy + medium + hard
    for i, q in enumerate(all_q, 1):
        q["id"] = i
    ec = sum(1 for q in all_q if q["difficulty"]=="Easy")
    mc = sum(1 for q in all_q if q["difficulty"]=="Medium")
    hc = sum(1 for q in all_q if q["difficulty"]=="Hard")
    print(f"Generated {len(all_q)} questions: Easy={ec}, Medium={mc}, Hard={hc}")
    errors = 0
    for q in all_q:
        if q["answer"] not in q["choices"]:
            print(f"  ERR id={q['id']}: answer not in choices")
            errors += 1
        if len(q["choices"]) != 4:
            print(f"  ERR id={q['id']}: {len(q['choices'])} choices")
            errors += 1
    print(f"  Validation errors: {errors}")
    out_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data","seed","questions","clerical-ability","indexing-and-record-organization","record-retrieval")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "questions.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_q, f, indent=2, ensure_ascii=False)
    print(f"Written to: {out_path}")

if __name__ == "__main__":
    main()
