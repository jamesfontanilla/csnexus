"""Generate the Verbal Ability / Sentence Structure / Complex Sentences question bank."""

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
    / "complex-sentences"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Complex Sentences"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "complex-sentences"
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
    complex: str
    simple: str
    compound: str
    compound_complex: str
    dependent_clause: str
    main_clause: str
    fragment: str
    repaired: str
    intro_missing_comma: str
    punctuation_blank: str
    fill_blank: str
    subordinator: str
    relation_prompt: str
    subordinator_choices: tuple[str, str, str, str]


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
        "complex": scene.complex,
        "simple": scene.simple,
        "compound": scene.compound,
        "compound_complex": scene.compound_complex,
        "dependent_clause": scene.dependent_clause,
        "main_clause": scene.main_clause,
        "fragment": scene.fragment,
        "repaired": scene.repaired,
        "intro_missing_comma": scene.intro_missing_comma,
        "punctuation_blank": scene.punctuation_blank,
        "fill_blank": scene.fill_blank,
        "subordinator": scene.subordinator,
        "relation_prompt": scene.relation_prompt,
    }


def _choices_from_attrs(*attrs: str) -> Callable[[Scene], list[str]]:
    def builder(scene: Scene) -> list[str]:
        return [getattr(scene, attr) for attr in attrs]

    return builder


def _fixed_choices(*choices: str) -> Callable[[Scene], list[str]]:
    def builder(_: Scene) -> list[str]:
        return list(choices)

    return builder


def _subordinator_choices(scene: Scene) -> list[str]:
    return list(scene.subordinator_choices)


def _answer_attr(attr: str) -> Callable[[Scene], str]:
    def builder(scene: Scene) -> str:
        return str(getattr(scene, attr))

    return builder


def _answer_value(value: str) -> Callable[[Scene], str]:
    def builder(_: Scene) -> str:
        return value

    return builder


