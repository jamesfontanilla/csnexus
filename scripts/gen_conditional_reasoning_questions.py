"""
Generate 600 conditional reasoning questions for the Analytical Ability module.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/analytical-ability/symbolic-logic/conditional-reasoning/questions.json
"""
import json
import random
from pathlib import Path

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions" / "analytical-ability"
    / "symbolic-logic" / "conditional-reasoning" / "questions.json"
)

B = {
    "subtest": "Analytical Ability",
    "module": "Symbolic Logic",
    "subtopic": "Conditional Reasoning",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}

# ---------------------------------------------------------------------------
# Question templates and data banks
# ---------------------------------------------------------------------------

# Conditional pairs: (antecedent, consequent) for building questions
WORKPLACE_CONDITIONALS = [
    ("an employee is late three times", "a written warning is issued"),
    ("the budget exceeds ₱1 million", "board approval is required"),
    ("the report is submitted on time", "no penalty is imposed"),
    ("an applicant passes the interview", "they proceed to the next stage"),
    ("the project is approved", "funding is released"),
    ("an employee completes training", "they receive a certificate"),
    ("the supervisor signs the form", "the request is processed"),
    ("overtime is pre-approved", "overtime pay is granted"),
    ("the deadline passes", "late submissions are penalized"),
    ("all requirements are met", "the application is approved"),
    ("the employee has 15 years of service", "they are eligible for early retirement"),
    ("the document is classified", "only authorized personnel may access it"),
    ("a fire alarm sounds", "all personnel must evacuate"),
    ("the procurement exceeds ₱50,000", "competitive bidding is required"),
    ("the employee passes the CSE", "they qualify for permanent appointment"),
    ("the director approves the memo", "it is disseminated to all offices"),
    ("the audit finds irregularities", "an investigation is launched"),
    ("the contract expires", "services are discontinued"),
    ("the applicant submits all documents", "their application is evaluated"),
    ("the committee reaches a quorum", "voting may proceed"),
]

ACADEMIC_CONDITIONALS = [
    ("a student passes all subjects", "they are promoted to the next level"),
    ("the thesis is approved", "the student may graduate"),
    ("attendance falls below 75%", "the student is marked absent"),
    ("the research is published", "the professor earns academic credit"),
    ("the student submits the project late", "a grade deduction applies"),
    ("all prerequisites are completed", "enrollment in the advanced course is allowed"),
    ("the student maintains a GPA of 1.5", "they qualify for the dean's list"),
    ("the exam score is below 50%", "the student fails the subject"),
    ("the scholarship is renewed", "tuition is covered for the next semester"),
    ("the student violates academic integrity", "disciplinary action is taken"),
]

GENERAL_CONDITIONALS = [
    ("it rains", "the ground becomes wet"),
    ("the temperature drops below zero", "water freezes"),
    ("electricity fails", "computers shut down"),
    ("traffic increases", "travel time becomes longer"),
    ("a person exercises regularly", "their health improves"),
    ("the alarm is triggered", "security responds"),
    ("the bridge is closed", "drivers must use an alternate route"),
    ("the medicine is taken as prescribed", "the patient recovers"),
    ("the battery is fully charged", "the device operates normally"),
    ("the key is inserted correctly", "the door opens"),
    ("sunlight is blocked", "the room becomes dark"),
    ("the road is icy", "driving becomes dangerous"),
    ("the package is insured", "losses are covered"),
    ("the soil is fertile", "crops grow well"),
    ("the signal is strong", "the call connects clearly"),
]

CHAIN_SETS = [
    # (A, B, C) where A→B and B→C
    ("the employee is late three times", "a memo is issued", "their performance rating decreases"),
    ("the project is approved", "construction begins", "materials are ordered"),
    ("the applicant scores above 80", "they are shortlisted", "they are invited for interview"),
    ("the report is complete", "it is submitted to the supervisor", "it is reviewed within 3 days"),
    ("the senator files the bill", "the committee reviews it", "a public hearing is scheduled"),
    ("the student passes the entrance exam", "they are admitted", "they attend orientation"),
    ("the budget is approved", "procurement begins", "supplies are delivered"),
    ("the alarm sounds", "personnel evacuate", "they proceed to the assembly point"),
    ("the patient is diagnosed", "treatment is prescribed", "recovery begins"),
    ("the contract is signed", "work commences", "the first milestone is delivered"),
    ("the complaint is filed", "an investigation is conducted", "a resolution is issued"),
    ("the training is completed", "certification is granted", "the employee is eligible for promotion"),
    ("the proposal is accepted", "a team is assembled", "the project kicks off"),
    ("the inspection passes", "the permit is issued", "construction may begin"),
    ("the election is held", "votes are counted", "results are announced"),
]

NECESSARY_SUFFICIENT_PAIRS = [
    # (condition, outcome, relationship: "necessary" or "sufficient")
    ("having a valid passport", "international travel", "necessary"),
    ("being a Filipino citizen", "taking the Civil Service Exam", "necessary"),
    ("passing the bar exam", "practicing law", "necessary"),
    ("having four sides", "being a square", "necessary"),
    ("being 18 years old", "voting in elections", "necessary"),
    ("completing residency", "becoming a licensed physician", "necessary"),
    ("having a driver's license", "legally driving a vehicle", "necessary"),
    ("oxygen", "fire", "necessary"),
    ("water", "plant growth", "necessary"),
    ("electricity", "operating a computer", "necessary"),
    ("being a square", "having four sides", "sufficient"),
    ("a presidential appointment", "becoming a Cabinet secretary", "sufficient"),
    ("scoring 100%", "passing the exam", "sufficient"),
    ("being a triangle", "having three angles", "sufficient"),
    ("being a mammal", "being warm-blooded", "sufficient"),
    ("completing all requirements", "graduating", "sufficient"),
    ("having a master's degree", "meeting the educational requirement for the position", "sufficient"),
    ("being a senator", "being a public official", "sufficient"),
    ("winning the gold medal", "being on the podium", "sufficient"),
    ("being a whale", "being an animal", "sufficient"),
]

# ---------------------------------------------------------------------------
# Question generators
# ---------------------------------------------------------------------------

def _modus_ponens_easy(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a modus ponens question (easy)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Easy",
        "question": f'If {p}, then {q}. Given that {p}, which conclusion is valid?',
        "choices": [
            f"{q.capitalize()}.",
            f"It is uncertain whether {q}.",
            f"{q.capitalize()} does not occur.",
            f"We cannot determine the outcome.",
        ],
        "answer": f"{q.capitalize()}.",
        "explanation": f"This is modus ponens. The conditional states: if {p}, then {q}. Since {p} is true, {q} must follow.",
        "tags": ["conditional reasoning", "modus ponens", "valid argument"],
    }


def _modus_tollens_easy(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a modus tollens question (easy)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Easy",
        "question": f'If {p}, then {q}. Given that {q} did not occur, which conclusion is valid?',
        "choices": [
            f"It is not the case that {p}.",
            f"{p.capitalize()} still occurred.",
            f"We cannot determine anything.",
            f"{q.capitalize()} might still occur later.",
        ],
        "answer": f"It is not the case that {p}.",
        "explanation": f"This is modus tollens. If {p} guarantees {q}, and {q} did not occur, then {p} could not have occurred.",
        "tags": ["conditional reasoning", "modus tollens", "valid argument"],
    }


