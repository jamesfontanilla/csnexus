"""Generate the Pronoun Agreement question bank."""

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
    / "pronoun-agreement"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Pronoun Agreement"
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
    "singular-nonhuman": {
        "Easy": "Which pronoun best completes the sentence:",
        "Medium": "Which option best completes the sentence:",
        "Hard": "Which choice best fixes the pronoun agreement:",
        "Ultra": "Which completion is most accurate:",
    },
    "plural-nonhuman": {
        "Easy": "Which pronoun best completes the plural sentence:",
        "Medium": "Which option best completes the plural sentence:",
        "Hard": "Which choice best fixes the plural pronoun:",
        "Ultra": "Which completion is most accurate for the plural antecedent:",
    },
    "singular-human": {
        "Easy": "Which pronoun best completes the singular-person sentence:",
        "Medium": "Which option best completes the singular-person sentence:",
        "Hard": "Which choice best fixes the singular pronoun:",
        "Ultra": "Which completion is most accurate for the singular person:",
    },
    "indefinite-pronouns": {
        "Easy": "Which pronoun best fits the singular antecedent:",
        "Medium": "Which option best fits the singular antecedent:",
        "Hard": "Which choice best fixes the indefinite-pronoun agreement:",
        "Ultra": "Which completion is most accurate for the indefinite pronoun:",
    },
    "collective-quantity": {
        "Easy": "Which pronoun best fits the group-or-quantity sentence:",
        "Medium": "Which option best fits the group-or-quantity sentence:",
        "Hard": "Which choice best fixes the collective-or-quantity agreement:",
        "Ultra": "Which completion is most accurate for the group or quantity:",
    },
}

