"""Generate the Subject-Verb Agreement question bank."""

from __future__ import annotations

import json
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
    / "subject-verb-agreement"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Subject-Verb Agreement"
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
    "basic-number": {
        "Easy": "Which choice best completes the sentence:",
        "Medium": "Which option best completes the sentence:",
        "Hard": "Which choice best fixes the agreement error:",
        "Ultra": "Which completion is most accurate:",
    },
    "compound-and": {
        "Easy": "Which choice best completes the compound-subject sentence:",
        "Medium": "Which option best completes the compound-subject sentence:",
        "Hard": "Which choice best fixes the compound-subject agreement:",
        "Ultra": "Which completion is most accurate for the compound subject:",
    },
    "either-or": {
        "Easy": "Which choice best completes the either/or sentence:",
        "Medium": "Which option best completes the either/or sentence:",
        "Hard": "Which choice best fixes the nearer-subject agreement:",
        "Ultra": "Which completion is most accurate for the nearer subject:",
    },
    "intervening": {
        "Easy": "Which choice best completes the sentence:",
        "Medium": "Which option best completes the sentence:",
        "Hard": "Which choice best fixes the verb form:",
        "Ultra": "Which completion is most accurate:",
    },
    "special-nouns": {
        "Easy": "Which choice best completes the sentence with the special subject:",
        "Medium": "Which option best completes the sentence with the special subject:",
        "Hard": "Which choice best fixes the special-subject agreement:",
        "Ultra": "Which completion is most accurate for the special subject:",
    },
    "quantity-there": {
        "Easy": "Which choice best completes the quantity sentence:",
        "Medium": "Which option best completes the quantity sentence:",
        "Hard": "Which choice best fixes the quantity or there-construction:",
        "Ultra": "Which completion is most accurate for the there/quantity rule:",
    },
}


@dataclass(frozen=True)
class BaseSpec:
    subject: str
    number: str
    singular_form: str
    plural_form: str
    extra_distractors: tuple[str, str]
    contexts: tuple[str, ...]
    explanation: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class FamilySpec:
    slug: str
    topic_tag: str
    rows: tuple[BaseSpec, ...]


