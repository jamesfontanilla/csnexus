"""Generate the Verbal Ability / Sentence Structure / Simple Sentences bank."""

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
    / "simple-sentences"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Simple Sentences"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "simple-sentences"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

FAMILY_ORDER = (
    "simple-sentence-identification",
    "one-independent-clause-count",
    "sentence-type-classification",
    "simple-sentence-with-modifiers",
    "fragment-diagnosis",
    "run-on-diagnosis",
    "subject-identification",
    "predicate-identification",
    "main-verb-identification",
    "introductory-phrase-comma",
    "appositive-comma",
    "fragment-repair-simple-sentence",
    "simple-vs-compound-classification",
    "simple-vs-complex-classification",
    "clause-vs-phrase-classification",
)

QUESTION_STEMS: dict[str, dict[str, str]] = {
    "simple-sentence-identification": {
        "Easy": 'Which option is the simple sentence in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice can stand alone as a complete thought?',
        "Hard": 'Which choice is the simple sentence rather than the other options in the set for "{sentence}"?',
        "Ultra": 'Which sentence in the set is structurally simple in "{sentence}"?',
    },
    "one-independent-clause-count": {
        "Easy": 'Which option has one independent clause and no dependent clauses in "{sentence}"?',
        "Medium": 'Which sentence contains exactly one independent clause in "{sentence}"?',
        "Hard": 'Which choice is the sentence with a single independent clause in "{sentence}"?',
        "Ultra": 'Which option is the one-independent-clause sentence in "{sentence}"?',
    },
    "sentence-type-classification": {
        "Easy": 'What sentence type is "{sentence}"?',
        "Medium": 'How should "{sentence}" be classified structurally?',
        "Hard": 'Which sentence type best fits "{sentence}"?',
        "Ultra": 'What structural label matches "{sentence}"?',
    },
    "simple-sentence-with-modifiers": {
        "Easy": 'Which sentence is still simple even though it has {modifier_label}: "{sentence}"?',
        "Medium": 'Which sentence remains simple even with {modifier_label}: "{sentence}"?',
        "Hard": 'Which choice is the simple sentence with {modifier_label} in "{sentence}"?',
        "Ultra": 'Which option stays simple despite {modifier_label} in "{sentence}"?',
    },
    "fragment-diagnosis": {
        "Easy": 'Which option is a fragment in the set for "{fragment}"?',
        "Medium": 'Which choice is incomplete in the set for "{fragment}"?',
        "Hard": 'Which option cannot stand alone as a sentence in the set for "{fragment}"?',
        "Ultra": 'Which choice is the fragment in the set for "{fragment}"?',
    },
    "run-on-diagnosis": {
        "Easy": 'What error best describes "{sentence}"?',
        "Medium": 'Which label fits "{sentence}" best?',
        "Hard": 'Which sentence-level error appears in "{sentence}"?',
        "Ultra": 'What structural error does "{sentence}" contain?',
    },
    "subject-identification": {
        "Easy": 'What is the subject in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice is the subject?',
        "Hard": 'Which word or phrase controls the verb in "{sentence}"?',
        "Ultra": 'Which choice names the true subject in "{sentence}"?',
    },
    "predicate-identification": {
        "Easy": 'What is the complete predicate in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice is the complete predicate?',
        "Hard": 'Which part of "{sentence}" tells what the subject does?',
        "Ultra": 'Which choice names the complete predicate in "{sentence}"?',
    },
    "main-verb-identification": {
        "Easy": 'What is the main verb in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice is the main verb?',
        "Hard": 'Which word carries the action in "{sentence}"?',
        "Ultra": 'Which choice names the main verb in "{sentence}"?',
    },
    "introductory-phrase-comma": {
        "Easy": 'Which revision correctly adds the comma after the introductory phrase in "{original}"?',
        "Medium": 'Which sentence is punctuated correctly after the introductory phrase in "{original}"?',
        "Hard": 'Which choice correctly separates the introductory phrase in "{original}"?',
        "Ultra": 'Which revision best punctuates the opening phrase in "{original}"?',
    },
    "appositive-comma": {
        "Easy": 'Which revision correctly punctuates the appositive in "{original}"?',
        "Medium": 'Which sentence correctly sets off the nonessential appositive in "{original}"?',
        "Hard": 'Which choice correctly brackets the added appositive information in "{original}"?',
        "Ultra": 'Which revision is punctuated correctly for the appositive in "{original}"?',
    },
    "fragment-repair-simple-sentence": {
        "Easy": 'Which revision turns "{fragment}" into a complete simple sentence?',
        "Medium": 'Which sentence repairs the fragment "{fragment}"?',
        "Hard": 'Which choice most accurately fixes "{fragment}" into a simple sentence?',
        "Ultra": 'Which revision correctly turns "{fragment}" into a complete thought?',
    },
    "simple-vs-compound-classification": {
        "Easy": 'Which option is simple, not compound, in the compound-sentence pair for "{sentence}"?',
        "Medium": 'In the compound-sentence pair for "{sentence}", which choice is the simple sentence rather than the compound one?',
        "Hard": 'Which choice is the simple sentence instead of the compound sentence in the compound pair for "{sentence}"?',
        "Ultra": 'Which option belongs on the simple-sentence side of the compound comparison for "{sentence}"?',
    },
    "simple-vs-complex-classification": {
        "Easy": 'Which option is simple, not complex, in the complex-sentence pair for "{sentence}"?',
        "Medium": 'In the complex-sentence pair for "{sentence}", which choice is the simple sentence rather than the complex one?',
        "Hard": 'Which choice is the simple sentence instead of the complex sentence in the complex pair for "{sentence}"?',
        "Ultra": 'Which option belongs on the simple-sentence side of the complex comparison for "{sentence}"?',
    },
    "clause-vs-phrase-classification": {
        "Easy": 'Which option is the complete sentence, not the phrase, in the sentence-or-phrase set for "{sentence}"?',
        "Medium": 'In the sentence-or-phrase set for "{sentence}", which choice is a sentence and not a phrase?',
        "Hard": 'Which choice is the sentence rather than the phrase in "{sentence}"?',
        "Ultra": 'Which option belongs to the sentence side rather than the phrase side of the sentence-or-phrase comparison for "{sentence}"?',
    },
}


