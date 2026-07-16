"""Generate the Prepositions question bank."""

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
    / "prepositions"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Prepositions"
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
    "time-prepositions": {
        "Easy": "Which preposition best completes the time sentence:",
        "Medium": "Which option best fits the time expression:",
        "Hard": "Which choice best matches the time relationship:",
        "Ultra": "Which completion is most accurate for the time phrase:",
    },
    "place-prepositions": {
        "Easy": "Which preposition best completes the place sentence:",
        "Medium": "Which option best fits the location:",
        "Hard": "Which choice best matches the place relationship:",
        "Ultra": "Which completion is most accurate for the location phrase:",
    },
    "direction-prepositions": {
        "Easy": "Which preposition best completes the movement sentence:",
        "Medium": "Which option best fits the direction:",
        "Hard": "Which choice best matches the movement relationship:",
        "Ultra": "Which completion is most accurate for the direction phrase:",
    },
    "verb-collocations": {
        "Easy": "Which preposition best completes the verb pattern:",
        "Medium": "Which option best fits the verb collocation:",
        "Hard": "Which choice best matches the fixed verb pattern:",
        "Ultra": "Which completion is most accurate for the verb phrase:",
    },
    "adjective-collocations": {
        "Easy": "Which preposition best completes the adjective pattern:",
        "Medium": "Which option best fits the adjective collocation:",
        "Hard": "Which choice best matches the fixed adjective pattern:",
        "Ultra": "Which completion is most accurate for the adjective phrase:",
    },
}

