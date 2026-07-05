"""Generate the Verbal Ability / Sentence Completion / Grammar Fit bank.

The bank follows the lesson's grammar-fit ladder and deliberately varies the
surface form of the sentence so the item set covers:

- subject-verb agreement
- pronoun case and pronoun fit
- verb tense consistency
- parallel structure
- articles, prepositions, and modifiers
- comparison patterns and mixed grammar checks

Each difficulty band contains 150 items, for 600 items total. The bank is
fully deterministic and writes directly to the seed tree so the reset script
can pick it up automatically.
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
    / "grammar-fit"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Grammar Fit"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

QUESTION_STEMS = {
    "subject-verb": [
        "Which word best completes the sentence below?",
        "Which choice keeps the sentence grammatical?",
        "Which option best fits the blank?",
        "Which word most precisely completes the sentence below?",
    ],
    "pronoun": [
        "Which pronoun best completes the sentence below?",
        "Which choice fits the blank and keeps pronoun case correct?",
        "Which option best completes the sentence grammatically?",
        "Which pronoun most precisely completes the sentence below?",
    ],
    "tense": [
        "Which verb form best completes the sentence below?",
        "Which choice keeps the tense consistent?",
        "Which option best fits the blank in time?",
        "Which verb most precisely completes the sentence below?",
    ],
    "parallelism": [
        "Which choice best preserves parallel structure?",
        "Which option keeps the list balanced?",
        "Which word best completes the sentence in parallel form?",
        "Which choice most precisely completes the sentence below?",
    ],
    "modifiers": [
        "Which word best completes the sentence below?",
        "Which choice best fits the grammar of the sentence?",
        "Which option best completes the blank?",
        "Which word most precisely completes the sentence below?",
    ],
    "comparison": [
        "Which word best completes the comparison?",
        "Which choice best fits the blank?",
        "Which option keeps the sentence grammatical?",
        "Which word most precisely completes the sentence below?",
    ],
}

DIFFICULTY_PREFIXES = {
    "Easy": "",
    "Medium": "After a brief review, ",
    "Hard": "After a brief review, despite the pressure, ",
    "Ultra": "After a brief review, despite the pressure and the time limit, ",
}


@dataclass(frozen=True)
class GroupSpec:
    family: str
    answer: str
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


def _build_choices(answer: str, rng: random.Random) -> list[str]:
    pool = CHOICE_POOLS.get(answer)
    if pool is None:
        raise KeyError(f"missing choice pool for answer: {answer}")
    choices = list(dict.fromkeys(pool))
    if answer not in choices:
        raise ValueError(f"answer {answer!r} missing from choice pool")
    if len(choices) != 4:
        raise ValueError(f"choice pool for {answer!r} must contain 4 distinct items")
    rng.shuffle(choices)
    return choices


def _question_stem(family: str, difficulty: str, index: int) -> str:
    stems = QUESTION_STEMS[family]
    stem = stems[(index + DIFFICULTY_ORDER.index(difficulty)) % len(stems)]
    return stem.rstrip("?.!")


def _difficulty_wrap(sentence: str, difficulty: str) -> str:
    prefix = DIFFICULTY_PREFIXES[difficulty]
    if not prefix:
        return _cap_sentence(_normalize_sentence(sentence))
    return _cap_sentence(_normalize_sentence(f"{prefix}{sentence}"))


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
    choices = _build_choices(answer, rng)
    explanation = _build_explanation(family, answer, note)
    tags = [family, difficulty.lower(), SUBTOPIC.lower().replace(" ", "-")]

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


def _build_explanation(family: str, answer: str, note: str) -> str:
    if family == "subject-verb":
        return f"The sentence needs {answer} because {note}."
    if family == "pronoun":
        return f"The sentence needs {answer} because {note}."
    if family == "tense":
        return f"The sentence needs {answer} because {note}."
    if family == "parallelism":
        return f"The sentence needs {answer} because {note}."
    if family == "modifiers":
        return f"The sentence needs {answer} because {note}."
    return f"The sentence needs {answer} because {note}."


def _expand_groups(groups: list[GroupSpec]) -> list[tuple[str, str, str]]:
    rows: list[tuple[str, str, str]] = []
    for group in groups:
        if len(group.templates) != 5:
            raise ValueError(f"group {group.answer!r} must have 5 templates")
        for template in group.templates:
            rows.append((group.family, group.answer, group.note, template))
    return rows


def _validate_bank(questions: list[dict[str, object]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [int(question["id"]) for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise ValueError(f"unexpected difficulty distribution: {dict(counts)}")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise ValueError("question texts are not unique")

    seen_choices: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        choices = [str(choice) for choice in question["choices"]]  # type: ignore[index]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")
        key = (str(question["question"]), tuple(sorted(choices)))
        if key in seen_choices:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_choices.add(key)


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
    return 0


FAMILY_ORDER = (
    "subject-verb",
    "pronoun",
    "tense",
    "parallelism",
    "modifiers",
    "comparison",
)


GROUPS_BY_FAMILY: dict[str, list[GroupSpec]] = {
    "subject-verb": [
        GroupSpec(
            family="subject-verb",
            answer="is",
            note="the subject is singular",
            templates=(
                "the committee ____ divided on the proposal.",
                "the committee ____ ready for the briefing.",
                "the committee ____ short on time.",
                "the committee ____ in favor of the plan.",
                "the committee ____ responsible for the review.",
            ),
        ),
        GroupSpec(
            family="subject-verb",
            answer="are",
            note="the subject is plural",
            templates=(
                "the officers ____ ready for the briefing.",
                "the officers ____ outside the room.",
                "the officers ____ on duty tonight.",
                "the officers ____ in the lobby.",
                "the officers ____ behind the desk.",
            ),
        ),
        GroupSpec(
            family="subject-verb",
            answer="was",
            note="the subject is singular and the sentence refers to the past",
            templates=(
                "the report ____ approved by the board yesterday.",
                "the report ____ missing from the file yesterday.",
                "the report ____ on the director's desk yesterday.",
                "the report ____ under review yesterday.",
                "the report ____ not ready for release yesterday.",
            ),
        ),
        GroupSpec(
            family="subject-verb",
            answer="were",
            note="the subject is plural and the sentence refers to the past",
            templates=(
                "the files ____ checked by the team last week.",
                "the files ____ shipped to the branch last week.",
                "the files ____ sorted by the clerk last week.",
                "the files ____ moved to storage last week.",
                "the files ____ missing from the cabinet last week.",
            ),
        ),
        GroupSpec(
            family="subject-verb",
            answer="has",
            note="each of + plural noun takes a singular verb",
            templates=(
                "each of the volunteers ____ been assigned a badge.",
                "each of the volunteers ____ already submitted the form.",
                "each of the volunteers ____ a clear task.",
                "each of the volunteers ____ the required materials.",
                "each of the volunteers ____ one question to ask.",
            ),
        ),
    ],
    "pronoun": [
        GroupSpec(
            family="pronoun",
            answer="she",
            note="the blank is the subject of the sentence",
            templates=(
                "____ submitted the report after the meeting.",
                "____ presented the findings during the review.",
                "____ checked the forms before lunch.",
                "____ explained the plan at the briefing.",
                "____ signed the memo later that day.",
            ),
        ),
        GroupSpec(
            family="pronoun",
            answer="her",
            note="the pronoun follows a verb and takes object case",
            templates=(
                "the director thanked ____ after the review.",
                "the officer asked ____ to wait outside.",
                "the reviewer sent the file to ____.",
                "the coach congratulated ____ on the win.",
                "the supervisor praised ____ for the clear summary.",
            ),
        ),
        GroupSpec(
            family="pronoun",
            answer="their",
            note="the pronoun comes before a noun and shows ownership",
            templates=(
                "____ report was filed on time.",
                "____ notes were complete before the meeting.",
                "____ memo was approved by the board.",
                "____ forms were placed on the desk.",
                "____ schedule was posted near the door.",
            ),
        ),
        GroupSpec(
            family="pronoun",
            answer="theirs",
            note="the pronoun stands alone after the verb be",
            templates=(
                "the cabinet near the door is ____.",
                "the folders on the shelf are ____.",
                "the awards on the wall are ____.",
                "the seats in the back are ____.",
                "the final copy is ____.",
            ),
        ),
        GroupSpec(
            family="pronoun",
            answer="herself",
            note="the action returns to the same subject",
            templates=(
                "the assistant prepared the slides by ____.",
                "the clerk reminded ____ to check the list.",
                "the officer trained ____ before the exam.",
                "the analyst praised ____ for the careful work.",
                "the speaker coached ____ to stay calm.",
            ),
        ),
    ],
    "tense": [
        GroupSpec(
            family="tense",
            answer="reviewed",
            note="the sentence points to a completed past action",
            templates=(
                "yesterday, the clerk ____ the records before lunch.",
                "last night, the assistant ____ the forms before leaving.",
                "two days ago, the manager ____ the memo.",
                "earlier, the officer ____ the list.",
                "the team ____ the report before the deadline yesterday.",
            ),
        ),
        GroupSpec(
            family="tense",
            answer="meets",
            note="the sentence describes a repeated present action",
            templates=(
                "every Monday, the manager ____ the team.",
                "every friday, the director ____ with the staff.",
                "each week, the committee ____ to review changes.",
                "on most mornings, the officer ____ with the volunteers.",
                "on schedule, the board ____ to approve requests.",
            ),
        ),
        GroupSpec(
            family="tense",
            answer="had arranged",
            note="one past action happened before another past action",
            templates=(
                "by the time the meeting started, the officers ____ the room.",
                "by the time the notice went out, the team ____ the chairs.",
                "by the time the supervisor arrived, the staff ____ the files.",
                "by dawn, the clerk ____ the documents.",
                "before the call came, the office ____ the schedule.",
            ),
        ),
        GroupSpec(
            family="tense",
            answer="will adopt",
            note="the sentence points to a future action",
            templates=(
                "next week, the office ____ the new procedure.",
                "tomorrow, the board ____ the revised plan.",
                "soon, the agency ____ the new rule.",
                "next month, the committee ____ the updated policy.",
                "later this year, the school ____ the new format.",
            ),
        ),
        GroupSpec(
            family="tense",
            answer="has prepared",
            note="the action began in the past and continues up to now",
            templates=(
                "since dawn, the staff ____ the notice.",
                "for hours, the team ____ the slides.",
                "all morning, the clerk ____ the records.",
                "by now, the office ____ the briefing notes.",
                "since Monday, the analyst ____ the summary.",
            ),
        ),
    ],
    "parallelism": [
        GroupSpec(
            family="parallelism",
            answer="update",
            note="the verb must match the earlier verbs in the list",
            templates=(
                "the officer was asked to file the forms, stamp the receipts, and ____ the log.",
                "the clerk was told to sort the papers, label the folders, and ____ the database.",
                "the assistant must check the list, lock the drawer, and ____ the files.",
                "the team will review the memo, compare the figures, and ____ the report.",
                "the supervisor likes to plan, prepare, and ____ the schedule.",
            ),
        ),
        GroupSpec(
            family="parallelism",
            answer="respond",
            note="the verb must stay parallel to the other infinitives",
            templates=(
                "the trainer asked the staff to listen carefully, speak clearly, and ____ respectfully.",
                "the officer must read the notice, answer politely, and ____ quickly.",
                "the team will review the issue, discuss it calmly, and ____ officially.",
                "the clerk likes to greet visitors, answer questions, and ____ patiently.",
                "the manager expects workers to call back, confirm details, and ____ promptly.",
            ),
        ),
        GroupSpec(
            family="parallelism",
            answer="fairness",
            note="the list needs a noun to match the other nouns",
            templates=(
                "honesty, accuracy, and ____ matter in the office.",
                "discipline, patience, and ____ build trust.",
                "speed, care, and ____ guide the review.",
                "respect, clarity, and ____ are part of the policy.",
                "effort, judgment, and ____ influence the outcome.",
            ),
        ),
        GroupSpec(
            family="parallelism",
            answer="organized",
            note="the blank must match the other adjectives in the list",
            templates=(
                "clear, concise, and ____ writing helps the reader.",
                "calm, careful, and ____ leadership keeps the team steady.",
                "fast, accurate, and ____ filing saves time.",
                "honest, polite, and ____ communication works best.",
                "simple, neat, and ____ records are easier to check.",
            ),
        ),
        GroupSpec(
            family="parallelism",
            answer="approved",
            note="the final word must stay parallel to the passive verb forms",
            templates=(
                "the memo was drafted, revised, and ____ before release.",
                "the plan was discussed, edited, and ____ by the board.",
                "the request was checked, signed, and ____ by the director.",
                "the proposal was reviewed, corrected, and ____ on Monday.",
                "the report was written, polished, and ____ for submission.",
            ),
        ),
    ],
    "modifiers": [
        GroupSpec(
            family="modifiers",
            answer="an",
            note="the next word begins with a vowel sound",
            templates=(
                "she carried ____ umbrella because the forecast was wet.",
                "he needed ____ honest answer from the clerk.",
                "the applicant brought ____ envelope to the desk.",
                "the officer found ____ unusual error in the memo.",
                "the clerk requested ____ urgent update from the team.",
            ),
        ),
        GroupSpec(
            family="modifiers",
            answer="on",
            note="the sentence needs the preposition for a surface or day",
            templates=(
                "the notice was posted ____ the door.",
                "the meeting is ____ Monday.",
                "the folder was placed ____ the desk.",
                "the sign hangs ____ the wall.",
                "the report stayed ____ the shelf.",
            ),
        ),
        GroupSpec(
            family="modifiers",
            answer="in",
            note="the sentence needs the preposition for enclosure or location",
            templates=(
                "the files are stored ____ the cabinet.",
                "the officers waited ____ the lobby.",
                "the memo was filed ____ the drawer.",
                "the map is ____ the binder.",
                "the forms are ____ alphabetical order.",
            ),
        ),
        GroupSpec(
            family="modifiers",
            answer="by",
            note="the sentence needs the preposition showing agency or method",
            templates=(
                "the package was sent ____ courier.",
                "the plan was approved ____ the council.",
                "the message was delivered ____ email.",
                "the report was written ____ hand.",
                "the rules were explained ____ the director.",
            ),
        ),
        GroupSpec(
            family="modifiers",
            answer="Signed",
            note="the participial modifier must match the noun that follows",
            templates=(
                "____ by the supervisor, the notice was sent at once.",
                "____ carefully, the forms were filed in order.",
                "____ before lunch, the memo reached the director.",
                "____ by the committee, the report was released.",
                "____ to the clerk, the package was returned.",
            ),
        ),
    ],
    "comparison": [
        GroupSpec(
            family="comparison",
            answer="than",
            note="the comparison calls for than",
            templates=(
                "the new policy is clearer ____ the old one.",
                "she works faster ____ her colleague does.",
                "the report is more detailed ____ the draft.",
                "the package arrived earlier ____ expected.",
                "the office is busier ____ it was last week.",
            ),
        ),
        GroupSpec(
            family="comparison",
            answer="as",
            note="the comparison uses the as...as pattern",
            templates=(
                "the clerk is as careful ____ the supervisor.",
                "the team is as calm ____ it is organized.",
                "the memo is as helpful ____ the guide.",
                "the officer is as patient ____ the trainer.",
                "the files are as complete ____ the originals.",
            ),
        ),
        GroupSpec(
            family="comparison",
            answer="between",
            note="the sentence compares two items, so between fits",
            templates=(
                "the package was shared ____ the two offices.",
                "the work was divided ____ the manager and the assistant.",
                "the notes were split ____ the two reviewers.",
                "the contract was negotiated ____ the buyer and the seller.",
                "the prize was shared ____ the lead and the support team.",
            ),
        ),
        GroupSpec(
            family="comparison",
            answer="among",
            note="the sentence compares more than two items, so among fits",
            templates=(
                "the data were divided ____ the four units.",
                "the memo was circulated ____ the staff members.",
                "the responsibilities were shared ____ the committee members.",
                "the folders were sorted ____ the files on the table.",
                "the idea spread ____ the students.",
            ),
        ),
        GroupSpec(
            family="comparison",
            answer="who",
            note="the blank is a subject relative pronoun",
            templates=(
                "the applicant ____ submitted the clean file was chosen.",
                "the officer ____ reviewed the case signed the memo.",
                "the person ____ called the office left a message.",
                "the manager ____ arrived first opened the meeting.",
                "the clerk ____ finished early went home.",
            ),
        ),
    ],
}


CHOICE_POOLS: dict[str, list[str]] = {
    "is": ["is", "are", "was", "were"],
    "are": ["are", "is", "was", "were"],
    "was": ["was", "is", "are", "were"],
    "were": ["were", "is", "are", "was"],
    "has": ["has", "have", "had", "is"],
    "she": ["she", "her", "hers", "herself"],
    "her": ["her", "she", "hers", "herself"],
    "their": ["their", "they", "theirs", "them"],
    "theirs": ["theirs", "their", "them", "they"],
    "herself": ["herself", "her", "she", "theirs"],
    "reviewed": ["reviewed", "reviews", "will review", "has reviewed"],
    "meets": ["meets", "met", "will meet", "is meeting"],
    "had arranged": ["had arranged", "arranged", "has arranged", "will arrange"],
    "will adopt": ["will adopt", "adopts", "adopted", "is adopting"],
    "has prepared": ["has prepared", "had prepared", "will prepare", "prepares"],
    "update": ["update", "updates", "updated", "updating"],
    "respond": ["respond", "responds", "responded", "responding"],
    "fairness": ["fairness", "fair", "fairly", "unfair"],
    "organized": ["organized", "organize", "organizing", "organization"],
    "approved": ["approved", "approving", "approves", "approve"],
    "an": ["an", "a", "the", "one"],
    "on": ["on", "in", "at", "by"],
    "in": ["in", "on", "at", "by"],
    "by": ["by", "with", "from", "to"],
    "Signed": ["Signed", "Signing", "Signs", "Sign"],
    "than": ["than", "then", "that", "as"],
    "as": ["as", "than", "then", "so"],
    "between": ["between", "among", "inside", "around"],
    "among": ["among", "between", "inside", "around"],
    "who": ["who", "whom", "whose", "which"],
}


if __name__ == "__main__":
    raise SystemExit(main())
