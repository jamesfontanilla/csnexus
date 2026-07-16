"""Generate the Tense Consistency question bank."""

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
    / "tense-consistency"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Tense Consistency"
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
    "present-reference": {
        "Easy": "Which verb best keeps the present-time frame:",
        "Medium": "Which option best preserves the present tense:",
        "Hard": "Which choice best fixes the present-time consistency:",
        "Ultra": "Which completion is most accurate for the present frame:",
    },
    "past-reference": {
        "Easy": "Which verb best keeps the past-time frame:",
        "Medium": "Which option best preserves the past tense:",
        "Hard": "Which choice best fixes the past-time consistency:",
        "Ultra": "Which completion is most accurate for the past frame:",
    },
    "future-reference": {
        "Easy": "Which verb best keeps the future timeline:",
        "Medium": "Which option best preserves the future form:",
        "Hard": "Which choice best fixes the future-time consistency:",
        "Ultra": "Which completion is most accurate for the future timeline:",
    },
    "perfect-tenses": {
        "Easy": "Which verb best preserves the completed-action timeline:",
        "Medium": "Which option best preserves the perfect tense:",
        "Hard": "Which choice best fixes the sequence of events:",
        "Ultra": "Which completion is most accurate for the perfect-tense logic:",
    },
    "reported-sequence": {
        "Easy": "Which verb best fixes the reported-speech shift:",
        "Medium": "Which option best preserves the indirect-statement tense:",
        "Hard": "Which choice best fixes the backshift:",
        "Ultra": "Which completion is most accurate for reported speech:",
    },
}


@dataclass(frozen=True)
class Frame:
    before: str
    after: str


@dataclass(frozen=True)
class RowSpec:
    family: str
    answer: str
    choices: tuple[str, ...]
    frames: tuple[Frame, ...]
    explanation: str
    tags: tuple[str, ...]


def fr(*pairs: tuple[str, str]) -> tuple[Frame, ...]:
    return tuple(Frame(before=before, after=after) for before, after in pairs)