def _dedupe_preserve_order(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        normalized = value.strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(normalized)
    return result


def _correct_form(row: BaseSpec) -> str:
    return row.singular_form if row.number == "singular" else row.plural_form


def _opposite_form(row: BaseSpec) -> str:
    return row.plural_form if row.number == "singular" else row.singular_form


def _build_question(
    *,
    question_id: int,
    family: FamilySpec,
    difficulty: str,
    row: BaseSpec,
    context: str,
    context_index: int,
) -> dict:
    prefix = PROMPT_PREFIXES[family.slug][difficulty]
    stem = f'{prefix} "{row.subject} ____ {context}."'
    correct = _correct_form(row)
    choices = _dedupe_preserve_order(
        [correct, _opposite_form(row), *row.extra_distractors]
    )
    if len(choices) != 4:
        raise ValueError(
            f"expected 4 unique choices for question {question_id}, got {choices}"
        )
    if correct not in choices:
        raise ValueError(f"correct answer missing from choices for question {question_id}")

    rotation = (question_id + context_index) % 4
    choices = choices[rotation:] + choices[:rotation]

    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": stem,
        "choices": choices,
        "answer": correct,
        "explanation": row.explanation,
        "tags": [
            "subject-verb",
            family.topic_tag,
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
    seen_questions: set[str] = set()

    for index, item in enumerate(items, start=1):
        if item.get("id") != index:
            raise ValueError(f"question ids must be sequential; found {item.get('id')} at position {index}")

        question = str(item.get("question", "")).strip()
        if not question:
            raise ValueError(f"blank question text at id {index}")
        if question in seen_questions:
            raise ValueError(f"duplicate question text at id {index}")
        seen_questions.add(question)

        difficulty = str(item.get("difficulty", "")).strip()
        if difficulty not in actual_difficulties:
            raise ValueError(f"invalid difficulty {difficulty!r} at id {index}")
        actual_difficulties[difficulty] += 1

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

    if actual_difficulties != expected_difficulties:
        raise ValueError(f"unexpected difficulty counts: {actual_difficulties}")


def _family_rows() -> tuple[FamilySpec, ...]:
    shared_number_contexts = (
        "ready for the briefing",
        "under review",
        "on the agenda",
        "before lunch",
        "after the briefing",
    )

    shared_compound_contexts = (
        "already submitted the final forms",
        "just reviewed the schedule",
        "already packed the files",
        "recently finished the checklist",
        "already signed the memo",
    )

    shared_either_or_contexts = (
        "ready for the briefing",
        "on duty in the control room",
        "in charge of the filing desk",
        "waiting near the gate",
        "available after lunch",
    )

    shared_regular_contexts = (
        "the account numbers before filing",
        "the corrected entries",
        "the final notes from the meeting",
        "the shipping details for the form",
        "the updated report data",
    )

    return (
        FamilySpec(
            slug="basic-number",
            topic_tag="basic-number-agreement",
            rows=(
                BaseSpec(
                    subject="The committee",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_number_contexts,
                    explanation="The head noun committee is singular, so the verb must be singular.",
                    tags=("agreement", "head-noun", "be-verb"),
                ),
                BaseSpec(
                    subject="The research team",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_number_contexts,
                    explanation="The head noun team is singular, so the verb must be singular.",
                    tags=("agreement", "head-noun", "be-verb"),
                ),
                BaseSpec(
                    subject="The reports from the branch office",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_number_contexts,
                    explanation="The head noun reports is plural, so the verb must be plural.",
                    tags=("agreement", "head-noun", "be-verb"),
                ),
                BaseSpec(
                    subject="The analysts in the review unit",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_number_contexts,
                    explanation="The head noun analysts is plural, so the verb must be plural.",
                    tags=("agreement", "head-noun", "be-verb"),
                ),
                BaseSpec(
                    subject="The archive of signed forms",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_number_contexts,
                    explanation="The head noun archive is singular; the phrase after of does not change the verb.",
                    tags=("agreement", "head-noun", "be-verb"),
                ),
            ),
        ),
        FamilySpec(
            slug="compound-and",
            topic_tag="compound-subject",
            rows=(
                BaseSpec(
                    subject="Nina and Marco",
                    number="plural",
                    singular_form="has",
                    plural_form="have",
                    extra_distractors=("had", "having"),
                    contexts=shared_compound_contexts,
                    explanation="Subjects joined by and are plural, so the verb must be plural.",
                    tags=("agreement", "compound-subject", "and"),
                ),
                BaseSpec(
                    subject="The manager and the assistant",
                    number="plural",
                    singular_form="has",
                    plural_form="have",
                    extra_distractors=("had", "having"),
                    contexts=shared_compound_contexts,
                    explanation="Subjects joined by and are plural, so the verb must be plural.",
                    tags=("agreement", "compound-subject", "and"),
                ),
                BaseSpec(
                    subject="My aunt and my uncle",
                    number="plural",
                    singular_form="has",
                    plural_form="have",
                    extra_distractors=("had", "having"),
                    contexts=shared_compound_contexts,
                    explanation="Subjects joined by and are plural, so the verb must be plural.",
                    tags=("agreement", "compound-subject", "and"),
                ),
                BaseSpec(
                    subject="The chairperson and the secretary",
                    number="plural",
                    singular_form="has",
                    plural_form="have",
                    extra_distractors=("had", "having"),
                    contexts=shared_compound_contexts,
                    explanation="Subjects joined by and are plural, so the verb must be plural.",
                    tags=("agreement", "compound-subject", "and"),
                ),
                BaseSpec(
                    subject="The driver and the guide",
                    number="plural",
                    singular_form="has",
                    plural_form="have",
                    extra_distractors=("had", "having"),
                    contexts=shared_compound_contexts,
                    explanation="Subjects joined by and are plural, so the verb must be plural.",
                    tags=("agreement", "compound-subject", "and"),
                ),
            ),
        ),
        FamilySpec(
            slug="either-or",
            topic_tag="either-or-agreement",
            rows=(
                BaseSpec(
                    subject="Either the director or the assistants",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_either_or_contexts,
                    explanation="With either/or, the verb agrees with the nearer subject. Here the nearer subject is assistants, which is plural.",
                    tags=("agreement", "either-or", "nearest-subject"),
                ),
                BaseSpec(
                    subject="Either the assistants or the director",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_either_or_contexts,
                    explanation="With either/or, the verb agrees with the nearer subject. Here the nearer subject is director, which is singular.",
                    tags=("agreement", "either-or", "nearest-subject"),
                ),
                BaseSpec(
                    subject="Neither the guards nor the supervisor",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_either_or_contexts,
                    explanation="With neither/nor, the verb agrees with the nearer subject. Here the nearer subject is supervisor, which is singular.",
                    tags=("agreement", "neither-nor", "nearest-subject"),
                ),
                BaseSpec(
                    subject="Neither the supervisor nor the guards",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_either_or_contexts,
                    explanation="With neither/nor, the verb agrees with the nearer subject. Here the nearer subject is guards, which is plural.",
                    tags=("agreement", "neither-nor", "nearest-subject"),
                ),
                BaseSpec(
                    subject="Either the clerk or the records officers",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=shared_either_or_contexts,
                    explanation="With either/or, the verb agrees with the nearer subject. Here the nearer subject is records officers, which is plural.",
                    tags=("agreement", "either-or", "nearest-subject"),
                ),
            ),
        ),
        FamilySpec(
            slug="intervening",
            topic_tag="intervening-phrases",
            rows=(
                BaseSpec(
                    subject="The inspector",
                    number="singular",
                    singular_form="reviews",
                    plural_form="review",
                    extra_distractors=("reviewed", "reviewing"),
                    contexts=shared_regular_contexts,
                    explanation="The subject inspector is singular, so the present-tense verb must take -s.",
                    tags=("agreement", "regular-verb", "singular"),
                ),
                BaseSpec(
                    subject="The inspectors",
                    number="plural",
                    singular_form="reviews",
                    plural_form="review",
                    extra_distractors=("reviewed", "reviewing"),
                    contexts=shared_regular_contexts,
                    explanation="The subject inspectors is plural, so the present-tense verb must stay in base form.",
                    tags=("agreement", "regular-verb", "plural"),
                ),
                BaseSpec(
                    subject="The system log",
                    number="singular",
                    singular_form="contains",
                    plural_form="contain",
                    extra_distractors=("contained", "containing"),
                    contexts=shared_regular_contexts,
                    explanation="The subject log is singular, so the verb must be singular.",
                    tags=("agreement", "regular-verb", "singular"),
                ),
                BaseSpec(
                    subject="The system logs",
                    number="plural",
                    singular_form="contains",
                    plural_form="contain",
                    extra_distractors=("contained", "containing"),
                    contexts=shared_regular_contexts,
                    explanation="The subject logs is plural, so the verb must be plural.",
                    tags=("agreement", "regular-verb", "plural"),
                ),
                BaseSpec(
                    subject="The clerk",
                    number="singular",
                    singular_form="checks",
                    plural_form="check",
                    extra_distractors=("checked", "checking"),
                    contexts=shared_regular_contexts,
                    explanation="The subject clerk is singular, so the present-tense verb must take -s.",
                    tags=("agreement", "regular-verb", "singular"),
                ),
            ),
        ),
        FamilySpec(
            slug="special-nouns",
            topic_tag="special-nouns",
            rows=(
                BaseSpec(
                    subject="Each of the applicants",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "ready for the interview",
                        "waiting outside the office",
                        "under the new screening rule",
                        "short on time before lunch",
                        "being checked by the clerk",
                    ),
                    explanation="Each is singular, even when it refers to many people.",
                    tags=("agreement", "indefinite-pronoun", "singular"),
                ),
                BaseSpec(
                    subject="Everyone on the committee",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "ready for the meeting",
                        "at the front table",
                        "under review this morning",
                        "waiting for the signal",
                        "being asked to sign in",
                    ),
                    explanation="Everyone is singular in grammar, even when it means many people.",
                    tags=("agreement", "indefinite-pronoun", "singular"),
                ),
                BaseSpec(
                    subject="Neither of the routes",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "open before dawn",
                        "available after the rain",
                        "clear for travel",
                        "under repair",
                        "ready for use",
                    ),
                    explanation="Neither is singular in grammar.",
                    tags=("agreement", "indefinite-pronoun", "singular"),
                ),
                BaseSpec(
                    subject="The news from the province",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "encouraging",
                        "under review by the editor",
                        "lacking detail",
                        "coming from the district office",
                        "being discussed on air",
                    ),
                    explanation="News is a special singular noun in standard agreement.",
                    tags=("agreement", "special-singular-noun", "singular"),
                ),
                BaseSpec(
                    subject="The scissors on the tray",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "ready for use",
                        "on the tray",
                        "missing from the supply box",
                        "near the paper stack",
                        "kept in the drawer",
                    ),
                    explanation="Scissors is plural in form and takes a plural verb.",
                    tags=("agreement", "pluralia-tantum", "plural"),
                ),
            ),
        ),
        FamilySpec(
            slug="quantity-there",
            topic_tag="quantity-there",
            rows=(
                BaseSpec(
                    subject="There",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "several folders on the cart",
                        "many reasons for the delay",
                        "two open windows in the hall",
                        "a stack of files beside the desk",
                        "numerous officers at the gate",
                    ),
                    explanation="In there-constructions, the verb agrees with the noun that follows it. Here the noun is plural.",
                    tags=("agreement", "there-construction", "plural"),
                ),
                BaseSpec(
                    subject="There",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "a single folder on the cart",
                        "one reason for the delay",
                        "one open window in the hall",
                        "a sealed file beside the desk",
                        "a lone officer at the gate",
                    ),
                    explanation="In there-constructions, the verb agrees with the noun that follows it. Here the noun is singular.",
                    tags=("agreement", "there-construction", "singular"),
                ),
                BaseSpec(
                    subject="A number of volunteers",
                    number="plural",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "waiting outside the hall",
                        "arriving after the briefing",
                        "still signing in",
                        "assembling near the gate",
                        "ready to help with registration",
                    ),
                    explanation="A number of means several, so it takes a plural verb.",
                    tags=("agreement", "quantity", "plural"),
                ),
                BaseSpec(
                    subject="The number of volunteers",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "rising this week",
                        "still unknown",
                        "small this year",
                        "limited by the budget",
                        "exactly ten",
                    ),
                    explanation="The number of is singular because number is the head noun.",
                    tags=("agreement", "quantity", "singular"),
                ),
                BaseSpec(
                    subject="The committee",
                    number="singular",
                    singular_form="is",
                    plural_form="are",
                    extra_distractors=("was", "were"),
                    contexts=(
                        "meeting as a unit",
                        "ready to vote",
                        "under review",
                        "still waiting",
                        "scheduled for tomorrow",
                    ),
                    explanation="A collective noun like committee is singular when the group is treated as one unit.",
                    tags=("agreement", "collective-noun", "singular"),
                ),
            ),
        ),
    )


def build_bank() -> list[dict]:
    items: list[dict] = []
    question_id = 1
    families = _family_rows()

    for difficulty in DIFFICULTIES:
        for family in families:
            for row in family.rows:
                for context_index, context in enumerate(row.contexts):
                    items.append(
                        _build_question(
                            question_id=question_id,
                            family=family,
                            difficulty=difficulty,
                            row=row,
                            context=context,
                            context_index=context_index,
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
    print("Validation passed: unique questions, sequential ids, and balanced difficulty counts.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
