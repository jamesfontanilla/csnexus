"""Generate the Verbal Ability / Sentence Completion / Contrast Signals bank."""

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
    / "contrast-signals"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Contrast Signals"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "direct-contrast",
    "contrast-transition",
    "concessive-clause",
    "comparison-contrast",
    "prepositional-concession",
    "corrective-shift",
)

QUESTION_STEMS = {
    "direct-contrast": (
        "Which connector best joins the direct contrast in the sentence below",
        "Which option best fits the opposing idea in the sentence below",
        "Which connector best preserves the turn in meaning",
        "Which choice best matches the direct-contrast pattern",
    ),
    "contrast-transition": (
        "Which connector best introduces the contrasting second clause",
        "Which option best fits the formal contrast transition",
        "Which connector best preserves the pause-and-turn structure",
        "Which choice best matches the contrast-transition pattern",
    ),
    "concessive-clause": (
        "Which connector best admits a fact but keeps the main point",
        "Which option best introduces the concessive clause",
        "Which connector best preserves the concession structure",
        "Which choice best matches the concessive-clause pattern",
    ),
    "comparison-contrast": (
        "Which connector best compares the two clauses side by side",
        "Which option best fits the comparison contrast in the sentence below",
        "Which connector best preserves the side-by-side contrast",
        "Which choice best matches the comparison-contrast pattern",
    ),
    "prepositional-concession": (
        "Which connector best fits the phrase pattern after the blank",
        "Which option best introduces the concessive phrase",
        "Which connector best preserves the phrase-level contrast",
        "Which choice best matches the prepositional-concession pattern",
    ),
    "corrective-shift": (
        "Which connector best corrects the first idea",
        "Which option best replaces the expected action",
        "Which connector best preserves the corrective shift",
        "Which choice best matches the replacement pattern",
    ),
}

ANSWER_BY_FAMILY = {
    "direct-contrast": "but",
    "contrast-transition": "however",
    "concessive-clause": "although",
    "comparison-contrast": "whereas",
    "prepositional-concession": "despite",
    "corrective-shift": "instead",
}

CHOICE_POOLS = {
    "but": ["but", "however", "because", "unless"],
    "however": ["however", "but", "because", "unless"],
    "although": ["although", "but", "because", "however"],
    "whereas": ["whereas", "but", "because", "however"],
    "despite": ["despite", "although", "however", "because"],
    "instead": ["instead", "however", "because", "although"],
}


@dataclass(frozen=True)
class Case:
    noun: str
    noun2: str
    adj1: str
    adj2: str
    base1: str
    base2: str
    verb1: str
    verb2: str
    object1: str
    object2: str
    gerund: str


NOUNS = [
    "memo",
    "report",
    "briefing",
    "queue",
    "form",
    "audit",
    "schedule",
    "draft",
    "notice",
    "record",
    "ledger",
    "request",
    "package",
    "file",
    "inbox",
    "checklist",
    "meeting",
    "counter",
    "folder",
    "summary",
    "route",
    "policy",
    "shipment",
    "archive",
    "bulletin",
]

ADJ_PRIMARY = [
    "brief",
    "crowded",
    "delayed",
    "noisy",
    "rough",
    "incomplete",
    "strict",
    "heavy",
    "unclear",
    "rushed",
    "basic",
    "messy",
    "tense",
    "bright",
    "early",
    "narrow",
    "weak",
    "formal",
    "slow",
    "fragile",
    "simple",
    "plain",
    "careless",
    "busy",
    "stale",
]

ADJ_SECONDARY = [
    "complete",
    "organized",
    "prompt",
    "calm",
    "polished",
    "detailed",
    "flexible",
    "light",
    "clear",
    "careful",
    "thorough",
    "tidy",
    "relaxed",
    "dim",
    "late",
    "wide",
    "strong",
    "casual",
    "fast",
    "sturdy",
    "complex",
    "vivid",
    "precise",
    "steady",
    "fresh",
]

VERBS = [
    "checked",
    "sorted",
    "reviewed",
    "filed",
    "delivered",
    "opened",
    "posted",
    "signed",
    "copied",
    "updated",
    "verified",
    "prepared",
    "cleaned",
    "balanced",
    "sent",
    "read",
    "fixed",
    "explained",
    "logged",
    "processed",
    "accepted",
    "moved",
    "printed",
    "stored",
    "compiled",
]