def cs(*choices: str) -> tuple[str, ...]:
    unique = _dedupe_preserve_order(choices)
    if len(unique) != 4:
        raise ValueError(f"expected 4 unique choices, got {unique}")
    return tuple(unique)


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
    choices = _dedupe_preserve_order(row.choices)
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
            "tense-consistency",
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
            family="present-reference",
            answer="checks",
            choices=cs("checks", "checked", "is checking", "has checked"),
            frames=fr(
                ("Every morning, the clerk", "the logbook before the office opens"),
                ("On weekdays, the clerk", "the logbook before lunch"),
                ("During routine rounds, the clerk", "the file tray before noon"),
                ("Each afternoon, the clerk", "the ledger and files the notes"),
                ("When the office opens, the clerk", "the mail and stamps the forms"),
                ("Before the day ends, the clerk", "the signatures"),
            ),
            explanation="The sentence describes a repeated present-time habit, so the verb should stay in the present simple.",
            tags=("present-simple", "habit", "routine"),
        ),
        RowSpec(
            family="present-reference",
            answer="remains",
            choices=cs("remains", "remained", "will remain", "is remaining"),
            frames=fr(
                ("The policy", "in effect until the director changes it"),
                ("The notice", "posted until the forms are collected"),
                ("The rule", "active while the audit continues"),
                ("The schedule", "fixed for the rest of the week"),
                ("The record", "confidential while the case is open"),
                ("The process", "unchanged for now"),
            ),
            explanation="The sentence stays in the present frame, so the linking verb should remain in the present.",
            tags=("present-linking-verb", "state", "consistency"),
        ),
        RowSpec(
            family="present-reference",
            answer="is reviewing",
            choices=cs("is reviewing", "reviews", "reviewed", "has reviewed"),
            frames=fr(
                ("Right now, the inspector", "the files on the desk"),
                ("At the moment, the team", "the entries in the ledger"),
                ("At present, the clerk", "the forms for missing signatures"),
                ("During this meeting, the officer", "the documents line by line"),
                ("For now, the committee", "the report carefully"),
                ("At this point, the supervisor", "the draft before approval"),
            ),
            explanation="The sentence describes an action happening now, so the progressive present is the best fit.",
            tags=("present-progressive", "current-action", "consistency"),
        ),
        RowSpec(
            family="present-reference",
            answer="asks",
            choices=cs("asks", "asked", "is asking", "has asked"),
            frames=fr(
                ("Every time the applicant needs help, he", "the clerk for instructions"),
                ("On each visit, the caller", "for the queue number"),
                ("In formal interviews, the speaker", "clear questions"),
                ("Whenever the form is unclear, the staff", "for clarification"),
                ("During registration, each student", "about the deadline"),
                ("At the counter, the citizen", "for the receipt"),
            ),
            explanation="The sentence expresses a repeated present action, so the simple present is correct.",
            tags=("present-simple", "repetition", "consistency"),
        ),
        RowSpec(
            family="present-reference",
            answer="stays",
            choices=cs("stays", "stayed", "is staying", "has stayed"),
            frames=fr(
                ("The package", "on the shelf until pickup"),
                ("The key", "in the drawer after the shift"),
                ("The badge", "visible while inside the building"),
                ("The file", "with the clerk until the signature is complete"),
                ("The notice", "on the wall during the week"),
                ("The card", "in the folder until collection"),
            ),
            explanation="The sentence keeps a present state, so the present simple verb is the clearest choice.",
            tags=("present-simple", "state", "consistency"),
        ),
        RowSpec(
            family="past-reference",
            answer="reviewed",
            choices=cs("reviewed", "reviews", "is reviewing", "has reviewed"),
            frames=fr(
                ("Yesterday, the inspector", "the records and signed the log"),
                ("Last Tuesday, the clerk", "the application and sealed the envelope"),
                ("Earlier that day, the officer", "the report before the meeting"),
                ("During the audit, the supervisor", "the entries one by one"),
                ("After lunch, the team", "the files for missing pages"),
                ("On Monday, the assistant", "the memo and sent it upstairs"),
            ),
            explanation="The sentence is in the past narrative, so the verb should stay in the past simple.",
            tags=("past-simple", "narrative", "consistency"),
        ),
        RowSpec(
            family="past-reference",
            answer="were sorting",
            choices=cs("were sorting", "sort", "sorted", "have sorted"),
            frames=fr(
                ("At noon, the clerks", "the boxes when the lights went out"),
                ("While the manager spoke, the assistants", "the forms by date"),
                ("During the briefing, the staff", "the documents into trays"),
                ("At 3 p.m., the volunteers", "the supplies for delivery"),
                ("As the bell rang, the officers", "the logs into folders"),
                ("When the call came, the workers", "the reports by hand"),
            ),
            explanation="The sentence describes an ongoing past action, so the past progressive is the best fit.",
            tags=("past-progressive", "ongoing-past", "consistency"),
        ),
        RowSpec(
            family="past-reference",
            answer="called",
            choices=cs("called", "calls", "is calling", "has called"),
            frames=fr(
                ("The supervisor", "the applicant after the roster was checked"),
                ("Yesterday, the officer", "the witness to the front desk"),
                ("Last week, the clerk", "the courier before closing time"),
                ("Earlier, the manager", "the team to the conference room"),
                ("During the investigation, the staff", "the driver for his receipt"),
                ("At noon, the assistant", "the next name on the list"),
            ),
            explanation="The action is completed in the past, so the simple past is correct.",
            tags=("past-simple", "completed-action", "consistency"),
        ),
        RowSpec(
            family="past-reference",
            answer="was",
            choices=cs("was", "is", "will be", "has been"),
            frames=fr(
                ("The office", "closed when we arrived"),
                ("The schedule", "final after the meeting"),
                ("The report", "ready before noon"),
                ("The gate", "open when the guard checked it"),
                ("The file", "missing from the tray"),
                ("The hallway", "quiet after the announcement"),
            ),
            explanation="The sentence describes a past state, so the linking verb should be in the past.",
            tags=("past-linking-verb", "state", "consistency"),
        ),
        RowSpec(
            family="past-reference",
            answer="returned",
            choices=cs("returned", "returns", "is returning", "has returned"),
            frames=fr(
                ("After the audit, the courier", "the package to the desk"),
                ("Later that day, the supervisor", "the forms to records"),
                ("Before evening, the clerk", "the signed memo to the file room"),
                ("At the end of the shift, the staff", "the folders to storage"),
                ("After lunch, the assistant", "the corrected copy to the manager"),
                ("By sunset, the volunteer", "the key to the guard"),
            ),
            explanation="The sentence is a finished past event, so the verb should remain in the past simple.",
            tags=("past-simple", "completed-action", "consistency"),
        ),
        RowSpec(
            family="future-reference",
            answer="will submit",
            choices=cs("will submit", "submits", "submitted", "has submitted"),
            frames=fr(
                ("Tomorrow, the clerk", "the documents after lunch"),
                ("Next week, the officer", "the completed form to records"),
                ("By Friday, the team", "the request to the supervisor"),
                ("Later this afternoon, the assistant", "the summary by email"),
                ("At the end of the day, the office", "the final copy"),
                ("On Monday, the manager", "the schedule for approval"),
            ),
            explanation="The sentence refers to a later action, so the simple future form is correct.",
            tags=("future-simple", "later-action", "consistency"),
        ),
        RowSpec(
            family="future-reference",
            answer="arrives",
            choices=cs("arrives", "will arrive", "arrived", "has arrived"),
            frames=fr(
                ("The meeting will begin when the director", ""),
                ("The team will leave after the inspector", ""),
                ("The clerk will file the form when the courier", ""),
                ("The office will open when the supervisor", ""),
                ("The guards will step aside before the witness", ""),
                ("The staff will continue once the manager", ""),
            ),
            explanation="A future time clause uses present tense, even though the meaning is future.",
            tags=("future-time-clause", "time-clause", "consistency"),
        ),
        RowSpec(
            family="future-reference",
            answer="will be using",
            choices=cs("will be using", "uses", "used", "has used"),
            frames=fr(
                ("This time next week, the staff", "the new records system"),
                ("By this time tomorrow, the team", "the revised checklist"),
                ("At 3 p.m. next Monday, the office", "the temporary filing room"),
                ("During the training session, the clerks", "the online portal"),
                ("Next month at this time, the department", "the updated form"),
                ("By the end of the quarter, the branch", "the new archive process"),
            ),
            explanation="The sentence describes an ongoing future action, so the future progressive is the best fit.",
            tags=("future-progressive", "ongoing-future", "consistency"),
        ),
        RowSpec(
            family="future-reference",
            answer="opens",
            choices=cs("opens", "will open", "opened", "has opened"),
            frames=fr(
                ("Before the courthouse", "for the day, the clerk will secure the files"),
                ("After the gate", "in the morning, the guard will check the badges"),
                ("When the office", "at eight, the staff will line up"),
                ("Once the store", "tomorrow, the manager will review the reports"),
                ("After the museum", "on Monday, the guide will start the tour"),
                ("Before the clinic", "for patients, the nurse will ready the desk"),
            ),
            explanation="In a future time clause, the action should be in the present tense.",
            tags=("future-time-clause", "time-clause", "consistency"),
        ),
        RowSpec(
            family="future-reference",
            answer="will have finished",
            choices=cs("will have finished", "will finish", "has finished", "had finished"),
            frames=fr(
                ("By Friday evening, the team", "the report"),
                ("By the time the director arrives, the office", "the labels"),
                ("Before the deadline, the staff", "the archive transfer"),
                ("By next Monday, the clerk", "the forms"),
                ("When the inspector returns, the assistant", "the checklist"),
                ("By the end of the month, the branch", "the inventory"),
            ),
            explanation="The sentence shows completion before a future point, so the future perfect is correct.",
            tags=("future-perfect", "completed-before-future", "consistency"),
        ),
        RowSpec(
            family="perfect-tenses",
            answer="has approved",
            choices=cs("has approved", "approved", "approves", "will approve"),
            frames=fr(
                ("So far, the committee", "three requests"),
                ("Up to now, the supervisor", "the revised plan"),
                ("This month, the board", "the proposal twice"),
                ("By now, the manager", "the final schedule"),
                ("Recently, the office", "the new forms"),
                ("To date, the agency", "the corrections"),
            ),
            explanation="The sentence connects a past action to the present, so the present perfect is the best fit.",
            tags=("present-perfect", "connected-to-now", "consistency"),
        ),
        RowSpec(
            family="perfect-tenses",
            answer="has been waiting",
            choices=cs("has been waiting", "was waiting", "waits", "had waited"),
            frames=fr(
                ("The applicant", "for the interview since nine o'clock"),
                ("The driver", "outside since the rain began"),
                ("The clerk", "at the counter all morning"),
                ("The witness", "for the call since noon"),
                ("The volunteer", "by the desk since early afternoon"),
                ("The manager", "in the hallway for several minutes"),
            ),
            explanation="The sentence shows an action that started in the past and continues now, so the present perfect progressive is correct.",
            tags=("present-perfect-progressive", "ongoing-to-now", "consistency"),
        ),
        RowSpec(
            family="perfect-tenses",
            answer="had left",
            choices=cs("had left", "left", "has left", "will leave"),
            frames=fr(
                ("By the time the officer arrived, the suspect", ""),
                ("Before the meeting began, the team leader", "the room"),
                ("When the lights went out, the clerk", "the office"),
                ("By the time the siren sounded, the workers", "the site"),
                ("Long before the supervisor called, the witness", ""),
                ("Before the audit started, the manager", "the building"),
            ),
            explanation="The sentence involves two past events, and the leaving happened first, so past perfect is required.",
            tags=("past-perfect", "earlier-past", "consistency"),
        ),
        RowSpec(
            family="perfect-tenses",
            answer="had been working",
            choices=cs("had been working", "worked", "is working", "has worked"),
            frames=fr(
                ("The staff", "for hours before the power returned"),
                ("The clerks", "on the list before lunch was served"),
                ("The team", "through the documents when the alarm sounded"),
                ("The officers", "in the records room before the break"),
                ("The assistants", "on the draft all morning before the director arrived"),
                ("The volunteers", "in the heat before the rain came"),
            ),
            explanation="The sentence shows an action that was already in progress before another past event, so past perfect progressive is correct.",
            tags=("past-perfect-progressive", "earlier-past", "consistency"),
        ),
        RowSpec(
            family="perfect-tenses",
            answer="will have completed",
            choices=cs("will have completed", "will complete", "has completed", "had completed"),
            frames=fr(
                ("By Friday evening, the team", "the report"),
                ("By the time the director arrives, the office", "the labels"),
                ("Before the deadline, the staff", "the archive transfer"),
                ("By next Monday, the clerk", "the forms"),
                ("When the inspector returns, the assistant", "the checklist"),
                ("By the end of the month, the branch", "the inventory"),
            ),
            explanation="The sentence shows completion before a future point, so the future perfect is correct.",
            tags=("future-perfect", "completed-before-future", "consistency"),
        ),
        RowSpec(
            family="reported-sequence",
            answer="were",
            choices=cs("were", "are", "will be", "have been"),
            frames=fr(
                ("The officer said that the forms", "ready yesterday"),
                ("The manager explained that the records", "missing from the cabinet"),
                ("The clerk reported that the doors", "open when he arrived"),
                ("The witness stated that the lights", "on during the check"),
                ("The supervisor said that the files", "on the desk the whole time"),
                ("The assistant told the team that the forms", "incomplete"),
            ),
            explanation="The reporting verb is past tense, so the present idea in the reported clause shifts back to past.",
            tags=("reported-past", "backshift", "consistency"),
        ),
        RowSpec(
            family="reported-sequence",
            answer="had been",
            choices=cs("had been", "was", "is", "will be"),
            frames=fr(
                ("She said that the file", "missing before the correction"),
                ("He explained that the team", "waiting for the call"),
                ("The witness reported that the lights", "off before the alarm"),
                ("The clerk said that the envelope", "sealed earlier"),
                ("The supervisor stated that the forms", "misplaced before noon"),
                ("The manager said that the report", "reviewed before the meeting"),
            ),
            explanation="The reporting verb is past tense, so the earlier state shifts back with had been.",
            tags=("reported-past-perfect", "backshift", "consistency"),
        ),
        RowSpec(
            family="reported-sequence",
            answer="would",
            choices=cs("would", "will", "is going to", "can"),
            frames=fr(
                ("He said that the staff", "return after lunch"),
                ("She told us that the office", "open again on Monday"),
                ("The director explained that the committee", "release the results later"),
                ("The witness said that the inspector", "call back the next day"),
                ("The clerk reported that the branch", "send another copy"),
                ("The manager said that the courier", "arrive by noon"),
            ),
            explanation="A future idea in reported speech usually backshifts to would.",
            tags=("reported-future", "backshift", "consistency"),
        ),
        RowSpec(
            family="reported-sequence",
            answer="could",
            choices=cs("could", "can", "will be able to", "should"),
            frames=fr(
                ("The witness said that she", "identify the driver"),
                ("The officer explained that the team", "check the records later"),
                ("The supervisor said that the clerk", "enter the room after signing"),
                ("The manager reported that the staff", "finish early if needed"),
                ("The witness said that the guards", "see the plate number"),
                ("The clerk explained that he", "open the cabinet only with permission"),
            ),
            explanation="The modal usually backshifts in reported speech, so could is the safest choice.",
            tags=("reported-modal", "backshift", "consistency"),
        ),
        RowSpec(
            family="reported-sequence",
            answer="was",
            choices=cs("was", "is", "had been", "will be"),
            frames=fr(
                ("She said that the report", "accurate when she checked it"),
                ("He explained that the office", "quiet after the briefing"),
                ("The witness stated that the road", "clear before dawn"),
                ("The clerk reported that the file", "on the counter earlier"),
                ("The manager said that the door", "locked when he left"),
                ("The supervisor explained that the system", "offline during the test"),
            ),
            explanation="A past reporting verb usually shifts a present state back to past tense.",
            tags=("reported-past-state", "backshift", "consistency"),
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
