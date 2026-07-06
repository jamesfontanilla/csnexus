"""Generate the Verbal Ability / Sentence Completion / Cause and Effect bank."""

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
    / "cause-and-effect"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Cause and Effect"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "because-clause",
    "since-clause",
    "because-of-phrase",
    "so-result",
    "therefore-result",
    "as-a-result",
)

QUESTION_STEMS: dict[str, dict[str, tuple[str, str, str, str]]] = {
    "because-clause": {
        "Easy": (
            "Which connector best introduces the reason",
            "Which word best shows why the action happened",
            "Which connector best fits the cause clause",
            "Which option best matches the reason relationship",
        ),
        "Medium": (
            "Which connector best completes the explanatory cause",
            "Which word best links the result to its reason",
            "Which connector best preserves the reason logic",
            "Which option best fits the direct cause-clause pattern",
        ),
        "Hard": (
            "Which connector best keeps the sentence pointing to the cause",
            "Which word best introduces the explanation for the action",
            "Which connector best matches the causal clause",
            "Which option best fits the why-relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's causal logic",
            "Which word best handles the explanatory clause with precision",
            "Which connector best matches the direct reason structure",
            "Which option best fits the cause-and-explanation pattern",
        ),
    },
    "since-clause": {
        "Easy": (
            "Which connector best introduces the reason at the start",
            "Which word best fits the causal sense of since",
            "Which connector best shows why the event happened",
            "Which option best matches the reason-clause relationship",
        ),
        "Medium": (
            "Which connector best keeps since in its causal role",
            "Which word best links the explanation to the effect",
            "Which connector best preserves the reason clause",
            "Which option best fits the cause logic of since",
        ),
        "Hard": (
            "Which connector best distinguishes cause from time",
            "Which word best shows since being used as a reason word",
            "Which connector best completes the explanatory sentence",
            "Which option best fits the reason-clause pattern",
        ),
        "Ultra": (
            "Which connector best preserves the causal meaning of since",
            "Which word best avoids the time meaning of since",
            "Which connector best fits the sentence's reason structure",
            "Which option best matches the cause-before-effect logic",
        ),
    },
    "because-of-phrase": {
        "Easy": (
            "Which connector best fits the noun-phrase cause",
            "Which word best shows the reason as a phrase",
            "Which connector best introduces the cause phrase",
            "Which option best matches the phrase-level cause",
        ),
        "Medium": (
            "Which connector best keeps the cause in phrase form",
            "Which word best introduces the noun phrase that explains the result",
            "Which connector best preserves the phrase-level reason",
            "Which option best fits the cause-phrase pattern",
        ),
        "Hard": (
            "Which connector best handles a cause without a full clause",
            "Which word best points to the reason phrase precisely",
            "Which connector best matches the noun-phrase explanation",
            "Which option best fits the prepositional cause",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's phrase-level cause",
            "Which word best handles the reason noun phrase with precision",
            "Which connector best fits the prepositional cause structure",
            "Which option best matches the cause-phrase relationship",
        ),
    },
    "so-result": {
        "Easy": (
            "Which connector best shows the result",
            "Which word best shows what happened next",
            "Which connector best fits the direct consequence",
            "Which option best matches the result relationship",
        ),
        "Medium": (
            "Which connector best links the cause to its result",
            "Which word best introduces the consequence",
            "Which connector best preserves the result logic",
            "Which option best fits the cause-to-effect pattern",
        ),
        "Hard": (
            "Which connector best keeps the sentence moving toward the outcome",
            "Which word best shows the consequence of the first idea",
            "Which connector best matches the direct effect",
            "Which option best fits the consequence relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's consequence logic",
            "Which word best fits the direct result with precision",
            "Which connector best completes the effect clause",
            "Which option best matches the cause-and-result pattern",
        ),
    },
    "therefore-result": {
        "Easy": (
            "Which connector best introduces the conclusion",
            "Which word best shows the formal result",
            "Which connector best fits the semicolon pattern",
            "Which option best matches the conclusion relationship",
        ),
        "Medium": (
            "Which connector best signals the formal consequence",
            "Which word best introduces the outcome after a pause",
            "Which connector best preserves the result transition",
            "Which option best fits the logical conclusion",
        ),
        "Hard": (
            "Which connector best matches the semicolon plus comma pattern",
            "Which word best shows a formal cause-and-effect result",
            "Which connector best keeps the conclusion precise",
            "Which option best fits the transition to the result",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's formal conclusion",
            "Which word best fits the result transition with clarity",
            "Which connector best matches the inference pattern",
            "Which option best fits the consequence after a pause",
        ),
    },
    "as-a-result": {
        "Easy": (
            "Which connector best shows the outcome",
            "Which word best introduces the result phrase",
            "Which connector best fits the formal consequence phrase",
            "Which option best matches the outcome relationship",
        ),
        "Medium": (
            "Which connector best presents the result in phrase form",
            "Which word best signals the consequence after a full stop",
            "Which connector best preserves the outcome phrase",
            "Which option best fits the result phrase pattern",
        ),
        "Hard": (
            "Which connector best keeps the consequence phrase clear",
            "Which word best shows what followed from the cause",
            "Which connector best matches the formal outcome phrase",
            "Which option best fits the after-effect relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's result phrase",
            "Which word best fits the consequence with precision",
            "Which connector best handles the formal outcome marker",
            "Which option best matches the result-after-causes pattern",
        ),
    },
}

