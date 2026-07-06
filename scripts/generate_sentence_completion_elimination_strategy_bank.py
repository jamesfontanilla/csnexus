"""Generate the Verbal Ability / Sentence Completion / Elimination Strategy bank."""

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
    / "elimination-strategy"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Elimination Strategy"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "meaning-elimination",
    "grammar-elimination",
    "tone-elimination",
    "logic-elimination",
    "reference-elimination",
    "punctuation-elimination",
)

STEM_LABELS = {
    "meaning-elimination": "meaning check",
    "grammar-elimination": "grammar frame",
    "tone-elimination": "tone clue",
    "logic-elimination": "logic clue",
    "reference-elimination": "reference clue",
    "punctuation-elimination": "punctuation clue",
}

CHOICE_BY_KEY: dict[str, tuple[str, list[str]]] = {
    "accurate": ("accurate", ["accurate", "vague", "noisy", "broken"]),
    "temporary": ("temporary", ["temporary", "permanent", "formal", "local"]),
    "urgent": ("urgent", ["urgent", "optional", "distant", "sleepy"]),
    "careful": ("careful", ["careful", "careless", "loud", "wide"]),
    "complete": ("complete", ["complete", "empty", "late", "private"]),
    "is": ("is", ["is", "are", "was", "were"]),
    "are": ("are", ["are", "is", "was", "were"]),
    "was": ("was", ["was", "were", "is", "are"]),
    "were": ("were", ["were", "was", "is", "are"]),
    "has": ("has", ["has", "have", "had", "is"]),
    "requests": ("requests", ["requests", "asks", "begs", "orders"]),
    "asks": ("asks", ["asks", "requests", "orders", "begs"]),
    "texts": ("texts", ["texts", "calls", "emails", "posts"]),
    "informs": ("informs", ["informs", "tells", "jokes", "shrugs"]),
    "advises": ("advises", ["advises", "guesses", "shouts", "whispers"]),
    "because": ("because", ["because", "so", "however", "unless"]),
    "so": ("so", ["so", "because", "however", "unless"]),
    "however": ("however", ["however", "therefore", "because", "unless"]),
    "unless": ("unless", ["unless", "because", "so", "therefore"]),
    "therefore": ("therefore", ["therefore", "because", "so", "yet"]),
    "it": ("it", ["it", "they", "he", "she"]),
    "they": ("they", ["they", "it", "he", "she"]),
    "he": ("he", ["he", "she", "it", "they"]),
    "she": ("she", ["she", "he", "it", "they"]),
    "its": ("its", ["its", "their", "his", "her"]),
    "as a result": ("as a result", ["as a result", "however", "because", "unless"]),
    "for example": ("for example", ["for example", "however", "therefore", "unless"]),
    "nevertheless": ("nevertheless", ["nevertheless", "however", "because", "so"]),
}


@dataclass(frozen=True)
class GroupSpec:
    family: str
    answer: str
    choice_key: str
    note: str
    frame: str
    contexts: tuple[str, str, str, str, str]


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


def _family_label(family: str) -> str:
    return STEM_LABELS[family]


def _question_stem(family: str, difficulty: str, case_index: int) -> str:
    label = _family_label(family)
    if difficulty == "Easy":
        stems = (
            f"Which choice best fits the {label}",
            f"Which word best survives the {label}",
            f"Which option best matches the {label}",
            f"Which answer best fits the {label}",
        )
    elif difficulty == "Medium":
        stems = (
            f"Which choice best survives the {label}",
            f"Which option best matches the {label}",
            f"Which answer best fits the {label}",
            f"Which word best passes the {label}",
        )
    elif difficulty == "Hard":
        stems = (
            f"Which choice best survives the final {label}",
            f"Which option best fits the sentence after elimination",
            f"Which answer best matches the sentence after elimination",
            f"Which word best remains after the clue check",
        )
    else:
        stems = (
            f"Which choice best survives the most precise {label}",
            f"Which option best fits the sentence after every elimination check",
            f"Which answer best remains after the final clue check",
            f"Which word best fits the exact sentence frame",
        )
    return stems[case_index % len(stems)]


def _render_sentence(template: str, difficulty: str) -> str:
    sentence = _normalize(template)
    if difficulty == "Easy":
        return sentence
    if difficulty == "Medium":
        return _normalize(f"In the sentence below, {_lower_first_char(sentence)}")
    if difficulty == "Hard":
        return _normalize(f"In the sentence below, after a quick elimination check, {_lower_first_char(sentence)}")
    return _normalize(
        f"In the sentence below, after every clue is checked carefully, {_lower_first_char(sentence)}"
    )


def _build_choices(answer: str, choice_pool: list[str], seed: int) -> list[str]:
    choices = list(dict.fromkeys(choice_pool))
    if len(choices) != 4:
        raise ValueError(f"choice pool for {answer!r} must contain 4 distinct items")
    rng = random.Random(seed)
    rng.shuffle(choices)
    return choices