CHOICE_POOLS: dict[str, tuple[str, ...]] = {
    "on": ("on", "in", "at", "to"),
    "at": ("at", "in", "on", "to"),
    "in": ("in", "on", "at", "for"),
    "since": ("since", "for", "during", "from"),
    "for": ("for", "since", "during", "to"),
    "between": ("between", "among", "in", "on"),
    "among": ("among", "between", "in", "at"),
    "to": ("to", "into", "onto", "toward"),
    "into": ("into", "to", "onto", "toward"),
    "onto": ("onto", "to", "into", "toward"),
    "toward": ("toward", "to", "into", "from"),
    "from": ("from", "to", "into", "toward"),
    "of": ("of", "with", "for", "to"),
    "with": ("with", "to", "of", "for"),
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


def fr(*pairs: tuple[str, str]) -> tuple[Frame, ...]:
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
    if after:
        return f"{before} ____ {after}."
    return f"{before} ____."


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
            "prepositions",
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
            family="time-prepositions",
            answer="on",
            frames=fr(
                ("The meeting is scheduled", "Monday morning before the audit"),
                ("The forms were submitted", "July 14 by the clerk"),
                ("The report was filed", "Friday afternoon after lunch"),
                ("The briefing will start", "March 3 at the branch"),
                ("The memo arrived", "New Year's Day from the office"),
                ("The call was made", "Wednesday evening after the shift"),
            ),
            explanation="Days and dates take on.",
            tags=("time", "days-and-dates", "calendar"),
        ),
        RowSpec(
            family="time-prepositions",
            answer="at",
            frames=fr(
                ("The office opens", "eight o'clock each day"),
                ("The train left", "noon after the announcement"),
                ("The clerk returned", "midnight without delay"),
                ("The seminar begins", "3:30 p.m. on Friday"),
                ("The guard arrived", "sunrise before patrol"),
                ("The line moved", "half past nine in the morning"),
            ),
            explanation="Exact times and specific moments take at.",
            tags=("time", "clock-time", "specific-moment"),
        ),
        RowSpec(
            family="time-prepositions",
            answer="in",
            frames=fr(
                ("The audit started", "March after the holiday"),
                ("The branch opened", "2022 with a small team"),
                ("The team trained", "summer for three weeks"),
                ("The memo was released", "the morning before the call"),
                ("The records were updated", "winter during the review"),
                ("The conference was held", "September at the main hall"),
            ),
            explanation="Months, years, seasons, and parts of the day take in.",
            tags=("time", "months-years-seasons", "calendar"),
        ),
        RowSpec(
            family="time-prepositions",
            answer="since",
            frames=fr(
                ("The clerk has worked here", "2019"),
                ("The office has used this system", "January"),
                ("The team has been on duty", "last Monday"),
                ("The supervisor has monitored the line", "sunrise"),
                ("The records have been available", "the morning of the audit"),
                ("The branch has operated here", "the new building opened"),
            ),
            explanation="Since marks the starting point of a period that continues now.",
            tags=("time", "starting-point", "present-perfect"),
        ),
        RowSpec(
            family="time-prepositions",
            answer="for",
            frames=fr(
                ("The clerk worked there", "three years before transferring"),
                ("The meeting lasted", "two hours"),
                ("The office has been busy", "several weeks"),
                ("The system remained offline", "a short time"),
                ("The team waited", "an hour outside"),
                ("The manager had studied the file", "many days"),
            ),
            explanation="For expresses duration or length of time.",
            tags=("time", "duration", "length"),
        ),
        RowSpec(
            family="place-prepositions",
            answer="in",
            frames=fr(
                ("The keys were left", "the drawer beside the chair"),
                ("The forms were stored", "the cabinet after sorting"),
                ("The files are kept", "the archive room"),
                ("The letter was found", "the box under the desk"),
                ("The documents were locked", "the safe overnight"),
                ("The pen was hidden", "the bag with the receipts"),
            ),
            explanation="In shows containment or being inside a space.",
            tags=("place", "containment", "inside"),
        ),
        RowSpec(
            family="place-prepositions",
            answer="on",
            frames=fr(
                ("The memo rested", "the table during the meeting"),
                ("The keys were placed", "the counter by the door"),
                ("The notice hung", "the wall near the gate"),
                ("The cup stood", "the shelf above the sink"),
                ("The file lay", "the desk beside the lamp"),
                ("The stamp sat", "the envelope before mailing"),
            ),
            explanation="On shows a surface or something resting on a surface.",
            tags=("place", "surface", "contact"),
        ),
        RowSpec(
            family="place-prepositions",
            answer="at",
            frames=fr(
                ("The guard waited", "the gate outside the compound"),
                ("The clerk met us", "the office entrance"),
                ("The driver stopped", "the station before dusk"),
                ("The team gathered", "the junction near the market"),
                ("The witness stood", "the counter to sign"),
                ("The visitor was seen", "the clinic lobby"),
            ),
            explanation="At is used for a general location, point, or place.",
            tags=("place", "general-location", "point"),
        ),
        RowSpec(
            family="place-prepositions",
            answer="between",
            frames=fr(
                ("The house stood", "the bank and the school"),
                ("The road ran", "the river and the hill"),
                ("The folder was placed", "the memo and the receipt"),
                ("The park lies", "the museum and the station"),
                ("The chair was squeezed", "the window and the desk"),
                ("The meeting was set", "the audit and the briefing"),
            ),
            explanation="Between is used for two distinct items or points.",
            tags=("place", "two-points", "comparison"),
        ),
        RowSpec(
            family="place-prepositions",
            answer="among",
            frames=fr(
                ("The form was buried", "the papers on the tray"),
                ("The rumor spread", "the employees in the hall"),
                ("The report was lost", "the many folders"),
                ("The clerk found the key", "the office supplies"),
                ("The memo was shared", "the team members"),
                ("The badge was hidden", "the records in the drawer"),
            ),
            explanation="Among is used for a group or several items taken together.",
            tags=("place", "group", "collective-location"),
        ),
        RowSpec(
            family="direction-prepositions",
            answer="to",
            frames=fr(
                ("The clerk walked", "the records room after lunch"),
                ("The package was sent", "the branch in Cebu"),
                ("The officer returned", "the desk for review"),
                ("The team moved", "the new office on Monday"),
                ("The file was delivered", "the supervisor for approval"),
                ("The visitor came", "the counter to ask a question"),
            ),
            explanation="To shows a destination or point reached by movement.",
            tags=("movement", "destination", "arrival"),
        ),
        RowSpec(
            family="direction-prepositions",
            answer="into",
            frames=fr(
                ("The box was carried", "the storage room"),
                ("The water flowed", "the basin below"),
                ("The clerk stepped", "the corridor after the call"),
                ("The papers fell", "the drawer during the rush"),
                ("The team moved", "the hall for shelter"),
                ("The cat jumped", "the cart"),
            ),
            explanation="Into shows movement from outside to the inside of something.",
            tags=("movement", "inside-motion", "entry"),
        ),
        RowSpec(
            family="direction-prepositions",
            answer="onto",
            frames=fr(
                ("The report was placed", "the shelf"),
                ("The box slid", "the table"),
                ("The document fell", "the floor"),
                ("The files were moved", "the cart"),
                ("The notice was pinned", "the board"),
                ("The bag was lifted", "the seat"),
            ),
            explanation="Onto shows movement to the surface of something.",
            tags=("movement", "surface-motion", "landing"),
        ),
        RowSpec(
            family="direction-prepositions",
            answer="toward",
            frames=fr(
                ("The officer walked", "the gate"),
                ("The crowd moved", "the exit"),
                ("The light pointed", "the window"),
                ("The car headed", "the town center"),
                ("The clerk leaned", "the speaker"),
                ("The plane turned", "the runway"),
            ),
            explanation="Toward shows direction in the general path of something.",
            tags=("movement", "directional", "approach"),
        ),
        RowSpec(
            family="direction-prepositions",
            answer="from",
            frames=fr(
                ("The memo came", "the director"),
                ("The package arrived", "the branch office"),
                ("The call came", "the supervisor"),
                ("The report was copied", "the archive"),
                ("The team returned", "the site"),
                ("The form was taken", "the tray"),
            ),
            explanation="From shows source, origin, or starting point.",
            tags=("movement", "source", "origin"),
        ),
        RowSpec(
            family="verb-collocations",
            answer="on",
            frames=fr(
                ("The office depends", "accurate records"),
                ("The plan depends", "the final budget"),
                ("The branch relies", "clear instructions"),
                ("The system depends", "regular updates"),
                ("The team depends", "each member doing the task"),
                ("The audit depends", "careful checking"),
            ),
            explanation="Many verbs take fixed prepositions, and depend on is a standard pattern.",
            tags=("verb", "depend-on", "collocation"),
        ),
        RowSpec(
            family="verb-collocations",
            answer="for",
            frames=fr(
                ("The clerk waited", "the courier"),
                ("The applicant asked", "an extra copy"),
                ("The office looked", "the missing file"),
                ("The manager applied", "a transfer"),
                ("The team prepared", "the inspection"),
                ("The witness searched", "the correct form"),
            ),
            explanation="Many verbs take fixed prepositions, and these verbs commonly take for.",
            tags=("verb", "for-pattern", "collocation"),
        ),
        RowSpec(
            family="verb-collocations",
            answer="to",
            frames=fr(
                ("The officer listened", "the announcement"),
                ("The clerk replied", "the supervisor"),
                ("The staff objected", "the proposal"),
                ("The manager spoke", "the visitors after lunch"),
                ("The report referred", "the earlier memo"),
                ("The officer appealed", "the director"),
            ),
            explanation="Many verbs take fixed prepositions, and listen to and reply to are standard patterns.",
            tags=("verb", "to-pattern", "collocation"),
        ),
        RowSpec(
            family="verb-collocations",
            answer="with",
            frames=fr(
                ("The supervisor discussed", "the clerk after lunch"),
                ("The manager met", "the staff in the hall"),
                ("The office complied", "the new rule"),
                ("The committee agreed", "the recommendation"),
                ("The lawyer corresponded", "the client by email"),
                ("The officer checked", "the investigator"),
            ),
            explanation="Many verbs take fixed prepositions, and these verbs commonly take with.",
            tags=("verb", "with-pattern", "collocation"),
        ),
        RowSpec(
            family="verb-collocations",
            answer="of",
            frames=fr(
                ("The committee approved", "the request"),
                ("The class consisted", "ten students"),
                ("The officer thought", "the proposal"),
                ("The clerk heard", "the policy before the memo"),
                ("The child dreamed", "the new uniform"),
                ("The room smelled", "fresh paint"),
            ),
            explanation="Many verbs take fixed prepositions, and these verbs commonly take of.",
            tags=("verb", "of-pattern", "collocation"),
        ),
        RowSpec(
            family="adjective-collocations",
            answer="in",
            frames=fr(
                ("The applicant is interested", "public service"),
                ("The clerk is skilled", "record keeping"),
                ("The officer is involved", "the project"),
                ("The team remained engaged", "the review"),
                ("The soil is rich", "minerals"),
                ("The manager is proficient", "data entry"),
            ),
            explanation="Many adjectives take fixed prepositions, and these adjectives commonly take in.",
            tags=("adjective", "in-pattern", "collocation"),
        ),
        RowSpec(
            family="adjective-collocations",
            answer="for",
            frames=fr(
                ("The supervisor is responsible", "the records"),
                ("The town is famous", "its old bridge"),
                ("The team is ready", "the inspection"),
                ("The clerk was grateful", "the assistance"),
                ("The village is known", "its clean roads"),
                ("The applicant is eligible", "the scholarship"),
            ),
            explanation="Many adjectives take fixed prepositions, and these adjectives commonly take for.",
            tags=("adjective", "for-pattern", "collocation"),
        ),
        RowSpec(
            family="adjective-collocations",
            answer="of",
            frames=fr(
                ("The child is afraid", "the dark"),
                ("The staff are aware", "the delay"),
                ("The office is proud", "its volunteers"),
                ("The team is tired", "the long wait"),
                ("The clerk is capable", "the task"),
                ("The manager is certain", "the date"),
            ),
            explanation="Many adjectives take fixed prepositions, and these adjectives commonly take of.",
            tags=("adjective", "of-pattern", "collocation"),
        ),
        RowSpec(
            family="adjective-collocations",
            answer="to",
            frames=fr(
                ("The report is similar", "the draft"),
                ("The store is close", "the station"),
                ("The workers are accustomed", "the routine"),
                ("The clerk remained attentive", "the details"),
                ("The schedule is subject", "change"),
                ("The officer is dedicated", "public service"),
            ),
            explanation="Many adjectives take fixed prepositions, and these adjectives commonly take to.",
            tags=("adjective", "to-pattern", "collocation"),
        ),
        RowSpec(
            family="adjective-collocations",
            answer="from",
            frames=fr(
                ("The policy is different", "the old rule"),
                ("The annex is separate", "the main building"),
                ("The sample is free", "contamination"),
                ("The children were safe", "harm"),
                ("The witness was absent", "the meeting"),
                ("The new form is distinct", "the draft"),
            ),
            explanation="Many adjectives take fixed prepositions, and these adjectives commonly take from.",
            tags=("adjective", "from-pattern", "collocation"),
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