@dataclass(frozen=True)
class Scene:
    values: dict[str, str]
    choices: tuple[str, str, str, str]
    answer: str
    explanation: str
    tags: tuple[str, ...]


def _scene(
    *,
    values: dict[str, str],
    choices: tuple[str, str, str, str],
    answer: str,
    explanation: str,
    tags: tuple[str, ...],
) -> Scene:
    return Scene(values=values, choices=choices, answer=answer, explanation=explanation, tags=tags)


def _rotate_choices(choices: tuple[str, str, str, str], offset: int) -> list[str]:
    items = list(choices)
    rotation = offset % len(items)
    return items[rotation:] + items[:rotation]


def _expand_family(family: str, scenes: list[Scene]) -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    for scene_index, scene in enumerate(scenes):
        for difficulty_index, difficulty in enumerate(DIFFICULTIES):
            question_id = len(questions) + 1
            rotated = _rotate_choices(scene.choices, question_id + scene_index + difficulty_index)
            questions.append(
                {
                    "id": question_id,
                    "subtest": SUBTEST,
                    "module": MODULE,
                    "subtopic": SUBTOPIC,
                    "difficulty": difficulty,
                    "question": QUESTION_STEMS[family][difficulty].format(**scene.values),
                    "choices": rotated,
                    "answer": scene.answer,
                    "explanation": scene.explanation,
                    "tags": [ROOT_TAG, family, DIFFICULTY_TAGS[difficulty], *scene.tags],
                    "category": CATEGORY,
                    "language": LANGUAGE,
                }
            )
    return questions