def _affirming_consequent_easy(idx: int, cond: tuple[str, str]) -> dict:
    """Generate an affirming-the-consequent question (easy)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Easy",
        "question": f'If {p}, then {q}. Given that {q} occurred, can we conclude that {p}?',
        "choices": [
            "No, because other causes could produce the same result.",
            f"Yes, because {q} proves {p}.",
            f"Yes, because the conditional guarantees it.",
            "Yes, because the converse is always true.",
        ],
        "answer": "No, because other causes could produce the same result.",
        "explanation": f"This is affirming the consequent (invalid). {q.capitalize()} being true does not prove {p} caused it. Other factors could produce {q}.",
        "tags": ["conditional reasoning", "affirming the consequent", "invalid argument"],
    }


def _denying_antecedent_easy(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a denying-the-antecedent question (easy)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Easy",
        "question": f'If {p}, then {q}. Given that {p} did not occur, can we conclude that {q} did not occur?',
        "choices": [
            "No, because the conditional says nothing about what happens when the antecedent is false.",
            f"Yes, because without {p}, {q} cannot happen.",
            "Yes, because the inverse is always valid.",
            f"Yes, because {p} is the only cause of {q}.",
        ],
        "answer": "No, because the conditional says nothing about what happens when the antecedent is false.",
        "explanation": f"This is denying the antecedent (invalid). The conditional only guarantees what happens when {p} is true. When {p} is false, {q} might still occur through other means.",
        "tags": ["conditional reasoning", "denying the antecedent", "invalid argument"],
    }

def _identify_form_easy(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a question asking to identify the argument form (easy)."""
    p, q = cond
    forms = random.choice([
        ("modus_ponens", f"If {p}, then {q}. {p.capitalize()}. Therefore, {q}.",
         "Modus Ponens (Affirming the Antecedent)", "valid"),
        ("modus_tollens", f"If {p}, then {q}. {q.capitalize()} did not occur. Therefore, it is not the case that {p}.",
         "Modus Tollens (Denying the Consequent)", "valid"),
        ("affirming_consequent", f"If {p}, then {q}. {q.capitalize()}. Therefore, {p}.",
         "Affirming the Consequent (Invalid)", "invalid"),
        ("denying_antecedent", f"If {p}, then {q}. It is not the case that {p}. Therefore, {q} did not occur.",
         "Denying the Antecedent (Invalid)", "invalid"),
    ])
    form_key, argument, correct_name, validity = forms
    choices = [
        "Modus Ponens (Valid)",
        "Modus Tollens (Valid)",
        "Affirming the Consequent (Invalid)",
        "Denying the Antecedent (Invalid)",
    ]
    if validity == "valid":
        if "Ponens" in correct_name:
            answer = "Modus Ponens (Valid)"
        else:
            answer = "Modus Tollens (Valid)"
    else:
        if "Consequent" in correct_name:
            answer = "Affirming the Consequent (Invalid)"
        else:
            answer = "Denying the Antecedent (Invalid)"

    return {
        "id": idx,
        **B,
        "difficulty": "Easy",
        "question": f'Identify the argument form: "{argument}"',
        "choices": choices,
        "answer": answer,
        "explanation": f"The argument follows the pattern of {correct_name}. This form is {validity}.",
        "tags": ["conditional reasoning", "argument form identification", form_key],
    }


def _necessary_sufficient_easy(idx: int, ns_pair: tuple[str, str, str]) -> dict:
    """Generate a necessary/sufficient condition question (easy)."""
    condition, outcome, relationship = ns_pair
    if relationship == "necessary":
        question = f'"{condition.capitalize()} is required for {outcome}." This means {condition} is a _____ condition for {outcome}.'
        answer = "Necessary condition"
        explanation = f"{condition.capitalize()} is necessary for {outcome} because without it, {outcome} cannot occur. However, {condition} alone may not guarantee {outcome}."
    else:
        question = f'"{condition.capitalize()} guarantees {outcome}." This means {condition} is a _____ condition for {outcome}.'
        answer = "Sufficient condition"
        explanation = f"{condition.capitalize()} is sufficient for {outcome} because it guarantees the outcome. However, there may be other ways to achieve {outcome}."

    return {
        "id": idx,
        **B,
        "difficulty": "Easy",
        "question": question,
        "choices": [
            "Necessary condition",
            "Sufficient condition",
            "Both necessary and sufficient",
            "Neither necessary nor sufficient",
        ],
        "answer": answer,
        "explanation": explanation,
        "tags": ["conditional reasoning", "necessary and sufficient conditions"],
    }

# ---------------------------------------------------------------------------
# MEDIUM generators
# ---------------------------------------------------------------------------

def _chain_reasoning_medium(idx: int, chain: tuple[str, str, str]) -> dict:
    """Generate a chain reasoning question (medium)."""
    a, b, c = chain
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'If {a}, then {b}. If {b}, then {c}. Given that {a}, which conclusion is valid?',
        "choices": [
            f"{c.capitalize()}.",
            f"It is uncertain whether {c}.",
            f"{b.capitalize()}, but not necessarily {c}.",
            f"None of the above can be concluded.",
        ],
        "answer": f"{c.capitalize()}.",
        "explanation": f"This is hypothetical syllogism (chain reasoning). {a.capitalize()} triggers {b}, and {b} triggers {c}. Since {a} is true, both {b} and {c} must follow.",
        "tags": ["conditional reasoning", "hypothetical syllogism", "chain reasoning"],
    }


def _chain_modus_tollens_medium(idx: int, chain: tuple[str, str, str]) -> dict:
    """Generate a chain + modus tollens question (medium)."""
    a, b, c = chain
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'If {a}, then {b}. If {b}, then {c}. Given that {c} did not occur, which conclusion is valid?',
        "choices": [
            f"It is not the case that {a}.",
            f"{a.capitalize()} might still have occurred.",
            f"Only {b} did not occur, but {a} could be true.",
            f"We cannot determine anything about {a}.",
        ],
        "answer": f"It is not the case that {a}.",
        "explanation": f"Modus tollens through a chain: If {a}→{b}→{c} and {c} is false, then {b} must be false (MT on second link), and then {a} must be false (MT on first link).",
        "tags": ["conditional reasoning", "modus tollens", "chain reasoning"],
    }


def _contrapositive_medium(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a contrapositive identification question (medium)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'The statement "If {p}, then {q}" is given. Which of the following is logically equivalent to this statement?',
        "choices": [
            f"If {q} does not occur, then it is not the case that {p}.",
            f"If {q}, then {p}.",
            f"If it is not the case that {p}, then {q} does not occur.",
            f"If {p} does not occur, then {q} occurs.",
        ],
        "answer": f"If {q} does not occur, then it is not the case that {p}.",
        "explanation": f"The contrapositive of P → Q is ¬Q → ¬P, which is always logically equivalent to the original. The converse (Q → P) and inverse (¬P → ¬Q) are NOT equivalent.",
        "tags": ["conditional reasoning", "contrapositive", "logical equivalence"],
    }