VERBS_BASE = [
    "check",
    "sort",
    "review",
    "file",
    "deliver",
    "open",
    "post",
    "sign",
    "copy",
    "update",
    "verify",
    "prepare",
    "clean",
    "balance",
    "send",
    "read",
    "fix",
    "explain",
    "log",
    "process",
    "accept",
    "move",
    "print",
    "store",
    "compile",
]

VERBS_ALT = [
    "rechecked",
    "arranged",
    "confirmed",
    "archived",
    "forwarded",
    "unlocked",
    "issued",
    "stamped",
    "scanned",
    "revised",
    "cross-checked",
    "assembled",
    "wiped",
    "reconciled",
    "relayed",
    "inspected",
    "repaired",
    "clarified",
    "tracked",
    "classified",
    "approved",
    "shifted",
    "duplicated",
    "summarized",
    "redistributed",
]

OBJECTS = [
    "the totals",
    "the logs",
    "the attachments",
    "the request",
    "the notice",
    "the forms",
    "the inventory",
    "the memo",
    "the schedule",
    "the figures",
    "the package",
    "the comments",
    "the records",
    "the files",
    "the report",
    "the desk",
    "the archive",
    "the receipt",
    "the list",
    "the draft",
    "the backlog",
    "the queue",
    "the packet",
    "the complaint",
    "the order",
]

GERUNDS = [
    "checking",
    "sorting",
    "reviewing",
    "filing",
    "delivering",
    "opening",
    "posting",
    "signing",
    "copying",
    "updating",
    "verifying",
    "preparing",
    "cleaning",
    "balancing",
    "sending",
    "reading",
    "fixing",
    "explaining",
    "logging",
    "processing",
    "accepting",
    "moving",
    "printing",
    "storing",
    "compiling",
]


def _cap_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return text
    return text[0].upper() + text[1:]


def _normalize_sentence(sentence: str) -> str:
    sentence = re.sub(r"\s+", " ", sentence.strip())
    if sentence and sentence[-1] not in ".!?":
        sentence += "."
    return sentence


def _build_cases() -> list[Case]:
    cases: list[Case] = []
    for index in range(25):
        cases.append(
            Case(
                noun=NOUNS[index],
                noun2=NOUNS[(index + 7) % 25],
                adj1=ADJ_PRIMARY[index],
                adj2=ADJ_SECONDARY[index],
                base1=VERBS_BASE[index],
                base2=VERBS_BASE[(index + 11) % 25],
                verb1=VERBS[index],
                verb2=VERBS_ALT[index],
                object1=OBJECTS[index],
                object2=OBJECTS[(index + 11) % 25],
                gerund=GERUNDS[index],
            )
        )
    return cases


CASES = _build_cases()


def _stem(family: str, case_index: int) -> str:
    stems = QUESTION_STEMS[family]
    return stems[case_index % len(stems)]


def _choice_pool(answer: str) -> list[str]:
    pool = CHOICE_POOLS.get(answer)
    if pool is None:
        raise KeyError(f"missing choice pool for answer: {answer}")
    choices = list(dict.fromkeys(pool))
    if len(choices) != 4:
        raise ValueError(f"choice pool for {answer!r} must contain 4 distinct items")
    return choices


def _render_direct_contrast(case: Case, difficulty: str, case_index: int) -> str:
    if difficulty == "Easy":
        templates = (
            f"The {case.noun} was {case.adj1}, ____ it was {case.adj2}.",
            f"The {case.noun} looked {case.adj1}, ____ the {case.noun2} looked {case.adj2}.",
        )
    elif difficulty == "Medium":
        templates = (
            f"The {case.noun} was {case.adj1}, ____ the {case.noun2} was {case.adj2}.",
            f"The first {case.noun} was {case.adj1}, ____ the second {case.noun2} stayed {case.adj2}.",
        )
    elif difficulty == "Hard":
        templates = (
            f"The first {case.noun} was {case.adj1}, ____ the second {case.noun2} stayed {case.adj2}.",
            f"The {case.noun} seemed {case.adj1}, ____ the {case.noun2} still looked {case.adj2}.",
        )
    else:
        templates = (
            f"The first {case.noun} seemed {case.adj1}, ____ the second {case.noun2} remained {case.adj2} after the review.",
            f"The {case.noun} stayed {case.adj1}, ____ the {case.noun2} kept a {case.adj2} tone.",
        )
    return _normalize_sentence(templates[case_index % len(templates)])


