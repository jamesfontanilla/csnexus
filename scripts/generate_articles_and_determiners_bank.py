"""Generate the Articles and Determiners question bank."""

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
    / "articles-and-determiners"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Articles and Determiners"
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
    "article-sound": {
        "Easy": "Which article best completes the sentence:",
        "Medium": "Which option best follows the sound rule:",
        "Hard": "Which choice best applies the pronunciation rule:",
        "Ultra": "Which completion is most accurate by sound:",
    },
    "definite-the": {
        "Easy": "Which article best completes the specific sentence:",
        "Medium": "Which option best fits the definite-article rule:",
        "Hard": "Which choice best uses the definite article:",
        "Ultra": "Which completion is most accurate for the definite article:",
    },
    "zero-article": {
        "Easy": "Which option best completes the sentence with no article:",
        "Medium": "Which option best fits the zero-article rule:",
        "Hard": "Which choice best completes the sentence without an article:",
        "Ultra": "Which completion is most accurate with zero article:",
    },
    "countability": {
        "Easy": "Which determiner best completes the countability sentence:",
        "Medium": "Which option best fits the count/noncount rule:",
        "Hard": "Which choice best matches the noun type:",
        "Ultra": "Which completion is most accurate for quantity:",
    },
    "pair-determiners": {
        "Easy": "Which determiner best completes the noun phrase:",
        "Medium": "Which option best fits the pair-or-distribution rule:",
        "Hard": "Which choice best matches the determiner logic:",
        "Ultra": "Which completion is most accurate for the determiner:",
    },
}

