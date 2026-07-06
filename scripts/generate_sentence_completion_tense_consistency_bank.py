"""Generate the Verbal Ability / Sentence Completion / Tense Consistency bank.

The bank covers:

- simple present versus simple past
- future forms and time clauses
- perfect tenses and earlier completion
- sequence of tenses in reported speech

Each difficulty band contains 150 items, for 600 items total. The script is
deterministic and writes directly to the seed tree so the reset script can
pick it up automatically.
"""

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
    / "tense-consistency"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Tense Consistency"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "present-reference",
    "past-reference",
    "future-reference",
    "present-perfect",
    "past-perfect",
    "reported-sequence",
)

QUESTION_STEMS: dict[str, dict[str, tuple[str, str, str, str]]] = {
    "present-reference": {
        "Easy": (
            "Which verb form best completes the sentence below",
            "Which option best matches the present-time clue",
            "Which verb best keeps the routine consistent",
            "Which choice best preserves the present timeline",
        ),
        "Medium": (
            "Which verb form best keeps the habit or routine consistent",
            "Which option best fits the present-time frame",
            "Which verb best matches the repeated action",
            "Which choice best maintains tense consistency",
        ),
        "Hard": (
            "Which verb phrase best matches the present timeline",
            "Which option best fits the sentence's present reference point",
            "Which verb best completes the routine action",
            "Which choice best keeps the verb in the present",
        ),
        "Ultra": (
            "Which verb phrase best preserves the sentence's present-time logic",
            "Which option best fits the present reference most precisely",
            "Which verb best keeps the ongoing routine clear",
            "Which choice best maintains tense consistency in the present",
        ),
    },
    "past-reference": {
        "Easy": (
            "Which verb form best completes the sentence below",
            "Which option best matches the past-time clue",
            "Which verb best keeps the finished event consistent",
            "Which choice best preserves the past timeline",
        ),
        "Medium": (
            "Which verb form best fits the finished past action",
            "Which option best matches the past reference point",
            "Which verb best completes the past event",
            "Which choice best maintains tense consistency",
        ),
        "Hard": (
            "Which verb phrase best matches the closed past frame",
            "Which option best fits the sentence's past reference point",
            "Which verb best completes the finished action",
            "Which choice best keeps the verb in the past",
        ),
        "Ultra": (
            "Which verb phrase best preserves the sentence's past-time logic",
            "Which option best fits the past reference most precisely",
            "Which verb best keeps the completed action clear",
            "Which choice best maintains tense consistency in the past",
        ),
    },
    "future-reference": {
        "Easy": (
            "Which verb form best completes the sentence below",
            "Which option best matches the later action",
            "Which verb best keeps the future plan consistent",
            "Which choice best preserves the future timeline",
        ),
        "Medium": (
            "Which verb form best fits the later time clue",
            "Which option best matches the future reference point",
            "Which verb best completes the action that happens later",
            "Which choice best maintains tense consistency",
        ),
        "Hard": (
            "Which verb phrase best matches the future timeline",
            "Which option best fits the sentence's later reference point",
            "Which verb best completes the planned action",
            "Which choice best keeps the verb in the future",
        ),
        "Ultra": (
            "Which verb phrase best preserves the sentence's future-time logic",
            "Which option best fits the future reference most precisely",
            "Which verb best keeps the later action clear",
            "Which choice best maintains tense consistency in the future",
        ),
    },
    "present-perfect": {
        "Easy": (
            "Which verb form best completes the sentence below",
            "Which option best matches the action linked to now",
            "Which verb best keeps the completed action connected to the present",
            "Which choice best preserves the present-perfect timeline",
        ),
        "Medium": (
            "Which verb form best fits the completion clue",
            "Which option best matches the present reference point",
            "Which verb best completes the action that still matters now",
            "Which choice best maintains tense consistency",
        ),
        "Hard": (
            "Which verb phrase best matches the present-perfect frame",
            "Which option best fits the sentence's link to now",
            "Which verb best completes the already-finished action",
            "Which choice best keeps the verb linked to the present",
        ),
        "Ultra": (
            "Which verb phrase best preserves the sentence's present-perfect logic",
            "Which option best fits the present reference most precisely",
            "Which verb best keeps the completed action relevant now",
            "Which choice best maintains tense consistency in the present perfect",
        ),
    },
    "past-perfect": {
        "Easy": (
            "Which verb form best completes the sentence below",
            "Which option best matches the earlier past action",
            "Which verb best keeps the timeline in order",
            "Which choice best preserves the past-perfect timeline",
        ),
        "Medium": (
            "Which verb form best fits the two-past-event clue",
            "Which option best matches the earlier completed action",
            "Which verb best completes the action that happened first",
            "Which choice best maintains tense consistency",
        ),
        "Hard": (
            "Which verb phrase best matches the past-perfect frame",
            "Which option best fits the sentence's earlier past reference point",
            "Which verb best completes the action that came first",
            "Which choice best keeps the verb in the past perfect",
        ),
        "Ultra": (
            "Which verb phrase best preserves the sentence's earlier-past logic",
            "Which option best fits the first completed action most precisely",
            "Which verb best keeps the order of events clear",
            "Which choice best maintains tense consistency in the past perfect",
        ),
    },
    "reported-sequence": {
        "Easy": (
            "Which verb phrase best completes the reported statement",
            "Which option best matches the backshifted verb",
            "Which verb best fits the indirect speech clue",
            "Which choice best preserves the reported timeline",
        ),
        "Medium": (
            "Which verb phrase best fits the reported clause",
            "Which option best matches the indirect-speech frame",
            "Which verb best completes the backshifted action",
            "Which choice best maintains tense consistency",
        ),
        "Hard": (
            "Which verb phrase best matches the sequence-of-tenses rule",
            "Which option best fits the sentence's reported reference point",
            "Which verb best completes the indirect statement",
            "Which choice best keeps the reported timeline clear",
        ),
        "Ultra": (
            "Which verb phrase best preserves the sentence's reported-speech logic",
            "Which option best fits the backshift most precisely",
            "Which verb best keeps the indirect statement consistent",
            "Which choice best maintains tense consistency in reported speech",
        ),
    },
}

