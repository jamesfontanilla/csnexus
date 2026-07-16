"""Generate the Comparative Forms question bank."""

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
    / "comparative-forms"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Comparative Forms"
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
    "word": {
        "Easy": "Which word best completes the sentence",
        "Medium": "Which option best completes the sentence",
        "Hard": "Which choice best completes the sentence",
        "Ultra": "Which completion is most accurate for the sentence",
    },
    "phrase": {
        "Easy": "Which phrase best completes the sentence",
        "Medium": "Which option best completes the sentence",
        "Hard": "Which choice best completes the sentence",
        "Ultra": "Which completion is most accurate for the sentence",
    },
    "structure": {
        "Easy": "Which completion best fits the comparison structure",
        "Medium": "Which option best fits the comparison structure",
        "Hard": "Which choice best fits the comparison structure",
        "Ultra": "Which completion is most accurate for the comparison structure",
    },
}


@dataclass(frozen=True)
class Frame:
    before: str
    after: str


@dataclass(frozen=True)
class FamilySpec:
    base_family: str
    kind: str
    answer: str
    choices: tuple[str, str, str, str]
    frames: tuple[Frame, ...]
    explanation: str
    tags: tuple[str, ...]


def frames(*pairs: tuple[str, str]) -> tuple[Frame, ...]:
    return tuple(Frame(before=before, after=after) for before, after in pairs)


def _compose_sentence(frame: Frame) -> str:
    before = " ".join(frame.before.split())
    after = " ".join(frame.after.split())
    if before and after:
        return f"{before} ____ {after}."
    if before:
        return f"{before} ____."
    if after:
        return f"____ {after}."
    return "____."