def _render_contrast_transition(case: Case, difficulty: str, case_index: int) -> str:
    if difficulty == "Easy":
        templates = (
            f"The {case.noun} was {case.adj1}; ____, it was {case.adj2}.",
            f"The {case.noun} was {case.adj1}. ____, the team stayed focused.",
        )
    elif difficulty == "Medium":
        templates = (
            f"The {case.noun} was {case.adj1}; ____, the team {case.verb1} {case.object1}.",
            f"The {case.noun} was {case.adj1}; ____, the staff still {case.verb2} {case.object2}.",
        )
    elif difficulty == "Hard":
        templates = (
            f"The {case.noun} was {case.adj1}. ____, the team {case.verb1} {case.object1}.",
            f"The {case.noun} was {case.adj1}; ____, the team still {case.verb2} {case.object2}.",
        )
    else:
        templates = (
            f"The {case.noun} was {case.adj1}; ____, the team {case.verb1} {case.object1} before the deadline.",
            f"The {case.noun} was {case.adj1}. ____, the office still {case.verb2} {case.object2} in time.",
        )
    return _normalize_sentence(templates[case_index % len(templates)])


def _render_concessive_clause(case: Case, difficulty: str, case_index: int) -> str:
    if difficulty == "Easy":
        templates = (
            f"____ the {case.noun} was {case.adj1}, the team {case.verb1} {case.object1}.",
            f"____ the {case.noun} was {case.adj1}, the office still {case.verb2} {case.object2}.",
        )
    elif difficulty == "Medium":
        templates = (
            f"The team {case.verb1} {case.object1} ____ the {case.noun} was {case.adj1}.",
            f"The office still {case.verb2} {case.object2} ____ the {case.noun} was {case.adj1}.",
        )
    elif difficulty == "Hard":
        templates = (
            f"____ the {case.noun} seemed {case.adj1}, the team still {case.verb1} {case.object1}.",
            f"____ the {case.noun} looked {case.adj1}, the office kept the plan moving.",
        )
    else:
        templates = (
            f"The team still {case.verb1} {case.object1} ____ the {case.noun} was {case.adj1} and the schedule was tight.",
            f"The office still {case.verb2} {case.object2} ____ the {case.noun} looked {case.adj1} and the line was long.",
        )
    return _normalize_sentence(templates[case_index % len(templates)])


def _render_comparison_contrast(case: Case, difficulty: str, case_index: int) -> str:
    if difficulty == "Easy":
        templates = (
            f"The first {case.noun} was {case.adj1}, ____ the second {case.noun2} was {case.adj2}.",
            f"The {case.noun} was {case.adj1}, ____ the {case.noun2} was {case.adj2}.",
        )
    elif difficulty == "Medium":
        templates = (
            f"The first {case.noun} stayed {case.adj1}, ____ the second {case.noun2} stayed {case.adj2}.",
            f"The {case.noun} stayed {case.adj1}, ____ the {case.noun2} stayed {case.adj2}.",
        )
    elif difficulty == "Hard":
        templates = (
            f"The {case.noun} handled {case.object1} quickly, ____ the {case.noun2} handled {case.object2} slowly.",
            f"The first {case.noun} handled {case.object1} quickly, ____ the second {case.noun2} handled {case.object2} slowly.",
        )
    else:
        templates = (
            f"The {case.noun} desk handled {case.object1} quickly, ____ the {case.noun2} desk handled {case.object2} slowly.",
            f"The first {case.noun} desk handled {case.object1} quickly, ____ the second {case.noun2} desk handled {case.object2} slowly.",
        )
    return _normalize_sentence(templates[case_index % len(templates)])


