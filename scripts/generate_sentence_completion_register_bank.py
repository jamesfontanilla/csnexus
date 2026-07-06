"""Generate the Verbal Ability / Sentence Completion / Register bank."""

from __future__ import annotations

import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "sentence-completion"
    / "register"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Register"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "formal-register",
    "casual-register",
    "consultative-register",
    "official-register",
    "academic-register",
    "technical-register",
)

QUESTION_STEMS: dict[str, dict[str, tuple[str, str, str, str]]] = {
    "formal-register": {
        "Easy": (
            "Which word best fits the formal sentence",
            "Which phrase best fits the formal sentence",
            "Which choice best matches the office tone",
            "Which option best fits the formal register",
        ),
        "Medium": (
            "Which word best preserves the formal register",
            "Which phrase best matches the formal tone",
            "Which choice best fits the institutional voice",
            "Which option best suits the official context",
        ),
        "Hard": (
            "Which word best matches the careful office tone",
            "Which phrase best keeps the sentence formal",
            "Which choice best fits the serious context",
            "Which option best preserves the professional register",
        ),
        "Ultra": (
            "Which word best matches the institutional register",
            "Which phrase best preserves the formal voice",
            "Which choice best fits the authoritative context",
            "Which option best suits the polished office style",
        ),
    },
    "casual-register": {
        "Easy": (
            "Which word best fits the casual sentence",
            "Which phrase best fits the casual sentence",
            "Which choice best matches the friendly tone",
            "Which option best fits the relaxed register",
        ),
        "Medium": (
            "Which word best preserves the casual register",
            "Which phrase best matches the friendly tone",
            "Which choice best fits the conversational voice",
            "Which option best suits the relaxed context",
        ),
        "Hard": (
            "Which word best matches the relaxed everyday tone",
            "Which phrase best keeps the sentence casual",
            "Which choice best fits the familiar setting",
            "Which option best preserves the conversational register",
        ),
        "Ultra": (
            "Which word best matches the spoken register",
            "Which phrase best preserves the easygoing voice",
            "Which choice best fits the personal context",
            "Which option best suits the informal style",
        ),
    },
    "consultative-register": {
        "Easy": (
            "Which phrase best fits the polite exchange",
            "Which phrase best fits the consultative sentence",
            "Which choice best matches the courteous tone",
            "Which option best fits the two-way professional voice",
        ),
        "Medium": (
            "Which phrase best preserves the consultative register",
            "Which phrase best matches the polite interaction",
            "Which choice best fits the service tone",
            "Which option best suits the helpful context",
        ),
        "Hard": (
            "Which phrase best matches the respectful exchange",
            "Which phrase best keeps the sentence courteous",
            "Which choice best fits the guidance setting",
            "Which option best preserves the professional conversation",
        ),
        "Ultra": (
            "Which phrase best matches the guided interaction",
            "Which phrase best preserves the consultative voice",
            "Which choice best fits the polite service setting",
            "Which option best suits the advisory tone",
        ),
    },
    "official-register": {
        "Easy": (
            "Which phrase best fits the official sentence",
            "Which phrase best fits the policy sentence",
            "Which choice best matches the institutional tone",
            "Which option best fits the authoritative register",
        ),
        "Medium": (
            "Which phrase best preserves the official register",
            "Which phrase best matches the policy tone",
            "Which choice best fits the directive voice",
            "Which option best suits the government context",
        ),
        "Hard": (
            "Which phrase best matches the formal directive",
            "Which phrase best keeps the sentence official",
            "Which choice best fits the regulatory setting",
            "Which option best preserves the authoritative voice",
        ),
        "Ultra": (
            "Which phrase best matches the institutional directive",
            "Which phrase best preserves the official voice",
            "Which choice best fits the regulatory context",
            "Which option best suits the legal-administrative style",
        ),
    },
    "academic-register": {
        "Easy": (
            "Which word best fits the academic sentence",
            "Which phrase best fits the academic sentence",
            "Which choice best matches the analytical tone",
            "Which option best fits the scholarly register",
        ),
        "Medium": (
            "Which word best preserves the academic register",
            "Which phrase best matches the research tone",
            "Which choice best fits the study context",
            "Which option best suits the analytical voice",
        ),
        "Hard": (
            "Which word best matches the scholarly discussion",
            "Which phrase best keeps the sentence academic",
            "Which choice best fits the evidence-based setting",
            "Which option best preserves the research register",
        ),
        "Ultra": (
            "Which word best matches the scholarly voice",
            "Which phrase best preserves the analytical style",
            "Which choice best fits the empirical context",
            "Which option best suits the academic discussion",
        ),
    },
    "technical-register": {
        "Easy": (
            "Which word best fits the technical sentence",
            "Which phrase best fits the technical sentence",
            "Which choice best matches the procedural tone",
            "Which option best fits the technical register",
        ),
        "Medium": (
            "Which word best preserves the technical register",
            "Which phrase best matches the procedural tone",
            "Which choice best fits the operational voice",
            "Which option best suits the field-specific context",
        ),
        "Hard": (
            "Which word best matches the procedural instruction",
            "Which phrase best keeps the sentence technical",
            "Which choice best fits the specialist setting",
            "Which option best preserves the operational register",
        ),
        "Ultra": (
            "Which word best matches the specialist voice",
            "Which phrase best preserves the technical style",
            "Which choice best fits the device-level context",
            "Which option best suits the field instruction",
        ),
    },
}