def _build_question(
    *,
    question_id: int,
    spec: FamilySpec,
    family_name: str,
    frame: Frame,
    frame_index: int,
    difficulty: str,
) -> dict:
    prefix = PROMPT_PREFIXES[spec.kind][difficulty]
    sentence = _compose_sentence(frame)
    choices = list(spec.choices)
    rotation = (question_id + frame_index) % 4
    choices = choices[rotation:] + choices[:rotation]

    if spec.answer not in choices:
        raise ValueError(f"answer {spec.answer!r} missing from choices for {family_name}")

    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": f'{prefix}: "{sentence}"',
        "choices": choices,
        "answer": spec.answer,
        "explanation": spec.explanation,
        "tags": [
            "comparative-forms",
            family_name,
            DIFFICULTY_TAGS[difficulty],
            spec.base_family,
            spec.kind,
            *spec.tags,
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

        if item.get("subtest") != SUBTEST:
            raise ValueError(f"invalid subtest at id {index}")
        if item.get("module") != MODULE:
            raise ValueError(f"invalid module at id {index}")
        if item.get("subtopic") != SUBTOPIC:
            raise ValueError(f"invalid subtopic at id {index}")
        if item.get("category") != CATEGORY:
            raise ValueError(f"invalid category at id {index}")
        if item.get("language") != LANGUAGE:
            raise ValueError(f"invalid language at id {index}")

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
        if not isinstance(tags, list) or len(tags) < 5:
            raise ValueError(f"invalid tags at id {index}")
        if tags[0] != "comparative-forms":
            raise ValueError(f"invalid root tag at id {index}")
        actual_families[str(tags[1])] += 1

    if actual_difficulties != expected_difficulties:
        raise ValueError(f"unexpected difficulty counts: {actual_difficulties}")

    expected_families = {
        f"{difficulty.lower()}-{spec.base_family}": 10
        for difficulty in DIFFICULTIES
        for spec in _family_specs()
    }
    if dict(actual_families) != expected_families:
        raise ValueError(f"unexpected family counts: {dict(actual_families)}")


def _family_specs() -> tuple[FamilySpec, ...]:
    return (
        FamilySpec(
            base_family="bigger",
            kind="word",
            answer="bigger",
            choices=("bigger", "biggest", "more big", "big"),
            frames=frames(
                ("The storage room is", "than the pantry"),
                ("The new desk is", "than the old desk"),
                ("The river is", "than the canal"),
                ("The second box is", "than the first box"),
                ("The truck is", "than the van"),
                ("The tall shelf is", "than the short shelf"),
                ("The printed map is", "than the folded map"),
                ("The conference hall is", "than the waiting area"),
                ("The blue folder is", "than the red folder"),
                ("The new screen is", "than the old screen"),
            ),
            explanation="One-syllable adjectives usually take -er in the comparative form.",
            tags=("regular-comparative", "than", "one-syllable"),
        ),
        FamilySpec(
            base_family="nicer",
            kind="word",
            answer="nicer",
            choices=("nicer", "nicest", "more nice", "nice"),
            frames=frames(
                ("The revised notice is", "than the draft"),
                ("The updated layout is", "than the old layout"),
                ("The new policy is", "than the earlier policy"),
                ("The printed copy is", "than the scan"),
                ("The office lobby looks", "than the storage area"),
                ("The second message sounds", "than the first message"),
                ("The cleaned hall feels", "than the corridor"),
                ("The newer version is", "than the old version"),
                ("The final draft is", "than the rough draft"),
                ("The second offer seems", "than the first offer"),
            ),
            explanation="Adjectives ending in e usually take -r in the comparative form.",
            tags=("regular-comparative", "than", "ends-in-e"),
        ),
        FamilySpec(
            base_family="happier",
            kind="word",
            answer="happier",
            choices=("happier", "happy", "happiest", "more happy"),
            frames=frames(
                ("The clerk felt", "after the news"),
                ("The team looked", "after the result"),
                ("The child was", "after lunch"),
                ("The staff seemed", "after the meeting"),
                ("The officer sounded", "after the update"),
                ("The applicant looked", "before the interview ended"),
                ("The class felt", "after the announcement"),
                ("The new volunteer appeared", "after the orientation"),
                ("The customer seemed", "after the call"),
                ("The manager was", "after the review"),
            ),
            explanation="When an adjective ends in consonant plus y, change y to i before adding -er.",
            tags=("regular-comparative", "change-y-to-i", "change-in-degree"),
        ),
        FamilySpec(
            base_family="more-carefully",
            kind="phrase",
            answer="more carefully",
            choices=("more carefully", "carefully", "most carefully", "careful"),
            frames=frames(
                ("The inspector reviewed the file", "than the trainee did"),
                ("The clerk checked the form", "than the intern did"),
                ("The editor read the letter", "than the assistant did"),
                ("The auditor examined the figures", "than the team did"),
                ("The teacher listened to the answer", "than the class did"),
                ("The officer guarded the door", "than the guard did"),
                ("The archivist sorted the papers", "than the helper did"),
                ("The manager read the report", "than the analyst did"),
                ("The nurse filled out the form", "than the aide did"),
                ("The reviewer studied the note", "than the writer did"),
            ),
            explanation="Longer adverbs usually use more in the comparative form.",
            tags=("comparative-adverb", "than", "long-form-with-more"),
        ),
        FamilySpec(
            base_family="biggest",
            kind="word",
            answer="biggest",
            choices=("biggest", "bigger", "big", "more big"),
            frames=frames(
                ("This is the", "warehouse in the district"),
                ("That was the", "envelope in the stack"),
                ("The truck was the", "vehicle at the depot"),
                ("This room is the", "room in the building"),
                ("The hall is the", "venue in town"),
                ("The garden is the", "part of the lot"),
                ("The screen is the", "one in the office"),
                ("This box is the", "box on the shelf"),
                ("The second pile was the", "pile in the stack"),
                ("The new sign is the", "sign on the block"),
            ),
            explanation="One-syllable adjectives usually take -est in the superlative form, and superlatives normally use the.",
            tags=("superlative", "the", "one-syllable"),
        ),
        FamilySpec(
            base_family="happiest",
            kind="word",
            answer="happiest",
            choices=("happiest", "happier", "happy", "more happy"),
            frames=frames(
                ("This was the", "day of the trip"),
                ("That was the", "moment of the ceremony"),
                ("She had the", "expression in the room"),
                ("The class was the", "group after the result"),
                ("The team became the", "group at the celebration"),
                ("This is the", "part of the year"),
                ("It was the", "time for the family"),
                ("He gave the", "reply in the interview"),
                ("The office had the", "staff after the announcement"),
                ("This was the", "crowd at the event"),
            ),
            explanation="Words ending in consonant plus y usually change y to i before adding -est.",
            tags=("superlative", "the", "change-y-to-i"),
        ),
        FamilySpec(
            base_family="better",
            kind="word",
            answer="better",
            choices=("better", "best", "good", "well"),
            frames=frames(
                ("The new route is", "than the old route"),
                ("This version is", "than the first version"),
                ("Her explanation was", "than the earlier explanation"),
                ("The second draft looked", "than the rough draft"),
                ("The revised schedule is", "than the old schedule"),
                ("The updated guide is", "than the previous guide"),
                ("The answer felt", "than the first attempt"),
                ("The new policy is", "than the former policy"),
                ("The printed copy is", "than the blurry scan"),
                ("The second option is", "than the original option"),
            ),
            explanation="Good has the irregular comparative form better.",
            tags=("irregular-comparative", "than", "good"),
        ),
        FamilySpec(
            base_family="best",
            kind="word",
            answer="best",
            choices=("best", "better", "good", "well"),
            frames=frames(
                ("This is the", "option of the three"),
                ("That was the", "report on the table"),
                ("She gave the", "answer in the group"),
                ("The revised draft was the", "version available"),
                ("This is the", "route for the trip"),
                ("He chose the", "seat in the hall"),
                ("The committee selected the", "proposal"),
                ("That is the", "result from the test"),
                ("This was the", "decision for the office"),
                ("The team found the", "solution first"),
            ),
            explanation="Good has the irregular superlative form best.",
            tags=("irregular-superlative", "the", "good"),
        ),
        FamilySpec(
            base_family="worse",
            kind="word",
            answer="worse",
            choices=("worse", "worst", "bad", "badly"),
            frames=frames(
                ("This forecast is", "than yesterday's forecast"),
                ("The second draft was", "than the first draft"),
                ("His headache felt", "than before"),
                ("The new plan was", "than the original plan"),
                ("The delay looked", "than expected"),
                ("The noise became", "than earlier"),
                ("The report was", "than the sample report"),
                ("Her condition was", "than in the morning"),
                ("The error was", "than the one in the log"),
                ("This result is", "than last week's result"),
            ),
            explanation="Bad has the irregular comparative form worse.",
            tags=("irregular-comparative", "than", "bad"),
        ),
        FamilySpec(
            base_family="worst",
            kind="word",
            answer="worst",
            choices=("worst", "worse", "bad", "badly"),
            frames=frames(
                ("This was the", "result of the three tests"),
                ("That was the", "delay of the week"),
                ("He picked the", "route of all"),
                ("This is the", "outcome in the report"),
                ("The storm brought the", "damage to the town"),
                ("It was the", "mistake in the file"),
                ("This appeared to be the", "option available"),
                ("That gave the", "impression in the interview"),
                ("The team faced the", "problem of the month"),
                ("This note had the", "error in the set"),
            ),
            explanation="Bad has the irregular superlative form worst.",
            tags=("irregular-superlative", "the", "bad"),
        ),
        FamilySpec(
            base_family="the-more-carefully",
            kind="structure",
            answer="the more carefully",
            choices=("the more carefully", "more carefully", "the most carefully", "the less carefully"),
            frames=frames(
                ("", "you review the figures, the fewer errors you make"),
                ("", "the clerk checks the records, the cleaner the list becomes"),
                ("", "the auditor studies the report, the fewer problems appear"),
                ("", "the team inspects the file, the better the final copy looks"),
                ("", "the applicant practices, the smoother the answer sounds"),
                ("", "the staff compares the entries, the fewer mistakes appear"),
                ("", "the officer reviews the memo, the more accurate the summary becomes"),
                ("", "the analyst checks the totals, the more reliable the figures become"),
                ("", "the assistant proofreads the notice, the fewer corrections are needed"),
                ("", "the manager reads the report, the clearer the final version becomes"),
            ),
            explanation="The more...the more/fewer pattern shows linked change across two clauses.",
            tags=("correlative-comparative", "linked-change", "the-more-pattern"),
        ),
        FamilySpec(
            base_family="as-tall-as",
            kind="phrase",
            answer="as tall as",
            choices=("as tall as", "taller than", "the tallest", "as taller as"),
            frames=frames(
                ("The new shelf is", "the old shelf in the hall"),
                ("The tree is", "the building beside it"),
                ("Her stack of books is", "his stack on the desk"),
                ("The sign is", "the gate at the entrance"),
                ("The ladder is", "the wall in the shed"),
                ("The tower is", "the nearby tower"),
                ("The desk is", "the counter in the lobby"),
                ("The post is", "the fence by the road"),
                ("The cabinet is", "the refrigerator in the break room"),
                ("The lamp is", "the chair in the corner"),
            ),
            explanation="Use as + adjective + as to show equal degree.",
            tags=("equality", "as-as", "same-degree"),
        ),
        FamilySpec(
            base_family="not-as-tall-as",
            kind="phrase",
            answer="not as tall as",
            choices=("not as tall as", "as tall as", "taller than", "the tallest"),
            frames=frames(
                ("The display shelf is", "the old shelf in the lobby"),
                ("The antenna is", "the tower beside the station"),
                ("The side tree is", "the building across the street"),
                ("The doorway is", "the main entrance"),
                ("The railing is", "the wall beside it"),
                ("The statue is", "the monument in the square"),
                ("The window frame is", "the doorway in the hall"),
                ("The bridge railing is", "the river wall below"),
                ("The ceiling beam is", "the roof truss above"),
                ("The signpost is", "the streetlight nearby"),
            ),
            explanation="Use not as + adjective + as to show a lower degree.",
            tags=("inequality", "not-as-as", "same-degree"),
        ),
        FamilySpec(
            base_family="fewer",
            kind="word",
            answer="fewer",
            choices=("fewer", "less", "many", "much"),
            frames=frames(
                ("The branch received", "complaints this month than last month"),
                ("The office recorded", "errors after the review than before"),
                ("The team handled", "tasks today than yesterday"),
                ("The clerk found", "forms in the tray than expected"),
                ("The report showed", "mistakes than the draft"),
                ("The desk held", "files after the cleanup than before"),
                ("The counter had", "cups after lunch than before"),
                ("The office had", "visitors than usual"),
                ("The memo created", "questions than expected"),
                ("The form caused", "delays than before"),
            ),
            explanation="Use fewer with countable plural nouns.",
            tags=("quantity", "count-noun", "plural"),
        ),
        FamilySpec(
            base_family="less",
            kind="word",
            answer="less",
            choices=("less", "fewer", "many", "much"),
            frames=frames(
                ("The branch had", "time to review the form this week than last week"),
                ("The office spent", "money on supplies this month than before"),
                ("The team had", "patience during the delay than the group expected"),
                ("The clerk used", "paper after the switch than before"),
                ("The report required", "effort than the draft"),
                ("The office used", "water during the closure"),
                ("The supervisor had", "space for the new files than before"),
                ("The memo needed", "attention after the correction"),
                ("The branch consumed", "fuel last quarter"),
                ("The staff had", "information before the briefing"),
            ),
            explanation="Use less with uncountable nouns and amounts.",
            tags=("quantity", "uncountable", "mass-noun"),
        ),
    )


def _generate() -> list[dict]:
    items: list[dict] = []
    question_id = 1
    specs = _family_specs()

    for difficulty in DIFFICULTIES:
        for spec in specs:
            family_name = f"{difficulty.lower()}-{spec.base_family}"
            for frame_index, frame in enumerate(spec.frames):
                items.append(
                    _build_question(
                        question_id=question_id,
                        spec=spec,
                        family_name=family_name,
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
