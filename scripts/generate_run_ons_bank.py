"""Generate the Verbal Ability / Sentence Structure / Run-ons question bank."""

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
    / "sentence-structure"
    / "run-ons"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Run-ons"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "run-ons"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

QUESTION_STEMS: dict[str, dict[str, str]] = {
    "complete-sentence": {
        "Easy": "Which sentence is complete as written in the {context}?",
        "Medium": "Which sentence can stand alone as a complete sentence in the {context}?",
        "Hard": "Which sentence is the only complete sentence in the {context}?",
        "Ultra": "Which sentence needs no boundary repair in the {context}?",
    },
    "run-on-identification": {
        "Easy": "Which sentence is the run-on in the {context}?",
        "Medium": "Which sentence shows a run-on error in the {context}?",
        "Hard": "Which sentence best shows two independent clauses joined incorrectly in the {context}?",
        "Ultra": "Which sentence is the clear run-on in the {context}?",
    },
    "comma-splice-identification": {
        "Easy": "Which sentence is the comma splice in the {context}?",
        "Medium": "Which sentence shows a comma splice in the {context}?",
        "Hard": "Which sentence best shows two independent clauses joined by only a comma in the {context}?",
        "Ultra": "Which sentence is the clear comma splice in the {context}?",
    },
    "fused-sentence-identification": {
        "Easy": "Which sentence is the fused sentence in the {context}?",
        "Medium": "Which sentence shows a fused sentence in the {context}?",
        "Hard": "Which sentence best shows two independent clauses pushed together with no punctuation in the {context}?",
        "Ultra": "Which sentence is the clear fused sentence in the {context}?",
    },
    "fix-period": {
        "Easy": 'Which revision correctly fixes "{original}" by splitting it into two sentences?',
        "Medium": 'Which revision best fixes "{original}" with two separate sentences?',
        "Hard": 'Which choice best repairs "{original}" by using a period?',
        "Ultra": 'Which revision is the correct two-sentence fix for "{original}"?',
    },
    "split-period": {
        "Easy": 'Which revision correctly separates the clauses in "{original}" with a period?',
        "Medium": 'Which revision best separates the clauses in "{original}" with a period?',
        "Hard": 'Which choice best splits "{original}" into two complete sentences?',
        "Ultra": 'Which revision is the clean period split for "{original}"?',
    },
    "fix-semicolon": {
        "Easy": 'Which revision correctly fixes "{original}" with a semicolon?',
        "Medium": 'Which revision best fixes "{original}" with a semicolon?',
        "Hard": 'Which choice best uses a semicolon to repair "{original}"?',
        "Ultra": 'Which revision is the correct semicolon fix for "{original}"?',
    },
    "join-semicolon": {
        "Easy": 'Which revision correctly joins the clauses in "{original}" with a semicolon?',
        "Medium": 'Which revision best joins the clauses in "{original}" with a semicolon?',
        "Hard": 'Which choice best turns "{original}" into a semicolon-linked pair?',
        "Ultra": 'Which revision is the clearest semicolon join for "{original}"?',
    },
    "fix-comma-conjunction": {
        "Easy": 'Which revision correctly fixes "{original}" with a comma and a coordinating conjunction?',
        "Medium": 'Which revision best fixes "{original}" with a comma and conjunction?',
        "Hard": 'Which choice best uses comma plus coordinating conjunction to repair "{original}"?',
        "Ultra": 'Which revision is the correct comma-and-conjunction fix for "{original}"?',
    },
    "join-comma-conjunction": {
        "Easy": 'Which revision correctly joins the clauses in "{original}" with a comma and a coordinating conjunction?',
        "Medium": 'Which revision best joins the clauses in "{original}" with a comma and a coordinating conjunction?',
        "Hard": 'Which choice best makes "{original}" into a proper compound sentence?',
        "Ultra": 'Which revision is the clearest comma-plus-conjunction join for "{original}"?',
    },
    "fix-subordinator": {
        "Easy": 'Which revision correctly fixes "{original}" by making one clause dependent?',
        "Medium": 'Which revision best fixes "{original}" with a subordinating conjunction?',
        "Hard": 'Which choice best repairs "{original}" by turning one clause into a dependent clause?',
        "Ultra": 'Which revision is the correct subordinating fix for "{original}"?',
    },
    "join-subordinator": {
        "Easy": 'Which revision correctly joins the ideas in "{original}" with a subordinating conjunction?',
        "Medium": 'Which revision best joins the ideas in "{original}" with a subordinating conjunction?',
        "Hard": 'Which choice best makes one clause dependent in "{original}"?',
        "Ultra": 'Which revision is the clearest subordinating join for "{original}"?',
    },
    "no-correction-needed": {
        "Easy": "Which sentence needs no correction in the {context}?",
        "Medium": "Which sentence is already correct in the {context}?",
        "Hard": "Which sentence can stay exactly as written in the {context}?",
        "Ultra": "Which sentence is the one that needs no run-on fix in the {context}?",
    },
    "sentence-boundary-check": {
        "Easy": 'Which revision keeps the boundary between the two ideas clearest in "{original}"?',
        "Medium": 'Which revision best keeps the clauses separate in "{original}"?',
        "Hard": 'Which choice best uses a full stop to separate the clauses in "{original}"?',
        "Ultra": 'Which revision is the clearest sentence-boundary repair for "{original}"?',
    },
    "same-meaning-revision": {
        "Easy": 'Which revision best preserves the relationship between the ideas in "{original}"?',
        "Medium": 'Which revision keeps the original meaning while fixing the run-on in "{original}"?',
        "Hard": 'Which choice best repairs "{original}" without losing the connection between the clauses?',
        "Ultra": 'Which revision is the most faithful meaning-preserving fix for "{original}"?',
    },
}