SIMPLE_BASE = (
    {
        "sentence": "The clerk filed the memo in the cabinet.",
        "subject": "The clerk",
        "predicate": "filed the memo in the cabinet",
        "verb": "filed",
        "phrase": "in the cabinet",
        "compound": "The clerk filed the memo in the cabinet, and the manager approved it.",
        "complex": "Because the memo was late, the clerk filed it in the cabinet.",
        "fragment": "in the cabinet before noon",
    },
    {
        "sentence": "The manager approved the report before noon.",
        "subject": "The manager",
        "predicate": "approved the report before noon",
        "verb": "approved",
        "phrase": "before noon",
        "compound": "The manager approved the report before noon, and the assistant filed it.",
        "complex": "Because the report was ready, the manager approved it before noon.",
        "fragment": "before noon on Monday",
    },
    {
        "sentence": "The supervisor called the applicant on Monday.",
        "subject": "The supervisor",
        "predicate": "called the applicant on Monday",
        "verb": "called",
        "phrase": "on Monday",
        "compound": "The supervisor called the applicant on Monday, and the clerk took notes.",
        "complex": "After the interview ended, the supervisor called the applicant on Monday.",
        "fragment": "on Monday in the office",
    },
    {
        "sentence": "The team waited quietly in the lobby.",
        "subject": "The team",
        "predicate": "waited quietly in the lobby",
        "verb": "waited",
        "phrase": "in the lobby",
        "compound": "The team waited quietly in the lobby, and the trainer arrived later.",
        "complex": "When the doors opened, the team waited quietly in the lobby.",
        "fragment": "in the lobby after lunch",
    },
    {
        "sentence": "The auditor checked the files on the table.",
        "subject": "The auditor",
        "predicate": "checked the files on the table",
        "verb": "checked",
        "phrase": "on the table",
        "compound": "The auditor checked the files on the table, and the assistant copied the notes.",
        "complex": "Because the files were missing, the auditor checked the files on the table.",
        "fragment": "on the table near the window",
    },
    {
        "sentence": "The office reopened after lunch.",
        "subject": "The office",
        "predicate": "reopened after lunch",
        "verb": "reopened",
        "phrase": "after lunch",
        "compound": "The office reopened after lunch, and the staff returned.",
        "complex": "Because the repairs were finished, the office reopened after lunch.",
        "fragment": "after lunch at the branch",
    },
    {
        "sentence": "The courier delivered the package by noon.",
        "subject": "The courier",
        "predicate": "delivered the package by noon",
        "verb": "delivered",
        "phrase": "by noon",
        "compound": "The courier delivered the package by noon, and the clerk signed the receipt.",
        "complex": "Since the van was ready, the courier delivered the package by noon.",
        "fragment": "by noon for the office",
    },
    {
        "sentence": "The branch closed early on Friday.",
        "subject": "The branch",
        "predicate": "closed early on Friday",
        "verb": "closed",
        "phrase": "on Friday",
        "compound": "The branch closed early on Friday, but the staff stayed late.",
        "complex": "When the storm worsened, the branch closed early on Friday.",
        "fragment": "on Friday after lunch",
    },
    {
        "sentence": "The trainer explained the rules to the class.",
        "subject": "The trainer",
        "predicate": "explained the rules to the class",
        "verb": "explained",
        "phrase": "to the class",
        "compound": "The trainer explained the rules to the class, and the students took notes.",
        "complex": "Because the class was new, the trainer explained the rules to the class.",
        "fragment": "to the class during recess",
    },
    {
        "sentence": "The children played outside during recess.",
        "subject": "The children",
        "predicate": "played outside during recess",
        "verb": "played",
        "phrase": "during recess",
        "compound": "The children played outside during recess, and the bell rang later.",
        "complex": "When the bell rang, the children played outside during recess.",
        "fragment": "during recess after lunch",
    },
)