QUESTION_STEMS: dict[str, dict[str, str]] = {
    "complex-sentence-identification": {
        "Easy": "Which sentence is the complex sentence in the {context}?",
        "Medium": "In the {context}, which sentence has one independent clause and one dependent clause?",
        "Hard": "Which choice is the complex sentence in the {context}?",
        "Ultra": "Which sentence shows a dependent clause attached to a main clause in the {context}?",
    },
    "sentence-type-classification": {
        "Easy": 'How should "{complex}" be classified?',
        "Medium": 'Which sentence type best describes "{complex}"?',
        "Hard": 'Which label fits "{complex}"?',
        "Ultra": 'What structural type is "{complex}"?',
    },
    "dependent-clause-identification": {
        "Easy": 'Which clause is the dependent clause in "{complex}"?',
        "Medium": 'In "{complex}", which clause cannot stand alone?',
        "Hard": 'Which phrase is the subordinate clause in "{complex}"?',
        "Ultra": 'Which part of "{complex}" is the dependent clause?',
    },
    "main-clause-identification": {
        "Easy": 'Which clause is the main clause in "{complex}"?',
        "Medium": 'In "{complex}", which clause carries the complete thought?',
        "Hard": 'Which phrase is the independent clause in "{complex}"?',
        "Ultra": 'Which part of "{complex}" can stand alone as the main idea?',
    },
    "subordinating-conjunction-identification": {
        "Easy": 'Which word is the subordinating conjunction in "{complex}"?',
        "Medium": 'In "{complex}", which word introduces the dependent clause?',
        "Hard": 'Which clause marker appears in "{complex}"?',
        "Ultra": 'Which subordinating conjunction links the dependent clause in "{complex}"?',
    },
    "relation-based-subordinator-choice": {
        "Easy": "Which subordinating conjunction best shows {relation_prompt} in the {context}?",
        "Medium": "Which conjunction best fits {relation_prompt} in the {context}?",
        "Hard": "Which subordinating conjunction most clearly shows {relation_prompt} in the {context}?",
        "Ultra": "Which clause marker best matches {relation_prompt} in the {context}?",
    },
    "subordinating-conjunction-fill-in": {
        "Easy": 'Which subordinating conjunction completes "{fill_blank}"?',
        "Medium": 'Which word correctly completes "{fill_blank}"?',
        "Hard": 'Which clause marker belongs in the blank in "{fill_blank}"?',
        "Ultra": 'Which subordinating conjunction should replace the blank in "{fill_blank}"?',
    },
    "introductory-dependent-clause-comma-revision": {
        "Easy": 'Which revision correctly punctuates "{intro_missing_comma}"?',
        "Medium": 'Which sentence correctly adds the comma after the opening dependent clause in "{intro_missing_comma}"?',
        "Hard": 'Which choice correctly separates the introductory clause in "{intro_missing_comma}"?',
        "Ultra": 'Which revision is correct for the introductory dependent clause in "{intro_missing_comma}"?',
    },
    "comma-placement-selection": {
        "Easy": 'Which punctuation mark should appear after the introductory clause in "{punctuation_blank}"?',
        "Medium": 'In "{punctuation_blank}", which punctuation mark belongs after the dependent clause?',
        "Hard": 'Which punctuation mark correctly separates the opening dependent clause from the main clause in "{punctuation_blank}"?',
        "Ultra": 'Which punctuation mark should replace the blank in "{punctuation_blank}"?',
    },
    "simple-sentence-identification": {
        "Easy": "Which sentence is simple, not complex, in the {context}?",
        "Medium": "In the {context}, which sentence has only one independent clause?",
        "Hard": "Which choice is the simple sentence in the {context}?",
        "Ultra": "Which sentence can stand alone without a dependent clause in the {context}?",
    },
    "compound-sentence-identification": {
        "Easy": "Which sentence is compound, not complex, in the {context}?",
        "Medium": "In the {context}, which sentence joins two independent clauses correctly?",
        "Hard": "Which choice is the compound sentence in the {context}?",
        "Ultra": "Which sentence shows two complete thoughts joined correctly in the {context}?",
    },
    "compound-complex-identification": {
        "Easy": "Which sentence is compound-complex in the {context}?",
        "Medium": "In the {context}, which sentence has two independent clauses and one dependent clause?",
        "Hard": "Which choice is the compound-complex sentence in the {context}?",
        "Ultra": "Which sentence combines a dependent clause with two independent clauses in the {context}?",
    },
    "fragment-diagnosis": {
        "Easy": 'Which option is only a dependent-clause fragment in "{fragment}"?',
        "Medium": 'In "{fragment}", which choice cannot stand alone as a complete sentence?',
        "Hard": 'Which option is the fragment in "{fragment}"?',
        "Ultra": 'Which choice is the dependent-clause fragment in "{fragment}"?',
    },
    "fragment-repair": {
        "Easy": 'Which revision turns "{fragment}" into a complete complex sentence?',
        "Medium": 'Which sentence best repairs "{fragment}"?',
        "Hard": 'Which choice best completes the dependent clause in "{fragment}"?',
        "Ultra": 'Which revision is the most accurate fix for "{fragment}"?',
    },
    "no-correction-needed": {
        "Easy": "Which sentence needs no correction in the {context}?",
        "Medium": "Which sentence is already correct in the {context}?",
        "Hard": "Which choice can stay exactly as written in the {context}?",
        "Ultra": "Which sentence is already punctuated and structured correctly in the {context}?",
    },
}