def _render_prepositional_concession(case: Case, difficulty: str, case_index: int) -> str:
    if difficulty == "Easy":
        templates = (
            f"____ the {case.adj1} {case.noun}, the team {case.verb1} {case.object1}.",
            f"____ the {case.adj1} {case.noun}, the office still {case.verb2} {case.object2}.",
        )
    elif difficulty == "Medium":
        templates = (
            f"____ working late, the team still {case.verb1} {case.object1}.",
            f"____ the crowded schedule, the office still {case.verb2} {case.object2}.",
        )
    elif difficulty == "Hard":
        templates = (
            f"The team {case.verb1} {case.object1} ____ the {case.adj1} {case.noun}.",
            f"The office still {case.verb2} {case.object2} ____ the {case.adj1} {case.noun}.",
        )
    else:
        templates = (
            f"____ the {case.adj1} {case.noun} and the crowded schedule, the team still {case.verb1} {case.object1}.",
            f"____ the long delay and the {case.adj1} {case.noun}, the office still {case.verb2} {case.object2}.",
        )
    return _normalize_sentence(templates[case_index % len(templates)])


def _render_corrective_shift(case: Case, difficulty: str, case_index: int) -> str:
    if difficulty == "Easy":
        templates = (
            f"The office did not {case.base1} {case.object1}; ____, it {case.base2} {case.object2}.",
            f"The office did not {case.base1} {case.object1}; ____, it moved the schedule earlier.",
        )
    elif difficulty == "Medium":
        templates = (
            f"The office did not delay {case.object1}; ____, it moved {case.object2} earlier.",
            f"The team did not add another delay; ____, it cut the {case.adj1} waiting time.",
        )
    elif difficulty == "Hard":
        templates = (
            f"The report was not {case.adj1}; ____, it was {case.adj2}.",
            f"The plan was not {case.adj1}; ____, it became {case.adj2} after the review.",
        )
    else:
        templates = (
            f"The plan did not add more delay; ____, it shortened the {case.noun2} process.",
            f"The memo did not create another problem; ____, it cleared the path for the {case.noun2} review.",
        )
    return _normalize_sentence(templates[case_index % len(templates)])


def _render_sentence(family: str, difficulty: str, case: Case, case_index: int) -> str:
    if family == "direct-contrast":
        return _render_direct_contrast(case, difficulty, case_index)
    if family == "contrast-transition":
        return _render_contrast_transition(case, difficulty, case_index)
    if family == "concessive-clause":
        return _render_concessive_clause(case, difficulty, case_index)
    if family == "comparison-contrast":
        return _render_comparison_contrast(case, difficulty, case_index)
    if family == "prepositional-concession":
        return _render_prepositional_concession(case, difficulty, case_index)
    if family == "corrective-shift":
        return _render_corrective_shift(case, difficulty, case_index)
    raise KeyError(f"unsupported family: {family}")


def _explanation(family: str, answer: str) -> str:
    explanations = {
        "direct-contrast": f"The sentence needs {answer} because the second idea directly contrasts with the first idea.",
        "contrast-transition": f"The semicolon and the change in meaning call for {answer} as a contrast transition.",
        "concessive-clause": f"The blank begins a dependent clause, so {answer} fits the concessive structure.",
        "comparison-contrast": f"The sentence compares two related ideas side by side, so {answer} fits.",
        "prepositional-concession": f"The blank is followed by a phrase pattern, so {answer} fits the concessive structure.",
        "corrective-shift": f"The sentence replaces the expected idea with another one, so {answer} fits.",
    }
    return explanations[family]


def _make_item(
    *,
    item_id: int,
    family: str,
    difficulty: str,
    case: Case,
    case_index: int,
) -> dict[str, object]:
    answer = ANSWER_BY_FAMILY[family]
    choices = _choice_pool(answer)
    rng = random.Random(2070600 + item_id)
    rng.shuffle(choices)
    stem = _stem(family, case_index)
    sentence = _render_sentence(family, difficulty, case, case_index)
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
        "tags": [family, difficulty.lower(), "contrast-signals"],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _build_bank() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    item_id = 1

    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for case_index, case in enumerate(CASES):
                questions.append(
                    _make_item(
                        item_id=item_id,
                        family=family,
                        difficulty=difficulty,
                        case=case,
                        case_index=case_index,
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


if __name__ == "__main__":
    raise SystemExit(main())