MODIFIER_BASE = (
    {
        "sentence": "Before the meeting, the clerk filed the memo.",
        "modifier_label": "a fronted time phrase",
        "subject": "The clerk",
        "predicate": "filed the memo",
        "verb": "filed",
        "compound": "Before the meeting, the clerk filed the memo, and the manager approved it.",
        "complex": "Because the meeting was near, the clerk filed the memo.",
        "fragment": "Before the meeting.",
    },
    {
        "sentence": "In the cabinet, the clerk found the memo.",
        "modifier_label": "a fronted prepositional phrase",
        "subject": "The clerk",
        "predicate": "found the memo",
        "verb": "found",
        "compound": "In the cabinet, the clerk found the memo, and the manager kept searching.",
        "complex": "Because the memo was missing, the clerk found it in the cabinet.",
        "fragment": "In the cabinet.",
    },
    {
        "sentence": "Maya, the branch coordinator, filed the memo.",
        "modifier_label": "an appositive",
        "subject": "Maya",
        "predicate": "filed the memo",
        "verb": "filed",
        "compound": "Maya, the branch coordinator, filed the memo, and the manager signed it.",
        "complex": "Because Maya was the branch coordinator, she filed the memo.",
        "fragment": "Maya, the branch coordinator.",
    },
    {
        "sentence": "With her hands full, the clerk answered the phone.",
        "modifier_label": "a fronted participial phrase",
        "subject": "The clerk",
        "predicate": "answered the phone",
        "verb": "answered",
        "compound": "With her hands full, the clerk answered the phone, and the supervisor waited.",
        "complex": "Because her hands were full, the clerk answered the phone.",
        "fragment": "With her hands full.",
    },
    {
        "sentence": "After lunch, the manager approved the report.",
        "modifier_label": "a fronted time phrase",
        "subject": "The manager",
        "predicate": "approved the report",
        "verb": "approved",
        "compound": "After lunch, the manager approved the report, and the assistant filed it.",
        "complex": "Because the report was ready, the manager approved it after lunch.",
        "fragment": "After lunch.",
    },
    {
        "sentence": "Under the desk, the office assistant found the stamp.",
        "modifier_label": "a fronted prepositional phrase",
        "subject": "The office assistant",
        "predicate": "found the stamp",
        "verb": "found",
        "compound": "Under the desk, the office assistant found the stamp, and the clerk wrote it down.",
        "complex": "Because the stamp was missing, the office assistant found it under the desk.",
        "fragment": "Under the desk.",
    },
    {
        "sentence": "During the briefing, the supervisor took notes.",
        "modifier_label": "a fronted prepositional phrase",
        "subject": "The supervisor",
        "predicate": "took notes",
        "verb": "took",
        "compound": "During the briefing, the supervisor took notes, and the trainees listened.",
        "complex": "While the briefing was ongoing, the supervisor took notes.",
        "fragment": "During the briefing.",
    },
    {
        "sentence": "By the window, the courier waited quietly.",
        "modifier_label": "a fronted prepositional phrase",
        "subject": "The courier",
        "predicate": "waited quietly",
        "verb": "waited",
        "compound": "By the window, the courier waited quietly, and the clerk called inside.",
        "complex": "Because the rain started, the courier waited quietly by the window.",
        "fragment": "By the window.",
    },
    {
        "sentence": "On Friday, the branch reopened.",
        "modifier_label": "a fronted time phrase",
        "subject": "The branch",
        "predicate": "reopened",
        "verb": "reopened",
        "compound": "On Friday, the branch reopened, and the staff returned.",
        "complex": "When the repairs ended, the branch reopened on Friday.",
        "fragment": "On Friday.",
    },
    {
        "sentence": "His notes carefully arranged, the trainer left the room.",
        "modifier_label": "an absolute phrase",
        "subject": "The trainer",
        "predicate": "left the room",
        "verb": "left",
        "compound": "His notes carefully arranged, the trainer left the room, and the students followed.",
        "complex": "After his notes were carefully arranged, the trainer left the room.",
        "fragment": "His notes carefully arranged.",
    },
)


TYPE_BASE = (
    {"sentence": "The clerk filed the memo.", "type": "Simple sentence"},
    {"sentence": "The clerk filed the memo, and the manager approved it.", "type": "Compound sentence"},
    {"sentence": "Because the memo was late, the clerk apologized.", "type": "Complex sentence"},
    {
        "sentence": "Because the memo was late, the clerk apologized, and the manager helped.",
        "type": "Compound-complex sentence",
    },
    {"sentence": "The office reopened.", "type": "Simple sentence"},
    {"sentence": "The office reopened, but the staff stayed late.", "type": "Compound sentence"},
    {"sentence": "After the meeting ended, the team filed out.", "type": "Complex sentence"},
    {
        "sentence": "After the meeting ended, the team filed out, and the supervisor locked the door.",
        "type": "Compound-complex sentence",
    },
    {"sentence": "The courier delivered the package.", "type": "Simple sentence"},
    {"sentence": "If the printer jams, the assistant will call IT.", "type": "Complex sentence"},
)


FRAGMENT_BASE = (
    {
        "fragment": "In the cabinet.",
        "repair": "The memo was in the cabinet.",
        "compound": "The memo was in the cabinet, and the manager approved it.",
        "complex": "Because the memo was in the cabinet, the clerk found it.",
    },
    {
        "fragment": "Before the meeting.",
        "repair": "The clerk filed the memo before the meeting.",
        "compound": "The clerk filed the memo before the meeting, and the manager signed it.",
        "complex": "When the meeting started, the clerk filed the memo.",
    },
    {
        "fragment": "After lunch.",
        "repair": "The office reopened after lunch.",
        "compound": "The office reopened after lunch, and the staff returned.",
        "complex": "After lunch, the office reopened.",
    },
    {
        "fragment": "With the forms.",
        "repair": "The clerk worked with the forms.",
        "compound": "The clerk worked with the forms, and the auditor checked them.",
        "complex": "Because the forms were ready, the clerk worked with them.",
    },
    {
        "fragment": "On Friday.",
        "repair": "The branch closed early on Friday.",
        "compound": "The branch closed early on Friday, and the staff left.",
        "complex": "When Friday arrived, the branch closed early.",
    },
    {
        "fragment": "The memo in the cabinet.",
        "repair": "The memo in the cabinet was missing.",
        "compound": "The memo in the cabinet was missing, and the clerk searched again.",
        "complex": "Because the memo in the cabinet was missing, the clerk searched again.",
    },
    {
        "fragment": "Because the report was late.",
        "repair": "The manager apologized because the report was late.",
        "compound": "The report was late, and the manager apologized.",
        "complex": "Because the report was late, the manager apologized.",
    },
    {
        "fragment": "The branch near the terminal.",
        "repair": "The branch near the terminal was busy.",
        "compound": "The branch near the terminal was busy, and the staff kept working.",
        "complex": "Because the branch near the terminal was busy, the staff kept working.",
    },
    {
        "fragment": "For the signature.",
        "repair": "The manager asked for the signature.",
        "compound": "The manager asked for the signature, and the clerk signed the form.",
        "complex": "Because the manager needed the signature, the clerk signed the form.",
    },
    {
        "fragment": "At the desk.",
        "repair": "The auditor checked the files at the desk.",
        "compound": "The auditor checked the files at the desk, and the clerk took notes.",
        "complex": "Because the audit was underway, the auditor checked the files at the desk.",
    },
)