def _converse_trap_medium(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a converse-trap question (medium)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'Given: "If {p}, then {q}." Someone concludes: "If {q}, then {p}." Is this conclusion valid?',
        "choices": [
            "No — the converse of a conditional is not necessarily true.",
            "Yes — the converse is always logically equivalent.",
            "Yes — if one implies the other, the reverse must also hold.",
            "It depends on the specific content of the statements.",
        ],
        "answer": "No — the converse of a conditional is not necessarily true.",
        "explanation": f"The converse (Q → P) is NOT logically equivalent to the original (P → Q). {q.capitalize()} could occur for reasons other than {p}.",
        "tags": ["conditional reasoning", "converse fallacy", "invalid argument"],
    }


def _compound_antecedent_medium(idx: int) -> dict:
    """Generate a compound antecedent question (medium)."""
    scenarios = [
        {
            "rule": "If an employee has a degree AND passes the interview, they are hired",
            "given": "The employee has a degree but did not pass the interview",
            "correct": "We cannot conclude the employee is hired.",
            "wrong1": "The employee is hired because they have a degree.",
            "wrong2": "The employee is definitely not hired.",
            "wrong3": "The interview result is irrelevant.",
            "explanation": "Both conditions (degree AND interview) must be met. Having only one is insufficient to trigger the consequent.",
        },
        {
            "rule": "If the report is complete AND the supervisor signs it, it is forwarded to the director",
            "given": "The report is complete but the supervisor has not signed it",
            "correct": "We cannot conclude the report is forwarded.",
            "wrong1": "The report is forwarded because it is complete.",
            "wrong2": "The report will never be forwarded.",
            "wrong3": "The supervisor's signature is optional.",
            "explanation": "The conjunctive antecedent requires BOTH conditions. Completeness alone does not trigger forwarding.",
        },
        {
            "rule": "If the budget is approved AND the timeline is feasible, the project proceeds",
            "given": "The budget is approved but the timeline is not feasible",
            "correct": "We cannot conclude the project proceeds.",
            "wrong1": "The project proceeds because the budget is approved.",
            "wrong2": "The project is permanently cancelled.",
            "wrong3": "Timeline feasibility is not a real requirement.",
            "explanation": "Both budget approval AND feasible timeline are required. One condition alone is insufficient.",
        },
        {
            "rule": "If the applicant is qualified AND the position is vacant, they are appointed",
            "given": "The applicant is qualified but the position is not vacant",
            "correct": "We cannot conclude the applicant is appointed.",
            "wrong1": "The applicant is appointed because they are qualified.",
            "wrong2": "The applicant will never be appointed.",
            "wrong3": "Vacancy is irrelevant to appointment.",
            "explanation": "Both qualification AND vacancy are required. Qualification alone does not guarantee appointment.",
        },
        {
            "rule": "If all members are present AND the agenda is distributed, the meeting may proceed",
            "given": "All members are present but the agenda was not distributed",
            "correct": "We cannot conclude the meeting may proceed.",
            "wrong1": "The meeting proceeds because all members are present.",
            "wrong2": "The meeting is cancelled permanently.",
            "wrong3": "The agenda is not a prerequisite.",
            "explanation": "Both conditions must be satisfied. Full attendance without agenda distribution is insufficient.",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'Rule: "{s["rule"]}." Given: {s["given"]}. What can be concluded?',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "compound antecedent", "conjunctive condition"],
    }

def _only_if_medium(idx: int) -> dict:
    """Generate an 'only if' interpretation question (medium)."""
    scenarios = [
        {
            "statement": "An employee is promoted only if they pass the performance evaluation",
            "question_text": 'What does this statement mean logically?',
            "correct": "If the employee is promoted, then they passed the performance evaluation.",
            "wrong1": "If the employee passes the evaluation, they are promoted.",
            "wrong2": "The employee cannot pass the evaluation without being promoted.",
            "wrong3": "Passing the evaluation and being promoted are the same thing.",
            "explanation": "'P only if Q' means P → Q. Being promoted requires having passed the evaluation, but passing alone does not guarantee promotion.",
        },
        {
            "statement": "The contract is valid only if both parties sign",
            "question_text": 'What does this statement mean logically?',
            "correct": "If the contract is valid, then both parties signed.",
            "wrong1": "If both parties sign, the contract is valid.",
            "wrong2": "Signing is optional for contract validity.",
            "wrong3": "The contract becomes valid before signing.",
            "explanation": "'P only if Q' means P → Q. Contract validity requires both signatures, but both signatures alone may not guarantee validity (other conditions might exist).",
        },
        {
            "statement": "A student graduates only if they complete all required units",
            "question_text": 'What does this statement mean logically?',
            "correct": "If the student graduates, then they completed all required units.",
            "wrong1": "If the student completes all units, they graduate.",
            "wrong2": "Completing units is unrelated to graduation.",
            "wrong3": "Graduation happens before completing units.",
            "explanation": "'P only if Q' means P → Q. Graduation requires unit completion, but completion alone may not guarantee graduation.",
        },
        {
            "statement": "The building permit is issued only if the inspection passes",
            "question_text": 'What does this statement mean logically?',
            "correct": "If the permit is issued, then the inspection passed.",
            "wrong1": "If the inspection passes, the permit is issued.",
            "wrong2": "The permit can be issued without inspection.",
            "wrong3": "Inspection and permit issuance are simultaneous.",
            "explanation": "'P only if Q' means P → Q. Permit issuance requires passing inspection, but passing inspection alone may not guarantee the permit.",
        },
        {
            "statement": "You may drive legally only if you have a valid license",
            "question_text": 'What does this statement mean logically?',
            "correct": "If you drive legally, then you have a valid license.",
            "wrong1": "If you have a valid license, you are driving legally.",
            "wrong2": "A license is not required for legal driving.",
            "wrong3": "Having a license means you must drive.",
            "explanation": "'P only if Q' means P → Q. Legal driving requires a license, but having a license doesn't mean you are currently driving.",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'Statement: "{s["statement"]}." {s["question_text"]}',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "only if", "necessary condition"],
    }