CHOICE_BY_KEY: dict[str, tuple[str, list[str]]] = {
    "formal-requests": ("requests", ["requests", "asks", "begs", "orders"]),
    "formal-informs": ("informs", ["informs", "notifies", "tells", "says"]),
    "formal-submits": ("submits", ["submits", "files", "hands in", "sends"]),
    "formal-acknowledges": ("acknowledges", ["acknowledges", "recognizes", "notes", "accepts"]),
    "formal-authorizes": ("authorizes", ["authorizes", "approves", "permits", "allows"]),
    "casual-asks": ("asks", ["asks", "inquires", "questions", "demands"]),
    "casual-says": ("says", ["says", "tells", "mentions", "states"]),
    "casual-hangs-out": ("hangs out", ["hangs out", "meets up", "spends time", "visits"]),
    "casual-texts": ("texts", ["texts", "messages", "calls", "emails"]),
    "casual-checks-in": ("checks in", ["checks in", "follows up", "calls", "reaches out"]),
    "consultative-could-you-please": (
        "Could you please",
        ["Could you please", "Can you please", "Please", "Would you mind"],
    ),
    "consultative-may-i": ("May I", ["May I", "Can I", "Could I", "Do I"]),
    "consultative-would-you-mind": (
        "Would you mind",
        ["Would you mind", "Can you", "Could you", "Please"],
    ),
    "consultative-let-me": ("Let me", ["Let me", "I will", "I can", "Please let me"]),
    "consultative-i-recommend": ("I recommend", ["I recommend", "I suggest", "I think", "I hope"]),
    "official-hereby": ("hereby", ["hereby", "officially", "formally", "publicly"]),
    "official-shall": ("shall", ["shall", "will", "must", "can"]),
    "official-pursuant-to": ("pursuant to", ["pursuant to", "according to", "because of", "under"]),
    "official-in-accordance-with": (
        "in accordance with",
        ["in accordance with", "according to", "based on", "following"],
    ),
    "official-is-directed-to": (
        "is directed to",
        ["is directed to", "is instructed to", "is required to", "is asked to"],
    ),
    "academic-suggests": ("suggests", ["suggests", "indicates", "shows", "implies"]),
    "academic-indicates": ("indicates", ["indicates", "shows", "reveals", "suggests"]),
    "academic-demonstrates": (
        "demonstrates",
        ["demonstrates", "illustrates", "shows", "proves"],
    ),
    "academic-analyzes": ("analyzes", ["analyzes", "examines", "reviews", "summarizes"]),
    "academic-supports": ("supports", ["supports", "backs", "confirms", "reinforces"]),
    "technical-calibrates": (
        "calibrates",
        ["calibrates", "adjusts", "tests", "checks"],
    ),
    "technical-configures": (
        "configures",
        ["configures", "sets up", "programs", "arranges"],
    ),
    "technical-diagnoses": ("diagnoses", ["diagnoses", "identifies", "checks", "inspects"]),
    "technical-installs": ("installs", ["installs", "sets up", "fits", "mounts"]),
    "technical-resets": ("resets", ["resets", "restarts", "reboots", "restores"]),
}