CHOICE_POOLS: dict[str, tuple[str, ...]] = {
    "a": ("a", "an", "the", "no article"),
    "an": ("an", "a", "the", "no article"),
    "the": ("the", "a", "an", "no article"),
    "no article": ("no article", "a", "an", "the"),
    "many": ("many", "much", "few", "little"),
    "much": ("much", "many", "fewer", "few"),
    "fewer": ("fewer", "less", "many", "much"),
    "less": ("less", "fewer", "many", "few"),
    "little": ("little", "a little", "many", "much"),
    "each": ("each", "every", "either", "both"),
    "every": ("every", "each", "either", "both"),
    "either": ("either", "neither", "both", "any"),
    "neither": ("neither", "either", "both", "any"),
    "both": ("both", "either", "neither", "all"),
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
            "articles-and-determiners",
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
            family="article-sound",
            answer="an",
            frames=fr(
                ("She prepared", "honest answer for the panel"),
                ("The clerk requested", "hour to finish the form"),
                ("We hired", "MBA graduate for the office"),
                ("The manager packed", "umbrella for the trip"),
                ("The lawyer interviewed", "heir to the estate"),
                ("The team examined", "X-ray before the diagnosis"),
            ),
            explanation="The next word begins with a vowel sound, so the article must be an.",
            tags=("sound-rule", "vowel-sound", "article"),
        ),
        RowSpec(
            family="article-sound",
            answer="a",
            frames=fr(
                ("The agency hired", "university graduate for the desk"),
                ("The office approved", "useful update for the branch"),
                ("She needed", "one-time pass for the gate"),
                ("The clerk issued", "European permit for travel"),
                ("He carried", "U-turn sign for the road"),
                ("They opened", "user account for the applicant"),
            ),
            explanation="The next word begins with a consonant sound, so the article must be a.",
            tags=("sound-rule", "consonant-sound", "article"),
        ),
        RowSpec(
            family="article-sound",
            answer="an",
            frames=fr(
                ("The candidate gave", "honest response during the hearing"),
                ("The nurse prepared", "hour-long note for the chart"),
                ("The office issued", "honor certificate to the trainee"),
                ("The analyst reviewed", "MRI report from the clinic"),
                ("The clerk sent", "NGO memo to the director"),
                ("The student brought", "SOS message to the desk"),
            ),
            explanation="The next word begins with a vowel sound, so the article must be an.",
            tags=("sound-rule", "acronym", "article"),
        ),
        RowSpec(
            family="article-sound",
            answer="a",
            frames=fr(
                ("The hospital opened", "one-way lane near the gate"),
                ("The department used", "uniform policy for the staff"),
                ("The traveler booked", "European tour for the summer"),
                ("The branch hired", "useful assistant for records"),
                ("The clerk prepared", "union badge for the visitor"),
                ("The office printed", "U.S. form for the file"),
            ),
            explanation="The next word begins with a consonant sound, so the article must be a.",
            tags=("sound-rule", "consonant-sound", "article"),
        ),
        RowSpec(
            family="article-sound",
            answer="an",
            frames=fr(
                ("The witness saw", "honest witness near the door"),
                ("The editor found", "heirloom in the drawer"),
                ("The lawyer ordered", "X-ray of the wrist"),
                ("The office scheduled", "MBA interview for the applicant"),
                ("The technician reviewed", "FBI report before lunch"),
                ("The team received", "MRI scan from the clinic"),
            ),
            explanation="The next word begins with a vowel sound, so the article must be an.",
            tags=("sound-rule", "initialism", "article"),
        ),
        RowSpec(
            family="definite-the",
            answer="the",
            frames=fr(
                ("A file was misplaced, so", "file was checked again"),
                ("A memo was copied, and", "memo was sent upstairs"),
                ("A stamp was found in the drawer. Later,", "stamp was entered in the log"),
                ("A form arrived early, but", "form still needed a signature"),
                ("A package was opened, and", "package revealed a receipt"),
                ("A report was filed, and", "report was archived the same day"),
            ),
            explanation="The noun is specific because it is already known from the sentence, so the definite article is needed.",
            tags=("specific-reference", "previous-mention", "definite-article"),
        ),
        RowSpec(
            family="definite-the",
            answer="the",
            frames=fr(
                ("The clerk checked", "smallest error in the draft"),
                ("The team waited for", "first bus after noon"),
                ("The officer opened", "last room on the left"),
                ("The branch selected", "best candidate for the post"),
                ("The assistant kept", "only copy on the desk"),
                ("The memo reached", "next office in the building"),
            ),
            explanation="The noun is uniquely identified by a superlative or ordinal idea, so the definite article is needed.",
            tags=("specific-reference", "superlative", "definite-article"),
        ),
        RowSpec(
            family="definite-the",
            answer="the",
            frames=fr(
                ("Please hand me", "report on the table"),
                ("The officer opened", "drawer beside him"),
                ("We reviewed", "form you sent yesterday"),
                ("The applicant signed", "copy on the counter"),
                ("The team entered", "room at the back"),
                ("The clerk filed", "receipt from lunch"),
            ),
            explanation="The noun is a particular item in context, so the definite article is needed.",
            tags=("specific-reference", "identified-object", "definite-article"),
        ),
        RowSpec(
            family="definite-the",
            answer="the",
            frames=fr(
                ("The manager reviewed", "same report again"),
                ("The clerk checked", "other form on the list"),
                ("The file was stored on", "following shelf"),
                ("The team briefed", "whole office before the audit"),
                ("The director met", "entire staff after lunch"),
                ("The guard pointed to", "nearest exit in the hall"),
            ),
            explanation="The phrase needs the definite article because the reference is fixed or specific.",
            tags=("specific-reference", "fixed-phrase", "definite-article"),
        ),
        RowSpec(
            family="definite-the",
            answer="the",
            frames=fr(
                ("The report was sent to", "president of the organization"),
                ("The meeting ended near", "moon above the field"),
                ("The clerk saw", "main gate from the window"),
                ("The driver parked by", "front desk at the entrance"),
                ("The supervisor waited beside", "main office during the call"),
                ("The guide pointed toward", "only copy in the archive"),
            ),
            explanation="The phrase refers to a specific or unique item, so the definite article is needed.",
            tags=("specific-reference", "unique-or-known", "definite-article"),
        ),
        RowSpec(
            family="zero-article",
            answer="no article",
            frames=fr(
                ("In general,", "students need practice before the exam"),
                ("For most audits,", "forms help the staff track errors"),
                ("At work,", "officers rely on records"),
                ("During training,", "trainees review examples"),
                ("In many offices,", "reports guide decisions"),
                ("At the desk,", "clerks sort documents"),
            ),
            explanation="Plural nouns used in a general sense often take no article.",
            tags=("general-plural", "plural-general", "zero-article"),
        ),
        RowSpec(
            family="zero-article",
            answer="no article",
            frames=fr(
                ("At the office,", "information is useful during an audit"),
                ("For safety,", "water should be available at all times"),
                ("During the meeting,", "advice helped the applicant"),
                ("In this process,", "equipment must be checked first"),
                ("The supervisor said that", "money was missing from the envelope"),
                ("For the report,", "patience is essential"),
            ),
            explanation="Noncount nouns used in a general sense often take no article.",
            tags=("general-noncount", "noncount-general", "zero-article"),
        ),
        RowSpec(
            family="zero-article",
            answer="no article",
            frames=fr(
                ("The applicant speaks", "English at work"),
                ("The student studies", "biology every afternoon"),
                ("The family ate", "lunch before the meeting"),
                ("The officers drank", "coffee during the break"),
                ("The clerk practiced", "Spanish after work"),
                ("The teacher reviewed", "algebra during class"),
            ),
            explanation="Languages, meals, and school subjects usually take no article in these general uses.",
            tags=("fixed-expression", "language-subject-meal", "zero-article"),
        ),
        RowSpec(
            family="zero-article",
            answer="no article",
            frames=fr(
                ("Every morning, the children go to", "school by bus"),
                ("The suspect stayed in", "prison for five years"),
                ("The clerk arrived at", "noon before the briefing"),
                ("The workers met on", "Monday after the shift"),
                ("The technician was at", "home all day"),
                ("The team waited until", "sunset before leaving"),
            ),
            explanation="Some fixed expressions use no article even though the noun is singular.",
            tags=("fixed-expression", "common-omission", "zero-article"),
        ),
        RowSpec(
            family="zero-article",
            answer="no article",
            frames=fr(
                ("In general,", "reports help managers track problems"),
                ("At work,", "officers follow procedures"),
                ("During orientation,", "applicants wait outside"),
                ("For most cases,", "documents should be copied first"),
                ("In the archive,", "files were sorted by date"),
                ("Before closing,", "letters were placed in trays"),
            ),
            explanation="General plural nouns usually take no article.",
            tags=("general-plural", "plural-general", "zero-article"),
        ),
        RowSpec(
            family="countability",
            answer="many",
            frames=fr(
                ("The office received", "complaints this month"),
                ("The branch hired", "applicants after the posting"),
                ("The record had", "errors before revision"),
                ("The manager reviewed", "reports this morning"),
                ("The clerk sorted", "forms in the tray"),
                ("The team handled", "cases during the week"),
            ),
            explanation="The noun is countable and plural, so many is the correct quantity word.",
            tags=("count-plural", "quantity", "countability"),
        ),
        RowSpec(
            family="countability",
            answer="much",
            frames=fr(
                ("The clerk had", "time to check the file"),
                ("The office used", "space for the archive"),
                ("The report needed", "information from the witness"),
                ("The supervisor spent", "patience on the delay"),
                ("The branch wasted", "money on the old printer"),
                ("The team found", "water in the container"),
            ),
            explanation="The noun is noncount, so much is the correct quantity word.",
            tags=("noncount-quantity", "quantity", "countability"),
        ),
        RowSpec(
            family="countability",
            answer="fewer",
            frames=fr(
                ("The revision produced", "errors than before"),
                ("The new process created", "complaints from the staff"),
                ("The update left", "mistakes in the draft"),
                ("The schedule allowed", "delays in the line"),
                ("The cleanup meant", "problems for the team"),
                ("The audit revealed", "gaps in the record"),
            ),
            explanation="The noun is countable and plural, so the comparative determiner should be fewer.",
            tags=("comparative-count", "comparison", "countability"),
        ),
        RowSpec(
            family="countability",
            answer="less",
            frames=fr(
                ("The clerk had", "time after the briefing"),
                ("The office used", "money than expected"),
                ("The meeting caused", "noise in the hallway"),
                ("The process required", "effort from the staff"),
                ("The branch showed", "patience during the delay"),
                ("The change produced", "stress for the team"),
            ),
            explanation="The noun is noncount, so the comparative determiner should be less.",
            tags=("comparative-noncount", "comparison", "countability"),
        ),
        RowSpec(
            family="countability",
            answer="little",
            frames=fr(
                ("The office had", "energy after lunch"),
                ("The report contained", "information about the case"),
                ("The supervisor showed", "interest in the change"),
                ("The staff had", "time before closing"),
                ("The branch gave", "support during the test"),
                ("The clerk had", "patience after the call"),
            ),
            explanation="The noun is noncount and the amount is small, so little is the correct choice.",
            tags=("noncount-small-amount", "quantity", "countability"),
        ),
        RowSpec(
            family="pair-determiners",
            answer="each",
            frames=fr(
                ("At the gate,", "applicant must show an ID before entering"),
                ("In the office,", "officer received a badge at the gate"),
                ("During orientation,", "student signed the attendance sheet"),
                ("At the counter,", "clerk checked the seal"),
                ("Before the briefing,", "visitor got a copy of the rules"),
                ("At the branch,", "department submitted a report"),
            ),
            explanation="Each is used to refer to people or things one by one.",
            tags=("singular-each", "distribution", "pair-determiners"),
        ),
        RowSpec(
            family="pair-determiners",
            answer="every",
            frames=fr(
                ("In this system,", "office needs a backup plan"),
                ("At headquarters,", "branch received the memo"),
                ("Before closing,", "officer must sign the log"),
                ("In the archive,", "report was filed on time"),
                ("During the shift,", "clerk should check the list"),
                ("For the class,", "trainee needs the handbook"),
            ),
            explanation="Every is used with singular count nouns to mean all members of a group.",
            tags=("singular-every", "distribution", "pair-determiners"),
        ),
        RowSpec(
            family="pair-determiners",
            answer="either",
            frames=fr(
                ("For the campus,", "route leads to the main gate"),
                ("At registration,", "form may be used"),
                ("In the meeting,", "option will solve the problem"),
                ("At the desk,", "window is available this morning"),
                ("At the hall,", "door opens to the hallway"),
                ("For the office,", "proposal can be submitted today"),
            ),
            explanation="Either means one of two choices.",
            tags=("two-choice-either", "pair", "pair-determiners"),
        ),
        RowSpec(
            family="pair-determiners",
            answer="neither",
            frames=fr(
                ("In the review,", "option solved the problem"),
                ("At the desk,", "answer was accepted by the clerk"),
                ("After dark,", "route was safe"),
                ("For the audit,", "proposal matched the rules"),
                ("In the file room,", "document was complete on its own"),
                ("During the vote,", "choice felt practical to the manager"),
            ),
            explanation="Neither means not one of two choices.",
            tags=("two-choice-neither", "pair", "pair-determiners"),
        ),
        RowSpec(
            family="pair-determiners",
            answer="both",
            frames=fr(
                ("By noon,", "forms were complete"),
                ("Before the briefing,", "applicants arrived early"),
                ("At the gate,", "officers signed the log"),
                ("For the audit,", "reports were correct"),
                ("At headquarters,", "departments approved the schedule"),
                ("Yesterday,", "copies were filed"),
            ),
            explanation="Both refers to two items together.",
            tags=("two-choice-both", "pair", "pair-determiners"),
        ),
    )


def build_bank() -> list[dict]:
    rows = _rows()
    items: list[dict] = []
    question_id = 1

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

    return items


def main() -> int:
    bank = build_bank()
    _validate_bank(bank)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(bank, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(bank)} questions to {OUTPUT_PATH}")
    print(
        "Validation passed: unique questions, sequential ids, balanced difficulty counts, and balanced family counts."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