SCENES: tuple[Scene, ...] = (
    Scene(
        context="weather-delay set",
        complex="Because the roads were flooded, the bus arrived late.",
        simple="The bus arrived late.",
        compound="The roads were flooded, and the bus arrived late.",
        compound_complex="Because the roads were flooded, the bus arrived late, and the passengers waited quietly.",
        dependent_clause="Because the roads were flooded",
        main_clause="The bus arrived late",
        fragment="Because the roads were flooded.",
        repaired="Because the roads were flooded, the bus arrived late.",
        intro_missing_comma="Because the roads were flooded the bus arrived late.",
        punctuation_blank="Because the roads were flooded ____ the bus arrived late.",
        fill_blank="____ the roads were flooded, the bus arrived late.",
        subordinator="because",
        relation_prompt="a reason",
        subordinator_choices=("because", "although", "when", "if"),
    ),
    Scene(
        context="office contrast set",
        complex="Although the office was busy, the clerk stayed calm.",
        simple="The office was busy all morning.",
        compound="The office was busy, but the clerk stayed calm.",
        compound_complex="Although the office was busy, the clerk stayed calm, and the manager reviewed the report.",
        dependent_clause="Although the office was busy",
        main_clause="the clerk stayed calm",
        fragment="Although the office was busy.",
        repaired="Although the office was busy, the clerk stayed calm.",
        intro_missing_comma="Although the office was busy the clerk stayed calm.",
        punctuation_blank="Although the office was busy ____ the clerk stayed calm.",
        fill_blank="____ the office was busy, the clerk stayed calm.",
        subordinator="although",
        relation_prompt="contrast",
        subordinator_choices=("although", "because", "when", "if"),
    ),
    Scene(
        context="meeting time set",
        complex="When the meeting ended, the team filed out.",
        simple="The meeting ended at noon.",
        compound="The meeting ended, and the team filed out.",
        compound_complex="When the meeting ended, the team filed out, and the assistant sent the notice.",
        dependent_clause="When the meeting ended",
        main_clause="the team filed out",
        fragment="When the meeting ended.",
        repaired="When the meeting ended, the team filed out.",
        intro_missing_comma="When the meeting ended the team filed out.",
        punctuation_blank="When the meeting ended ____ the team filed out.",
        fill_blank="____ the meeting ended, the team filed out.",
        subordinator="when",
        relation_prompt="time",
        subordinator_choices=("when", "before", "after", "since"),
    ),
    Scene(
        context="condition memo set",
        complex="If the supervisor approves, the office will print the memo.",
        simple="The office will print the memo.",
        compound="The supervisor approves, and the office will print the memo.",
        compound_complex="If the supervisor approves, the office will print the memo, and the staff will send copies.",
        dependent_clause="If the supervisor approves",
        main_clause="the office will print the memo",
        fragment="If the supervisor approves.",
        repaired="If the supervisor approves, the office will print the memo.",
        intro_missing_comma="If the supervisor approves the office will print the memo.",
        punctuation_blank="If the supervisor approves ____ the office will print the memo.",
        fill_blank="____ the supervisor approves, the office will print the memo.",
        subordinator="if",
        relation_prompt="a condition",
        subordinator_choices=("if", "unless", "when", "because"),
    ),
    Scene(
        context="training set",
        complex="While the trainer explained the rule, the trainees took notes.",
        simple="The trainees took notes quietly.",
        compound="The trainer explained the rule, and the trainees took notes.",
        compound_complex="While the trainer explained the rule, the trainees took notes, and the assistant recorded the questions.",
        dependent_clause="While the trainer explained the rule",
        main_clause="the trainees took notes",
        fragment="While the trainer explained the rule.",
        repaired="While the trainer explained the rule, the trainees took notes.",
        intro_missing_comma="While the trainer explained the rule the trainees took notes.",
        punctuation_blank="While the trainer explained the rule ____ the trainees took notes.",
        fill_blank="____ the trainer explained the rule, the trainees took notes.",
        subordinator="while",
        relation_prompt="simultaneous action",
        subordinator_choices=("while", "when", "because", "although"),
    ),
    Scene(
        context="memo reply set",
        complex="Since the memo was short, the branch sent a reply.",
        simple="The branch sent a reply.",
        compound="The memo was short, so the branch sent a reply.",
        compound_complex="Since the memo was short, the branch sent a reply, and the manager filed it.",
        dependent_clause="Since the memo was short",
        main_clause="the branch sent a reply",
        fragment="Since the memo was short.",
        repaired="Since the memo was short, the branch sent a reply.",
        intro_missing_comma="Since the memo was short the branch sent a reply.",
        punctuation_blank="Since the memo was short ____ the branch sent a reply.",
        fill_blank="____ the memo was short, the branch sent a reply.",
        subordinator="since",
        relation_prompt="a reason",
        subordinator_choices=("since", "because", "after", "when"),
    ),
    Scene(
        context="audit set",
        complex="After the audit finished, the supervisor signed the report.",
        simple="The audit finished on time.",
        compound="The audit finished, and the supervisor signed the report.",
        compound_complex="After the audit finished, the supervisor signed the report, and the clerk filed the copy.",
        dependent_clause="After the audit finished",
        main_clause="the supervisor signed the report",
        fragment="After the audit finished.",
        repaired="After the audit finished, the supervisor signed the report.",
        intro_missing_comma="After the audit finished the supervisor signed the report.",
        punctuation_blank="After the audit finished ____ the supervisor signed the report.",
        fill_blank="____ the audit finished, the supervisor signed the report.",
        subordinator="after",
        relation_prompt="a later time",
        subordinator_choices=("after", "before", "when", "since"),
    ),
    Scene(
        context="opening set",
        complex="Before the office opened, the staff arranged the chairs.",
        simple="The staff arranged the chairs.",
        compound="The office opened, and the staff arranged the chairs.",
        compound_complex="Before the office opened, the staff arranged the chairs, and the clerk checked the register.",
        dependent_clause="Before the office opened",
        main_clause="the staff arranged the chairs",
        fragment="Before the office opened.",
        repaired="Before the office opened, the staff arranged the chairs.",
        intro_missing_comma="Before the office opened the staff arranged the chairs.",
        punctuation_blank="Before the office opened ____ the staff arranged the chairs.",
        fill_blank="____ the office opened, the staff arranged the chairs.",
        subordinator="before",
        relation_prompt="an earlier time",
        subordinator_choices=("before", "after", "when", "if"),
    ),
    Scene(
        context="printer wait set",
        complex="Until the printer is repaired, the copies will wait.",
        simple="The copies will wait.",
        compound="The printer is repaired, and the copies will wait.",
        compound_complex="Until the printer is repaired, the copies will wait, and the staff will use the backup.",
        dependent_clause="Until the printer is repaired",
        main_clause="the copies will wait",
        fragment="Until the printer is repaired.",
        repaired="Until the printer is repaired, the copies will wait.",
        intro_missing_comma="Until the printer is repaired the copies will wait.",
        punctuation_blank="Until the printer is repaired ____ the copies will wait.",
        fill_blank="____ the printer is repaired, the copies will wait.",
        subordinator="until",
        relation_prompt="a time limit",
        subordinator_choices=("until", "when", "before", "if"),
    ),
    Scene(
        context="deadline condition set",
        complex="Unless the manager calls, the team will leave.",
        simple="The team will leave soon.",
        compound="The manager calls, and the team will leave.",
        compound_complex="Unless the manager calls, the team will leave, and the office will close.",
        dependent_clause="Unless the manager calls",
        main_clause="the team will leave",
        fragment="Unless the manager calls.",
        repaired="Unless the manager calls, the team will leave.",
        intro_missing_comma="Unless the manager calls the team will leave.",
        punctuation_blank="Unless the manager calls ____ the team will leave.",
        fill_blank="____ the manager calls, the team will leave.",
        subordinator="unless",
        relation_prompt="a negative condition",
        subordinator_choices=("unless", "if", "when", "because"),
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
        base_family="complex-sentence-identification",
        choice_builder=_choices_from_attrs("complex", "simple", "compound", "compound_complex"),
        answer_builder=_answer_attr("complex"),
        explanation="A complex sentence has one independent clause and at least one dependent clause.",
        tags=("classification", "complex"),
    ),
    FamilySpec(
        base_family="sentence-type-classification",
        choice_builder=_choices_from_attrs("complex", "simple", "compound", "compound_complex"),
        answer_builder=_answer_attr("complex"),
        explanation="The sentence has one independent clause and one dependent clause, so it is complex.",
        tags=("classification", "sentence-type"),
    ),
    FamilySpec(
        base_family="dependent-clause-identification",
        choice_builder=_choices_from_attrs("dependent_clause", "main_clause", "simple", "compound"),
        answer_builder=_answer_attr("dependent_clause"),
        explanation="The dependent clause cannot stand alone as a complete sentence.",
        tags=("clause", "dependent"),
    ),
    FamilySpec(
        base_family="main-clause-identification",
        choice_builder=_choices_from_attrs("main_clause", "dependent_clause", "simple", "compound"),
        answer_builder=_answer_attr("main_clause"),
        explanation="The main clause carries the complete thought and can stand alone.",
        tags=("clause", "main"),
    ),
    FamilySpec(
        base_family="subordinating-conjunction-identification",
        choice_builder=_subordinator_choices,
        answer_builder=_answer_attr("subordinator"),
        explanation="The subordinating conjunction is the marker that makes the clause dependent.",
        tags=("conjunction", "subordinator"),
    ),
    FamilySpec(
        base_family="relation-based-subordinator-choice",
        choice_builder=_subordinator_choices,
        answer_builder=_answer_attr("subordinator"),
        explanation="The conjunction must match the relation shown by the dependent clause.",
        tags=("conjunction", "relation"),
    ),
    FamilySpec(
        base_family="subordinating-conjunction-fill-in",
        choice_builder=_subordinator_choices,
        answer_builder=_answer_attr("subordinator"),
        explanation="A subordinating conjunction can complete the dependent clause and make the relationship clear.",
        tags=("completion", "subordinator"),
    ),
    FamilySpec(
        base_family="introductory-dependent-clause-comma-revision",
        choice_builder=_choices_from_attrs("complex", "intro_missing_comma", "compound", "fragment"),
        answer_builder=_answer_attr("complex"),
        explanation="An introductory dependent clause should be followed by a comma before the main clause.",
        tags=("punctuation", "introductory-clause"),
    ),
    FamilySpec(
        base_family="comma-placement-selection",
        choice_builder=_fixed_choices("comma", "semicolon", "period", "apostrophe"),
        answer_builder=_answer_value("comma"),
        explanation="A comma should follow the introductory dependent clause.",
        tags=("punctuation", "comma"),
    ),
    FamilySpec(
        base_family="simple-sentence-identification",
        choice_builder=_choices_from_attrs("simple", "complex", "compound", "compound_complex"),
        answer_builder=_answer_attr("simple"),
        explanation="A simple sentence has one independent clause and no dependent clause.",
        tags=("classification", "simple"),
    ),
    FamilySpec(
        base_family="compound-sentence-identification",
        choice_builder=_choices_from_attrs("compound", "complex", "simple", "compound_complex"),
        answer_builder=_answer_attr("compound"),
        explanation="A compound sentence joins two independent clauses correctly.",
        tags=("classification", "compound"),
    ),
    FamilySpec(
        base_family="compound-complex-identification",
        choice_builder=_choices_from_attrs("compound_complex", "complex", "compound", "simple"),
        answer_builder=_answer_attr("compound_complex"),
        explanation="A compound-complex sentence has one dependent clause and two independent clauses.",
        tags=("classification", "compound-complex"),
    ),
    FamilySpec(
        base_family="fragment-diagnosis",
        choice_builder=_choices_from_attrs("fragment", "complex", "compound", "simple"),
        answer_builder=_answer_attr("fragment"),
        explanation="A dependent clause by itself is a fragment because it cannot stand alone.",
        tags=("diagnosis", "fragment"),
    ),
    FamilySpec(
        base_family="fragment-repair",
        choice_builder=_choices_from_attrs("repaired", "compound", "simple", "fragment"),
        answer_builder=_answer_attr("repaired"),
        explanation="A fragment becomes complete when the dependent clause is attached to a main clause.",
        tags=("repair", "fragment"),
    ),
    FamilySpec(
        base_family="no-correction-needed",
        choice_builder=_choices_from_attrs("complex", "intro_missing_comma", "compound", "fragment"),
        answer_builder=_answer_attr("complex"),
        explanation="The sentence is already a correctly punctuated complex sentence.",
        tags=("diagnosis", "correct"),
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
    expected_family_counts = {family.base_family: 40 for family in FAMILY_SPECS}
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