FAMILY_MARKERS: dict[str, tuple[str, ...]] = {
    "present-reference": ("every", "each", "regular", "whenever", "routine", "before"),
    "past-reference": ("yesterday", "last", "earlier", "during", "on tuesday"),
    "future-reference": ("tomorrow", "next", "later", "when the new schedule is posted", "on friday"),
    "present-perfect": ("so far", "already", "up to now", "recently", "this month"),
    "past-perfect": ("by the time", "before", "long before", "after", "earlier"),
    "reported-sequence": ("said that", "stated that", "reported that", "explained that", "confirmed that"),
}


@dataclass(frozen=True)
class ActionSpec:
    lead: str
    answer: str
    object_phrase: str
    choices: tuple[str, str, str, str]
    note: str
    tail: str = ""


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


def _descriptor(answer: str) -> str:
    return "verb phrase" if " " in answer else "verb"


def _build_choices(choices: tuple[str, str, str, str], rng: random.Random) -> list[str]:
    unique_choices = list(dict.fromkeys(choices))
    if len(unique_choices) != 4:
        raise ValueError(f"choice set must contain 4 distinct items: {choices}")
    rng.shuffle(unique_choices)
    return unique_choices


def _question_stem(family: str, difficulty: str, position: int) -> str:
    stems = QUESTION_STEMS[family][difficulty]
    stem = stems[position % len(stems)]
    return stem.rstrip("?.!")


