"""Generate the Verbal Ability / Sentence Completion / Connector Words bank.

The bank covers the major connector families used in CSE sentence completion:

- addition and reinforcement
- contrast and concession
- cause, result, and conclusion
- sequence and time order
- example and restatement
- condition and exception

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
    / "connector-words"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Connector Words"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "addition-reinforcement",
    "contrast-concession",
    "cause-result",
    "sequence-order",
    "example-restatement",
    "condition-exception",
)

QUESTION_STEMS = {
    "addition-reinforcement": {
        "Easy": (
            "Which connector best adds another point",
            "Which word best keeps the idea moving in the same direction",
            "Which connector best reinforces the first idea",
            "Which option best fits the supportive relationship",
        ),
        "Medium": (
            "Which connector best continues the same line of thought",
            "Which word best adds a second point",
            "Which connector best strengthens the first clause",
            "Which option best fits the addition relationship",
        ),
        "Hard": (
            "Which connector best keeps the sentence moving forward",
            "Which word best reinforces the earlier idea",
            "Which connector best extends the support",
            "Which option best fits the additive relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's additive logic",
            "Which word best adds support without changing direction",
            "Which connector best reinforces the message most precisely",
            "Which option best fits the same-direction relationship",
        ),
    },
    "contrast-concession": {
        "Easy": (
            "Which connector best signals contrast",
            "Which word best shows the opposite idea",
            "Which connector best turns the sentence",
            "Which option best fits the concession",
        ),
        "Medium": (
            "Which connector best introduces an opposite idea",
            "Which word best shifts the sentence in another direction",
            "Which connector best shows a turn in meaning",
            "Which option best fits the contrast relationship",
        ),
        "Hard": (
            "Which connector best shows a clear contrast",
            "Which word best admits one fact but keeps the main point",
            "Which connector best marks the turn",
            "Which option best fits the concessive relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's contrastive logic",
            "Which word best shows a precise concession",
            "Which connector best turns without losing the main idea",
            "Which option best fits the opposite-direction relationship",
        ),
    },
    "cause-result": {
        "Easy": (
            "Which connector best shows a reason",
            "Which word best shows a result",
            "Which connector best explains why",
            "Which option best fits the cause-and-effect relationship",
        ),
        "Medium": (
            "Which connector best links a cause to its result",
            "Which word best shows the effect",
            "Which connector best explains the reason",
            "Which option best fits the causal relationship",
        ),
        "Hard": (
            "Which connector best shows why something happened",
            "Which word best shows what happened because of it",
            "Which connector best marks the consequence",
            "Which option best fits the reason-result relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's cause-result logic",
            "Which word best shows the consequence most precisely",
            "Which connector best explains the relationship with clarity",
            "Which option best fits the explanatory relationship",
        ),
    },
    "sequence-order": {
        "Easy": (
            "Which connector best shows order",
            "Which word best marks the next step",
            "Which connector best shows time sequence",
            "Which option best fits the order of events",
        ),
        "Medium": (
            "Which connector best signals the following step",
            "Which word best shows progression",
            "Which connector best keeps the steps in order",
            "Which option best fits the sequence relationship",
        ),
        "Hard": (
            "Which connector best shows the sentence's timeline",
            "Which word best points to the next part",
            "Which connector best marks the transition to another step",
            "Which option best fits the sequential relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's order logic",
            "Which word best shows the movement through steps",
            "Which connector best keeps the chronology clear",
            "Which option best fits the progression relationship",
        ),
    },
    "example-restatement": {
        "Easy": (
            "Which connector best introduces an example",
            "Which connector best restates the idea",
            "Which word best gives a specific case",
            "Which option best fits the illustration or paraphrase",
        ),
        "Medium": (
            "Which connector best gives a concrete example",
            "Which connector best rephrases the same idea",
            "Which word best points to one case",
            "Which option best fits the clarification relationship",
        ),
        "Hard": (
            "Which connector best illustrates the point",
            "Which connector best explains the same idea differently",
            "Which word best introduces a specific instance",
            "Which option best fits the example or restatement relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's clarifying logic",
            "Which connector best gives the precise rephrasing",
            "Which word best highlights one representative case",
            "Which option best fits the illustration relationship",
        ),
    },
    "condition-exception": {
        "Easy": (
            "Which connector best shows a condition",
            "Which word best shows an exception",
            "Which connector best sets a requirement",
            "Which option best fits the rule or limit",
        ),
        "Medium": (
            "Which connector best states a rule",
            "Which word best points to what happens if the rule is not met",
            "Which connector best adds the condition",
            "Which option best fits the conditional relationship",
        ),
        "Hard": (
            "Which connector best shows what must happen first",
            "Which word best shows the exception to the rule",
            "Which connector best sets the limit",
            "Which option best fits the requirement relationship",
        ),
        "Ultra": (
            "Which connector best preserves the sentence's conditional logic",
            "Which word best signals the exception most precisely",
            "Which connector best sets the governing rule",
            "Which option best fits the condition-or-exception relationship",
        ),
    },
}

DIFFICULTY_PREFIXES = {
    "Easy": "",
    "Medium": "During a routine memo review, ",
    "Hard": "During a routine memo review after a second check, ",
    "Ultra": "During a routine memo review after a second check and a schedule change, ",
}


@dataclass(frozen=True)
class GroupSpec:
    family: str
    answer: str
    choice_key: str
    note: str
    templates: tuple[str, str, str, str, str]


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
    return "connector phrase" if " " in answer else "connector"


def _build_choices(choice_key: str, rng: random.Random) -> list[str]:
    pool = CHOICE_POOLS.get(choice_key)
    if pool is None:
        raise KeyError(f"missing choice pool for key: {choice_key}")
    choices = list(dict.fromkeys(pool))
    if len(choices) != 4:
        raise ValueError(f"choice pool for {choice_key!r} must contain 4 distinct items")
    rng.shuffle(choices)
    return choices


def _question_stem(family: str, difficulty: str, index: int) -> str:
    stems = QUESTION_STEMS[family][difficulty]
    stem = stems[(index + DIFFICULTY_ORDER.index(difficulty)) % len(stems)]
    return stem.rstrip("?.!")


def _difficulty_wrap(sentence: str, difficulty: str) -> str:
    prefix = DIFFICULTY_PREFIXES[difficulty]
    if not prefix:
        return _cap_sentence(_normalize_sentence(sentence))
    return _cap_sentence(_normalize_sentence(f"{prefix}{sentence}"))


def _build_explanation(answer: str, note: str) -> str:
    return f"The sentence needs the {_descriptor(answer)} {answer} because {note}."


def _make_item(
    *,
    family: str,
    answer: str,
    note: str,
    sentence: str,
    difficulty: str,
    index: int,
) -> dict[str, object]:
    rng = random.Random(f"{family}:{answer}:{difficulty}:{index}")
    wrapped_sentence = _difficulty_wrap(sentence, difficulty)
    question = _question_stem(family, difficulty, index)
    question_text = f'{question}: "{wrapped_sentence}"'
    choices = _build_choices(CHOICE_KEY_BY_ANSWER[answer], rng)
    explanation = _build_explanation(answer, note)
    tags = [family, difficulty.lower(), "connector-words"]

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question_text,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": CATEGORY,
        "language": LANGUAGE,
    }


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
    questions: list[dict[str, object]] = []
    index = 1

    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for group in GROUPS_BY_FAMILY[family]:
                for template in group.templates:
                    questions.append(
                        _make_item(
                            family=family,
                            answer=group.answer,
                            note=group.note,
                            sentence=template,
                            difficulty=difficulty,
                            index=index,
                        )
                    )
                    index += 1

    _validate_bank(questions)
    _write_bank(questions)

    difficulty_summary = Counter(str(question["difficulty"]) for question in questions)
    family_summary = Counter(str(question["tags"][0]) for question in questions)  # type: ignore[index]
    print(f"Difficulty summary: {dict(difficulty_summary)}")
    print(f"Family summary: {dict(family_summary)}")
    return 0


GROUPS_BY_FAMILY: dict[str, list[GroupSpec]] = {
    "addition-reinforcement": [
        GroupSpec(
            family="addition-reinforcement",
            answer="and",
            choice_key="and",
            note="the second clause adds another action in the same direction",
            templates=(
                "the clerk checked the totals, ____ it verified the signatures.",
                "the analyst compared the figures, ____ it logged the comments.",
                "the team revised the memo, ____ it sent the final copy.",
                "the committee reviewed the request, ____ it filed the notes.",
                "the office counted the forms, ____ it labeled each folder.",
            ),
        ),
        GroupSpec(
            family="addition-reinforcement",
            answer="also",
            choice_key="also",
            note="the second clause adds another point without changing direction",
            templates=(
                "the clerk checked the totals; it ____ verified the signatures.",
                "the analyst compared the figures; it ____ logged the comments.",
                "the team revised the memo; it ____ sent the final copy.",
                "the committee reviewed the request; it ____ filed the notes.",
                "the office counted the forms; it ____ labeled each folder.",
            ),
        ),
        GroupSpec(
            family="addition-reinforcement",
            answer="moreover",
            choice_key="moreover",
            note="the second sentence adds formal reinforcement",
            templates=(
                "the clerk checked the totals; ____, it verified the signatures.",
                "the analyst compared the figures; ____, it logged the comments.",
                "the team revised the memo; ____, it sent the final copy.",
                "the committee reviewed the request; ____, it filed the notes.",
                "the office counted the forms; ____, it labeled each folder.",
            ),
        ),
        GroupSpec(
            family="addition-reinforcement",
            answer="furthermore",
            choice_key="furthermore",
            note="the second sentence adds another formal support point",
            templates=(
                "the clerk checked the totals; ____, it verified the signatures.",
                "the analyst compared the figures; ____, it logged the comments.",
                "the team revised the memo; ____, it sent the final copy.",
                "the committee reviewed the request; ____, it filed the notes.",
                "the office counted the forms; ____, it labeled each folder.",
            ),
        ),
        GroupSpec(
            family="addition-reinforcement",
            answer="in addition",
            choice_key="in addition",
            note="the second sentence adds an extra point in a formal way",
            templates=(
                "the clerk checked the totals. ____, it verified the signatures.",
                "the analyst compared the figures. ____, it logged the comments.",
                "the team revised the memo. ____, it sent the final copy.",
                "the committee reviewed the request. ____, it filed the notes.",
                "the office counted the forms. ____, it labeled each folder.",
            ),
        ),
    ],
    "contrast-concession": [
        GroupSpec(
            family="contrast-concession",
            answer="but",
            choice_key="but",
            note="the second clause presents an opposite idea",
            templates=(
                "the memo was short, ____ it was clear.",
                "the report was late, ____ it was accurate.",
                "the hallway was crowded, ____ the desk area stayed quiet.",
                "the draft looked rough, ____ the main idea was solid.",
                "the file was old, ____ the information was still useful.",
            ),
        ),
        GroupSpec(
            family="contrast-concession",
            answer="however",
            choice_key="however",
            note="the second sentence turns to a contrasting idea",
            templates=(
                "the memo was short; ____, it was clear.",
                "the report was late; ____, it was accurate.",
                "the hallway was crowded; ____, the desk area stayed quiet.",
                "the draft looked rough; ____, the main idea was solid.",
                "the file was old; ____, the information was still useful.",
            ),
        ),
        GroupSpec(
            family="contrast-concession",
            answer="yet",
            choice_key="yet",
            note="the second clause adds a contrast to the first idea",
            templates=(
                "the memo was short, ____ it was clear.",
                "the report was late, ____ it was accurate.",
                "the hallway was crowded, ____ the desk area stayed quiet.",
                "the draft looked rough, ____ the main idea was solid.",
                "the file was old, ____ the information was still useful.",
            ),
        ),
        GroupSpec(
            family="contrast-concession",
            answer="nevertheless",
            choice_key="nevertheless",
            note="the second sentence concedes the first point and keeps going",
            templates=(
                "the memo was short; ____, it was clear.",
                "the report was late; ____, it was accurate.",
                "the hallway was crowded; ____, the desk area stayed quiet.",
                "the draft looked rough; ____, the main idea was solid.",
                "the file was old; ____, the information was still useful.",
            ),
        ),
        GroupSpec(
            family="contrast-concession",
            answer="on the other hand",
            choice_key="on-the-other-hand",
            note="the second sentence presents the other side of the comparison",
            templates=(
                "the branch office had more staff. ____, the main office handled more files.",
                "the report covered fewer pages. ____, it gave more detail.",
                "the desk area was quieter. ____, the lobby was busier.",
                "the memo was shorter. ____, it required more follow-up.",
                "the form was simpler. ____, it still needed two signatures.",
            ),
        ),
    ],
    "cause-result": [
        GroupSpec(
            family="cause-result",
            answer="because",
            choice_key="because",
            note="the second clause gives the reason for the first",
            templates=(
                "the meeting was postponed because the supervisor was ill.",
                "the copies were delayed because the printer jammed.",
                "the forms were rewritten because the original draft was unclear.",
                "the audit took longer because the records were incomplete.",
                "the notice was sent again because the deadline changed.",
            ),
        ),
        GroupSpec(
            family="cause-result",
            answer="so",
            choice_key="so",
            note="the second clause shows the result of the first",
            templates=(
                "the printer jammed, ____ the copies were delayed.",
                "the office lost power, ____ the meeting moved indoors.",
                "the files were mixed up, ____ the clerk sorted them again.",
                "the notes were clear, ____ the team finished quickly.",
                "the room was quiet, ____ the supervisor could speak clearly.",
            ),
        ),
        GroupSpec(
            family="cause-result",
            answer="therefore",
            choice_key="therefore",
            note="the second sentence shows a formal result or conclusion",
            templates=(
                "the office lost power; ____, the meeting moved indoors.",
                "the files were mixed up; ____, the clerk sorted them again.",
                "the notes were clear; ____, the team finished quickly.",
                "the room was quiet; ____, the supervisor could speak clearly.",
                "the file was missing; ____, the search continued.",
            ),
        ),
        GroupSpec(
            family="cause-result",
            answer="thus",
            choice_key="thus",
            note="the second sentence gives a formal conclusion or result",
            templates=(
                "the office lost power; ____, the meeting moved indoors.",
                "the files were mixed up; ____, the clerk sorted them again.",
                "the notes were clear; ____, the team finished quickly.",
                "the room was quiet; ____, the supervisor could speak clearly.",
                "the file was missing; ____, the search continued.",
            ),
        ),
        GroupSpec(
            family="cause-result",
            answer="as a result",
            choice_key="as-a-result",
            note="the second sentence shows the consequence in a formal way",
            templates=(
                "the printer jammed. ____, the copies were delayed.",
                "the office lost power. ____, the meeting moved indoors.",
                "the files were mixed up. ____, the clerk sorted them again.",
                "the notes were clear. ____, the team finished quickly.",
                "the room was quiet. ____, the supervisor could speak clearly.",
            ),
        ),
    ],
    "sequence-order": [
        GroupSpec(
            family="sequence-order",
            answer="first",
            choice_key="first",
            note="the connector shows the beginning of a sequence",
            templates=(
                "____, the clerk sorted the forms.",
                "____, the analyst reviewed the figures.",
                "____, the team checked the schedule.",
                "____, the manager read the memo.",
                "____, the inspector logged the complaint.",
            ),
        ),
        GroupSpec(
            family="sequence-order",
            answer="next",
            choice_key="next",
            note="the connector shows the step that follows the first one",
            templates=(
                "the clerk sorted the forms. ____, it labeled each folder.",
                "the analyst reviewed the figures. ____, it compared the totals.",
                "the team checked the schedule. ____, it sent the reminder.",
                "the manager read the memo. ____, it filed the notes.",
                "the inspector logged the complaint. ____, it called the office.",
            ),
        ),
        GroupSpec(
            family="sequence-order",
            answer="then",
            choice_key="then",
            note="the connector shows the next action in the series",
            templates=(
                "the clerk sorted the forms. ____, it filed each packet.",
                "the analyst reviewed the figures. ____, it marked the changes.",
                "the team checked the schedule. ____, it prepared the room.",
                "the manager read the memo. ____, it sent the reply.",
                "the inspector logged the complaint. ____, it followed up with the staff.",
            ),
        ),
        GroupSpec(
            family="sequence-order",
            answer="afterward",
            choice_key="afterward",
            note="the connector shows a later step in the process",
            templates=(
                "the clerk sorted the forms. ____, it labeled each folder.",
                "the analyst reviewed the figures. ____, it compared the totals.",
                "the team checked the schedule. ____, it sent the reminder.",
                "the manager read the memo. ____, it filed the notes.",
                "the inspector logged the complaint. ____, it called the office.",
            ),
        ),
        GroupSpec(
            family="sequence-order",
            answer="finally",
            choice_key="finally",
            note="the connector shows the last step in the sequence",
            templates=(
                "the clerk sorted the forms. ____, it sealed the packets.",
                "the analyst reviewed the figures. ____, it approved the summary.",
                "the team checked the schedule. ____, it sent the final reminder.",
                "the manager read the memo. ____, it signed the report.",
                "the inspector logged the complaint. ____, it completed the form.",
            ),
        ),
    ],
    "example-restatement": [
        GroupSpec(
            family="example-restatement",
            answer="for example",
            choice_key="for-example",
            note="the second sentence gives one concrete case",
            templates=(
                "the policy allowed several checks. ____, it required two signatures.",
                "the rule covered several delays. ____, it included late deliveries.",
                "the notice listed several items. ____, it named the filing deadline.",
                "the guide mentioned several tasks. ____, it showed the review step.",
                "the memo allowed several options. ____, it suggested a second review.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="for instance",
            choice_key="for-instance",
            note="the second sentence gives a specific case",
            templates=(
                "the policy allowed several checks. ____, it required two signatures.",
                "the rule covered several delays. ____, it included late deliveries.",
                "the notice listed several items. ____, it named the filing deadline.",
                "the guide mentioned several tasks. ____, it showed the review step.",
                "the memo allowed several options. ____, it suggested a second review.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="specifically",
            choice_key="specifically",
            note="the second sentence points to one exact detail",
            templates=(
                "the policy allowed several checks. ____, it required two signatures.",
                "the rule covered several delays. ____, it included late deliveries.",
                "the notice listed several items. ____, it named the filing deadline.",
                "the guide mentioned several tasks. ____, it showed the review step.",
                "the memo allowed several options. ____, it suggested a second review.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="namely",
            choice_key="namely",
            note="the second sentence introduces the specific item named",
            templates=(
                "the policy allowed several checks, ____ two signatures for every release.",
                "the rule covered several delays, ____ late deliveries and missed pickups.",
                "the notice listed several items, ____ the filing deadline and the contact name.",
                "the guide mentioned several tasks, ____ the review step and the approval step.",
                "the memo allowed several options, ____ a second review and a final check.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="in other words",
            choice_key="in-other-words",
            note="the second sentence restates the idea in clearer terms",
            templates=(
                "the policy allowed several checks. ____, it needed more than one signature.",
                "the rule covered several delays. ____, late deliveries counted too.",
                "the notice listed several items. ____, the filing deadline mattered most.",
                "the guide mentioned several tasks. ____, the review step came first.",
                "the memo allowed several options. ____, a second review was expected.",
            ),
        ),
    ],
    "condition-exception": [
        GroupSpec(
            family="condition-exception",
            answer="if",
            choice_key="if",
            note="the connector sets a condition for the action",
            templates=(
                "if the signature is missing, the clerk returns the form.",
                "if the deadline changes, the office sends a new notice.",
                "if the figures are incomplete, the analyst checks them again.",
                "if the room is full, the manager moves the briefing.",
                "if the file is damaged, the team makes a copy.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="unless",
            choice_key="unless",
            note="the connector shows an exception to the rule",
            templates=(
                "the form will be accepted unless the signature is missing.",
                "the meeting will start unless the supervisor calls first.",
                "the report will be filed unless the figures need another check.",
                "the notice will stand unless the deadline changes again.",
                "the desk will stay open unless the office loses power.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="provided that",
            choice_key="provided-that",
            note="the connector sets a requirement that must be satisfied",
            templates=(
                "the request will be approved provided that the figures are verified.",
                "the room will be reserved provided that the schedule is confirmed.",
                "the form will be processed provided that the attachment is complete.",
                "the summary will be released provided that the manager signs it.",
                "the record will be updated provided that the date is checked.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="otherwise",
            choice_key="otherwise",
            note="the connector shows what happens if the condition is not met",
            templates=(
                "the clerk should resend the notice, ____ the deadline will be missed.",
                "the analyst must check the totals, ____ the report will be incomplete.",
                "the team should confirm the schedule, ____ the meeting will start late.",
                "the manager has to sign the memo, ____ the file will remain pending.",
                "the office needs to review the form, ____ the request will be delayed.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="even if",
            choice_key="even-if",
            note="the connector shows that the main action still happens despite the condition",
            templates=(
                "even if the line is long, the office will keep the counter open.",
                "even if the file is old, the clerk will still check it.",
                "even if the room is crowded, the briefing will continue.",
                "even if the memo is brief, the manager will review it carefully.",
                "even if the deadline is tight, the team will finish the draft.",
            ),
        ),
    ],
}


CHOICE_KEY_BY_ANSWER: dict[str, str] = {
    "and": "and",
    "also": "also",
    "moreover": "moreover",
    "furthermore": "furthermore",
    "in addition": "in addition",
    "but": "but",
    "however": "however",
    "yet": "yet",
    "nevertheless": "nevertheless",
    "on the other hand": "on-the-other-hand",
    "because": "because",
    "so": "so",
    "therefore": "therefore",
    "thus": "thus",
    "as a result": "as-a-result",
    "first": "first",
    "next": "next",
    "then": "then",
    "afterward": "afterward",
    "finally": "finally",
    "for example": "for-example",
    "for instance": "for-instance",
    "specifically": "specifically",
    "namely": "namely",
    "in other words": "in-other-words",
    "if": "if",
    "unless": "unless",
    "provided that": "provided-that",
    "otherwise": "otherwise",
    "even if": "even-if",
}


CHOICE_POOLS: dict[str, list[str]] = {
    "and": ["and", "however", "because", "unless"],
    "also": ["also", "however", "therefore", "unless"],
    "moreover": ["moreover", "but", "because", "for example"],
    "furthermore": ["furthermore", "yet", "because", "if"],
    "in addition": ["in addition", "however", "so", "for example"],
    "but": ["but", "therefore", "also", "unless"],
    "however": ["however", "and", "because", "for example"],
    "yet": ["yet", "therefore", "also", "unless"],
    "nevertheless": ["nevertheless", "so", "for instance", "if"],
    "on-the-other-hand": ["on the other hand", "because", "also", "unless"],
    "because": ["because", "so", "however", "for example"],
    "so": ["so", "however", "for example", "unless"],
    "therefore": ["therefore", "because", "also", "unless"],
    "thus": ["thus", "however", "also", "for example"],
    "as-a-result": ["as a result", "however", "also", "unless"],
    "first": ["first", "however", "because", "for example"],
    "next": ["next", "yet", "unless", "however"],
    "then": ["then", "however", "because", "for example"],
    "afterward": ["afterward", "therefore", "also", "unless"],
    "finally": ["finally", "however", "because", "also"],
    "for-example": ["for example", "therefore", "however", "unless"],
    "for-instance": ["for instance", "also", "yet", "if"],
    "specifically": ["specifically", "however", "moreover", "unless"],
    "namely": ["namely", "however", "also", "unless"],
    "in-other-words": ["in other words", "therefore", "instead", "for example"],
    "if": ["if", "however", "therefore", "for example"],
    "unless": ["unless", "also", "then", "because"],
    "provided-that": ["provided that", "therefore", "instead", "for example"],
    "otherwise": ["otherwise", "however", "moreover", "if"],
    "even-if": ["even if", "however", "therefore", "for example"],
}


FAMILY_MARKERS: dict[str, tuple[str, ...]] = {
    "addition-reinforcement": ("adds another point", "same direction", "reinforces", "supportive", "addition relationship"),
    "contrast-concession": ("contrast", "opposite idea", "turns", "concession", "opposite-direction"),
    "cause-result": ("reason", "result", "explains why", "cause-and-effect", "causal", "consequence"),
    "sequence-order": ("order", "next step", "time sequence", "sequence", "timeline", "order of events"),
    "example-restatement": ("example", "restates", "specific case", "illustration", "paraphrase", "clarification"),
    "condition-exception": ("condition", "exception", "requirement", "rule or limit", "conditional"),
}


def main() -> int:
    questions: list[dict[str, object]] = []
    index = 1

    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for group in GROUPS_BY_FAMILY[family]:
                for template in group.templates:
                    questions.append(
                        _make_item(
                            family=family,
                            answer=group.answer,
                            note=group.note,
                            sentence=template,
                            difficulty=difficulty,
                            index=index,
                        )
                    )
                    index += 1

    _validate_bank(questions)
    _write_bank(questions)

    difficulty_summary = Counter(str(question["difficulty"]) for question in questions)
    family_summary = Counter(str(question["tags"][0]) for question in questions)  # type: ignore[index]
    print(f"Difficulty summary: {dict(difficulty_summary)}")
    print(f"Family summary: {dict(family_summary)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