RUNON_BASE = (
    {"sentence": "The clerk filed the memo, the manager approved it.", "diagnosis": "comma splice"},
    {"sentence": "The office reopened the staff returned.", "diagnosis": "fused sentence"},
    {"sentence": "The supervisor called the applicant, the line was busy.", "diagnosis": "comma splice"},
    {"sentence": "The team waited quietly the trainer arrived.", "diagnosis": "fused sentence"},
    {"sentence": "The auditor checked the files, the assistant copied the notes.", "diagnosis": "comma splice"},
    {"sentence": "The branch closed early the lights stayed on.", "diagnosis": "fused sentence"},
    {"sentence": "The courier delivered the package, the clerk signed the receipt.", "diagnosis": "comma splice"},
    {"sentence": "The children played outside the bell rang.", "diagnosis": "fused sentence"},
    {"sentence": "The manager approved the report, the clerk filed it.", "diagnosis": "comma splice"},
    {"sentence": "The trainer explained the rules the class listened.", "diagnosis": "fused sentence"},
)


SENTENCE_TYPE_CHOICES = (
    "Simple sentence",
    "Compound sentence",
    "Complex sentence",
    "Compound-complex sentence",
)

RUNON_CHOICES = ("comma splice", "fused sentence", "fragment", "correct sentence")

STRUCTURE_CHOICES = ("sentence", "phrase", "fragment", "compound sentence")


def _build_simple_sentence_identification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["sentence"], entry["compound"], entry["complex"], entry["fragment"]),
                answer=entry["sentence"],
                explanation="It has one independent clause and no dependent clauses.",
                tags=("identification", "simple-sentence"),
            )
        )
    return _expand_family("simple-sentence-identification", scenes)


def _build_one_independent_clause_count() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["sentence"], entry["compound"], entry["complex"], entry["fragment"]),
                answer=entry["sentence"],
                explanation="It contains one independent clause and no dependent clause.",
                tags=("clause-count", "independent-clause"),
            )
        )
    return _expand_family("one-independent-clause-count", scenes)


def _build_sentence_type_classification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in TYPE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=SENTENCE_TYPE_CHOICES,
                answer=entry["type"],
                explanation=f'The sentence is a {entry["type"].lower()} because of its clause pattern.',
                tags=("sentence-type", "classification"),
            )
        )
    return _expand_family("sentence-type-classification", scenes)


def _build_simple_sentence_with_modifiers() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in MODIFIER_BASE:
        scenes.append(
            _scene(
                values={"modifier_label": entry["modifier_label"], "sentence": entry["sentence"]},
                choices=(entry["sentence"], entry["compound"], entry["complex"], entry["fragment"]),
                answer=entry["sentence"],
                explanation="The modifier adds detail, but the sentence still has only one independent clause.",
                tags=("modifiers", "simple-sentence"),
            )
        )
    return _expand_family("simple-sentence-with-modifiers", scenes)


def _build_fragment_diagnosis() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in FRAGMENT_BASE:
        scenes.append(
            _scene(
                values={"fragment": entry["fragment"]},
                choices=(entry["fragment"], entry["repair"], entry["compound"], entry["complex"]),
                answer=entry["fragment"],
                explanation="It is incomplete, so it cannot stand alone as a sentence.",
                tags=("fragment", "diagnosis"),
            )
        )
    return _expand_family("fragment-diagnosis", scenes)