CHOICE_BY_FAMILY = {
    "because-clause": ("because", ["because", "since", "so", "therefore"]),
    "since-clause": ("since", ["since", "because", "so", "therefore"]),
    "because-of-phrase": ("because of", ["because of", "due to", "owing to", "because"]),
    "so-result": ("so", ["so", "therefore", "thus", "because"]),
    "therefore-result": ("therefore", ["therefore", "as a result", "consequently", "so"]),
    "as-a-result": ("as a result", ["as a result", "therefore", "thus", "so"]),
}


@dataclass(frozen=True)
class SituationCase:
    effect_subject: str
    effect_verb_phrase: str
    cause_clause: str
    cause_np: str


CASES: tuple[SituationCase, ...] = (
    SituationCase("meeting", "was postponed", "the roads were flooded", "the flooded roads"),
    SituationCase("office", "opened a second counter", "the queue was long", "the long queue"),
    SituationCase("computers", "shut down", "the power failed", "the power failure"),
    SituationCase("clerk", "returned the form", "the signature was missing", "the missing signature"),
    SituationCase("staff", "arrived late", "traffic was heavy", "the heavy traffic"),
    SituationCase("report", "was delayed", "the printer jammed", "the jammed printer"),
    SituationCase("event", "moved indoors", "rain started suddenly", "the sudden rain"),
    SituationCase("tablet", "turned off", "the battery was low", "the low battery"),
    SituationCase("briefing", "was paused", "the noise grew louder", "the rising noise"),
    SituationCase("truck", "took a detour", "the road was closed", "the closed road"),
    SituationCase("break", "was extended", "the heat was intense", "the intense heat"),
    SituationCase("office", "limited printing", "paper supplies ran low", "the low paper supply"),
    SituationCase("letter", "was resent", "the envelope was damaged", "the damaged envelope"),
    SituationCase("records", "were backed up", "a system glitch appeared", "the system glitch"),
    SituationCase("entrance", "was roped off", "the floor was slippery", "the slippery floor"),
    SituationCase("request", "was held", "the fee was unpaid", "the unpaid fee"),
    SituationCase("inventory", "was adjusted", "the shipment arrived late", "the late shipment"),
    SituationCase("package", "was returned", "the address was wrong", "the wrong address"),
    SituationCase("team leader", "stepped in", "the supervisor fell ill", "the supervisor's illness"),
    SituationCase("audit", "was paused", "the file was missing", "the missing file"),
    SituationCase("lunch break", "was delayed", "the meeting ran long", "the long meeting"),
    SituationCase("office", "smelled bad", "the drain was blocked", "the blocked drain"),
    SituationCase("workers", "paused", "thunder rumbled loudly", "the loud thunder"),
    SituationCase("operation", "stopped", "the permit expired", "the expired permit"),
    SituationCase("overtime", "was scheduled", "the staff shortage worsened", "the staff shortage"),
)


def _normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if text and text[-1] not in ".!?":
        text += "."
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


def _render_sentence(family: str, difficulty: str, case: SituationCase, case_index: int) -> str:
    effect = f"the {case.effect_subject} {case.effect_verb_phrase}"
    cause_clause = case.cause_clause
    cause_np = case.cause_np

    if family == "because-clause":
        if difficulty in {"Easy", "Hard"}:
            return _normalize(f'{effect} ____ {cause_clause}')
        return _normalize(f'____ {cause_clause}, {effect}')

    if family == "since-clause":
        if difficulty in {"Easy", "Hard"}:
            return _normalize(f'____ {cause_clause}, {effect}')
        return _normalize(f'{effect} ____ {cause_clause}')

    if family == "because-of-phrase":
        if difficulty in {"Easy", "Hard"}:
            return _normalize(f'____ {cause_np}, {effect}')
        return _normalize(f'{effect} ____ {cause_np}')

    if family == "so-result":
        if difficulty in {"Easy", "Hard"}:
            return _normalize(f'{cause_clause}, ____ {effect}')
        return _normalize(f'{cause_clause}; ____, {effect}')

    if family == "therefore-result":
        if difficulty in {"Easy", "Hard"}:
            return _normalize(f'{cause_clause}; ____, {effect}')
        return _normalize(f'{cause_clause}. ____, {effect}')

    if family == "as-a-result":
        if difficulty in {"Easy", "Hard"}:
            return _normalize(f'{cause_clause}. ____, {effect}')
        return _normalize(f'{cause_clause}; ____, {effect}')

    raise KeyError(f"unsupported family: {family}")


def _explanation(family: str, answer: str) -> str:
    return {
        "because-clause": f"The sentence needs {answer} because the blank introduces the reason for the action.",
        "since-clause": f"The sentence needs {answer} because since is being used as a reason connector.",
        "because-of-phrase": f"The sentence needs {answer} because the blank is followed by a noun phrase.",
        "so-result": f"The sentence needs {answer} because the second idea is the result of the first.",
        "therefore-result": f"The sentence needs {answer} because the punctuation calls for a formal result connector.",
        "as-a-result": f"The sentence needs {answer} because it states the consequence in phrase form.",
    }[family]


def _make_item(
    *,
    item_id: int,
    family: str,
    difficulty: str,
    case: SituationCase,
    case_index: int,
) -> dict[str, object]:
    answer, choice_pool = CHOICE_BY_FAMILY[family]
    choices = _build_choices(answer, choice_pool, seed=2070700 + item_id)
    stem = _question_stem(family, difficulty, case_index)
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
        "tags": [family, difficulty.lower(), "cause-and-effect"],
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

        text = str(question["question"]).lower()
        if "the the" in text or "a a" in text or "an an" in text:
            raise ValueError(f"duplicate article detected in question {question['id']}")


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