@dataclass(frozen=True)
class Scene:
    context: str
    original: str
    complete: str
    run_on: str
    comma_splice: str
    period_fix: str
    semicolon_fix: str
    comma_conjunction_fix: str
    subordinator_fix: str


@dataclass(frozen=True)
class FamilySpec:
    base_family: str
    answer_attr: str
    option_attrs: tuple[str, str, str, str]
    explanation: str
    tags: tuple[str, ...]


def _lower_initial(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def _upper_initial(text: str) -> str:
    return text[:1].upper() + text[1:] if text else text


def _scene(
    *,
    context: str,
    complete: str,
    clause_one: str,
    clause_two: str,
    conjunction: str,
    subordinator: str,
) -> Scene:
    run_on = f"{clause_one} {_lower_initial(clause_two)}."
    comma_splice = f"{clause_one}, {_lower_initial(clause_two)}."
    period_fix = f"{clause_one}. {_upper_initial(clause_two)}."
    semicolon_fix = f"{clause_one}; {_lower_initial(clause_two)}."
    comma_conjunction_fix = f"{clause_one}, {conjunction} {_lower_initial(clause_two)}."
    subordinator_fix = f"{_upper_initial(subordinator)} {_lower_initial(clause_one)}, {_lower_initial(clause_two)}."
    return Scene(
        context=context,
        original=run_on,
        complete=complete,
        run_on=run_on,
        comma_splice=comma_splice,
        period_fix=period_fix,
        semicolon_fix=semicolon_fix,
        comma_conjunction_fix=comma_conjunction_fix,
        subordinator_fix=subordinator_fix,
    )


def _rotate_choices(choices: list[str], question_id: int, scene_index: int) -> list[str]:
    rotation = (question_id + scene_index) % len(choices)
    return choices[rotation:] + choices[:rotation]


def _scene_values(scene: Scene) -> dict[str, str]:
    return {
        "context": scene.context,
        "original": scene.original,
        "complete": scene.complete,
        "run_on": scene.run_on,
        "comma_splice": scene.comma_splice,
        "period_fix": scene.period_fix,
        "semicolon_fix": scene.semicolon_fix,
        "comma_conjunction_fix": scene.comma_conjunction_fix,
        "subordinator_fix": scene.subordinator_fix,
    }


SCENES: tuple[Scene, ...] = (
    _scene(
        context="filing-desk set",
        complete="The clerk filed the memo before lunch.",
        clause_one="The clerk filed the memo",
        clause_two="the supervisor signed it",
        conjunction="and",
        subordinator="After",
    ),
    _scene(
        context="morning memo set",
        complete="The office opened early today.",
        clause_one="The office opened early",
        clause_two="the lights stayed dim",
        conjunction="but",
        subordinator="Although",
    ),
    _scene(
        context="branch update set",
        complete="The printer jammed during the meeting.",
        clause_one="The printer jammed",
        clause_two="the staff waited",
        conjunction="so",
        subordinator="Because",
    ),
    _scene(
        context="training note set",
        complete="The meeting ended at noon.",
        clause_one="The meeting ended",
        clause_two="the assistant sent the notice",
        conjunction="and",
        subordinator="After",
    ),
    _scene(
        context="office reminder set",
        complete="The schedule changed overnight.",
        clause_one="The schedule changed",
        clause_two="everyone stayed calm",
        conjunction="yet",
        subordinator="Although",
    ),
    _scene(
        context="report excerpt set",
        complete="The server failed yesterday.",
        clause_one="The server failed",
        clause_two="the staff restarted it",
        conjunction="and",
        subordinator="When",
    ),
    _scene(
        context="noticeboard set",
        complete="The officer reviewed the file carefully.",
        clause_one="The officer reviewed the file",
        clause_two="the supervisor approved it",
        conjunction="and",
        subordinator="After",
    ),
    _scene(
        context="shift log set",
        complete="The lights flickered at dusk.",
        clause_one="The lights flickered",
        clause_two="the office lost power",
        conjunction="so",
        subordinator="Because",
    ),
    _scene(
        context="supervisor memo set",
        complete="The form was short but clear.",
        clause_one="The form was short",
        clause_two="the instructions were long",
        conjunction="but",
        subordinator="While",
    ),
    _scene(
        context="workplace bulletin set",
        complete="The report was ready this morning.",
        clause_one="The report was ready",
        clause_two="the manager approved it",
        conjunction="and",
        subordinator="After",
    ),
)


FAMILY_SPECS: tuple[FamilySpec, ...] = (
    FamilySpec(
        base_family="complete-sentence",
        answer_attr="complete",
        option_attrs=("complete", "run_on", "comma_splice", "period_fix"),
        explanation="A complete sentence has one independent clause and no boundary error.",
        tags=("diagnosis", "complete"),
    ),
    FamilySpec(
        base_family="run-on-identification",
        answer_attr="run_on",
        option_attrs=("run_on", "comma_splice", "complete", "period_fix"),
        explanation="A run-on joins independent clauses without a correct boundary.",
        tags=("diagnosis", "run-on"),
    ),
    FamilySpec(
        base_family="comma-splice-identification",
        answer_attr="comma_splice",
        option_attrs=("comma_splice", "run_on", "complete", "period_fix"),
        explanation="A comma splice joins two independent clauses with only a comma.",
        tags=("diagnosis", "comma-splice"),
    ),
    FamilySpec(
        base_family="fused-sentence-identification",
        answer_attr="run_on",
        option_attrs=("run_on", "comma_splice", "complete", "period_fix"),
        explanation="A fused sentence pushes two independent clauses together with no punctuation.",
        tags=("diagnosis", "fused"),
    ),
    FamilySpec(
        base_family="fix-period",
        answer_attr="period_fix",
        option_attrs=("period_fix", "semicolon_fix", "comma_conjunction_fix", "subordinator_fix"),
        explanation="A period creates two separate sentences and removes the run-on.",
        tags=("repair", "period"),
    ),
    FamilySpec(
        base_family="split-period",
        answer_attr="period_fix",
        option_attrs=("period_fix", "semicolon_fix", "comma_conjunction_fix", "subordinator_fix"),
        explanation="A period cleanly separates two independent clauses into two sentences.",
        tags=("repair", "period"),
    ),
    FamilySpec(
        base_family="fix-semicolon",
        answer_attr="semicolon_fix",
        option_attrs=("semicolon_fix", "period_fix", "comma_conjunction_fix", "subordinator_fix"),
        explanation="A semicolon can join two closely related independent clauses.",
        tags=("repair", "semicolon"),
    ),
    FamilySpec(
        base_family="join-semicolon",
        answer_attr="semicolon_fix",
        option_attrs=("semicolon_fix", "period_fix", "comma_conjunction_fix", "subordinator_fix"),
        explanation="A semicolon correctly links two independent clauses that belong together.",
        tags=("repair", "semicolon"),
    ),
    FamilySpec(
        base_family="fix-comma-conjunction",
        answer_attr="comma_conjunction_fix",
        option_attrs=("comma_conjunction_fix", "period_fix", "semicolon_fix", "subordinator_fix"),
        explanation="A comma plus a coordinating conjunction correctly joins two independent clauses.",
        tags=("repair", "comma-conjunction"),
    ),
    FamilySpec(
        base_family="join-comma-conjunction",
        answer_attr="comma_conjunction_fix",
        option_attrs=("comma_conjunction_fix", "period_fix", "semicolon_fix", "subordinator_fix"),
        explanation="A coordinating conjunction with a comma makes the sentence a proper compound sentence.",
        tags=("repair", "comma-conjunction"),
    ),
    FamilySpec(
        base_family="fix-subordinator",
        answer_attr="subordinator_fix",
        option_attrs=("subordinator_fix", "period_fix", "semicolon_fix", "comma_conjunction_fix"),
        explanation="A subordinating conjunction makes one clause dependent and clears the run-on.",
        tags=("repair", "subordinator"),
    ),
    FamilySpec(
        base_family="join-subordinator",
        answer_attr="subordinator_fix",
        option_attrs=("subordinator_fix", "period_fix", "semicolon_fix", "comma_conjunction_fix"),
        explanation="A subordinating conjunction can show the relationship between the clauses more clearly.",
        tags=("repair", "subordinator"),
    ),
    FamilySpec(
        base_family="no-correction-needed",
        answer_attr="complete",
        option_attrs=("complete", "run_on", "comma_splice", "period_fix"),
        explanation="The complete sentence has one independent clause and no boundary problem.",
        tags=("diagnosis", "complete"),
    ),
    FamilySpec(
        base_family="sentence-boundary-check",
        answer_attr="period_fix",
        option_attrs=("period_fix", "semicolon_fix", "comma_conjunction_fix", "subordinator_fix"),
        explanation="A period gives the clearest break when the ideas should stand separately.",
        tags=("repair", "boundary"),
    ),
    FamilySpec(
        base_family="same-meaning-revision",
        answer_attr="subordinator_fix",
        option_attrs=("subordinator_fix", "period_fix", "semicolon_fix", "comma_conjunction_fix"),
        explanation="A subordinating conjunction keeps the relationship between the ideas visible.",
        tags=("repair", "meaning"),
    ),
)


def _build_question(
    *,
    question_id: int,
    family: FamilySpec,
    scene: Scene,
    scene_index: int,
    difficulty: str,
) -> dict[str, object]:
    values = _scene_values(scene)
    choices = [getattr(scene, attr) for attr in family.option_attrs]
    answer = getattr(scene, family.answer_attr)
    question = QUESTION_STEMS[family.base_family][difficulty].format(**values)
    rotated = _rotate_choices(choices, question_id, scene_index)
    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": rotated,
        "answer": answer,
        "explanation": family.explanation,
        "tags": [ROOT_TAG, family.base_family, DIFFICULTY_TAGS[difficulty], *family.tags],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _build_bank() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    question_id = 1
    for difficulty in DIFFICULTIES:
        for family in FAMILY_SPECS:
            for scene_index, scene in enumerate(SCENES):
                questions.append(
                    _build_question(
                        question_id=question_id,
                        family=family,
                        scene=scene,
                        scene_index=scene_index,
                        difficulty=difficulty,
                    )
                )
                question_id += 1
    return questions


def _validate_bank(questions: list[dict[str, object]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [int(question["id"]) for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    difficulty_counts = Counter(str(question["difficulty"]) for question in questions)
    expected_difficulty_counts = {difficulty: 150 for difficulty in DIFFICULTIES}
    if difficulty_counts != expected_difficulty_counts:
        raise ValueError(f"unexpected difficulty distribution: {dict(difficulty_counts)}")

    family_counts = Counter(str(question["tags"][1]) for question in questions)
    expected_family_counts = {
        family.base_family: 40 for family in FAMILY_SPECS
    }
    if family_counts != expected_family_counts:
        raise ValueError(f"unexpected family distribution: {dict(family_counts)}")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise ValueError("question texts are not unique")

    for index, question in enumerate(questions, start=1):
        if question.get("subtest") != SUBTEST:
            raise ValueError(f"invalid subtest at id {index}")
        if question.get("module") != MODULE:
            raise ValueError(f"invalid module at id {index}")
        if question.get("subtopic") != SUBTOPIC:
            raise ValueError(f"invalid subtopic at id {index}")
        if question.get("category") != CATEGORY:
            raise ValueError(f"invalid category at id {index}")
        if question.get("language") != LANGUAGE:
            raise ValueError(f"invalid language at id {index}")

        choices = question.get("choices")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"invalid choices at id {index}")
        normalized = [str(choice).strip() for choice in choices]
        if any(not choice for choice in normalized):
            raise ValueError(f"blank choice at id {index}")
        if len(set(normalized)) != len(normalized):
            raise ValueError(f"duplicate choices at id {index}")

        answer = str(question.get("answer", "")).strip()
        if answer not in normalized:
            raise ValueError(f"answer {answer!r} not present in choices at id {index}")

        explanation = str(question.get("explanation", "")).strip()
        if not explanation:
            raise ValueError(f"blank explanation at id {index}")

        question_text = str(question.get("question", ""))
        if "Which option best completes the sentence" in question_text:
            raise ValueError(f"generic prompt detected at id {index}")


def main() -> None:
    questions = _build_bank()
    _validate_bank(questions)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(questions)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
