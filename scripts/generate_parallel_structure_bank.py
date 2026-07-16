"""Generate the Parallel Structure question bank."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "error-recognition"
    / "parallel-structure"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Parallel Structure"
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
    "clause": {
        "Easy": "Which clause best completes the sentence",
        "Medium": "Which option best completes the sentence",
        "Hard": "Which choice best completes the sentence",
        "Ultra": "Which completion is most accurate for the sentence",
    },
    "structure": {
        "Easy": "Which completion best fits the parallel structure",
        "Medium": "Which option best fits the parallel structure",
        "Hard": "Which choice best fits the parallel structure",
        "Ultra": "Which completion is most accurate for the parallel structure",
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
            "parallel-structure",
            family_name,
            DIFFICULTY_TAGS[difficulty],
            spec.base_family,
            spec.kind,
            *spec.tags,
        ],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _family_specs() -> tuple[FamilySpec, ...]:
    return (
        FamilySpec(
            base_family="gerund-series",
            kind="phrase",
            answer="reviewing",
            choices=("reviewing", "to review", "review", "reviewed"),
            frames=frames(
                ("The clerk enjoys reading, editing, and", "reports"),
                ("The analyst prefers checking figures, sorting files, and", "records"),
                ("The officer likes comparing data, organizing notes, and", "forms"),
                ("The team spent the afternoon reading memos, marking issues, and", "the log"),
                ("The reviewer was careful about scanning pages, noting errors, and", "the draft"),
                ("The assistant keeps reading summaries, filing documents, and", "briefs"),
                ("The student practiced reading examples, copying models, and", "answers"),
                ("The inspector was trained in checking lists, comparing counts, and", "the forms"),
                ("The editor spent the morning checking facts, editing copy, and", "the article"),
                ("The clerk continued reading letters, organizing records, and", "the notices"),
            ),
            explanation="A series should keep the same verbal form. If the list starts with gerunds, the missing item should also be a gerund.",
            tags=("gerund", "series", "word-form"),
        ),
        FamilySpec(
            base_family="infinitive-series",
            kind="word",
            answer="send",
            choices=("send", "to send", "sending", "sent"),
            frames=frames(
                ("The office plans to file the forms, archive the records, and", "the notices"),
                ("The manager hopes to review the report, sign the memo, and", "the update"),
                ("The clerk will sort the files, label the folders, and", "the package"),
                ("The team wants to check the data, compare the figures, and", "the summary"),
                ("The branch intends to print the forms, seal the envelopes, and", "the delivery"),
                ("The supervisor decided to draft the notice, print the copy, and", "the email"),
                ("The assistant will open the box, inspect the contents, and", "the keys"),
                ("The committee plans to approve the proposal, release the notice, and", "the schedule"),
                ("The staff agreed to call the witness, gather the facts, and", "the statement"),
                ("The officer expects to review the badge, record the number, and", "the form"),
            ),
            explanation="Infinitive series can repeat to before every item or use it only before the first item, but the verbal pattern should stay consistent.",
            tags=("infinitive", "series", "bare-verb"),
        ),
        FamilySpec(
            base_family="noun-series",
            kind="phrase",
            answer="attention to detail",
            choices=("attention to detail", "attention", "detail", "attentive"),
            frames=frames(
                ("The office values accuracy, patience, and", "in every report"),
                ("The job demands discipline, focus, and", "under pressure"),
                ("The work requires honesty, tact, and", "in public service"),
                ("The interview tested knowledge, memory, and", "of procedures"),
                ("The team showed skill, speed, and", "during the drill"),
                ("The branch needs order, silence, and", "at the counter"),
                ("The report needs clarity, brevity, and", "from the writer"),
                ("The clerk brought accuracy, neatness, and", "to the file"),
                ("The office rewards diligence, loyalty, and", "among staff"),
                ("The case called for patience, judgment, and", "from the supervisor"),
            ),
            explanation="A noun series should stay in noun form. The final item should not switch into an adjective or verb form.",
            tags=("noun", "series", "phrase-form"),
        ),
        FamilySpec(
            base_family="adjective-series",
            kind="word",
            answer="clear",
            choices=("clear", "clearly", "clearer", "clearest"),
            frames=frames(
                ("The instructions were simple, direct, and", ""),
                ("The report was brief, accurate, and", ""),
                ("The room felt calm, quiet, and", ""),
                ("The officer remained polite, firm, and", ""),
                ("The note was short, honest, and", ""),
                ("The policy looked strict, fair, and", ""),
                ("The answer was neat, complete, and", ""),
                ("The desk was clean, orderly, and", ""),
                ("The form was easy, fast, and", ""),
                ("The statement was plain, strong, and", ""),
            ),
            explanation="After a linking verb or verb of being, the complements should stay in the same form.",
            tags=("adjective", "linking-verb", "word-form"),
        ),
        FamilySpec(
            base_family="adverb-series",
            kind="word",
            answer="carefully",
            choices=("carefully", "careful", "carelessness", "cautiously"),
            frames=frames(
                ("The clerk worked quickly, quietly, and", ""),
                ("The officer checked the badge slowly, politely, and", ""),
                ("The team moved steadily, silently, and", ""),
                ("The reviewer read the memo closely, patiently, and", ""),
                ("The assistant filed the papers neatly, accurately, and", ""),
                ("The manager listened calmly, attentively, and", ""),
                ("The auditor measured the figures precisely, cautiously, and", ""),
                ("The nurse recorded the details clearly, quietly, and", ""),
                ("The driver parked the car slowly, safely, and", ""),
                ("The staff replied promptly, politely, and", ""),
            ),
            explanation="An adverb series should stay in adverb form. A sudden adjective or noun breaks the pattern.",
            tags=("adverb", "series", "word-form"),
        ),
        FamilySpec(
            base_family="clause-series",
            kind="clause",
            answer="that the work was done",
            choices=(
                "that the work was done",
                "the work was done",
                "that the work done",
                "the work did",
            ),
            frames=frames(
                ("The supervisor said that the memo was ready, that the file was complete, and", ""),
                ("The director explained that the schedule was fixed, that the room was reserved, and", ""),
                ("The report stated that the figures were verified, that the totals matched, and", ""),
                ("The witness testified that the lights were on, that the door was open, and", ""),
                ("The memo showed that the forms were signed, that the entries were correct, and", ""),
                ("The coach noted that the team was prepared, that the players were rested, and", ""),
                ("The letter said that the package had arrived, that the label was intact, and", ""),
                ("The notice confirmed that the office was closed, that the staff was away, and", ""),
                ("The summary explained that the problem was minor, that the fix was simple, and", ""),
                ("The record showed that the files were missing, that the drawer was open, and", ""),
            ),
            explanation="If a series begins with clauses, the final item should also be a clause.",
            tags=("clause", "series", "parallel-clause"),
        ),
        FamilySpec(
            base_family="either-or",
            kind="word",
            answer="call",
            choices=("call", "calling", "called", "to call"),
            frames=frames(
                ("The officer must either", "the witness or speak with the supervisor"),
                ("The clerk can either", "the applicant or review the file"),
                ("The team should either", "the witness or revise the summary"),
                ("The manager may either", "the branch or send the memo"),
                ("The assistant will either", "the office or update the record"),
                ("The supervisor can either", "the reporter or check the log"),
                ("The committee must either", "the witness or open the hearing"),
                ("The staff can either", "the customer or confirm the schedule"),
                ("The director may either", "the witness or report the issue"),
                ("The analyst should either", "the office or clarify the note"),
            ),
            explanation="In an either/or pair, both sides should use the same grammatical pattern.",
            tags=("correlative", "either-or", "verb-form"),
        ),
        FamilySpec(
            base_family="neither-nor",
            kind="word",
            answer="able",
            choices=("able", "ability", "ably", "unable"),
            frames=frames(
                ("The officer was neither tired nor", "to continue"),
                ("The clerk was neither nervous nor", "to present the report"),
                ("The team was neither angry nor", "to discuss the issue"),
                ("The applicant was neither late nor", "to enter"),
                ("The manager was neither distracted nor", "to answer questions"),
                ("The staff was neither confused nor", "to proceed"),
                ("The witness was neither frightened nor", "to testify"),
                ("The guard was neither asleep nor", "to watch the gate"),
                ("The supervisor was neither unwilling nor", "to help"),
                ("The reviewer was neither careless nor", "to check the figures"),
            ),
            explanation="A neither/nor pair should keep the same kind of structure on both sides.",
            tags=("correlative", "neither-nor", "adjective"),
        ),
        FamilySpec(
            base_family="both-and",
            kind="word",
            answer="approved",
            choices=("approved", "approve", "approving", "approval"),
            frames=frames(
                ("The manager both reviewed and", "the memo"),
                ("The officer both checked and", "the report"),
                ("The clerk both read and", "the notice"),
                ("The supervisor both studied and", "the proposal"),
                ("The team both discussed and", "the plan"),
                ("The assistant both drafted and", "the message"),
                ("The reviewer both examined and", "the request"),
                ("The branch both considered and", "the application"),
                ("The committee both checked and", "the budget"),
                ("The director both read and", "the recommendation"),
            ),
            explanation="The both/and pattern should connect matching verbs or matching phrases.",
            tags=("correlative", "both-and", "verb-form"),
        ),
        FamilySpec(
            base_family="not-only-but-also",
            kind="word",
            answer="filed",
            choices=("filed", "file", "filing", "to file"),
            frames=frames(
                ("The supervisor not only checked the figures but also", "the report"),
                ("The clerk not only copied the data but also", "the memo"),
                ("The team not only reviewed the forms but also", "the notices"),
                ("The officer not only explained the rule but also", "the forms"),
                ("The manager not only studied the facts but also", "the records"),
                ("The assistant not only read the note but also", "the letters"),
                ("The branch not only printed the forms but also", "the summary"),
                ("The reviewer not only corrected the draft but also", "the log"),
                ("The staff not only gathered the papers but also", "the statement"),
                ("The witness not only answered the question but also", "the request"),
            ),
            explanation="In a not only/but also pair, both sides should use the same grammatical form.",
            tags=("correlative", "not-only-but-also", "verb-form"),
        ),
        FamilySpec(
            base_family="comparison-than",
            kind="phrase",
            answer="reading",
            choices=("reading", "to read", "read", "reads"),
            frames=frames(
                ("Reading the report is easier than", "it aloud"),
                ("Reading the memo is faster than", "it twice"),
                ("Reading the notice is simpler than", "it in public"),
                ("Reading the draft is better than", "it on the screen"),
                ("Reading the file is easier than", "it from the copy"),
                ("Reading the summary is easier than", "it to the group"),
                ("Reading the chart is quicker than", "it under pressure"),
                ("Reading the note is easier than", "it to a crowd"),
                ("Reading the list is faster than", "it aloud to everyone"),
                ("Reading the memo is easier than", "it line by line"),
            ),
            explanation="A comparison introduced by than should keep the same grammatical form on both sides.",
            tags=("comparison", "than", "gerund"),
        ),
        FamilySpec(
            base_family="comparison-as",
            kind="word",
            answer="did",
            choices=("did", "do", "doing", "done"),
            frames=frames(
                ("The clerk worked as carefully as the auditor", ""),
                ("The assistant typed as neatly as the secretary", ""),
                ("The nurse moved as quietly as the guard", ""),
                ("The team responded as quickly as the staff", ""),
                ("The officer wrote as clearly as the manager", ""),
                ("The student spoke as politely as the applicant", ""),
                ("The reviewer read as closely as the editor", ""),
                ("The branch processed requests as efficiently as the office", ""),
                ("The witness testified as confidently as the expert", ""),
                ("The clerk explained the issue as plainly as the trainer", ""),
            ),
            explanation="An as...as comparison should keep the same grammatical shape on both sides.",
            tags=("comparison", "as-as", "verb-form"),
        ),
        FamilySpec(
            base_family="whether-or",
            kind="word",
            answer="reduce",
            choices=("reduce", "reducing", "reduced", "to reduce"),
            frames=frames(
                ("The office must decide whether to expand services or", "costs"),
                ("The branch must decide whether to hire staff or", "hours"),
                ("The manager asked whether to print more copies or", "paper use"),
                ("The committee debated whether to open early or", "delays"),
                ("The team discussed whether to keep the plan or", "expenses"),
                ("The office considered whether to send more mail or", "waste"),
                ("The supervisor wondered whether to add desks or", "clutter"),
                ("The staff checked whether to store more files or", "storage costs"),
                ("The clerk debated whether to post notices or", "waste"),
                ("The director decided whether to extend hours or", "noise"),
            ),
            explanation="The whether/or pair should keep a matching grammatical pattern after each option.",
            tags=("correlative", "whether-or", "verb-form"),
        ),
        FamilySpec(
            base_family="rather-than",
            kind="word",
            answer="store",
            choices=("store", "storing", "stored", "to store"),
            frames=frames(
                ("The branch chose to scan the records rather than", "them"),
                ("The office decided to email the notice rather than", "it"),
                ("The clerk preferred to copy the file rather than", "the original"),
                ("The team chose to digitize the papers rather than", "them"),
                ("The manager decided to save the memo rather than", "it"),
                ("The staff chose to sort the folders rather than", "them"),
                ("The reviewer wanted to keep the notes rather than", "them"),
                ("The supervisor preferred to archive the forms rather than", "them"),
                ("The officer chose to scan the receipts rather than", "them"),
                ("The analyst decided to record the data rather than", "it"),
            ),
            explanation="Rather than should keep the same grammatical type on both sides of the comparison.",
            tags=("correlative", "rather-than", "verb-form"),
        ),
        FamilySpec(
            base_family="the-more-the-more",
            kind="structure",
            answer="The more carefully",
            choices=("The more carefully", "More carefully", "The most carefully", "The less carefully"),
            frames=frames(
                ("", "the clerk checks the form, the fewer mistakes appear"),
                ("", "the officer reviews the memo, the clearer the summary becomes"),
                ("", "the team studies the report, the better the plan gets"),
                ("", "the assistant compares the figures, the fewer errors remain"),
                ("", "the manager reads the notice, the more accurate the reply becomes"),
                ("", "the clerk inspects the records, the cleaner the list looks"),
                ("", "the auditor checks the totals, the stronger the evidence is"),
                ("", "the reviewer edits the draft, the smoother the final copy sounds"),
                ("", "the staff proofreads the letter, the neater the version becomes"),
                ("", "the officer studies the plan, the more reliable the result is"),
            ),
            explanation="Linked comparisons should keep the repeated pattern balanced on both sides.",
            tags=("correlative-comparison", "linked-change", "parallel-comparison"),
        ),
    )


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
        if tags[0] != "parallel-structure":
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