def _disjunctive_syllogism_medium(idx: int, cond: tuple[str, str]) -> dict:
    """Generate a disjunctive syllogism question (medium)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'Either {p} or {q}. It is not the case that {p}. What can be concluded?',
        "choices": [
            f"{q.capitalize()}.",
            f"Neither {p} nor {q}.",
            f"Both {p} and {q}.",
            "Nothing can be concluded.",
        ],
        "answer": f"{q.capitalize()}.",
        "explanation": f"This is disjunctive syllogism. Given P ∨ Q and ¬P, Q must be true. Since {p} is ruled out, {q} must hold.",
        "tags": ["conditional reasoning", "disjunctive syllogism", "valid argument"],
    }

# ---------------------------------------------------------------------------
# HARD generators
# ---------------------------------------------------------------------------

def _multi_premise_hard(idx: int) -> dict:
    """Generate a multi-premise deduction question (hard)."""
    scenarios = [
        {
            "premises": "Premise 1: All department heads attend the executive meeting. Premise 2: No one who attends the executive meeting is below Salary Grade 24. Premise 3: Director Reyes is a department head.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "Director Reyes is not below Salary Grade 24.",
            "wrong1": "All people above Salary Grade 24 are department heads.",
            "wrong2": "Director Reyes does not attend the executive meeting.",
            "wrong3": "Some department heads are below Salary Grade 24.",
            "explanation": "Chain: Department head → Attends executive meeting → Not below SG 24. Director Reyes is a department head, so she attends the meeting (MP), and therefore is not below SG 24 (MP on second premise).",
        },
        {
            "premises": "Premise 1: If the audit report is unfavorable, the agency head is summoned. Premise 2: If the agency head is summoned, a corrective action plan is required. Premise 3: No corrective action plan was required.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "The audit report was not unfavorable.",
            "wrong1": "The agency head was summoned but no plan was needed.",
            "wrong2": "The audit was not conducted.",
            "wrong3": "The corrective action plan was submitted late.",
            "explanation": "Modus tollens through chain: Unfavorable → Summoned → Plan required. No plan required → Not summoned (MT) → Not unfavorable (MT).",
        },
        {
            "premises": "Premise 1: All licensed professionals passed a board exam. Premise 2: All who passed a board exam completed a degree program. Premise 3: Engineer Cruz is a licensed professional.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "Engineer Cruz completed a degree program.",
            "wrong1": "All who completed a degree program are licensed professionals.",
            "wrong2": "Engineer Cruz did not pass a board exam.",
            "wrong3": "Some licensed professionals did not complete a degree program.",
            "explanation": "Chain: Licensed professional → Passed board exam → Completed degree. Engineer Cruz is licensed, so he passed the board exam (MP) and completed a degree (MP).",
        },
        {
            "premises": "Premise 1: If the committee approves the resolution, it is forwarded to the Secretary. Premise 2: If the Secretary signs it, it becomes effective. Premise 3: The resolution did not become effective.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "The Secretary did not sign the resolution.",
            "wrong1": "The committee did not approve the resolution.",
            "wrong2": "The resolution was never forwarded.",
            "wrong3": "The Secretary rejected the resolution.",
            "explanation": "MT on Premise 2: Not effective → Secretary did not sign. Note: We CANNOT conclude the committee didn't approve it — the resolution might have been forwarded but unsigned. Only the direct MT on Premise 2 is guaranteed.",
        },
        {
            "premises": "Premise 1: All supervisors must submit weekly reports. Premise 2: Anyone who fails to submit weekly reports receives a memo. Premise 3: Supervisor Lim did not receive a memo.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "Supervisor Lim submitted weekly reports.",
            "wrong1": "Supervisor Lim is not a supervisor.",
            "wrong2": "Supervisor Lim was exempted from reporting.",
            "wrong3": "The memo system is not functioning.",
            "explanation": "Chain: Supervisor → Must submit reports. Fails to submit → Receives memo. Contrapositive: No memo → Did not fail to submit → Submitted reports. Since Lim is a supervisor and received no memo, she submitted her reports.",
        },
        {
            "premises": "Premise 1: If a government project exceeds ₱10 million, a public bidding is mandatory. Premise 2: If a public bidding is mandatory, at least three bidders must participate. Premise 3: Only two bidders participated in Project Alpha.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "Project Alpha does not exceed ₱10 million.",
            "wrong1": "Project Alpha's bidding was invalid.",
            "wrong2": "Public bidding was not mandatory for Project Alpha.",
            "wrong3": "The project should be cancelled.",
            "explanation": "Chain: Exceeds ₱10M → Public bidding mandatory → At least 3 bidders. Only 2 bidders → Not at least 3 → Public bidding not mandatory (MT) → Does not exceed ₱10M (MT). Wait — actually if only 2 participated but 3 were required, it means either the bidding rule was violated OR the project doesn't exceed ₱10M. The valid MT conclusion: fewer than 3 bidders → bidding not mandatory → not exceeding ₱10M.",
        },
        {
            "premises": "Premise 1: If an employee is on official travel, their leave credits are not deducted. Premise 2: If leave credits are not deducted, the employee's attendance record shows no absence. Premise 3: Employee Ramos's attendance record shows an absence.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "Employee Ramos was not on official travel.",
            "wrong1": "Employee Ramos's leave credits were deducted.",
            "wrong2": "Employee Ramos was absent without leave.",
            "wrong3": "The attendance system has an error.",
            "explanation": "Chain: Official travel → No deduction → No absence on record. Absence on record → Deduction occurred (MT) → Not on official travel (MT).",
        },
        {
            "premises": "Premise 1: All applicants who score 90 or above are automatically shortlisted. Premise 2: All shortlisted applicants are invited for a panel interview. Premise 3: Applicant Dela Cruz was not invited for a panel interview.",
            "question_text": "Which conclusion is logically valid?",
            "correct": "Applicant Dela Cruz did not score 90 or above.",
            "wrong1": "Applicant Dela Cruz was shortlisted but not invited.",
            "wrong2": "Applicant Dela Cruz failed the examination.",
            "wrong3": "The panel interview was cancelled.",
            "explanation": "Chain: Score ≥ 90 → Shortlisted → Invited. Not invited → Not shortlisted (MT) → Did not score ≥ 90 (MT).",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Hard",
        "question": f'{s["premises"]} {s["question_text"]}',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "multi-premise deduction", "advanced"],
    }

def _nested_conditional_hard(idx: int) -> dict:
    """Generate a nested/compound conditional question (hard)."""
    scenarios = [
        {
            "statement": "If the employee has a master's degree AND at least 5 years of experience, they qualify for the supervisory position. If they qualify, they must undergo leadership training.",
            "given": "Employee Villanueva has a master's degree and 7 years of experience.",
            "correct": "Employee Villanueva must undergo leadership training.",
            "wrong1": "Employee Villanueva is already a supervisor.",
            "wrong2": "Employee Villanueva only qualifies but need not train.",
            "wrong3": "We cannot determine if Villanueva qualifies.",
            "explanation": "Both conditions met (degree + 5 years) → qualifies. Qualifies → must undergo training. Chain with compound antecedent fully satisfied.",
        },
        {
            "statement": "If either the manager OR the director approves the leave, it is granted. If leave is granted, the employee's workload is redistributed.",
            "given": "The director approved the leave but the manager did not.",
            "correct": "The employee's workload is redistributed.",
            "wrong1": "The leave is not granted because the manager didn't approve.",
            "wrong2": "Both must approve for the leave to be granted.",
            "wrong3": "Workload redistribution is optional.",
            "explanation": "Disjunctive antecedent: Manager OR Director approves → Leave granted. Director approved (one is enough) → Leave granted → Workload redistributed.",
        },
        {
            "statement": "If the inspection reveals violations AND the violations are not corrected within 30 days, the business permit is revoked. If the permit is revoked, the establishment must cease operations.",
            "given": "The inspection revealed violations. The violations were corrected within 15 days.",
            "correct": "We cannot conclude the permit is revoked.",
            "wrong1": "The permit is revoked because violations were found.",
            "wrong2": "The establishment must cease operations.",
            "wrong3": "The business is permanently closed.",
            "explanation": "The compound antecedent requires violations AND non-correction within 30 days. Since violations were corrected within 15 days, the second condition is NOT met. The antecedent is not fully satisfied.",
        },
        {
            "statement": "If a bill passes both the House AND the Senate, it is transmitted to the President. If the President signs it, it becomes law. If the President vetoes it, it returns to Congress.",
            "given": "The bill passed both chambers. The President vetoed it.",
            "correct": "The bill returns to Congress.",
            "wrong1": "The bill becomes law despite the veto.",
            "wrong2": "The bill was not transmitted to the President.",
            "wrong3": "The bill is permanently rejected.",
            "explanation": "Passed both → Transmitted to President (MP). President vetoed → Returns to Congress (MP on third conditional). The veto path is triggered, not the signing path.",
        },
        {
            "statement": "If the applicant is a Filipino citizen AND at least 18 years old AND of good moral character, they may take the CSE. If they take and pass the CSE, they are eligible for government appointment.",
            "given": "Applicant Reyes is a 20-year-old Filipino citizen of good moral character who took and passed the CSE.",
            "correct": "Applicant Reyes is eligible for government appointment.",
            "wrong1": "Applicant Reyes is automatically appointed.",
            "wrong2": "We cannot determine eligibility without more information.",
            "wrong3": "Passing the CSE alone guarantees appointment.",
            "explanation": "All three conditions met → May take CSE. Took and passed → Eligible for appointment. Full chain satisfied through compound antecedent + subsequent conditional.",
        },
        {
            "statement": "If the project is classified as high-risk, both a risk assessment AND a contingency plan are required. If either document is missing, the project cannot proceed.",
            "given": "The project is classified as high-risk. The risk assessment was completed but no contingency plan was prepared.",
            "correct": "The project cannot proceed.",
            "wrong1": "The project can proceed with just the risk assessment.",
            "wrong2": "The contingency plan is optional for high-risk projects.",
            "wrong3": "The project is reclassified as low-risk.",
            "explanation": "High-risk → Both documents required. Contingency plan is missing → A required document is missing → Project cannot proceed (MP on second conditional).",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Hard",
        "question": f'{s["statement"]} Given: {s["given"]} What can be concluded?',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "nested conditionals", "compound conditions", "advanced"],
    }

def _symbolic_hard(idx: int) -> dict:
    """Generate a symbolic logic analysis question (hard)."""
    scenarios = [
        {
            "question_text": "Given: P → Q, Q → R, ¬R. What can be validly concluded?",
            "correct": "¬P",
            "wrong1": "P",
            "wrong2": "Q",
            "wrong3": "R",
            "explanation": "Modus tollens through chain: ¬R → ¬Q (MT on Q→R), then ¬Q → ¬P (MT on P→Q). Therefore ¬P.",
        },
        {
            "question_text": "Given: P → Q, R → Q, Q. What can be validly concluded?",
            "correct": "Nothing definitive about P or R individually.",
            "wrong1": "P is true.",
            "wrong2": "R is true.",
            "wrong3": "Both P and R are true.",
            "explanation": "Q being true does not tell us which antecedent caused it. Both P→Q and R→Q have Q as consequent. Affirming Q (the consequent) is invalid for concluding either P or R.",
        },
        {
            "question_text": "Given: P → (Q ∧ R), P, ¬R. Is this set of statements consistent?",
            "correct": "No — P and ¬R together contradict P → (Q ∧ R).",
            "wrong1": "Yes — all statements can be true simultaneously.",
            "wrong2": "Yes — P can be true while R is false.",
            "wrong3": "It depends on the value of Q.",
            "explanation": "P → (Q ∧ R) means if P is true, both Q and R must be true. P is given as true, so Q ∧ R must be true, meaning R must be true. But ¬R is given. Contradiction — inconsistent.",
        },
        {
            "question_text": "Given: (P ∨ Q) → R, ¬R. What can be validly concluded?",
            "correct": "¬P ∧ ¬Q (neither P nor Q is true).",
            "wrong1": "Only ¬P.",
            "wrong2": "Only ¬Q.",
            "wrong3": "Either ¬P or ¬Q but not both.",
            "explanation": "MT: ¬R → ¬(P ∨ Q). By De Morgan's law, ¬(P ∨ Q) = ¬P ∧ ¬Q. Both P and Q must be false.",
        },
        {
            "question_text": "Given: P → Q, P → R, P. What can be validly concluded?",
            "correct": "Both Q and R are true.",
            "wrong1": "Only Q is true.",
            "wrong2": "Only R is true.",
            "wrong3": "Q → R.",
            "explanation": "P is true. P → Q gives Q (MP). P → R gives R (MP). Both conclusions are independently valid. Note: Q → R is NOT a valid conclusion — Q and R are both triggered by P but not necessarily linked to each other.",
        },
        {
            "question_text": "Given: P → Q, ¬P → R, ¬Q. What can be validly concluded?",
            "correct": "R is true.",
            "wrong1": "P is true.",
            "wrong2": "Nothing can be concluded.",
            "wrong3": "Both Q and R are false.",
            "explanation": "From P → Q and ¬Q, by MT: ¬P. From ¬P → R and ¬P, by MP: R. Therefore R is true.",
        },
        {
            "question_text": "Given: P → (Q → R), P, Q. What can be validly concluded?",
            "correct": "R is true.",
            "wrong1": "Only Q → R is established, not R itself.",
            "wrong2": "P → R directly.",
            "wrong3": "Nothing beyond Q → R.",
            "explanation": "P is true, so Q → R follows (MP on outer conditional). Q is true, so R follows (MP on inner conditional). R is true.",
        },
        {
            "question_text": "Given: (P ∧ Q) → R, P, ¬R. What can be validly concluded?",
            "correct": "¬Q.",
            "wrong1": "¬P.",
            "wrong2": "¬P ∧ ¬Q.",
            "wrong3": "Nothing definitive.",
            "explanation": "MT: ¬R → ¬(P ∧ Q). ¬(P ∧ Q) means ¬P ∨ ¬Q. Since P is given as true, ¬P is false, so ¬Q must be true. Therefore Q is false.",
        },
        {
            "question_text": "Given: P ↔ Q (P if and only if Q), P. What can be validly concluded?",
            "correct": "Q is true.",
            "wrong1": "Q might or might not be true.",
            "wrong2": "¬Q.",
            "wrong3": "P → Q but not Q → P.",
            "explanation": "A biconditional P ↔ Q means P → Q AND Q → P. Since P is true, Q must be true (MP on P → Q).",
        },
        {
            "question_text": "Given: P → Q, Q → P, ¬P. What can be validly concluded?",
            "correct": "¬Q.",
            "wrong1": "Q is true.",
            "wrong2": "Nothing can be concluded about Q.",
            "wrong3": "The statements are inconsistent.",
            "explanation": "Q → P and ¬P gives ¬Q by modus tollens. (Note: P → Q and Q → P together form a biconditional. If one is false, the other must be false too.)",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Hard",
        "question": s["question_text"],
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "symbolic logic", "advanced deduction"],
    }

def _validity_judgment_hard(idx: int) -> dict:
    """Generate a validity judgment question with realistic scenario (hard)."""
    scenarios = [
        {
            "argument": "All government employees must file their SALN. Attorney Reyes filed her SALN. Therefore, Attorney Reyes is a government employee.",
            "correct": "Invalid — this affirms the consequent. Filing SALN does not prove government employment; she might file voluntarily or be required by another regulation.",
            "wrong1": "Valid — filing SALN proves government employment.",
            "wrong2": "Valid — the universal statement guarantees the conclusion.",
            "wrong3": "Invalid — but only because the premise is false.",
            "explanation": "Structure: All A are B. X is B. Therefore X is A. This is affirming the consequent / undistributed middle. Being B doesn't prove being A.",
        },
        {
            "argument": "If the procurement follows proper procedure, no anomaly is found. An anomaly was found in the procurement of office supplies. Therefore, proper procedure was not followed.",
            "correct": "Valid — this is modus tollens. Proper procedure guarantees no anomaly; anomaly found means procedure was not followed.",
            "wrong1": "Invalid — anomalies can occur even with proper procedure.",
            "wrong2": "Invalid — this denies the antecedent.",
            "wrong3": "Invalid — the conclusion is too strong.",
            "explanation": "Structure: P → Q, ¬Q ∴ ¬P. If proper procedure (P) guarantees no anomaly (Q), and an anomaly exists (¬Q), then procedure was not proper (¬P). Classic modus tollens — valid.",
        },
        {
            "argument": "If the mayor declares a state of calamity, emergency funds are released. Emergency funds were released. Therefore, the mayor declared a state of calamity.",
            "correct": "Invalid — this affirms the consequent. Emergency funds could be released for other reasons (national declaration, congressional allocation).",
            "wrong1": "Valid — emergency funds prove the declaration.",
            "wrong2": "Valid — the conditional guarantees this conclusion.",
            "wrong3": "Invalid — but only because emergency funds are never released.",
            "explanation": "Structure: P → Q, Q ∴ P. Affirming the consequent. The funds could have been released through other mechanisms.",
        },
        {
            "argument": "No unauthorized personnel may enter the restricted area. Security Guard Mendoza is authorized. Therefore, Security Guard Mendoza may enter the restricted area.",
            "correct": "Valid — the premise states unauthorized personnel may NOT enter. Being authorized means the restriction does not apply, so entry is permitted.",
            "wrong1": "Invalid — being authorized doesn't guarantee entry rights.",
            "wrong2": "Invalid — this reverses the conditional.",
            "wrong3": "Invalid — the premise only talks about unauthorized personnel.",
            "explanation": "The rule is: Unauthorized → May not enter. Contrapositive: May enter → Authorized. Equivalently: Authorized → May enter. Mendoza is authorized → May enter. Valid.",
        },
        {
            "argument": "If the training budget is exhausted, no more employees can be sent for seminars. The training budget is not exhausted. Therefore, more employees can be sent for seminars.",
            "correct": "Invalid — this denies the antecedent. The budget not being exhausted doesn't guarantee employees CAN be sent (other restrictions might apply).",
            "wrong1": "Valid — available budget means employees can attend.",
            "wrong2": "Valid — the conditional directly supports this.",
            "wrong3": "Invalid — but only because the premise is unrealistic.",
            "explanation": "Structure: P → Q, ¬P ∴ ¬Q. Denying the antecedent. Budget availability is necessary but might not be sufficient — scheduling conflicts, travel bans, or other policies could still prevent attendance.",
        },
        {
            "argument": "All division chiefs attended the planning conference. No one who attended the planning conference was absent on Monday. Division Chief Aquino was absent on Monday. Therefore, Aquino is not a division chief.",
            "correct": "Valid — chain with modus tollens. Division chief → Attended → Not absent Monday. Absent Monday → Did not attend → Not a division chief.",
            "wrong1": "Invalid — absence doesn't disprove being a division chief.",
            "wrong2": "Invalid — the premises might be wrong.",
            "wrong3": "Invalid — this affirms the consequent.",
            "explanation": "Chain: Division chief → Attended conference → Not absent Monday. Aquino was absent Monday (¬Q at end of chain). MT through chain: Not absent Monday is false → Did not attend → Not a division chief. Valid.",
        },
        {
            "argument": "If the resolution is approved by majority vote, it takes effect immediately. The resolution took effect immediately. Therefore, it was approved by majority vote.",
            "correct": "Invalid — affirming the consequent. The resolution might take effect immediately through other mechanisms (emergency powers, executive order).",
            "wrong1": "Valid — immediate effect proves majority approval.",
            "wrong2": "Valid — the conditional establishes this directly.",
            "wrong3": "Invalid — resolutions never take effect immediately.",
            "explanation": "Structure: P → Q, Q ∴ P. Affirming the consequent. Immediate effect could have other causes.",
        },
        {
            "argument": "If all required signatures are obtained, the document is forwarded to the records section. If the document is forwarded to records, it is assigned a tracking number. The document was not assigned a tracking number. Therefore, not all required signatures were obtained.",
            "correct": "Valid — modus tollens through chain. Signatures → Forwarded → Tracking number. No tracking number → Not forwarded → Not all signatures obtained.",
            "wrong1": "Invalid — the tracking system might be down.",
            "wrong2": "Invalid — this skips a step in the chain.",
            "wrong3": "Invalid — denying the antecedent.",
            "explanation": "Chain: All signatures → Forwarded → Tracking number. ¬Tracking number → ¬Forwarded (MT) → ¬All signatures (MT). Valid modus tollens through the entire chain.",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Hard",
        "question": f'Evaluate this argument: "{s["argument"]}"',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "validity judgment", "argument evaluation", "advanced"],
    }

def _abstract_deduction_hard(idx: int) -> dict:
    """Generate abstract deduction questions using letters/variables (hard)."""
    scenarios = [
        {
            "question_text": "If all X are Y, and all Y are Z, and W is an X, which must be true?",
            "correct": "W is Z.",
            "wrong1": "All Z are X.",
            "wrong2": "W is Y but not necessarily Z.",
            "wrong3": "Some Z are not Y.",
            "explanation": "Chain: X → Y → Z. W is X → W is Y (MP) → W is Z (MP). The conclusion W is Z is guaranteed.",
        },
        {
            "question_text": "If no A are B, and all C are A, which must be true?",
            "correct": "No C are B.",
            "wrong1": "Some C are B.",
            "wrong2": "All B are C.",
            "wrong3": "Some A are B.",
            "explanation": "No A are B means A → ¬B. All C are A means C → A. Chain: C → A → ¬B. Therefore no C are B.",
        },
        {
            "question_text": "If P → Q, Q → R, and S → ¬R, and S is true, what can be concluded about P?",
            "correct": "P is false.",
            "wrong1": "P is true.",
            "wrong2": "P might be true or false.",
            "wrong3": "P → S.",
            "explanation": "S is true → ¬R (MP on S→¬R). ¬R → ¬Q (MT on Q→R). ¬Q → ¬P (MT on P→Q). Therefore P is false.",
        },
        {
            "question_text": "All M are N. Some N are O. All O are P. Which must be true?",
            "correct": "Some N are P.",
            "wrong1": "All M are P.",
            "wrong2": "Some M are O.",
            "wrong3": "All P are N.",
            "explanation": "Some N are O (given). All O are P → those N that are O are also P. Therefore some N are P. Note: We cannot conclude all M are P because 'some N are O' doesn't tell us which N — the M-subset of N might not overlap with O.",
        },
        {
            "question_text": "If (P ∨ Q) → R, and (R ∧ S) → T, and P is true, and S is true, what can be concluded?",
            "correct": "T is true.",
            "wrong1": "Only R is true.",
            "wrong2": "T might or might not be true.",
            "wrong3": "We need Q to be true as well.",
            "explanation": "P is true → P ∨ Q is true → R is true (MP). R is true and S is true → R ∧ S is true → T is true (MP). Therefore T is true.",
        },
        {
            "question_text": "If A → B, B → C, C → D, and ¬D, what is the status of A, B, and C?",
            "correct": "All three (A, B, and C) are false.",
            "wrong1": "Only C is false; A and B could be true.",
            "wrong2": "Only D is false; the rest are unaffected.",
            "wrong3": "A is false but B and C are indeterminate.",
            "explanation": "¬D → ¬C (MT on C→D). ¬C → ¬B (MT on B→C). ¬B → ¬A (MT on A→B). All three must be false.",
        },
        {
            "question_text": "Given: If it is not the case that (P and Q), then R. Given: ¬R. What can be concluded?",
            "correct": "Both P and Q are true.",
            "wrong1": "At least one of P or Q is false.",
            "wrong2": "P is true but Q is indeterminate.",
            "wrong3": "Nothing can be concluded about P and Q.",
            "explanation": "¬(P ∧ Q) → R. Contrapositive: ¬R → ¬¬(P ∧ Q) = P ∧ Q. Since ¬R is given, P ∧ Q must be true. Both P and Q are true.",
        },
        {
            "question_text": "If all employees in Division A are certified, and some certified employees are supervisors, and all supervisors attend the leadership forum, can we conclude that some employees in Division A attend the leadership forum?",
            "correct": "No — 'some certified employees are supervisors' doesn't specify they are from Division A.",
            "wrong1": "Yes — the chain guarantees it.",
            "wrong2": "Yes — all Division A employees are supervisors.",
            "wrong3": "Yes — certification leads to the leadership forum.",
            "explanation": "The 'some' qualifier breaks the chain. Division A → Certified. SOME certified → Supervisor → Forum. But the 'some' might not include anyone from Division A. We cannot conclude Division A employees attend the forum.",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Hard",
        "question": s["question_text"],
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "abstract deduction", "symbolic logic", "advanced"],
    }

# ---------------------------------------------------------------------------
# Additional medium generators for variety
# ---------------------------------------------------------------------------

def _inverse_fallacy_medium(idx: int, cond: tuple[str, str]) -> dict:
    """Generate an inverse identification question (medium)."""
    p, q = cond
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'Given: "If {p}, then {q}." Which of the following is the INVERSE of this statement?',
        "choices": [
            f"If it is not the case that {p}, then {q} does not occur.",
            f"If {q} does not occur, then it is not the case that {p}.",
            f"If {q}, then {p}.",
            f"If {p}, then {q} does not occur.",
        ],
        "answer": f"If it is not the case that {p}, then {q} does not occur.",
        "explanation": f"The inverse of P → Q is ¬P → ¬Q. It negates both the antecedent and consequent without reversing direction. The inverse is NOT logically equivalent to the original.",
        "tags": ["conditional reasoning", "inverse", "related conditionals"],
    }


def _unless_medium(idx: int) -> dict:
    """Generate an 'unless' interpretation question (medium)."""
    scenarios = [
        {
            "statement": "The event will be cancelled unless the weather improves",
            "correct": "If the weather does not improve, the event will be cancelled.",
            "wrong1": "If the weather improves, the event will be cancelled.",
            "wrong2": "The event is cancelled regardless of weather.",
            "wrong3": "Weather improvement guarantees the event happens.",
            "explanation": "'Unless' means 'if not.' 'A unless B' = 'If not B, then A.' If weather does NOT improve → event cancelled.",
        },
        {
            "statement": "Employees will not receive a bonus unless they meet their targets",
            "correct": "If employees do not meet their targets, they will not receive a bonus.",
            "wrong1": "If employees meet their targets, they receive a bonus.",
            "wrong2": "Bonuses are never given.",
            "wrong3": "Meeting targets is unrelated to bonuses.",
            "explanation": "'Not A unless B' = 'If not B, then not A.' If targets not met → no bonus. Note: meeting targets is necessary but might not be sufficient.",
        },
        {
            "statement": "The permit will not be renewed unless all fees are paid",
            "correct": "If all fees are not paid, the permit will not be renewed.",
            "wrong1": "If all fees are paid, the permit is automatically renewed.",
            "wrong2": "Fees are optional for permit renewal.",
            "wrong3": "The permit expires regardless of payment.",
            "explanation": "'Not A unless B' = 'If not B, then not A.' If fees not paid → permit not renewed. Payment is necessary but may not be sufficient.",
        },
        {
            "statement": "The meeting will proceed unless the chairperson is absent",
            "correct": "If the chairperson is absent, the meeting will not proceed.",
            "wrong1": "If the chairperson is present, the meeting will not proceed.",
            "wrong2": "The meeting never proceeds.",
            "wrong3": "The chairperson's presence is irrelevant.",
            "explanation": "'A unless B' = 'If B, then not A.' If chairperson absent → meeting does not proceed.",
        },
        {
            "statement": "Students will fail unless they submit the final project",
            "correct": "If students do not submit the final project, they will fail.",
            "wrong1": "If students submit the project, they will pass.",
            "wrong2": "Submission guarantees a passing grade.",
            "wrong3": "Failure is inevitable regardless of submission.",
            "explanation": "'A unless B' = 'If not B, then A.' If project not submitted → fail. Submission is necessary to avoid failure but may not guarantee passing.",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'Statement: "{s["statement"]}." What does this mean logically?',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "unless", "logical translation"],
    }


def _biconditional_medium(idx: int) -> dict:
    """Generate a biconditional question (medium)."""
    scenarios = [
        {
            "statement": "A triangle is equilateral if and only if all its sides are equal",
            "given": "Figure X has all sides equal.",
            "correct": "Figure X is an equilateral triangle (assuming it is a triangle).",
            "wrong1": "Figure X might not be equilateral.",
            "wrong2": "We cannot determine anything about Figure X.",
            "wrong3": "Figure X has unequal sides.",
            "explanation": "A biconditional (P ↔ Q) means P → Q AND Q → P. All sides equal → equilateral (and vice versa). Since all sides are equal, it is equilateral.",
        },
        {
            "statement": "An employee is considered tardy if and only if they arrive after 8:00 AM",
            "given": "Employee Santos arrived at 7:45 AM.",
            "correct": "Employee Santos is not considered tardy.",
            "wrong1": "Employee Santos is tardy.",
            "wrong2": "We cannot determine tardiness.",
            "wrong3": "Arrival time is irrelevant to tardiness.",
            "explanation": "Biconditional: Tardy ↔ After 8:00 AM. Not after 8:00 AM → Not tardy. Santos arrived before 8:00, so not tardy.",
        },
        {
            "statement": "A number is even if and only if it is divisible by 2",
            "given": "The number 15 is not divisible by 2.",
            "correct": "The number 15 is not even.",
            "wrong1": "The number 15 is even.",
            "wrong2": "Divisibility by 2 is unrelated to being even.",
            "wrong3": "We cannot determine if 15 is even.",
            "explanation": "Biconditional: Even ↔ Divisible by 2. Not divisible by 2 → Not even. 15 is not divisible by 2, so it is not even.",
        },
    ]
    s = scenarios[idx % len(scenarios)]
    return {
        "id": idx,
        **B,
        "difficulty": "Medium",
        "question": f'"{s["statement"]}." Given: {s["given"]} What can be concluded?',
        "choices": [s["correct"], s["wrong1"], s["wrong2"], s["wrong3"]],
        "answer": s["correct"],
        "explanation": s["explanation"],
        "tags": ["conditional reasoning", "biconditional", "if and only if"],
    }

# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

def generate_all() -> list[dict]:
    """Generate all 600 questions: 200 Easy, 200 Medium, 200 Hard."""
    random.seed(42)  # Reproducible output
    questions: list[dict] = []
    idx = 1

    # ===== EASY (200 questions) =====
    all_conds = WORKPLACE_CONDITIONALS + ACADEMIC_CONDITIONALS + GENERAL_CONDITIONALS
    random.shuffle(all_conds)

    # Modus Ponens — 50 questions
    for i in range(50):
        cond = all_conds[i % len(all_conds)]
        q = _modus_ponens_easy(idx, cond)
        questions.append(q)
        idx += 1

    # Modus Tollens — 40 questions
    for i in range(40):
        cond = all_conds[(i + 10) % len(all_conds)]
        q = _modus_tollens_easy(idx, cond)
        questions.append(q)
        idx += 1

    # Affirming the Consequent — 40 questions
    for i in range(40):
        cond = all_conds[(i + 20) % len(all_conds)]
        q = _affirming_consequent_easy(idx, cond)
        questions.append(q)
        idx += 1

    # Denying the Antecedent — 30 questions
    for i in range(30):
        cond = all_conds[(i + 30) % len(all_conds)]
        q = _denying_antecedent_easy(idx, cond)
        questions.append(q)
        idx += 1

    # Identify Form — 20 questions
    for i in range(20):
        cond = all_conds[(i + 5) % len(all_conds)]
        q = _identify_form_easy(idx, cond)
        questions.append(q)
        idx += 1

    # Necessary/Sufficient — 20 questions
    ns_pairs = NECESSARY_SUFFICIENT_PAIRS[:]
    random.shuffle(ns_pairs)
    for i in range(20):
        ns = ns_pairs[i % len(ns_pairs)]
        q = _necessary_sufficient_easy(idx, ns)
        questions.append(q)
        idx += 1

    # ===== MEDIUM (200 questions) =====
    random.shuffle(all_conds)

    # Chain Reasoning — 35 questions
    chains = CHAIN_SETS[:]
    random.shuffle(chains)
    for i in range(35):
        chain = chains[i % len(chains)]
        q = _chain_reasoning_medium(idx, chain)
        questions.append(q)
        idx += 1

    # Chain + Modus Tollens — 30 questions
    for i in range(30):
        chain = chains[(i + 5) % len(chains)]
        q = _chain_modus_tollens_medium(idx, chain)
        questions.append(q)
        idx += 1

    # Contrapositive — 30 questions
    for i in range(30):
        cond = all_conds[i % len(all_conds)]
        q = _contrapositive_medium(idx, cond)
        questions.append(q)
        idx += 1

    # Converse Trap — 20 questions
    for i in range(20):
        cond = all_conds[(i + 15) % len(all_conds)]
        q = _converse_trap_medium(idx, cond)
        questions.append(q)
        idx += 1

    # Compound Antecedent — 20 questions
    for i in range(20):
        q = _compound_antecedent_medium(idx)
        questions.append(q)
        idx += 1

    # Only If — 15 questions
    for i in range(15):
        q = _only_if_medium(idx)
        questions.append(q)
        idx += 1

    # Disjunctive Syllogism — 15 questions
    disj_pairs = [
        ("the report was submitted on time", "a penalty is imposed"),
        ("the employee resigned", "they were terminated"),
        ("the project uses internal funds", "it uses external grants"),
        ("the meeting is held on Monday", "it is held on Tuesday"),
        ("the applicant has a bachelor's degree", "they have equivalent work experience"),
        ("the office is open", "a holiday was declared"),
        ("the vehicle is government-owned", "it is privately rented"),
        ("the employee is on leave", "they are on official business"),
        ("the document is original", "it is a certified true copy"),
        ("the payment is made in cash", "it is made by check"),
        ("the position is filled internally", "it is opened to external applicants"),
        ("the training is conducted online", "it is conducted face-to-face"),
        ("the complaint is resolved informally", "it proceeds to formal investigation"),
        ("the budget is sourced from MOOE", "it is sourced from capital outlay"),
        ("the employee works day shift", "they work night shift"),
    ]
    random.shuffle(disj_pairs)
    for i in range(15):
        cond = disj_pairs[i % len(disj_pairs)]
        q = _disjunctive_syllogism_medium(idx, cond)
        questions.append(q)
        idx += 1

    # Inverse Fallacy — 15 questions
    for i in range(15):
        cond = all_conds[(i + 25) % len(all_conds)]
        q = _inverse_fallacy_medium(idx, cond)
        questions.append(q)
        idx += 1

    # Unless — 10 questions
    for i in range(10):
        q = _unless_medium(idx)
        questions.append(q)
        idx += 1

    # Biconditional — 10 questions (use 3 scenarios cycling)
    for i in range(10):
        q = _biconditional_medium(idx)
        questions.append(q)
        idx += 1

    # ===== HARD (200 questions) =====

    # Multi-Premise Deduction — 50 questions
    for i in range(50):
        q = _multi_premise_hard(idx)
        questions.append(q)
        idx += 1

    # Nested Conditionals — 50 questions
    for i in range(50):
        q = _nested_conditional_hard(idx)
        questions.append(q)
        idx += 1

    # Symbolic Logic — 40 questions
    for i in range(40):
        q = _symbolic_hard(idx)
        questions.append(q)
        idx += 1

    # Validity Judgment — 35 questions
    for i in range(35):
        q = _validity_judgment_hard(idx)
        questions.append(q)
        idx += 1

    # Abstract Deduction — 25 questions
    for i in range(25):
        q = _abstract_deduction_hard(idx)
        questions.append(q)
        idx += 1

    # Shuffle choices for each question (keep answer tracking correct)
    for q in questions:
        correct_answer = q["answer"]
        choices = q["choices"][:]
        random.shuffle(choices)
        q["choices"] = choices
        # Ensure answer still matches one of the choices
        assert correct_answer in choices, f"Answer mismatch in question {q['id']}"

    return questions


def main() -> None:
    questions = generate_all()

    # Verify counts
    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]
    print(f"Generated: {len(easy)} Easy, {len(medium)} Medium, {len(hard)} Hard")
    print(f"Total: {len(questions)}")

    assert len(easy) == 200, f"Expected 200 Easy, got {len(easy)}"
    assert len(medium) == 200, f"Expected 200 Medium, got {len(medium)}"
    assert len(hard) == 200, f"Expected 200 Hard, got {len(hard)}"

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written to {OUTPUT}")


if __name__ == "__main__":
    main()