def _build_run_on_diagnosis() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in RUNON_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=RUNON_CHOICES,
                answer=entry["diagnosis"],
                explanation="Two independent clauses are joined incorrectly.",
                tags=("run-on", entry["diagnosis"].replace(" ", "-")),
            )
        )
    return _expand_family("run-on-diagnosis", scenes)


def _build_subject_identification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["subject"], entry["predicate"], entry["verb"], entry["phrase"]),
                answer=entry["subject"],
                explanation="It is the noun phrase that controls the verb.",
                tags=("subject", "identification"),
            )
        )
    return _expand_family("subject-identification", scenes)


def _build_predicate_identification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["predicate"], entry["subject"], entry["verb"], entry["phrase"]),
                answer=entry["predicate"],
                explanation="It includes the verb and everything that completes the subject's idea.",
                tags=("predicate", "identification"),
            )
        )
    return _expand_family("predicate-identification", scenes)


def _build_main_verb_identification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["verb"], entry["subject"], entry["phrase"], entry["predicate"]),
                answer=entry["verb"],
                explanation="It is the action word that carries the sentence.",
                tags=("verb", "main-verb"),
            )
        )
    return _expand_family("main-verb-identification", scenes)


def _build_introductory_phrase_comma() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in INTRO_BASE:
        scenes.append(
            _scene(
                values={"original": entry["original"]},
                choices=(entry["correct"], entry["wrong_1"], entry["wrong_2"], entry["wrong_3"]),
                answer=entry["correct"],
                explanation="The opening phrase should be followed by a comma.",
                tags=("introductory-phrase", "comma"),
            )
        )
    return _expand_family("introductory-phrase-comma", scenes)


def _build_appositive_comma() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in APPOSITIVE_BASE:
        scenes.append(
            _scene(
                values={"original": entry["original"]},
                choices=(entry["correct"], entry["wrong_1"], entry["wrong_2"], entry["wrong_3"]),
                answer=entry["correct"],
                explanation="The nonessential appositive should be set off by commas.",
                tags=("appositive", "comma"),
            )
        )
    return _expand_family("appositive-comma", scenes)


def _build_fragment_repair_simple_sentence() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in FRAGMENT_BASE:
        scenes.append(
            _scene(
                values={"fragment": entry["fragment"]},
                choices=(entry["repair"], entry["fragment"], entry["compound"], entry["complex"]),
                answer=entry["repair"],
                explanation="It adds the missing subject or predicate and becomes a complete simple sentence.",
                tags=("fragment", "repair"),
            )
        )
    return _expand_family("fragment-repair-simple-sentence", scenes)


def _build_simple_vs_compound_classification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["sentence"], entry["compound"], entry["complex"], entry["fragment"]),
                answer=entry["sentence"],
                explanation="It has one independent clause, while the compound option has two.",
                tags=("simple", "compound-contrast"),
            )
        )
    return _expand_family("simple-vs-compound-classification", scenes)


def _build_simple_vs_complex_classification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["sentence"], entry["complex"], entry["compound"], entry["fragment"]),
                answer=entry["sentence"],
                explanation="It has one independent clause and no dependent clause.",
                tags=("simple", "complex-contrast"),
            )
        )
    return _expand_family("simple-vs-complex-classification", scenes)


def _build_clause_vs_phrase_classification() -> list[dict[str, object]]:
    scenes: list[Scene] = []
    for entry in SIMPLE_BASE:
        scenes.append(
            _scene(
                values={"sentence": entry["sentence"]},
                choices=(entry["sentence"], entry["phrase"], entry["fragment"], entry["compound"]),
                answer=entry["sentence"],
                explanation="It is a complete sentence; the phrase option does not have both a subject and a verb.",
                tags=("sentence", "phrase-contrast"),
            )
        )
    return _expand_family("clause-vs-phrase-classification", scenes)


def _build_questions() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    builders = [
        _build_simple_sentence_identification,
        _build_one_independent_clause_count,
        _build_sentence_type_classification,
        _build_simple_sentence_with_modifiers,
        _build_fragment_diagnosis,
        _build_run_on_diagnosis,
        _build_subject_identification,
        _build_predicate_identification,
        _build_main_verb_identification,
        _build_introductory_phrase_comma,
        _build_appositive_comma,
        _build_fragment_repair_simple_sentence,
        _build_simple_vs_compound_classification,
        _build_simple_vs_complex_classification,
        _build_clause_vs_phrase_classification,
    ]
    for builder in builders:
        questions.extend(builder())
    for question_id, question in enumerate(questions, start=1):
        question["id"] = question_id
    return questions


