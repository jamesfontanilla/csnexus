"""Generate the Modifier Placement question bank."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "error-recognition"
    / "modifier-placement"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Modifier Placement"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

PROMPT_PREFIXES: dict[str, dict[str, str]] = {
    "dangling-participial": {
        "Easy": "Which phrase best completes the sentence and keeps the modifier attached to the right subject:",
        "Medium": "Which option best fixes the dangling participial modifier:",
        "Hard": "Which choice best makes the introductory action clear:",
        "Ultra": "Which completion is most accurate for the participial modifier:",
    },
    "dangling-infinitive": {
        "Easy": "Which phrase best completes the sentence and makes the doer clear:",
        "Medium": "Which option best fixes the dangling infinitive:",
        "Hard": "Which choice best makes the purpose phrase clear:",
        "Ultra": "Which completion is most accurate for the infinitive modifier:",
    },
    "adverb-placement": {
        "Easy": "Which word best completes the sentence with clear modifier placement:",
        "Medium": "Which option best places the adverb correctly:",
        "Hard": "Which choice best keeps the adverb near its target:",
        "Ultra": "Which completion is most accurate for the adverb placement:",
    },
    "prepositional-attachment": {
        "Easy": "Which phrase best completes the sentence so the modifier points to the intended noun:",
        "Medium": "Which option best fixes the attachment of the prepositional phrase:",
        "Hard": "Which choice best keeps the modifier near the right noun:",
        "Ultra": "Which completion is most accurate for the attachment:",
    },
    "squinting-modifiers": {
        "Easy": "Which completion best removes the ambiguity:",
        "Medium": "Which option best resolves the squinting modifier:",
        "Hard": "Which choice best makes the time or frequency clear:",
        "Ultra": "Which completion is most accurate for the ambiguous modifier:",
    },
}

CHOICE_POOLS: dict[str, tuple[str, ...]] = {
    "after checking the figures": (
        "after checking the figures",
        "checking after the figures",
        "after the figures checking",
        "the figures after checking",
    ),
    "having reviewed the memo": (
        "having reviewed the memo",
        "reviewing having the memo",
        "the memo having reviewed",
        "memo reviewed having",
    ),
    "while carrying the boxes": (
        "while carrying the boxes",
        "carrying while the boxes",
        "the boxes while carrying",
        "while the boxes carrying",
    ),
    "before leaving the office": (
        "before leaving the office",
        "leaving before the office",
        "the office before leaving",
        "before the office leaving",
    ),
    "after reading the notice": (
        "after reading the notice",
        "reading after the notice",
        "the notice after reading",
        "after the notice reading",
    ),
    "to avoid confusion": (
        "to avoid confusion",
        "for avoiding confusion",
        "avoiding to confusion",
        "to confusion avoid",
    ),
    "to save time": (
        "to save time",
        "for save time",
        "saving to time",
        "to time save",
    ),
    "to keep the records safe": (
        "to keep the records safe",
        "for keeping the records safe",
        "keeping to the records safe",
        "to the records safe keep",
    ),
    "to explain the delay": (
        "to explain the delay",
        "for explaining the delay",
        "explaining to the delay",
        "to the delay explain",
    ),
    "to finish the task": (
        "to finish the task",
        "for finishing the task",
        "finishing to the task",
        "to the task finish",
    ),
    "carefully": ("carefully", "careful", "carelessly", "careless"),
    "only": ("only", "just", "already", "almost"),
    "almost": ("almost", "hardly", "clearly", "usually"),
    "already": ("already", "still", "often", "just"),
    "often": ("often", "seldom", "never", "once"),
    "with red labels": (
        "with red labels",
        "with labels red",
        "red with labels",
        "with the red label",
    ),
    "from the old branch": (
        "from the old branch",
        "from branch the old",
        "the old branch from",
        "branch from the old",
    ),
    "near the entrance": (
        "near the entrance",
        "at the entrance",
        "beside the entrance",
        "near entrance",
    ),
    "in the storage room": (
        "in the storage room",
        "the storage room in",
        "storage in the room",
        "in room the storage",
    ),
    "on the top shelf": (
        "on the top shelf",
        "the top shelf on",
        "on shelf the top",
        "top on the shelf",
    ),
    "yesterday": ("yesterday", "today", "tomorrow", "daily"),
    "later": ("later", "earlier", "soon", "always"),
    "soon": ("soon", "later", "already", "daily"),
    "for now": ("for now", "at once", "soon", "daily"),
    "at once": ("at once", "later", "yesterday", "often"),
}


@dataclass(frozen=True)
class Frame:
    before: str
    after: str


@dataclass(frozen=True)
class RowSpec:
    family: str
    answer: str
    frames: tuple[Frame, ...]
    explanation: str
    tags: tuple[str, ...]


def start(*afters: str) -> tuple[Frame, ...]:
    return tuple(Frame(before="", after=after) for after in afters)


def end(*befores: str) -> tuple[Frame, ...]:
    return tuple(Frame(before=before, after="") for before in befores)


def mid(*pairs: tuple[str, str]) -> tuple[Frame, ...]:
    return tuple(Frame(before=before, after=after) for before, after in pairs)


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def _compose_sentence(frame: Frame) -> str:
    before = " ".join(frame.before.split())
    after = " ".join(frame.after.split())
    if before and after:
        return f"{before} ____ {after}."
    if before:
        return f"{before} ____."
    if after:
        if after[0] in ",.;:?!":
            return f"____{after}."
        return f"____ {after}."
    return "____."


def _build_question(
    *,
    question_id: int,
    row: RowSpec,
    frame: Frame,
    frame_index: int,
    difficulty: str,
) -> dict:
    prefix = PROMPT_PREFIXES[row.family][difficulty]
    sentence = _compose_sentence(frame)
    choices = _dedupe_preserve_order(CHOICE_POOLS[row.answer])
    if len(choices) != 4:
        raise ValueError(f"expected 4 unique choices for answer {row.answer!r}")
    if row.answer not in choices:
        raise ValueError(f"answer {row.answer!r} missing from choices")
    rotation = (question_id + frame_index) % 4
    choices = choices[rotation:] + choices[:rotation]

    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": f'{prefix} "{sentence}"',
        "choices": choices,
        "answer": row.answer,
        "explanation": row.explanation,
        "tags": [
            "modifier-placement",
            row.family,
            DIFFICULTY_TAGS[difficulty],
            *row.tags,
        ],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _validate_bank(items: list[dict]) -> None:
    if len(items) != 600:
        raise ValueError(f"expected 600 questions, found {len(items)}")

    expected_difficulties = {difficulty: 150 for difficulty in DIFFICULTIES}
    actual_difficulties: dict[str, int] = {difficulty: 0 for difficulty in DIFFICULTIES}
    actual_families: Counter[str] = Counter()
    seen_questions: set[str] = set()

    for index, item in enumerate(items, start=1):
        if item.get("id") != index:
            raise ValueError(
                f"question ids must be sequential; found {item.get('id')} at position {index}"
            )

        difficulty = str(item.get("difficulty", "")).strip()
        if difficulty not in actual_difficulties:
            raise ValueError(f"invalid difficulty {difficulty!r} at id {index}")
        actual_difficulties[difficulty] += 1

        question = str(item.get("question", "")).strip()
        if not question:
            raise ValueError(f"blank question text at id {index}")
        if "  " in question:
            raise ValueError(f"double space found in question text at id {index}")
        if question in seen_questions:
            raise ValueError(f"duplicate question text at id {index}")
        seen_questions.add(question)

        choices = item.get("choices")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"invalid choices at id {index}")
        normalized = [str(choice).strip() for choice in choices]
        if any(not choice for choice in normalized):
            raise ValueError(f"blank choice at id {index}")
        if len(set(normalized)) != len(normalized):
            raise ValueError(f"duplicate choices at id {index}")
        answer = str(item.get("answer", "")).strip()
        if answer not in normalized:
            raise ValueError(f"answer {answer!r} not present in choices at id {index}")

        explanation = str(item.get("explanation", "")).strip()
        if not explanation:
            raise ValueError(f"blank explanation at id {index}")

        tags = item.get("tags")
        if not isinstance(tags, list) or len(tags) < 3:
            raise ValueError(f"invalid tags at id {index}")
        actual_families[str(tags[1])] += 1

    if actual_difficulties != expected_difficulties:
        raise ValueError(f"unexpected difficulty counts: {actual_difficulties}")

    expected_family_counts = {family: 120 for family in PROMPT_PREFIXES}
    if dict(actual_families) != expected_family_counts:
        raise ValueError(f"unexpected family counts: {dict(actual_families)}")


def _rows() -> tuple[RowSpec, ...]:
    return (
        RowSpec(
            family="dangling-participial",
            answer="after checking the figures",
            frames=start(
                ", the clerk signed the report before leaving",
                ", the analyst corrected the totals after lunch",
                ", the guard checked the badges at the gate",
                ", the committee approved the request",
                ", the staff updated the log",
                ", the supervisor filed the memo",
            ),
            explanation="The introductory action should clearly belong to the subject that follows.",
            tags=("dangling", "participial", "introductory-phrase"),
        ),
        RowSpec(
            family="dangling-participial",
            answer="having reviewed the memo",
            frames=start(
                ", the director met the staff in the hall",
                ", the officer sent the summary to records",
                ", the clerk prepared the reply before noon",
                ", the team confirmed the schedule",
                ", the manager signed the notice",
                ", the auditor closed the file",
            ),
            explanation="The participial phrase must attach to a clear doer in the main clause.",
            tags=("dangling", "participial", "introductory-phrase"),
        ),
        RowSpec(
            family="dangling-participial",
            answer="while carrying the boxes",
            frames=start(
                ", the worker slipped on the steps",
                ", the volunteers crossed the hallway",
                ", the porter entered the archive room",
                ", the messenger climbed the stairs",
                ", the students moved toward the exit",
                ", the guard opened the side door",
            ),
            explanation="The phrase has to modify the person doing the carrying, not an object or place.",
            tags=("dangling", "participial", "introductory-phrase"),
        ),
        RowSpec(
            family="dangling-participial",
            answer="before leaving the office",
            frames=start(
                ", the assistant locked the drawer",
                ", the clerk returned the key",
                ", the manager switched off the lamp",
                ", the staff checked the door",
                ", the officer filed the memo",
                ", the trainee signed the log",
            ),
            explanation="The introductory phrase needs a logical subject in the main clause.",
            tags=("dangling", "participial", "introductory-phrase"),
        ),
        RowSpec(
            family="dangling-participial",
            answer="after reading the notice",
            frames=start(
                ", the applicant asked for help",
                ", the visitors returned to the desk",
                ", the staff called the office",
                ", the clerk took down the number",
                ", the team changed the schedule",
                ", the supervisor sent a reply",
            ),
            explanation="The participial phrase must clearly point to the reader or actor in the main clause.",
            tags=("dangling", "participial", "introductory-phrase"),
        ),
        RowSpec(
            family="dangling-infinitive",
            answer="to avoid confusion",
            frames=start(
                ", the clerk labeled the folders carefully",
                ", the manager separated the forms by date",
                ", the office posted the notices early",
                ", the staff organized the trays",
                ", the analyst marked the pages clearly",
                ", the team checked the labels twice",
            ),
            explanation="The infinitive phrase should clearly belong to the subject that follows.",
            tags=("dangling", "infinitive", "purpose"),
        ),
        RowSpec(
            family="dangling-infinitive",
            answer="to save time",
            frames=start(
                ", the supervisor grouped the files",
                ", the clerk filled out the form",
                ", the manager copied the report",
                ", the office sent the memo",
                ", the staff sorted the records",
                ", the team reviewed the checklist",
            ),
            explanation="The purpose phrase needs a clear doer in the main clause.",
            tags=("dangling", "infinitive", "purpose"),
        ),
        RowSpec(
            family="dangling-infinitive",
            answer="to keep the records safe",
            frames=start(
                ", the clerk locked the cabinet",
                ", the archivist sealed the box",
                ", the office stored the files",
                ", the manager moved the folder",
                ", the staff covered the tray",
                ", the team secured the drawer",
            ),
            explanation="The sentence should make clear who is trying to keep the records safe.",
            tags=("dangling", "infinitive", "purpose"),
        ),
        RowSpec(
            family="dangling-infinitive",
            answer="to explain the delay",
            frames=start(
                ", the director sent a note",
                ", the clerk answered the call",
                ", the manager wrote a memo",
                ", the office issued a statement",
                ", the supervisor replied to the email",
                ", the assistant spoke to the staff",
            ),
            explanation="The infinitive phrase must attach to a logical subject that can explain the delay.",
            tags=("dangling", "infinitive", "purpose"),
        ),
        RowSpec(
            family="dangling-infinitive",
            answer="to finish the task",
            frames=start(
                ", the clerk stayed late",
                ", the team worked through lunch",
                ", the manager returned after hours",
                ", the staff continued after the meeting",
                ", the analyst stayed at the desk",
                ", the officer remained in the office",
            ),
            explanation="The purpose phrase needs a clear doer so the sentence does not dangle.",
            tags=("dangling", "infinitive", "purpose"),
        ),
        RowSpec(
            family="adverb-placement",
            answer="carefully",
            frames=mid(
                ("The clerk", "filed the report before lunch"),
                ("The analyst", "checked the totals after the audit"),
                ("The guard", "locked the gate at dusk"),
                ("The supervisor", "signed the memo quickly"),
                ("The team", "packed the forms in order"),
                ("The officer", "sorted the files after the meeting"),
            ),
            explanation="The adverb should sit beside the verb it modifies.",
            tags=("adverb", "verb-placement", "clarity"),
        ),
        RowSpec(
            family="adverb-placement",
            answer="only",
            frames=mid(
                ("The manager", "approved the budget after review"),
                ("The clerk", "filed the report yesterday"),
                ("The committee", "accepted the request"),
                ("The officer", "checked the badge"),
                ("The staff", "reviewed the forms"),
                ("The supervisor", "called the witness"),
            ),
            explanation="The adverb should be positioned where the intended emphasis is clear.",
            tags=("adverb", "emphasis", "only"),
        ),
        RowSpec(
            family="adverb-placement",
            answer="almost",
            frames=mid(
                ("The train", "stopped at the station"),
                ("The clerk", "finished the audit when the call came"),
                ("The team", "missed the deadline"),
                ("The driver", "reached the gate"),
                ("The office", "closed when the alarm rang"),
                ("The inspector", "completed the inspection"),
            ),
            explanation="The adverb should be close enough to the verb so the degree is clear.",
            tags=("adverb", "degree", "almost"),
        ),
        RowSpec(
            family="adverb-placement",
            answer="already",
            frames=mid(
                ("The officer", "submitted the report before noon"),
                ("The clerk", "sent the memo"),
                ("The team", "reviewed the file"),
                ("The manager", "signed the notice"),
                ("The branch", "opened the new desk"),
                ("The staff", "prepared the log"),
            ),
            explanation="The adverb should go in a place that makes the timing clear.",
            tags=("adverb", "time", "already"),
        ),
        RowSpec(
            family="adverb-placement",
            answer="often",
            frames=mid(
                ("The office", "receives complaints in writing"),
                ("The supervisor", "checks the log"),
                ("The clerk", "verifies the forms"),
                ("The team", "meets after lunch"),
                ("The manager", "reviews the schedule"),
                ("The officer", "visits the records room"),
            ),
            explanation="The frequency adverb should sit near the action it modifies.",
            tags=("adverb", "frequency", "often"),
        ),
        RowSpec(
            family="prepositional-attachment",
            answer="with red labels",
            frames=end(
                "The clerk filed the folders",
                "The manager packed the envelopes",
                "The assistant sorted the trays",
                "The archivist arranged the boxes",
                "The office stored the files",
                "The staff marked the drawers",
            ),
            explanation="The prepositional phrase should attach to the noun it describes, not drift away from it.",
            tags=("prepositional-phrase", "attachment", "noun-target"),
        ),
        RowSpec(
            family="prepositional-attachment",
            answer="from the old branch",
            frames=end(
                "The office received the memo",
                "The team welcomed the inspector",
                "The clerk copied the form",
                "The branch imported the records",
                "The supervisor heard the update",
                "The committee got the report",
            ),
            explanation="The phrase should stay close to the word that needs the source information.",
            tags=("prepositional-phrase", "attachment", "source"),
        ),
        RowSpec(
            family="prepositional-attachment",
            answer="near the entrance",
            frames=end(
                "The guard waited",
                "The visitors stood",
                "The clerk posted the notice",
                "The driver parked the cart",
                "The supervisor greeted the team",
                "The officer placed the sign",
            ),
            explanation="The phrase should sit where it clearly describes the location.",
            tags=("prepositional-phrase", "attachment", "location"),
        ),
        RowSpec(
            family="prepositional-attachment",
            answer="in the storage room",
            frames=end(
                "The clerk placed the boxes",
                "The staff kept the forms",
                "The manager stored the folders",
                "The worker locked the spare files",
                "The archivist left the duplicates",
                "The office hid the old ledgers",
            ),
            explanation="The phrase should be placed where it obviously modifies the action or object.",
            tags=("prepositional-phrase", "attachment", "location"),
        ),
        RowSpec(
            family="prepositional-attachment",
            answer="on the top shelf",
            frames=end(
                "The helper stacked the jars",
                "The clerk left the envelope",
                "The worker placed the tray",
                "The assistant put the manuals",
                "The manager stored the file",
                "The staff kept the box",
            ),
            explanation="The prepositional phrase must stay close enough to show the intended location.",
            tags=("prepositional-phrase", "attachment", "location"),
        ),
        RowSpec(
            family="squinting-modifiers",
            answer="yesterday",
            frames=end(
                "The supervisor said the memo was ready",
                "The clerk reported the files were missing",
                "The manager explained the form had arrived",
                "The officer announced the audit was postponed",
                "The director stated the staff should wait",
                "The assistant noted the package was late",
            ),
            explanation="The time word should be placed where it clearly modifies the intended clause.",
            tags=("squinting", "time", "ambiguity"),
        ),
        RowSpec(
            family="squinting-modifiers",
            answer="later",
            frames=end(
                "The witness said the meeting would resume",
                "The clerk noted the records would arrive",
                "The supervisor explained the memo would follow",
                "The manager stated the branch would call",
                "The officer reported the courier would return",
                "The director confirmed the team would meet",
            ),
            explanation="The adverb should be placed so the reader knows what event it belongs to.",
            tags=("squinting", "time", "ambiguity"),
        ),
        RowSpec(
            family="squinting-modifiers",
            answer="soon",
            frames=end(
                "The office said the results would come",
                "The clerk replied the notice would be sent",
                "The manager explained the package would arrive",
                "The officer said the form would be released",
                "The director stated the memo would follow",
                "The assistant noted the audit would begin",
            ),
            explanation="The time word should be placed where it cannot be read as modifying the wrong clause.",
            tags=("squinting", "time", "ambiguity"),
        ),
        RowSpec(
            family="squinting-modifiers",
            answer="for now",
            frames=end(
                "The supervisor said the line would stay open",
                "The clerk explained the desk would remain closed",
                "The manager noted the archive would stay separate",
                "The officer reported the file would remain pending",
                "The director stated the order would hold",
                "The assistant confirmed the records would stay sealed",
            ),
            explanation="The phrase should be positioned so it clearly describes the temporary state.",
            tags=("squinting", "time", "ambiguity"),
        ),
        RowSpec(
            family="squinting-modifiers",
            answer="at once",
            frames=end(
                "The chief said the team would return",
                "The clerk explained the report would be delivered",
                "The manager stated the issue should be handled",
                "The officer reported the witness should come",
                "The director confirmed the call should be answered",
                "The assistant noted the forms should be checked",
            ),
            explanation="The adverb should sit where it clearly indicates immediate action.",
            tags=("squinting", "time", "ambiguity"),
        ),
    )


def _generate() -> list[dict]:
    items: list[dict] = []
    question_id = 1
    rows = _rows()

    for difficulty in DIFFICULTIES:
        for row in rows:
            for frame_index, frame in enumerate(row.frames):
                items.append(
                    _build_question(
                        question_id=question_id,
                        row=row,
                        frame=frame,
                        frame_index=frame_index,
                        difficulty=difficulty,
                    )
                )
                question_id += 1

    _validate_bank(items)
    return items


def main() -> None:
    items = _generate()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(items, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(items)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