@dataclass(frozen=True)
class GroupSpec:
    family: str
    answer: str
    choice_key: str
    note: str
    templates: tuple[str, str, str, str, str]


def _normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if text and text[-1] not in ".!?":
        text += "."
    return text


def _lower_first_char(text: str) -> str:
    if not text:
        return text
    if text[0].isalpha():
        return text[0].lower() + text[1:]
    return text


def _build_choices(answer: str, choice_pool: list[str], seed: int) -> list[str]:
    choices = list(dict.fromkeys(choice_pool))
    if len(choices) != 4:
        raise ValueError(f"choice pool for {answer!r} must contain 4 distinct items")
    rng = random.Random(seed)
    rng.shuffle(choices)
    return choices


def _question_stem(family: str, difficulty: str, case_index: int) -> str:
    stems = QUESTION_STEMS[family][difficulty]
    return stems[case_index % len(stems)]


def _render_sentence(template: str, difficulty: str) -> str:
    if difficulty == "Easy":
        return _normalize(template)
    if difficulty == "Medium":
        return _normalize(f"In the sentence below, {_lower_first_char(template)}")
    if difficulty == "Hard":
        return _normalize(f"In the sentence below, where register matters, {_lower_first_char(template)}")
    return _normalize(
        f"In the sentence below, where the register must stay precise, {_lower_first_char(template)}"
    )


def _explanation(family: str, answer: str) -> str:
    family_notes = {
        "formal-register": "the sentence is in a formal office or document setting",
        "casual-register": "the sentence is in a relaxed everyday setting",
        "consultative-register": "the sentence needs polite two-way communication",
        "official-register": "the sentence uses institutional or regulatory wording",
        "academic-register": "the sentence uses analytical or research-based wording",
        "technical-register": "the sentence uses procedural or field-specific wording",
    }
    return f"The sentence needs {answer} because {family_notes[family]}."