def _validate_questions(questions: list[dict[str, object]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, found {len(questions)}")

    expected_ids = list(range(1, 601))
    actual_ids = [int(question["id"]) for question in questions]
    if actual_ids != expected_ids:
        raise ValueError("question ids must run sequentially from 1 to 600")

    difficulty_counts = Counter(str(question["difficulty"]) for question in questions)
    expected_difficulty_counts = {difficulty: 150 for difficulty in DIFFICULTIES}
    if difficulty_counts != expected_difficulty_counts:
        raise ValueError(f"unexpected difficulty counts: {difficulty_counts}")

    family_counts = Counter(str(question["tags"][1]) for question in questions)  # type: ignore[index]
    expected_family_counts = {family: 40 for family in FAMILY_ORDER}
    if family_counts != expected_family_counts:
        raise ValueError(f"unexpected family counts: {family_counts}")

    question_texts = [str(question["question"]) for question in questions]
    if len(set(question_texts)) != len(question_texts):
        raise ValueError("question texts must be unique")

    for question in questions:
        choices = [str(choice) for choice in question.get("choices", [])]
        answer = str(question.get("answer") or "")
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} must have 4 choices")
        if answer not in choices:
            raise ValueError(f"answer missing from choices in question {question['id']}")


def _write_questions(questions: list[dict[str, object]]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    questions = _build_questions()
    _validate_questions(questions)
    _write_questions(questions)
    difficulty_counts = Counter(str(question["difficulty"]) for question in questions)
    family_counts = Counter(str(question["tags"][1]) for question in questions)  # type: ignore[index]
    print(f"Wrote {len(questions)} questions to {OUTPUT_PATH}")
    print(f"Difficulty counts: {dict(difficulty_counts)}")
    print(f"Family counts: {dict(family_counts)}")
    return 0


INTRO_BASE = (
    {
        "original": "Before the meeting the clerk filed the memo.",
        "correct": "Before the meeting, the clerk filed the memo.",
        "wrong_1": "Before the meeting the clerk filed the memo, and the manager approved it.",
        "wrong_2": "Before the meeting; the clerk filed the memo.",
        "wrong_3": "Before, the meeting the clerk filed the memo.",
    },
    {
        "original": "In the cabinet the clerk found the memo.",
        "correct": "In the cabinet, the clerk found the memo.",
        "wrong_1": "In the cabinet the clerk found the memo, and the manager kept searching.",
        "wrong_2": "In the cabinet; the clerk found the memo.",
        "wrong_3": "In, the cabinet the clerk found the memo.",
    },
    {
        "original": "After lunch the manager approved the report.",
        "correct": "After lunch, the manager approved the report.",
        "wrong_1": "After lunch the manager approved the report, and the assistant filed it.",
        "wrong_2": "After lunch; the manager approved the report.",
        "wrong_3": "After, lunch the manager approved the report.",
    },
    {
        "original": "During the briefing the supervisor took notes.",
        "correct": "During the briefing, the supervisor took notes.",
        "wrong_1": "During the briefing the supervisor took notes, and the trainees listened.",
        "wrong_2": "During the briefing; the supervisor took notes.",
        "wrong_3": "During, the briefing the supervisor took notes.",
    },
    {
        "original": "On Friday the branch reopened.",
        "correct": "On Friday, the branch reopened.",
        "wrong_1": "On Friday the branch reopened, and the staff returned.",
        "wrong_2": "On Friday; the branch reopened.",
        "wrong_3": "On, Friday the branch reopened.",
    },
    {
        "original": "By the window the courier waited quietly.",
        "correct": "By the window, the courier waited quietly.",
        "wrong_1": "By the window the courier waited quietly, and the clerk called inside.",
        "wrong_2": "By the window; the courier waited quietly.",
        "wrong_3": "By, the window the courier waited quietly.",
    },
    {
        "original": "Under the desk the office assistant found the stamp.",
        "correct": "Under the desk, the office assistant found the stamp.",
        "wrong_1": "Under the desk the office assistant found the stamp, and the clerk wrote it down.",
        "wrong_2": "Under the desk; the office assistant found the stamp.",
        "wrong_3": "Under, the desk the office assistant found the stamp.",
    },
    {
        "original": "Before noon the auditor checked the files.",
        "correct": "Before noon, the auditor checked the files.",
        "wrong_1": "Before noon the auditor checked the files, and the supervisor signed them.",
        "wrong_2": "Before noon; the auditor checked the files.",
        "wrong_3": "Before, noon the auditor checked the files.",
    },
    {
        "original": "With her hands full the clerk answered the phone.",
        "correct": "With her hands full, the clerk answered the phone.",
        "wrong_1": "With her hands full the clerk answered the phone, and the supervisor waited.",
        "wrong_2": "With her hands full; the clerk answered the phone.",
        "wrong_3": "With, her hands full the clerk answered the phone.",
    },
    {
        "original": "Her notes carefully arranged the trainer left the room.",
        "correct": "Her notes carefully arranged, the trainer left the room.",
        "wrong_1": "Her notes carefully arranged the trainer left the room, and the students followed.",
        "wrong_2": "Her notes carefully arranged; the trainer left the room.",
        "wrong_3": "Her notes carefully, arranged the trainer left the room.",
    },
)
APPOSITIVE_BASE = (
    {
        "original": "Maya the branch coordinator filed the memo.",
        "correct": "Maya, the branch coordinator, filed the memo.",
        "wrong_1": "Maya the branch coordinator, filed the memo.",
        "wrong_2": "Maya, the branch coordinator filed the memo.",
        "wrong_3": "Maya, the branch coordinator, filed the memo, and the manager approved it.",
    },
    {
        "original": "Mr. Santos the senior auditor reviewed the report.",
        "correct": "Mr. Santos, the senior auditor, reviewed the report.",
        "wrong_1": "Mr. Santos the senior auditor, reviewed the report.",
        "wrong_2": "Mr. Santos, the senior auditor reviewed the report.",
        "wrong_3": "Mr. Santos, the senior auditor, reviewed the report, and the clerk took notes.",
    },
    {
        "original": "Rina the clerk handled the forms.",
        "correct": "Rina, the clerk, handled the forms.",
        "wrong_1": "Rina the clerk, handled the forms.",
        "wrong_2": "Rina, the clerk handled the forms.",
        "wrong_3": "Rina, the clerk, handled the forms, and the auditor checked them.",
    },
    {
        "original": "Ben the courier delivered the package.",
        "correct": "Ben, the courier, delivered the package.",
        "wrong_1": "Ben the courier, delivered the package.",
        "wrong_2": "Ben, the courier delivered the package.",
        "wrong_3": "Ben, the courier, delivered the package, and the clerk signed the receipt.",
    },
    {
        "original": "Liza the trainer explained the rules.",
        "correct": "Liza, the trainer, explained the rules.",
        "wrong_1": "Liza the trainer, explained the rules.",
        "wrong_2": "Liza, the trainer explained the rules.",
        "wrong_3": "Liza, the trainer, explained the rules, and the students listened.",
    },
    {
        "original": "Paolo the auditor checked the records.",
        "correct": "Paolo, the auditor, checked the records.",
        "wrong_1": "Paolo the auditor, checked the records.",
        "wrong_2": "Paolo, the auditor checked the records.",
        "wrong_3": "Paolo, the auditor, checked the records, and the manager signed the log.",
    },
    {
        "original": "Joel the branch manager signed the letter.",
        "correct": "Joel, the branch manager, signed the letter.",
        "wrong_1": "Joel the branch manager, signed the letter.",
        "wrong_2": "Joel, the branch manager signed the letter.",
        "wrong_3": "Joel, the branch manager, signed the letter, and the assistant filed it.",
    },
    {
        "original": "Nina the student leader gave the update.",
        "correct": "Nina, the student leader, gave the update.",
        "wrong_1": "Nina the student leader, gave the update.",
        "wrong_2": "Nina, the student leader gave the update.",
        "wrong_3": "Nina, the student leader, gave the update, and the class cheered.",
    },
    {
        "original": "Ana the doctor reviewed the chart.",
        "correct": "Ana, the doctor, reviewed the chart.",
        "wrong_1": "Ana the doctor, reviewed the chart.",
        "wrong_2": "Ana, the doctor reviewed the chart.",
        "wrong_3": "Ana, the doctor, reviewed the chart, and the nurse waited.",
    },
    {
        "original": "Mrs. Cruz the office manager approved the notice.",
        "correct": "Mrs. Cruz, the office manager, approved the notice.",
        "wrong_1": "Mrs. Cruz the office manager, approved the notice.",
        "wrong_2": "Mrs. Cruz, the office manager approved the notice.",
        "wrong_3": "Mrs. Cruz, the office manager, approved the notice, and the staff copied it.",
    },
)


if __name__ == "__main__":
    raise SystemExit(main())
