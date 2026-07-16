"""Generate the Verbal Ability / Sentence Structure / Compound Sentences question bank."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "sentence-structure"
    / "compound-sentences"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Compound Sentences"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "compound-sentences"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}


@dataclass(frozen=True)
class Scene:
    context: str
    compound: str
    simple: str
    complex: str
    compound_complex: str
    comma_splice: str
    fused: str
    semicolon: str
    period_split: str
    conjunction: str
    relation_prompt: str
    clause_count: int = 2


@dataclass(frozen=True)
class FamilySpec:
    base_family: str
    choice_builder: Callable[[Scene], list[str]]
    answer_builder: Callable[[Scene], str]
    explanation: str
    tags: tuple[str, ...]


def _scene_values(scene: Scene) -> dict[str, str]:
    return {
        "context": scene.context,
        "compound": scene.compound,
        "simple": scene.simple,
        "complex": scene.complex,
        "compound_complex": scene.compound_complex,
        "comma_splice": scene.comma_splice,
        "fused": scene.fused,
        "semicolon": scene.semicolon,
        "period_split": scene.period_split,
        "conjunction": scene.conjunction,
        "relation_prompt": scene.relation_prompt,
        "conjunction_blank": scene.compound.replace(f", {scene.conjunction} ", ", ____ ", 1),
        "punctuation_blank": scene.compound.replace(
            f", {scene.conjunction} ", " ____ " + scene.conjunction + " ", 1
        ),
        "count": str(scene.clause_count),
    }


def _sentence_choices(*attrs: str) -> Callable[[Scene], list[str]]:
    def builder(scene: Scene) -> list[str]:
        return [getattr(scene, attr) for attr in attrs]

    return builder


def _fixed_choices(*choices: str) -> Callable[[Scene], list[str]]:
    def builder(_: Scene) -> list[str]:
        return list(choices)

    return builder


def _attr_answer(attr: str) -> Callable[[Scene], str]:
    def builder(scene: Scene) -> str:
        return str(getattr(scene, attr))

    return builder


def _fixed_answer(answer: str) -> Callable[[Scene], str]:
    def builder(_: Scene) -> str:
        return answer

    return builder


CONJUNCTION_CHOICES: dict[str, tuple[str, str, str, str]] = {
    "and": ("and", "but", "or", "because"),
    "but": ("but", "and", "or", "so"),
    "yet": ("yet", "and", "or", "so"),
    "so": ("so", "and", "but", "because"),
    "or": ("or", "and", "but", "nor"),
    "nor": ("nor", "and", "but", "or"),
    "for": ("for", "and", "but", "because"),
}


def _conjunction_choices(scene: Scene) -> list[str]:
    return list(CONJUNCTION_CHOICES[scene.conjunction])


QUESTION_STEMS: dict[str, dict[str, str]] = {
    "compound-sentence-identification": {
        "Easy": "Which sentence is the compound sentence in the {context}?",
        "Medium": "In the {context}, which sentence joins two independent clauses correctly?",
        "Hard": "Which choice is the compound sentence in the {context}?",
        "Ultra": "Which sentence shows two complete thoughts joined correctly in the {context}?",
    },
    "independent-clause-count": {
        "Easy": 'How many independent clauses are in "{compound}"?',
        "Medium": 'In "{compound}", how many independent clauses are present?',
        "Hard": 'What is the number of independent clauses in "{compound}"?',
        "Ultra": 'How many complete thoughts appear in "{compound}"?',
    },
    "coordinating-conjunction-identification": {
        "Easy": 'Which word is the coordinating conjunction in "{compound}"?',
        "Medium": 'In "{compound}", which word is the FANBOYS conjunction?',
        "Hard": 'Which coordinating conjunction links the two clauses in "{compound}"?',
        "Ultra": 'Which conjunction joins the independent clauses in "{compound}"?',
    },
    "relation-based-conjunction-choice": {
        "Easy": "Which coordinating conjunction best expresses {relation_prompt} in the {context}?",
        "Medium": "Which conjunction best fits {relation_prompt} in the {context}?",
        "Hard": "Which FANBOYS conjunction best expresses {relation_prompt} in the {context}?",
        "Ultra": "Which coordinating conjunction most clearly matches {relation_prompt} in the {context}?",
    },
    "coordinating-conjunction-fill-in": {
        "Easy": 'Which coordinating conjunction completes "{conjunction_blank}"?',
        "Medium": 'Which word correctly completes "{conjunction_blank}"?',
        "Hard": 'Which FANBOYS word belongs in the blank in "{conjunction_blank}"?',
        "Ultra": 'Which coordinating conjunction should replace the blank in "{conjunction_blank}"?',
    },
    "comma-conjunction-revision": {
        "Easy": 'Which revision correctly joins the clauses in "{comma_splice}" with a comma and conjunction?',
        "Medium": 'Which sentence best fixes "{comma_splice}" by adding the right comma and conjunction?',
        "Hard": 'Which choice correctly turns "{comma_splice}" into a compound sentence?',
        "Ultra": 'Which revision uses the correct comma-before-conjunction pattern for "{comma_splice}"?',
    },
    "semicolon-revision": {
        "Easy": 'Which revision correctly joins the clauses in "{fused}" with a semicolon?',
        "Medium": 'Which sentence best repairs "{fused}" with a semicolon?',
        "Hard": 'Which choice correctly uses a semicolon to connect the two clauses in "{fused}"?',
        "Ultra": 'Which revision gives the clearest semicolon join for "{fused}"?',
    },
    "simple-sentence-identification": {
        "Easy": "Which sentence is simple, not compound, in the {context}?",
        "Medium": "In the {context}, which sentence has only one independent clause?",
        "Hard": "Which choice is the simple sentence in the {context}?",
        "Ultra": "Which sentence is a single independent clause in the {context}?",
    },
    "complex-sentence-identification": {
        "Easy": "Which sentence is complex, not compound, in the {context}?",
        "Medium": "In the {context}, which sentence has one dependent clause?",
        "Hard": "Which choice is the complex sentence in the {context}?",
        "Ultra": "Which sentence shows one dependent clause and one independent clause in the {context}?",
    },
    "compound-complex-identification": {
        "Easy": "Which sentence is compound-complex in the {context}?",
        "Medium": "In the {context}, which sentence has two independent clauses and one dependent clause?",
        "Hard": "Which choice is the compound-complex sentence in the {context}?",
        "Ultra": "Which sentence combines dependent and compound structure in the {context}?",
    },
    "correct-compound-punctuation": {
        "Easy": "Which sentence is punctuated correctly as a compound sentence in the {context}?",
        "Medium": "In the {context}, which sentence uses the correct compound-sentence punctuation?",
        "Hard": "Which choice shows the proper punctuation for a compound sentence in the {context}?",
        "Ultra": "Which sentence is the correctly punctuated compound sentence in the {context}?",
    },
    "comma-splice-diagnosis": {
        "Easy": "Which sentence is the comma splice in the {context}?",
        "Medium": "In the {context}, which sentence joins two independent clauses with only a comma?",
        "Hard": "Which choice shows the comma splice in the {context}?",
        "Ultra": "Which sentence most clearly shows a comma splice in the {context}?",
    },
    "fused-sentence-diagnosis": {
        "Easy": "Which sentence is the fused sentence in the {context}?",
        "Medium": "In the {context}, which sentence joins two independent clauses with no punctuation?",
        "Hard": "Which choice shows the fused sentence in the {context}?",
        "Ultra": "Which sentence most clearly shows a fused sentence in the {context}?",
    },
    "period-split-revision": {
        "Easy": 'Which revision correctly splits the clauses in "{comma_splice}" into two sentences?',
        "Medium": 'Which sentence best separates the clauses in "{comma_splice}" with a period?',
        "Hard": 'Which choice correctly turns "{comma_splice}" into two separate sentences?',
        "Ultra": 'Which revision gives the correct period split for "{comma_splice}"?',
    },
    "punctuation-mark-selection": {
        "Easy": 'Which punctuation mark should appear before the coordinating conjunction in "{punctuation_blank}"?',
        "Medium": 'In "{punctuation_blank}", which punctuation mark belongs before the conjunction?',
        "Hard": 'Which punctuation mark correctly joins the clauses in "{punctuation_blank}"?',
        "Ultra": 'Which punctuation mark should replace the blank in "{punctuation_blank}"?',
    },
}


SCENES: tuple[Scene, ...] = (
    Scene(
        context="filing-desk set",
        compound="The clerk filed the memo, and the supervisor signed it.",
        simple="The clerk filed the memo before lunch.",
        complex="Because the memo was ready, the clerk filed it.",
        compound_complex="Because the memo was ready, the clerk filed it, and the supervisor signed it.",
        comma_splice="The clerk filed the memo, the supervisor signed it.",
        fused="The clerk filed the memo the supervisor signed it.",
        semicolon="The clerk filed the memo; the supervisor signed it.",
        period_split="The clerk filed the memo. The supervisor signed it.",
        conjunction="and",
        relation_prompt="added information",
    ),
    Scene(
        context="morning office set",
        compound="The office was busy, but the clerk stayed calm.",
        simple="The office was busy all morning.",
        complex="Although the office was busy, the clerk stayed calm.",
        compound_complex="Although the office was busy, the clerk stayed calm, and the manager reviewed the report.",
        comma_splice="The office was busy, the clerk stayed calm.",
        fused="The office was busy the clerk stayed calm.",
        semicolon="The office was busy; the clerk stayed calm.",
        period_split="The office was busy. The clerk stayed calm.",
        conjunction="but",
        relation_prompt="contrast",
    ),
    Scene(
        context="printer jam set",
        compound="The printer jammed, so the staff waited.",
        simple="The printer jammed during the meeting.",
        complex="Because the printer jammed, the staff waited.",
        compound_complex="Because the printer jammed, the staff waited, and the technician reset it.",
        comma_splice="The printer jammed, the staff waited.",
        fused="The printer jammed the staff waited.",
        semicolon="The printer jammed; the staff waited.",
        period_split="The printer jammed. The staff waited.",
        conjunction="so",
        relation_prompt="a result",
    ),
    Scene(
        context="choice set",
        compound="You may call now, or you may send an email later.",
        simple="You may call now.",
        complex="If you prefer, you may send an email later.",
        compound_complex="If you prefer, you may call now, or you may send an email later.",
        comma_splice="You may call now, you may send an email later.",
        fused="You may call now you may send an email later.",
        semicolon="You may call now; you may send an email later.",
        period_split="You may call now. You may send an email later.",
        conjunction="or",
        relation_prompt="a choice",
    ),
    Scene(
        context="night-watch set",
        compound="The team did not delay, nor did it complain.",
        simple="The team did not delay during the drill.",
        complex="Although the deadline was tight, the team did not delay.",
        compound_complex="Although the deadline was tight, the team did not delay, nor did it complain.",
        comma_splice="The team did not delay, it did not complain.",
        fused="The team did not delay it did not complain.",
        semicolon="The team did not delay; it did not complain.",
        period_split="The team did not delay. It did not complain.",
        conjunction="nor",
        relation_prompt="a negative idea",
    ),
    Scene(
        context="editor deadline set",
        compound="The editor left early, for the deadline was near.",
        simple="The editor left early that afternoon.",
        complex="Because the deadline was near, the editor left early.",
        compound_complex="Because the deadline was near, the editor left early, for the office was closing.",
        comma_splice="The editor left early, the deadline was near.",
        fused="The editor left early the deadline was near.",
        semicolon="The editor left early; the deadline was near.",
        period_split="The editor left early. The deadline was near.",
        conjunction="for",
        relation_prompt="a reason",
    ),
    Scene(
        context="schedule update set",
        compound="The schedule changed, yet everyone stayed calm.",
        simple="The schedule changed overnight.",
        complex="Although the schedule changed, everyone stayed calm.",
        compound_complex="Although the schedule changed, everyone stayed calm, and the supervisor explained the update.",
        comma_splice="The schedule changed, everyone stayed calm.",
        fused="The schedule changed everyone stayed calm.",
        semicolon="The schedule changed; everyone stayed calm.",
        period_split="The schedule changed. Everyone stayed calm.",
        conjunction="yet",
        relation_prompt="contrast",
    ),
    Scene(
        context="meeting note set",
        compound="The meeting ended at noon, and the assistant sent the notice.",
        simple="The meeting ended at noon.",
        complex="After the meeting ended, the assistant sent the notice.",
        compound_complex="After the meeting ended, the assistant sent the notice, and the manager reviewed the summary.",
        comma_splice="The meeting ended at noon, the assistant sent the notice.",
        fused="The meeting ended at noon the assistant sent the notice.",
        semicolon="The meeting ended at noon; the assistant sent the notice.",
        period_split="The meeting ended at noon. The assistant sent the notice.",
        conjunction="and",
        relation_prompt="added information",
    ),
    Scene(
        context="server failure set",
        compound="The server failed, so the staff restarted it.",
        simple="The server failed yesterday.",
        complex="Because the server failed, the staff restarted it.",
        compound_complex="Because the server failed, the staff restarted it, and the records were backed up.",
        comma_splice="The server failed, the staff restarted it.",
        fused="The server failed the staff restarted it.",
        semicolon="The server failed; the staff restarted it.",
        period_split="The server failed. The staff restarted it.",
        conjunction="so",
        relation_prompt="a result",
    ),
    Scene(
        context="planning note set",
        compound="The plan looked simple, yet the deadline remained tight.",
        simple="The plan looked simple at first.",
        complex="Although the plan looked simple, the deadline remained tight.",
        compound_complex="Although the plan looked simple, the deadline remained tight, and the team moved quickly.",
        comma_splice="The plan looked simple, the deadline remained tight.",
        fused="The plan looked simple the deadline remained tight.",
        semicolon="The plan looked simple; the deadline remained tight.",
        period_split="The plan looked simple. The deadline remained tight.",
        conjunction="yet",
        relation_prompt="contrast",
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
    question = QUESTION_STEMS[family.base_family][difficulty].format(**values)
    choices = family.choice_builder(scene)
    answer = family.answer_builder(scene)

    if answer not in choices:
        raise ValueError(
            f"answer {answer!r} missing from choices for {family.base_family} / {scene.context}"
        )

    rotation = (question_id + scene_index) % len(choices)
    rotated = choices[rotation:] + choices[:rotation]

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


FAMILY_SPECS: tuple[FamilySpec, ...] = (
    FamilySpec(
        base_family="compound-sentence-identification",
        choice_builder=_sentence_choices("compound", "simple", "complex", "compound_complex"),
        answer_builder=_attr_answer("compound"),
        explanation="A compound sentence has two or more independent clauses joined correctly.",
        tags=("classification", "compound"),
    ),
    FamilySpec(
        base_family="independent-clause-count",
        choice_builder=_fixed_choices("1", "2", "3", "4"),
        answer_builder=_fixed_answer("2"),
        explanation="A compound sentence contains two independent clauses.",
        tags=("count", "clauses"),
    ),
    FamilySpec(
        base_family="coordinating-conjunction-identification",
        choice_builder=_conjunction_choices,
        answer_builder=_attr_answer("conjunction"),
        explanation="The coordinating conjunction is the FANBOYS word that links the independent clauses.",
        tags=("conjunction", "fanboys"),
    ),
    FamilySpec(
        base_family="relation-based-conjunction-choice",
        choice_builder=_conjunction_choices,
        answer_builder=_attr_answer("conjunction"),
        explanation="The conjunction must match the relationship between the ideas.",
        tags=("conjunction", "relation"),
    ),
    FamilySpec(
        base_family="coordinating-conjunction-fill-in",
        choice_builder=_conjunction_choices,
        answer_builder=_attr_answer("conjunction"),
        explanation="A missing coordinating conjunction can complete the compound sentence cleanly.",
        tags=("completion", "conjunction"),
    ),
    FamilySpec(
        base_family="comma-conjunction-revision",
        choice_builder=_sentence_choices("compound", "comma_splice", "semicolon", "fused"),
        answer_builder=_attr_answer("compound"),
        explanation="A comma plus a coordinating conjunction correctly joins two independent clauses.",
        tags=("repair", "comma-conjunction"),
    ),
    FamilySpec(
        base_family="semicolon-revision",
        choice_builder=_sentence_choices("semicolon", "compound", "comma_splice", "fused"),
        answer_builder=_attr_answer("semicolon"),
        explanation="A semicolon can join two closely related independent clauses.",
        tags=("repair", "semicolon"),
    ),
    FamilySpec(
        base_family="simple-sentence-identification",
        choice_builder=_sentence_choices("simple", "compound", "complex", "compound_complex"),
        answer_builder=_attr_answer("simple"),
        explanation="A simple sentence has one independent clause only.",
        tags=("classification", "simple"),
    ),
    FamilySpec(
        base_family="complex-sentence-identification",
        choice_builder=_sentence_choices("complex", "simple", "compound", "compound_complex"),
        answer_builder=_attr_answer("complex"),
        explanation="A complex sentence has one independent clause and one dependent clause.",
        tags=("classification", "complex"),
    ),
    FamilySpec(
        base_family="compound-complex-identification",
        choice_builder=_sentence_choices("compound_complex", "compound", "complex", "simple"),
        answer_builder=_attr_answer("compound_complex"),
        explanation="A compound-complex sentence has two independent clauses and at least one dependent clause.",
        tags=("classification", "compound-complex"),
    ),
    FamilySpec(
        base_family="correct-compound-punctuation",
        choice_builder=_sentence_choices("compound", "comma_splice", "fused", "period_split"),
        answer_builder=_attr_answer("compound"),
        explanation="A correct compound sentence joins independent clauses with the right punctuation and conjunction.",
        tags=("punctuation", "compound"),
    ),
    FamilySpec(
        base_family="comma-splice-diagnosis",
        choice_builder=_sentence_choices("comma_splice", "compound", "fused", "period_split"),
        answer_builder=_attr_answer("comma_splice"),
        explanation="A comma splice joins independent clauses with only a comma.",
        tags=("diagnosis", "comma-splice"),
    ),
    FamilySpec(
        base_family="fused-sentence-diagnosis",
        choice_builder=_sentence_choices("fused", "compound", "comma_splice", "period_split"),
        answer_builder=_attr_answer("fused"),
        explanation="A fused sentence joins independent clauses with no punctuation.",
        tags=("diagnosis", "fused"),
    ),
    FamilySpec(
        base_family="period-split-revision",
        choice_builder=_sentence_choices("period_split", "compound", "semicolon", "comma_splice"),
        answer_builder=_attr_answer("period_split"),
        explanation="A period cleanly separates two independent clauses into two sentences.",
        tags=("repair", "period"),
    ),
    FamilySpec(
        base_family="punctuation-mark-selection",
        choice_builder=_fixed_choices("comma", "semicolon", "period", "apostrophe"),
        answer_builder=_fixed_answer("comma"),
        explanation="A comma belongs before a coordinating conjunction that joins two independent clauses.",
        tags=("punctuation", "comma"),
    ),
)


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
    expected_family_counts = {spec.base_family: 40 for spec in FAMILY_SPECS}
    if family_counts != expected_family_counts:
        raise ValueError(f"unexpected family distribution: {dict(family_counts)}")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise ValueError("question texts are not unique")

    banned_phrases = (
        "Which option best completes the sentence",
        "Which choice best completes the sentence",
        "best completes the sentence",
    )

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
        lowered = question_text.lower()
        if any(phrase.lower() in lowered for phrase in banned_phrases):
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