def _build_templates(group: GroupSpec) -> tuple[str, str, str, str, str]:
    return tuple(group.frame.format(context=context) for context in group.contexts)


def _explanation(family: str, answer: str, note: str) -> str:
    return f"The sentence needs {answer} because {note}."


def _make_item(
    *,
    item_id: int,
    family: str,
    difficulty: str,
    template: str,
    answer: str,
    choice_key: str,
    note: str,
    case_index: int,
) -> dict[str, object]:
    choices = _build_choices(answer, CHOICE_BY_KEY[choice_key][1], seed=4070700 + item_id)
    stem = _question_stem(family, difficulty, case_index)
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
        "explanation": _explanation(family, answer, note),
        "tags": [family, difficulty.lower(), "elimination-strategy"],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _build_bank() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    item_id = 1
    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for case_index, group in enumerate(GROUPS_BY_FAMILY[family]):
                for template in _build_templates(group):
                    questions.append(
                        _make_item(
                            item_id=item_id,
                            family=family,
                            difficulty=difficulty,
                            template=template,
                            answer=group.answer,
                            choice_key=group.choice_key,
                            note=group.note,
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


GROUPS_BY_FAMILY: dict[str, list[GroupSpec]] = {
    "meaning-elimination": [
        GroupSpec(
            family="meaning-elimination",
            answer="accurate",
            choice_key="accurate",
            note="the clue says the facts are given without mistakes",
            frame="The {context} was ____ because it gave the facts without mistakes.",
            contexts=("office memo", "report", "notice", "summary", "update"),
        ),
        GroupSpec(
            family="meaning-elimination",
            answer="temporary",
            choice_key="temporary",
            note="the clue says it would last only until the repairs were done",
            frame="The {context} was ____ because it would last only until the repairs were done.",
            contexts=("arrangement", "permit", "assignment", "lease", "solution"),
        ),
        GroupSpec(
            family="meaning-elimination",
            answer="urgent",
            choice_key="urgent",
            note="the clue says it needed immediate attention",
            frame="The {context} was ____ because it needed immediate attention.",
            contexts=("request", "notice", "message", "call", "deadline"),
        ),
        GroupSpec(
            family="meaning-elimination",
            answer="careful",
            choice_key="careful",
            note="the clue says it avoided mistakes and paid attention to detail",
            frame="The {context} was ____ because it avoided mistakes and paid attention to detail.",
            contexts=("clerk", "editor", "inspector", "teacher", "assistant"),
        ),
        GroupSpec(
            family="meaning-elimination",
            answer="complete",
            choice_key="complete",
            note="the clue says every required part was included",
            frame="The {context} was ____ because every required part was included.",
            contexts=("file", "form", "list", "set", "package"),
        ),
    ],
    "grammar-elimination": [
        GroupSpec(
            family="grammar-elimination",
            answer="is",
            choice_key="is",
            note="the subject is singular and takes a singular verb",
            frame="The {context} ____ ready to begin.",
            contexts=("committee", "office", "report", "policy", "device"),
        ),
        GroupSpec(
            family="grammar-elimination",
            answer="are",
            choice_key="are",
            note="the subject is plural and takes a plural verb",
            frame="The {context} ____ ready for filing.",
            contexts=("files", "workers", "notes", "tools", "steps"),
        ),
        GroupSpec(
            family="grammar-elimination",
            answer="was",
            choice_key="was",
            note="the time clue points to a finished past event",
            frame="The {context} ____ late yesterday.",
            contexts=("clerk", "manager", "driver", "inspector", "student"),
        ),
        GroupSpec(
            family="grammar-elimination",
            answer="were",
            choice_key="were",
            note="the plural subject needs a plural past verb",
            frame="The {context} ____ checked after lunch.",
            contexts=("files", "forms", "records", "notes", "reports"),
        ),
        GroupSpec(
            family="grammar-elimination",
            answer="has",
            choice_key="has",
            note="the singular subject needs present perfect with has",
            frame="The {context} ____ already signed the note.",
            contexts=("manager", "supervisor", "director", "clerk", "assistant"),
        ),
    ],
    "tone-elimination": [
        GroupSpec(
            family="tone-elimination",
            answer="requests",
            choice_key="requests",
            note="the memo needs formal office language",
            frame="In the {context}, the supervisor ____ the staff to submit the form.",
            contexts=("memo", "notice", "circular", "advisory", "letter"),
        ),
        GroupSpec(
            family="tone-elimination",
            answer="asks",
            choice_key="asks",
            note="the sentence uses relaxed conversational language",
            frame="In the {context}, my friend ____ if I want to go out later.",
            contexts=("chat", "text message", "group chat", "reply", "note"),
        ),
        GroupSpec(
            family="tone-elimination",
            answer="texts",
            choice_key="texts",
            note="the sentence uses a casual message-register action",
            frame="{context} ____ to say she is on her way.",
            contexts=("My cousin", "My friend", "The classmate", "My sister", "The neighbor"),
        ),
        GroupSpec(
            family="tone-elimination",
            answer="informs",
            choice_key="informs",
            note="the bulletin needs official informational wording",
            frame="In the {context}, the office ____ visitors of the new rule.",
            contexts=("bulletin", "notice", "circular", "advisory", "memo"),
        ),
        GroupSpec(
            family="tone-elimination",
            answer="advises",
            choice_key="advises",
            note="the clinic setting calls for polite consultative wording",
            frame="In the {context}, the doctor ____ that the patient rest for two days.",
            contexts=("clinic note", "consultation", "advice sheet", "treatment plan", "follow-up note"),
        ),
    ],
    "logic-elimination": [
        GroupSpec(
            family="logic-elimination",
            answer="because",
            choice_key="because",
            note="the blank introduces the reason for the delay",
            frame="The {context} was delayed ____ the roads were flooded.",
            contexts=("meeting", "briefing", "delivery", "report", "visit"),
        ),
        GroupSpec(
            family="logic-elimination",
            answer="so",
            choice_key="so",
            note="the second idea is the direct result of the first",
            frame="The roads were flooded, ____ the {context} was delayed.",
            contexts=("meeting", "briefing", "delivery", "report", "visit"),
        ),
        GroupSpec(
            family="logic-elimination",
            answer="however",
            choice_key="however",
            note="the sentence turns to a contrasting idea",
            frame="The {context} was short; ____, it was clear.",
            contexts=("memo", "report", "letter", "update", "notice"),
        ),
        GroupSpec(
            family="logic-elimination",
            answer="unless",
            choice_key="unless",
            note="the blank shows the condition that can stop the action",
            frame="The {context} will continue ____ the supervisor leaves.",
            contexts=("meeting", "briefing", "session", "review", "class"),
        ),
        GroupSpec(
            family="logic-elimination",
            answer="therefore",
            choice_key="therefore",
            note="the semicolon points to a formal result connector",
            frame="The {context} was missing; ____, the search continued.",
            contexts=("file", "form", "key", "document", "record"),
        ),
    ],
    "reference-elimination": [
        GroupSpec(
            family="reference-elimination",
            answer="it",
            choice_key="it",
            note="the antecedent is singular and inanimate",
            frame="The {context} was long, but ____ was clear.",
            contexts=("report", "memo", "letter", "notice", "summary"),
        ),
        GroupSpec(
            family="reference-elimination",
            answer="they",
            choice_key="they",
            note="the antecedent is plural",
            frame="The {context} were stacked neatly, and ____ were labeled.",
            contexts=("files", "records", "forms", "folders", "packets"),
        ),
        GroupSpec(
            family="reference-elimination",
            answer="he",
            choice_key="he",
            note="the antecedent is a singular male person",
            frame="The {context} was tired, so ____ left early.",
            contexts=("clerk", "driver", "guard", "manager", "editor"),
        ),
        GroupSpec(
            family="reference-elimination",
            answer="she",
            choice_key="she",
            note="the antecedent is a singular female person",
            frame="The {context} checked the forms, and ____ signed them afterward.",
            contexts=("mother", "aunt", "sister", "daughter", "actress"),
        ),
        GroupSpec(
            family="reference-elimination",
            answer="its",
            choice_key="its",
            note="the antecedent is singular and needs a possessive pronoun",
            frame="The {context} lost ____ cover during transport.",
            contexts=("machine", "device", "printer", "scanner", "tablet"),
        ),
    ],
    "punctuation-elimination": [
        GroupSpec(
            family="punctuation-elimination",
            answer="however",
            choice_key="however",
            note="the semicolon and comma point to a contrastive transition",
            frame="The {context} was short; ____, it was clear.",
            contexts=("memo", "report", "letter", "notice", "update"),
        ),
        GroupSpec(
            family="punctuation-elimination",
            answer="therefore",
            choice_key="therefore",
            note="the semicolon and comma point to a formal result",
            frame="The {context} was long; ____, the office opened another counter.",
            contexts=("queue", "line", "crowd", "wait", "rush"),
        ),
        GroupSpec(
            family="punctuation-elimination",
            answer="as a result",
            choice_key="as a result",
            note="the period before the blank points to a result phrase",
            frame="The {context} jammed. ____, the copies were delayed.",
            contexts=("printer", "machine", "scanner", "copier", "device"),
        ),
        GroupSpec(
            family="punctuation-elimination",
            answer="for example",
            choice_key="for example",
            note="the sentence introduces a specific case after the general idea",
            frame="The {context} covered many checks. ____, it required two signatures.",
            contexts=("policy", "rule", "procedure", "guideline", "notice"),
        ),
        GroupSpec(
            family="punctuation-elimination",
            answer="nevertheless",
            choice_key="nevertheless",
            note="the semicolon calls for a concession or contrast transition",
            frame="The {context} was difficult; ____, the staff finished on time.",
            contexts=("report", "task", "assignment", "review", "project"),
        ),
    ],
}


if __name__ == "__main__":
    raise SystemExit(main())