def _make_item(
    *,
    family: str,
    subject: str,
    action: ActionSpec,
    difficulty: str,
    index: int,
    position: int,
    reported: bool = False,
) -> dict[str, object]:
    if reported:
        sentence = f"{action.lead} {subject} {action.answer} {action.object_phrase}{action.tail}."
    else:
        sentence = f"{action.lead}, {subject} {action.answer} {action.object_phrase}{action.tail}."
    sentence = _cap_sentence(_normalize_sentence(sentence))
    stem = _question_stem(family, difficulty, position)
    question_text = f'{stem}: "{sentence}"'
    rng = random.Random(f"{family}:{difficulty}:{subject}:{action.lead}:{index}")
    choices = _build_choices(action.choices, rng)
    explanation = f"The sentence needs the {_descriptor(action.answer)} {action.answer} because {action.note}."
    tags = [family, difficulty.lower(), "tense-consistency"]

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question_text,
        "choices": choices,
        "answer": action.answer,
        "explanation": explanation,
        "tags": tags,
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _build_standard_family(
    *,
    family: str,
    subjects: tuple[str, str, str, str, str],
    actions: tuple[ActionSpec, ...],
    difficulty: str,
    start_id: int,
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    index = start_id
    position = 0
    for subject in subjects:
        for action in actions:
            items.append(
                _make_item(
                    family=family,
                    subject=subject,
                    action=action,
                    difficulty=difficulty,
                    index=index,
                    position=position,
                    reported=False,
                )
            )
            index += 1
            position += 1
    return items


def _build_reported_family(
    *,
    family: str,
    subjects: tuple[str, str, str, str, str],
    actions: tuple[ActionSpec, ...],
    difficulty: str,
    start_id: int,
) -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    index = start_id
    position = 0
    for subject in subjects:
        for action in actions:
            items.append(
                _make_item(
                    family=family,
                    subject=subject,
                    action=action,
                    difficulty=difficulty,
                    index=index,
                    position=position,
                    reported=True,
                )
            )
            index += 1
            position += 1
    return items


PRESENT_SUBJECTS = (
    "the clerk",
    "the analyst",
    "the manager",
    "the inspector",
    "the supervisor",
)

PAST_SUBJECTS = (
    "the clerk",
    "the analyst",
    "the manager",
    "the inspector",
    "the supervisor",
)

FUTURE_SUBJECTS = (
    "the clerk",
    "the analyst",
    "the manager",
    "the inspector",
    "the supervisor",
)

PRESENT_PERFECT_SUBJECTS = (
    "the clerk",
    "the analyst",
    "the manager",
    "the inspector",
    "the supervisor",
)

PAST_PERFECT_SUBJECTS = (
    "the clerk",
    "the analyst",
    "the manager",
    "the inspector",
    "the supervisor",
)

REPORTED_SUBJECTS = (
    "the clerk",
    "the analyst",
    "the manager",
    "the inspector",
    "the assistant",
)


PRESENT_ACTIONS = (
    ActionSpec(
        lead="Every Monday",
        answer="reviews",
        object_phrase="the filing log",
        choices=("reviews", "reviewed", "will review", "has reviewed"),
        note="the action is a weekly routine",
    ),
    ActionSpec(
        lead="Each morning",
        answer="checks",
        object_phrase="the monthly report",
        choices=("checks", "checked", "will check", "has checked"),
        note="the action is part of a daily routine",
    ),
    ActionSpec(
        lead="On regular workdays",
        answer="files",
        object_phrase="the signed forms",
        choices=("files", "filed", "will file", "has filed"),
        note="the sentence describes a repeated present pattern",
    ),
    ActionSpec(
        lead="Before lunch",
        answer="verifies",
        object_phrase="the figures",
        choices=("verifies", "verified", "will verify", "has verified"),
        note="the action is a routine present-time task",
    ),
    ActionSpec(
        lead="Whenever the office opens",
        answer="approves",
        object_phrase="the request",
        choices=("approves", "approved", "will approve", "has approved"),
        note="the sentence describes a repeated present pattern",
    ),
)

PAST_ACTIONS = (
    ActionSpec(
        lead="Yesterday afternoon",
        answer="reviewed",
        object_phrase="the filing log",
        choices=("reviewed", "reviews", "will review", "has reviewed"),
        note="the event is already finished in the past",
    ),
    ActionSpec(
        lead="Last week",
        answer="checked",
        object_phrase="the monthly report",
        choices=("checked", "checks", "will check", "has checked"),
        note="the time clue points to a completed past action",
    ),
    ActionSpec(
        lead="Earlier that day",
        answer="filed",
        object_phrase="the signed forms",
        choices=("filed", "files", "will file", "has filed"),
        note="the sentence refers to a finished action in the past",
    ),
    ActionSpec(
        lead="During the audit",
        answer="verified",
        object_phrase="the figures",
        choices=("verified", "verifies", "will verify", "has verified"),
        note="the action belongs to a closed past frame",
    ),
    ActionSpec(
        lead="On Tuesday",
        answer="approved",
        object_phrase="the request",
        choices=("approved", "approves", "will approve", "has approved"),
        note="the action happened in a finished past time",
    ),
)

FUTURE_ACTIONS = (
    ActionSpec(
        lead="Tomorrow morning",
        answer="will review",
        object_phrase="the filing log",
        choices=("will review", "reviews", "reviewed", "has reviewed"),
        note="the action happens later than now",
    ),
    ActionSpec(
        lead="Next week",
        answer="will check",
        object_phrase="the monthly report",
        choices=("will check", "checks", "checked", "has checked"),
        note="the action is scheduled for a later time",
    ),
    ActionSpec(
        lead="Later today",
        answer="will file",
        object_phrase="the signed forms",
        choices=("will file", "files", "filed", "has filed"),
        note="the action is still ahead of the reference point",
    ),
    ActionSpec(
        lead="On Friday",
        answer="will verify",
        object_phrase="the figures",
        choices=("will verify", "verifies", "verified", "has verified"),
        note="the sentence points to a later planned action",
    ),
    ActionSpec(
        lead="When the new schedule is posted",
        answer="will approve",
        object_phrase="the request",
        choices=("will approve", "approves", "approved", "has approved"),
        note="the main clause describes an action that will happen later",
    ),
)

PRESENT_PERFECT_ACTIONS = (
    ActionSpec(
        lead="So far this morning",
        answer="has reviewed",
        object_phrase="the filing log",
        choices=("has reviewed", "reviewed", "reviews", "will review"),
        note="the action is completed and still relevant now",
    ),
    ActionSpec(
        lead="Already this week",
        answer="has checked",
        object_phrase="the monthly report",
        choices=("has checked", "checked", "checks", "will check"),
        note="the sentence links a past action to the present",
    ),
    ActionSpec(
        lead="Up to now",
        answer="has filed",
        object_phrase="the signed forms",
        choices=("has filed", "filed", "files", "will file"),
        note="the result of the action matters at the present moment",
    ),
    ActionSpec(
        lead="Recently",
        answer="has verified",
        object_phrase="the figures",
        choices=("has verified", "verified", "verifies", "will verify"),
        note="the action is past but still connected to now",
    ),
    ActionSpec(
        lead="This month",
        answer="has approved",
        object_phrase="the request",
        choices=("has approved", "approved", "approves", "will approve"),
        note="the sentence shows completion within the current time frame",
    ),
)

PAST_PERFECT_ACTIONS = (
    ActionSpec(
        lead="By the time the meeting started",
        answer="had reviewed",
        object_phrase="the filing log",
        choices=("had reviewed", "reviewed", "has reviewed", "will review"),
        note="the filing happened before another past event",
    ),
    ActionSpec(
        lead="Before the supervisor arrived",
        answer="had checked",
        object_phrase="the monthly report",
        choices=("had checked", "checked", "has checked", "will check"),
        note="the checking happened first in the past sequence",
    ),
    ActionSpec(
        lead="Long before noon",
        answer="had filed",
        object_phrase="the signed forms",
        choices=("had filed", "filed", "has filed", "will file"),
        note="the action was already complete before the later past time",
    ),
    ActionSpec(
        lead="Before the call came in",
        answer="had verified",
        object_phrase="the figures",
        choices=("had verified", "verified", "has verified", "will verify"),
        note="the verification happened earlier than the other past event",
    ),
    ActionSpec(
        lead="After the first draft was rejected",
        answer="had approved",
        object_phrase="the request",
        choices=("had approved", "approved", "has approved", "will approve"),
        note="the approval is the earlier completed action in the past frame",
    ),
)

REPORTED_ACTIONS = (
    ActionSpec(
        lead="The supervisor said that",
        answer="had reviewed",
        object_phrase="the filing log",
        choices=("had reviewed", "reviewed", "has reviewed", "will review"),
        note="the reporting verb is past, so the reported action shifts back",
        tail=" before lunch",
    ),
    ActionSpec(
        lead="The memo stated that",
        answer="had checked",
        object_phrase="the monthly report",
        choices=("had checked", "checked", "has checked", "will check"),
        note="the indirect statement requires backshift",
        tail=" before the audit",
    ),
    ActionSpec(
        lead="The officer reported that",
        answer="had filed",
        object_phrase="the signed forms",
        choices=("had filed", "filed", "has filed", "will file"),
        note="the past reporting frame needs the earlier completed form",
        tail=" before the deadline",
    ),
    ActionSpec(
        lead="The clerk explained that",
        answer="had verified",
        object_phrase="the figures",
        choices=("had verified", "verified", "has verified", "will verify"),
        note="the sentence is in reported speech, so the verb shifts back",
        tail=" before the records were sent",
    ),
    ActionSpec(
        lead="The manager confirmed that",
        answer="had approved",
        object_phrase="the request",
        choices=("had approved", "approved", "has approved", "will approve"),
        note="the reported clause keeps the earlier action in past perfect",
        tail=" before the notice was issued",
    ),
)


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

    for question in questions:
        family = str(question["tags"][0])  # type: ignore[index]
        text = str(question["question"]).lower()
        markers = FAMILY_MARKERS[family]
        if not any(marker in text for marker in markers):
            raise ValueError(f"family marker missing for question {question['id']}: {family}")


def _write_bank(questions: list[dict[str, object]]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")


def main() -> int:
    questions: list[dict[str, object]] = []
    index = 1

    family_builders = {
        "present-reference": (
            PRESENT_SUBJECTS,
            PRESENT_ACTIONS,
            _build_standard_family,
        ),
        "past-reference": (
            PAST_SUBJECTS,
            PAST_ACTIONS,
            _build_standard_family,
        ),
        "future-reference": (
            FUTURE_SUBJECTS,
            FUTURE_ACTIONS,
            _build_standard_family,
        ),
        "present-perfect": (
            PRESENT_PERFECT_SUBJECTS,
            PRESENT_PERFECT_ACTIONS,
            _build_standard_family,
        ),
        "past-perfect": (
            PAST_PERFECT_SUBJECTS,
            PAST_PERFECT_ACTIONS,
            _build_standard_family,
        ),
        "reported-sequence": (
            REPORTED_SUBJECTS,
            REPORTED_ACTIONS,
            _build_reported_family,
        ),
    }

    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            subjects, actions, builder = family_builders[family]
            family_items = builder(
                family=family,
                subjects=subjects,
                actions=actions,
                difficulty=difficulty,
                start_id=index,
            )
            questions.extend(family_items)
            index += len(family_items)

    _validate_bank(questions)
    _write_bank(questions)

    difficulty_summary = Counter(str(question["difficulty"]) for question in questions)
    family_summary = Counter(str(question["tags"][0]) for question in questions)  # type: ignore[index]
    print(f"Difficulty summary: {dict(difficulty_summary)}")
    print(f"Family summary: {dict(family_summary)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