def _make_item(
    *,
    item_id: int,
    family: str,
    difficulty: str,
    case: GroupSpec,
    template: str,
) -> dict[str, object]:
    answer, choice_pool = CHOICE_BY_KEY[case.choice_key]
    choices = _build_choices(answer, choice_pool, seed=3070700 + item_id)
    stem = _question_stem(family, difficulty, item_id)
    sentence = _render_sentence(template, difficulty)
    question = f'{stem}: "{sentence}"'

    return {
        "id": item_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": _explanation(family, answer),
        "tags": [family, difficulty.lower(), "register"],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _build_bank() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    item_id = 1
    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for case in GROUPS_BY_FAMILY[family]:
                for template in case.templates:
                    questions.append(
                        _make_item(
                            item_id=item_id,
                            family=family,
                            difficulty=difficulty,
                            case=case,
                            template=template,
                        )
                    )
                    item_id += 1
    return questions


def _validate_bank(questions: list[dict[str, object]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [int(question["id"]) for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    difficulty_counts = Counter(str(question["difficulty"]) for question in questions)
    if difficulty_counts != TARGET_COUNTS:
        raise ValueError(f"unexpected difficulty distribution: {dict(difficulty_counts)}")

    family_counts = Counter(str(question["tags"][0]) for question in questions)  # type: ignore[index]
    expected_family_counts = {family: 100 for family in FAMILY_ORDER}
    if family_counts != expected_family_counts:
        raise ValueError(f"unexpected family distribution: {dict(family_counts)}")

    pair_counts = Counter(
        (str(question["difficulty"]), str(question["tags"][0])) for question in questions  # type: ignore[index]
    )
    expected_pair_counts = {
        (difficulty, family): 25
        for difficulty in DIFFICULTY_ORDER
        for family in FAMILY_ORDER
    }
    if pair_counts != expected_pair_counts:
        raise ValueError("unexpected difficulty/family distribution")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise ValueError("question texts are not unique")

    for question in questions:
        choices = [str(choice) for choice in question["choices"]]  # type: ignore[index]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")


def _write_bank(questions: list[dict[str, object]]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")


def main() -> int:
    questions = _build_bank()
    _validate_bank(questions)
    _write_bank(questions)

    difficulty_summary = Counter(str(question["difficulty"]) for question in questions)
    family_summary = Counter(str(question["tags"][0]) for question in questions)  # type: ignore[index]
    print(f"Difficulty summary: {dict(difficulty_summary)}")
    print(f"Family summary: {dict(family_summary)}")
    return 0


GROUPS_BY_FAMILY: dict[str, list[GroupSpec]] = {
    "formal-register": [
        GroupSpec(
            family="formal-register",
            answer="requests",
            choice_key="formal-requests",
            note="the sentence is a formal office request",
            templates=(
                "The office memo ____ that all staff update their contact details.",
                "The notice ____ that applicants bring two copies of the form.",
                "The circular ____ that teachers submit the report on time.",
                "The letter ____ that the supplier send the missing documents.",
                "The advisory ____ that visitors use the side entrance.",
            ),
        ),
        GroupSpec(
            family="formal-register",
            answer="informs",
            choice_key="formal-informs",
            note="the sentence states official information in a formal tone",
            templates=(
                "The bulletin ____ the public that the schedule has changed.",
                "The memo ____ employees of the new dress code.",
                "The report ____ the manager of the delay.",
                "The notice ____ applicants of the missing requirement.",
                "The advisory ____ the staff that the office will close early.",
            ),
        ),
        GroupSpec(
            family="formal-register",
            answer="submits",
            choice_key="formal-submits",
            note="the sentence needs a formal action in a work document",
            templates=(
                "The clerk ____ the completed form to the records section.",
                "The applicant ____ a copy of the certificate with the request.",
                "The team ____ the final report before noon.",
                "The officer ____ the signed document for review.",
                "The company ____ its proposal to the board.",
            ),
        ),
        GroupSpec(
            family="formal-register",
            answer="acknowledges",
            choice_key="formal-acknowledges",
            note="the sentence needs a formal response showing receipt or notice",
            templates=(
                "The office ____ receipt of the complaint.",
                "The committee ____ the concerns raised by the residents.",
                "The agency ____ the request in writing.",
                "The clerk ____ the letter from the mayor.",
                "The department ____ the correction in its notice.",
            ),
        ),
        GroupSpec(
            family="formal-register",
            answer="authorizes",
            choice_key="formal-authorizes",
            note="the sentence needs an official approval or permission",
            templates=(
                "The director ____ the release of the records.",
                "The board ____ the use of the room for the event.",
                "The manager ____ the overtime request.",
                "The office ____ the payment after verification.",
                "The commissioner ____ the new procedure.",
            ),
        ),
    ],
    "casual-register": [
        GroupSpec(
            family="casual-register",
            answer="asks",
            choice_key="casual-asks",
            note="the sentence sounds like relaxed everyday conversation",
            templates=(
                "My friend ____ if I want to go out later.",
                "The neighbor ____ for a quick favor.",
                "The cousin ____ about my plans for the weekend.",
                "The group chat ____ if I am free tonight.",
                "The classmate ____ to borrow my notes.",
            ),
        ),
        GroupSpec(
            family="casual-register",
            answer="says",
            choice_key="casual-says",
            note="the sentence uses simple conversational wording",
            templates=(
                "My brother ____ he will arrive after lunch.",
                "The friend ____ the movie was good.",
                "The cousin ____ the bus is late.",
                "The teammate ____ the plan sounds fine.",
                "The neighbor ____ the new shop opened yesterday.",
            ),
        ),
        GroupSpec(
            family="casual-register",
            answer="hangs out",
            choice_key="casual-hangs-out",
            note="the sentence needs relaxed language for friends or family",
            templates=(
                "My cousin ____ at the cafe after class.",
                "The neighbor ____ at the mall on Saturdays.",
                "My friend ____ near the riverbank after school.",
                "The classmate ____ whenever he finishes early.",
                "My brother ____ by the corner store in the afternoon.",
            ),
        ),
        GroupSpec(
            family="casual-register",
            answer="texts",
            choice_key="casual-texts",
            note="the sentence uses an everyday casual action",
            templates=(
                "She ____ me a photo of the menu.",
                "My friend ____ when he reached the gate.",
                "The cousin ____ to say she was on her way.",
                "The classmate ____ me updates after practice.",
                "The neighbor ____ later about the game.",
            ),
        ),
        GroupSpec(
            family="casual-register",
            answer="checks in",
            choice_key="casual-checks-in",
            note="the sentence shows a friendly everyday follow-up",
            templates=(
                "My sister ____ with me after each exam.",
                "The friend ____ on me when the rain starts.",
                "The teammate ____ before the meeting starts.",
                "The cousin ____ after each trip.",
                "The neighbor ____ to see if we need help.",
            ),
        ),
    ],
    "consultative-register": [
        GroupSpec(
            family="consultative-register",
            answer="Could you please",
            choice_key="consultative-could-you-please",
            note="the sentence needs a polite direct request",
            templates=(
                "____ hand me the patient file.",
                "____ explain the schedule again.",
                "____ check the form before you leave.",
                "____ send the details to my office.",
                "____ wait a moment while I confirm this.",
            ),
        ),
        GroupSpec(
            family="consultative-register",
            answer="May I",
            choice_key="consultative-may-i",
            note="the sentence needs a polite request for permission",
            templates=(
                "____ ask a follow-up question.",
                "____ see your identification card.",
                "____ speak with the supervisor.",
                "____ enter the room now.",
                "____ have another copy of the report.",
            ),
        ),
        GroupSpec(
            family="consultative-register",
            answer="Would you mind",
            choice_key="consultative-would-you-mind",
            note="the sentence needs a courteous request",
            templates=(
                "____ closing the window.",
                "____ repeating the instructions.",
                "____ signing here.",
                "____ waiting outside for a minute.",
                "____ sending the file later.",
            ),
        ),
        GroupSpec(
            family="consultative-register",
            answer="Let me",
            choice_key="consultative-let-me",
            note="the sentence needs a helpful offer in a polite exchange",
            templates=(
                "____ clarify the schedule for you.",
                "____ check the figures again.",
                "____ show you the next step.",
                "____ explain the form in simple terms.",
                "____ help you with the request.",
            ),
        ),
        GroupSpec(
            family="consultative-register",
            answer="I recommend",
            choice_key="consultative-i-recommend",
            note="the sentence needs polite professional advice",
            templates=(
                "____ that you rest before the interview.",
                "____ that you review the draft first.",
                "____ that you bring the receipt.",
                "____ that you call the office early.",
                "____ that you keep a copy of the form.",
            ),
        ),
    ],
    "official-register": [
        GroupSpec(
            family="official-register",
            answer="hereby",
            choice_key="official-hereby",
            note="the sentence uses official announcement language",
            templates=(
                "The agency ____ announces the revised rule.",
                "The board ____ orders the release of the notice.",
                "The office ____ declares the new schedule.",
                "The committee ____ states the policy change.",
                "The city ____ approves the resolution.",
            ),
        ),
        GroupSpec(
            family="official-register",
            answer="shall",
            choice_key="official-shall",
            note="the sentence uses authoritative legal or policy wording",
            templates=(
                "All employees ____ comply with the directive.",
                "The holder ____ present the permit upon request.",
                "The applicant ____ submit the form before noon.",
                "The office ____ provide a written reply.",
                "The agency ____ keep the records confidential.",
            ),
        ),
        GroupSpec(
            family="official-register",
            answer="pursuant to",
            choice_key="official-pursuant-to",
            note="the sentence uses formal legal phrasing",
            templates=(
                "The action was taken ____ the new policy.",
                "The review was conducted ____ the resolution.",
                "The office acted ____ the directive.",
                "The notice was issued ____ the ordinance.",
                "The request was processed ____ the procedure.",
            ),
        ),
        GroupSpec(
            family="official-register",
            answer="in accordance with",
            choice_key="official-in-accordance-with",
            note="the sentence needs formal compliance language",
            templates=(
                "The work was completed ____ the rules.",
                "The office acted ____ the guidelines.",
                "The decision was made ____ the policy.",
                "The permit was issued ____ the ordinance.",
                "The response was prepared ____ the directive.",
            ),
        ),
        GroupSpec(
            family="official-register",
            answer="is directed to",
            choice_key="official-is-directed-to",
            note="the sentence needs a formal instruction phrase",
            templates=(
                "The public ____ use the side gate.",
                "All visitors ____ register at the desk.",
                "Each applicant ____ submit one ID.",
                "The staff ____ report to the office.",
                "All drivers ____ follow the posted route.",
            ),
        ),
    ],
    "academic-register": [
        GroupSpec(
            family="academic-register",
            answer="suggests",
            choice_key="academic-suggests",
            note="the sentence needs analytical research language",
            templates=(
                "The report ____ that more review is needed.",
                "The study ____ a clear pattern in the results.",
                "The evidence ____ that the method was effective.",
                "The analysis ____ a connection between the two variables.",
                "The article ____ that the trend will continue.",
            ),
        ),
        GroupSpec(
            family="academic-register",
            answer="indicates",
            choice_key="academic-indicates",
            note="the sentence needs data-based scholarly wording",
            templates=(
                "The chart ____ a rise in demand.",
                "The survey ____ that most respondents agreed.",
                "The data set ____ better performance after training.",
                "The result ____ a change in attitude.",
                "The study ____ that the pattern is consistent.",
            ),
        ),
        GroupSpec(
            family="academic-register",
            answer="demonstrates",
            choice_key="academic-demonstrates",
            note="the sentence needs a scholarly explanation of evidence",
            templates=(
                "The experiment ____ that heat speeds the reaction.",
                "The table ____ the difference between the groups.",
                "The presentation ____ the main point clearly.",
                "The case study ____ the method in action.",
                "The report ____ the value of careful review.",
            ),
        ),
        GroupSpec(
            family="academic-register",
            answer="analyzes",
            choice_key="academic-analyzes",
            note="the sentence needs a careful study-oriented action",
            templates=(
                "The researcher ____ the responses by category.",
                "The article ____ the data in detail.",
                "The team ____ the survey results before drawing conclusions.",
                "The report ____ the causes of the delay.",
                "The student ____ the argument from several angles.",
            ),
        ),
        GroupSpec(
            family="academic-register",
            answer="supports",
            choice_key="academic-supports",
            note="the sentence needs evidence that strengthens a claim",
            templates=(
                "The evidence ____ the conclusion.",
                "The citation ____ the argument.",
                "The data set ____ the proposed explanation.",
                "The finding ____ the need for more research.",
                "The review ____ the main claim.",
            ),
        ),
    ],
    "technical-register": [
        GroupSpec(
            family="technical-register",
            answer="calibrates",
            choice_key="technical-calibrates",
            note="the sentence needs a precise equipment adjustment",
            templates=(
                "The technician ____ the scale before use.",
                "The lab assistant ____ the meter for accuracy.",
                "The engineer ____ the sensor before testing.",
                "The operator ____ the gauge after setup.",
                "The staff member ____ the device according to the manual.",
            ),
        ),
        GroupSpec(
            family="technical-register",
            answer="configures",
            choice_key="technical-configures",
            note="the sentence needs a system setup action",
            templates=(
                "The operator ____ the device for the network.",
                "The technician ____ the router for the office.",
                "The assistant ____ the program for the new user.",
                "The engineer ____ the system for remote access.",
                "The user ____ the device before the demo.",
            ),
        ),
        GroupSpec(
            family="technical-register",
            answer="diagnoses",
            choice_key="technical-diagnoses",
            note="the sentence needs a fault-finding procedure",
            templates=(
                "The technician ____ the fault before repair.",
                "The engineer ____ the problem with the machine.",
                "The system checker ____ the error quickly.",
                "The mechanic ____ the issue from the report.",
                "The assistant ____ the cause of the slowdown.",
            ),
        ),
        GroupSpec(
            family="technical-register",
            answer="installs",
            choice_key="technical-installs",
            note="the sentence needs a setup or fitting action",
            templates=(
                "The technician ____ the software on the laptop.",
                "The worker ____ the new cable in the room.",
                "The installer ____ the update on the tablet.",
                "The assistant ____ the equipment in the lab.",
                "The engineer ____ the sensor in the machine.",
            ),
        ),
        GroupSpec(
            family="technical-register",
            answer="resets",
            choice_key="technical-resets",
            note="the sentence needs a technical restart action",
            templates=(
                "The operator ____ the device after the error.",
                "The technician ____ the password system.",
                "The assistant ____ the timer before the trial.",
                "The engineer ____ the modem for the test.",
                "The user ____ the router after the update.",
            ),
        ),
    ],
}


if __name__ == "__main__":
    raise SystemExit(main())