CHOICE_POOLS: dict[str, tuple[str, ...]] = {
    "it": ("it", "they", "he or she", "we"),
    "its": ("its", "their", "his or her", "theirs"),
    "itself": ("itself", "themselves", "they", "he or she"),
    "they": ("they", "it", "he or she", "we"),
    "them": ("them", "it", "him or her", "us"),
    "their": ("their", "its", "his or her", "theirs"),
    "theirs": ("theirs", "its", "their", "his or hers"),
    "themselves": ("themselves", "itself", "they", "he or she"),
    "he or she": ("he or she", "they", "it", "we"),
    "him or her": ("him or her", "them", "it", "us"),
    "his or her": ("his or her", "their", "its", "her"),
    "his or hers": ("his or hers", "theirs", "its", "hers"),
    "himself or herself": ("himself or herself", "themselves", "itself", "they"),
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
            "pronoun-agreement",
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
        if not isinstance(choices, list) or not (2 <= len(choices) <= 6):
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
        if not isinstance(tags, list) or not tags:
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
            family="singular-nonhuman",
            answer="it",
            frames=fr(
                ("The folder was sealed, and", "was stored in the vault"),
                ("The folder sat on the desk, and", "was tagged for review"),
                ("The folder arrived early, so", "was checked first"),
                ("The folder had a torn corner, yet", "was still usable"),
                ("The folder was locked, and", "was kept in records"),
                ("The folder was thin, but", "was easy to carry"),
            ),
            explanation="The antecedent folder is singular, so the pronoun must be singular.",
            tags=("singular", "nonhuman", "subject-pronoun"),
        ),
        RowSpec(
            family="singular-nonhuman",
            answer="it",
            frames=fr(
                ("The report was approved, and", "was filed immediately"),
                ("The report was delayed, but", "was still useful"),
                ("The report was missing from the tray, so", "was logged separately"),
                ("The report was printed in error, and", "was corrected later"),
                ("The report was short, yet", "was complete"),
                ("The report was under review, and", "was kept confidential"),
            ),
            explanation="The antecedent report is singular, so the pronoun must be singular.",
            tags=("singular", "nonhuman", "subject-pronoun"),
        ),
        RowSpec(
            family="singular-nonhuman",
            answer="its",
            frames=fr(
                ("The envelope lost", "cover during transport"),
                ("The envelope had", "seal broken in the rain"),
                ("The envelope showed", "address clearly on the front"),
                ("The envelope kept", "tracking number visible"),
                ("The envelope needed", "label replaced"),
                ("The envelope displayed", "classification mark on top"),
            ),
            explanation="The antecedent envelope is singular, so the possessive adjective must be singular.",
            tags=("singular", "nonhuman", "possessive-adjective"),
        ),
        RowSpec(
            family="singular-nonhuman",
            answer="itself",
            frames=fr(
                ("The machine reset", "after the update"),
                ("The machine calibrated", "before the inspection"),
                ("The machine repaired", "after the outage"),
                ("The machine restarted", "without help"),
                ("The machine adjusted", "during the test run"),
                ("The machine shut down", "to protect the circuit"),
            ),
            explanation="The antecedent machine is singular and nonhuman, so the reflexive pronoun must be singular.",
            tags=("singular", "nonhuman", "reflexive"),
        ),
        RowSpec(
            family="singular-nonhuman",
            answer="its",
            frames=fr(
                ("The memo lost", "cover during delivery"),
                ("The memo had", "signature block missing"),
                ("The memo showed", "date printed in bold"),
                ("The memo kept", "reference code visible"),
                ("The memo needed", "heading revised"),
                ("The memo displayed", "seal at the bottom"),
            ),
            explanation="The antecedent memo is singular, so the possessive adjective must be singular.",
            tags=("singular", "nonhuman", "possessive-adjective"),
        ),
        RowSpec(
            family="plural-nonhuman",
            answer="they",
            frames=fr(
                ("The files were reviewed, and", "were sent to records"),
                ("The files were stacked, and", "were labeled by date"),
                ("The files were copied, and", "were placed in the drawer"),
                ("The files were sorted, and", "were checked twice"),
                ("The files were sealed, and", "were stored overnight"),
                ("The files were marked urgent, and", "were forwarded at once"),
            ),
            explanation="The antecedent files is plural, so the pronoun must be plural.",
            tags=("plural", "nonhuman", "subject-pronoun"),
        ),
        RowSpec(
            family="plural-nonhuman",
            answer="them",
            frames=fr(
                ("The clerk reviewed the records and filed", "by date"),
                ("The archivist gathered the forms and sorted", "into trays"),
                ("The officer checked the logs and reviewed", "before lunch"),
                ("The assistant copied the files and packed", "for storage"),
                ("The courier delivered the documents and handed", "to the clerk"),
                ("The inspector sorted the reports and returned", "to the archive"),
            ),
            explanation="The antecedent is plural, so the object pronoun must be plural.",
            tags=("plural", "nonhuman", "object-pronoun"),
        ),
        RowSpec(
            family="plural-nonhuman",
            answer="their",
            frames=fr(
                ("The forms lost", "serial numbers during transfer"),
                ("The forms kept", "order at the desk"),
                ("The forms showed", "reference marks clearly"),
                ("The forms needed", "pages signed by the clerk"),
                ("The forms carried", "tracking codes on top"),
                ("The forms displayed", "titles in bold"),
            ),
            explanation="The antecedent forms is plural, so the possessive adjective must be plural.",
            tags=("plural", "nonhuman", "possessive-adjective"),
        ),
        RowSpec(
            family="plural-nonhuman",
            answer="theirs",
            frames=fr(
                ("The final copies belong to the students, so the copies are", ""),
                ("The updated maps belong to the planners, so the maps are", ""),
                ("The sorted folders belong to the assistants, so the folders are", ""),
                ("The revised drafts belong to the editors, so the drafts are", ""),
                ("The printed handouts belong to the volunteers, so the handouts are", ""),
                ("The sealed envelopes belong to the clerks, so the envelopes are", ""),
            ),
            explanation="The antecedent is plural, so the possessive pronoun must be plural.",
            tags=("plural", "nonhuman", "possessive-pronoun"),
        ),
        RowSpec(
            family="plural-nonhuman",
            answer="themselves",
            frames=fr(
                ("The scanners reset", "after the update"),
                ("The scanners tested", "before going live"),
                ("The scanners calibrated", "without outside help"),
                ("The scanners checked", "before the audit"),
                ("The scanners powered down", "after the shift"),
                ("The scanners prepared", "for the next batch"),
            ),
            explanation="The antecedent scanners is plural, so the reflexive pronoun must be plural.",
            tags=("plural", "nonhuman", "reflexive"),
        ),
        RowSpec(
            family="singular-human",
            answer="he or she",
            frames=fr(
                ("When the applicant arrives,", "should sign in at the desk"),
                ("If the applicant needs help,", "should ask the clerk"),
                ("After the applicant is called,", "should show a valid ID"),
                ("Before the applicant leaves,", "should take the receipt"),
                ("Whenever the applicant returns,", "should follow the posted rules"),
                ("Once the applicant is admitted,", "should keep the badge visible"),
            ),
            explanation="The antecedent applicant is singular, so the subject pronoun must be singular.",
            tags=("singular", "human", "subject-pronoun"),
        ),
        RowSpec(
            family="singular-human",
            answer="him or her",
            frames=fr(
                ("The officer called", "to the counter"),
                ("The supervisor thanked", "for the report"),
                ("The clerk invited", "to the desk"),
                ("The manager guided", "through the process"),
                ("The registrar directed", "to the intake area"),
                ("The assistant referred", "to the filing room"),
            ),
            explanation="The antecedent officer is singular, so the object pronoun must be singular.",
            tags=("singular", "human", "object-pronoun"),
        ),
        RowSpec(
            family="singular-human",
            answer="his or her",
            frames=fr(
                ("The candidate misplaced", "ID before the interview"),
                ("The employee left", "badge in the drawer"),
                ("The applicant updated", "address on the form"),
                ("The trainee copied", "notes from the board"),
                ("The officer showed", "badge at the gate"),
                ("The speaker prepared", "remarks for the session"),
            ),
            explanation="The antecedent candidate is singular, so the possessive adjective must be singular.",
            tags=("singular", "human", "possessive-adjective"),
        ),
        RowSpec(
            family="singular-human",
            answer="his or hers",
            frames=fr(
                ("The blue binder belongs to the employee, so the binder is", ""),
                ("The reserved chair belongs to the applicant, so the chair is", ""),
                ("The final copy belongs to the officer, so the copy is", ""),
                ("The desk belongs to the supervisor, so the desk is", ""),
                ("The labeled folder belongs to the speaker, so the folder is", ""),
                ("The seat belongs to the presenter, so the seat is", ""),
            ),
            explanation="The antecedent is singular, so the possessive pronoun must be singular.",
            tags=("singular", "human", "possessive-pronoun"),
        ),
        RowSpec(
            family="singular-human",
            answer="himself or herself",
            frames=fr(
                ("The trainee introduced", "to the panel"),
                ("The candidate prepared", "before the talk"),
                ("The officer reminded", "before signing out"),
                ("The applicant described", "during the interview"),
                ("The student corrected", "after the review"),
                ("The presenter identified", "before the panel"),
            ),
            explanation="The antecedent trainee is singular, so the reflexive pronoun must be singular.",
            tags=("singular", "human", "reflexive"),
        ),
        RowSpec(
            family="indefinite-pronouns",
            answer="he or she",
            frames=fr(
                ("When each of the applicants arrives,", "should sign in at the desk"),
                ("If each of the applicants needs help,", "should ask the clerk"),
                ("After each of the applicants is called,", "should show a valid ID"),
                ("Before each of the applicants leaves,", "should take the receipt"),
                ("Whenever each of the applicants returns,", "should follow the posted rules"),
                ("Once each of the applicants is admitted,", "should keep the badge visible"),
            ),
            explanation="Each is singular in grammar, so the pronoun must be singular.",
            tags=("indefinite", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="indefinite-pronouns",
            answer="he or she",
            frames=fr(
                ("When everyone in the room is called,", "should answer at once"),
                ("If everyone in the room needs help,", "should ask the clerk"),
                ("After everyone in the room is seated,", "should remain silent"),
                ("Before everyone in the room leaves,", "should return the badge"),
                ("Whenever everyone in the room speaks,", "should use a calm tone"),
                ("Once everyone in the room is admitted,", "should keep the pass visible"),
            ),
            explanation="Everyone is singular in grammar, so the pronoun must be singular.",
            tags=("indefinite", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="indefinite-pronouns",
            answer="he or she",
            frames=fr(
                ("If someone from the office calls,", "should ask for the manager"),
                ("When someone from the office arrives,", "should sign in quickly"),
                ("After someone from the office is called,", "should present a valid ID"),
                ("Before someone from the office leaves,", "should return the slip"),
                ("Whenever someone from the office checks in,", "should follow the posted steps"),
                ("Once someone from the office is admitted,", "should wear the badge"),
            ),
            explanation="Someone is singular in grammar, so the pronoun must be singular.",
            tags=("indefinite", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="indefinite-pronouns",
            answer="it",
            frames=fr(
                ("Neither of the routes was safe, so", "was left unused"),
                ("Neither of the routes was open, and", "was marked for repair"),
                ("Neither of the routes was clear, so", "was avoided by the driver"),
                ("Neither of the routes was direct, but", "was still checked"),
                ("Neither of the routes was short, and", "was reviewed again"),
                ("Neither of the routes was easy, so", "was ruled out"),
            ),
            explanation="Neither is singular in grammar, so the pronoun must be singular.",
            tags=("indefinite", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="indefinite-pronouns",
            answer="he or she",
            frames=fr(
                ("When one of the coordinators is late,", "should send an apology"),
                ("If one of the coordinators is absent,", "should notify the office"),
                ("After one of the coordinators is called,", "should report at once"),
                ("Before one of the coordinators leaves,", "should check the roster"),
                ("Whenever one of the coordinators speaks,", "should use a clear tone"),
                ("Once one of the coordinators is selected,", "should receive the memo"),
            ),
            explanation="One is singular in grammar, so the pronoun must be singular.",
            tags=("indefinite", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="collective-quantity",
            answer="it",
            frames=fr(
                ("The committee said that", "would review the complaint tomorrow"),
                ("The committee explained that", "would release the notice today"),
                ("The committee noted that", "would meet again next week"),
                ("The committee confirmed that", "would postpone the hearing"),
                ("The committee reported that", "would publish the results soon"),
                ("The committee decided that", "would discuss the request later"),
            ),
            explanation="The committee is a collective noun treated as a unit here, so the pronoun is singular.",
            tags=("collective", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="collective-quantity",
            answer="it",
            frames=fr(
                ("The team said that", "would file the memo"),
                ("The team explained that", "would brief the staff"),
                ("The team noted that", "would arrive early"),
                ("The team confirmed that", "would submit the forms"),
                ("The team reported that", "would finish the task today"),
                ("The team decided that", "would keep the schedule"),
            ),
            explanation="The team is a collective noun treated as a unit here, so the pronoun is singular.",
            tags=("collective", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="collective-quantity",
            answer="they",
            frames=fr(
                ("A number of volunteers were waiting at the gate, and", "were ready to help"),
                ("A number of volunteers were assigned to the desk, and", "were checking the log"),
                ("A number of volunteers were carrying boxes, and", "were asked to stay late"),
                ("A number of volunteers were lined up, and", "were given badges"),
                ("A number of volunteers were briefed quickly, and", "were ready for the shift"),
                ("A number of volunteers were listed on the sheet, and", "were counted twice"),
            ),
            explanation="A number of means several, so the pronoun must be plural.",
            tags=("quantity", "plural", "subject-pronoun"),
        ),
        RowSpec(
            family="collective-quantity",
            answer="it",
            frames=fr(
                ("The number of volunteers was smaller than expected, so", "was recorded separately"),
                ("The number of volunteers was final, and", "was entered on the form"),
                ("The number of volunteers was low, so", "was discussed at the meeting"),
                ("The number of volunteers was uncertain, and", "was checked twice"),
                ("The number of volunteers was noted on the sheet, so", "was reviewed later"),
                ("The number of volunteers was published, and", "was copied to the memo"),
            ),
            explanation="The number of is singular because number is the head noun.",
            tags=("quantity", "singular", "subject-pronoun"),
        ),
        RowSpec(
            family="collective-quantity",
            answer="they",
            frames=fr(
                ("The manager and the assistant were reviewing the schedule, and", "were asked to sign in"),
                ("The manager and the assistant were at the desk, and", "were ready for the briefing"),
                ("The manager and the assistant were checking the notes, and", "were assigned to the case"),
                ("The manager and the assistant were discussing the file, and", "were asked to wait"),
                ("The manager and the assistant were standing by, and", "were called first"),
                ("The manager and the assistant were sorting the forms, and", "were told to continue"),
            ),
            explanation="Subjects joined by and are plural, so the pronoun must be plural.",
            tags=("compound", "plural", "subject-pronoun"),
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
    print("Validation passed: unique questions, sequential ids, balanced difficulty counts, and balanced family counts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
