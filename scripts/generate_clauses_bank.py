"""Generate the Verbal Ability / Sentence Structure / Clauses question bank."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "sentence-structure"
    / "clauses"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Clauses"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "clauses"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

FAMILY_ORDER = (
    "independent-clause-identification",
    "dependent-clause-identification",
    "sentence-type-classification",
    "clause-vs-phrase-classification",
    "noun-clause-identification",
    "adjective-clause-identification",
    "adverb-clause-identification",
    "relative-clause-repair",
    "introductory-dependent-clause-comma",
    "clause-joining-comma-conjunction",
    "clause-joining-semicolon",
    "dependent-clause-fragment-diagnosis",
    "run-on-diagnosis",
    "clause-repair-complete-sentence",
    "true-subject-clause-distractor",
)

QUESTION_STEMS: dict[str, dict[str, str]] = {
    "independent-clause-identification": {
        "Easy": 'Which option is the independent clause in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice can stand alone as a complete thought?',
        "Hard": 'Which phrase in "{sentence}" is the main clause?',
        "Ultra": 'Which choice names the independent clause in "{sentence}"?',
    },
    "dependent-clause-identification": {
        "Easy": 'Which option is the dependent clause in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice is the subordinate clause?',
        "Hard": 'Which phrase in "{sentence}" cannot stand alone as a complete sentence?',
        "Ultra": 'Which choice identifies the dependent clause in "{sentence}"?',
    },
    "sentence-type-classification": {
        "Easy": 'Which sentence type best describes "{sentence}"?',
        "Medium": 'How should "{sentence}" be classified?',
        "Hard": 'Which sentence type fits "{sentence}"?',
        "Ultra": 'What structural type is "{sentence}"?',
    },
    "clause-vs-phrase-classification": {
        "Easy": 'Which option is the {target_label}, not the {contrast_label}, in {set_name}?',
        "Medium": 'In {set_name}, which choice is the {target_label}?',
        "Hard": 'Which choice is the {target_label} rather than the {contrast_label} in {set_name}?',
        "Ultra": 'Which option belongs to the {target_label} side of {set_name}?',
    },
    "noun-clause-identification": {
        "Easy": 'Which option is the noun clause in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice acts as a noun?',
        "Hard": 'Which phrase in "{sentence}" is the noun clause?',
        "Ultra": 'Which choice names the noun clause that functions as {role} in "{sentence}"?',
    },
    "adjective-clause-identification": {
        "Easy": 'Which option is the adjective clause in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice describes a noun?',
        "Hard": 'Which phrase in "{sentence}" is the relative clause?',
        "Ultra": 'Which choice identifies the adjective clause modifying the noun in "{sentence}"?',
    },
    "adverb-clause-identification": {
        "Easy": 'Which option is the adverb clause in "{sentence}"?',
        "Medium": 'In "{sentence}", which choice shows the relation of {relation}?',
        "Hard": 'Which phrase in "{sentence}" is the subordinate adverb clause?',
        "Ultra": 'Which choice identifies the adverb clause showing {relation} in "{sentence}"?',
    },
    "relative-clause-repair": {
        "Easy": 'Which revision correctly punctuates and structures the relative clause in "{original}"?',
        "Medium": 'Which sentence is the best revision of "{original}"?',
        "Hard": 'Which choice correctly repairs the relative-clause sentence "{original}"?',
        "Ultra": 'Which revision preserves the right restrictive or nonrestrictive relative clause in "{original}"?',
    },
    "introductory-dependent-clause-comma": {
        "Easy": 'Which revision correctly adds the comma after the introductory clause in "{original}"?',
        "Medium": 'Which sentence is punctuated correctly after the opening dependent clause in "{original}"?',
        "Hard": 'Which choice correctly separates the introductory clause in "{original}"?',
        "Ultra": 'Which revision correctly punctuates the opening dependent clause in "{original}"?',
    },
    "clause-joining-comma-conjunction": {
        "Easy": 'Which revision correctly joins the two independent clauses in "{original}" with a comma and conjunction?',
        "Medium": 'Which sentence correctly combines the clauses in "{original}" with a comma and coordinating conjunction?',
        "Hard": 'Which choice uses the correct comma-plus-conjunction pattern for "{original}"?',
        "Ultra": 'Which revision correctly repairs the clause join in "{original}" by using a comma and conjunction?',
    },
    "clause-joining-semicolon": {
        "Easy": 'Which revision correctly joins the two independent clauses in "{original}" with a semicolon?',
        "Medium": 'Which sentence correctly uses a semicolon in "{original}"?',
        "Hard": 'Which choice repairs "{original}" with a semicolon and keeps both clauses independent?',
        "Ultra": 'Which revision shows the best semicolon link between the clauses in "{original}"?',
    },
    "dependent-clause-fragment-diagnosis": {
        "Easy": 'Which option is only a dependent-clause fragment in "{fragment}"?',
        "Medium": 'In "{fragment}", which choice cannot stand alone as a complete sentence?',
        "Hard": 'Which option is the fragment rather than a complete sentence in "{fragment}"?',
        "Ultra": 'Which choice is the dependent-clause fragment in "{fragment}"?',
    },
    "run-on-diagnosis": {
        "Easy": 'What error best describes "{sentence}"?',
        "Medium": 'In "{sentence}", which diagnosis fits best?',
        "Hard": 'Which label best names the error in "{sentence}"?',
        "Ultra": 'What clause-level error does "{sentence}" contain?',
    },
    "clause-repair-complete-sentence": {
        "Easy": 'Which revision turns "{fragment}" into a complete sentence?',
        "Medium": 'Which sentence repairs "{fragment}" most correctly?',
        "Hard": 'Which choice best turns "{fragment}" into a complete thought?',
        "Ultra": 'Which revision fixes "{fragment}" and makes the clause pattern correct?',
    },
    "true-subject-clause-distractor": {
        "Easy": 'What is the true subject in "{sentence}" after ignoring the prepositional phrase(s)?',
        "Medium": 'After removing the prepositional phrase(s), what word is the subject in "{sentence}"?',
        "Hard": 'Which word actually controls the verb in "{sentence}"?',
        "Ultra": 'What noun is the real subject of "{sentence}"?',
    },
}


def _stem(family: str, difficulty: str, values: dict[str, str]) -> str:
    return QUESTION_STEMS[family][difficulty].format(**values)


def _rotate_choices(choices: tuple[str, str, str, str], offset: int) -> list[str]:
    items = list(choices)
    rotation = offset % len(items)
    return items[rotation:] + items[:rotation]


def _scene(
    *,
    values: dict[str, str],
    choices: tuple[str, str, str, str],
    answer: str,
    explanation: str,
    tags: tuple[str, ...],
) -> dict[str, object]:
    return {
        "values": values,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
    }


def _expand_family(
    family: str,
    scenes: list[dict[str, object]],
) -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    for scene_index, scene in enumerate(scenes):
        values = dict(scene["values"])  # type: ignore[arg-type]
        choices = tuple(str(choice) for choice in scene["choices"])  # type: ignore[arg-type]
        answer = str(scene["answer"])
        explanation = str(scene["explanation"])
        scene_tags = tuple(str(tag) for tag in scene["tags"])  # type: ignore[arg-type]
        for difficulty_index, difficulty in enumerate(DIFFICULTIES):
            question_id = len(questions) + 1
            rotated = _rotate_choices(choices, question_id + scene_index + difficulty_index)
            questions.append(
                {
                    "id": question_id,
                    "subtest": SUBTEST,
                    "module": MODULE,
                    "subtopic": SUBTOPIC,
                    "difficulty": difficulty,
                    "question": _stem(family, difficulty, values),
                    "choices": rotated,
                    "answer": answer,
                    "explanation": explanation,
                    "tags": [ROOT_TAG, family, DIFFICULTY_TAGS[difficulty], *scene_tags],
                    "category": CATEGORY,
                    "language": LANGUAGE,
                }
            )
    return questions


def _build_independent_clause_identification() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "The clerk filed the report before lunch."},
            choices=(
                "before lunch",
                "the report",
                "filed the report before lunch",
                "The clerk filed the report",
            ),
            answer="The clerk filed the report",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The manager approved the memo after the review."},
            choices=(
                "after the review",
                "the memo",
                "approved the memo after the review",
                "The manager approved the memo",
            ),
            answer="The manager approved the memo",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The staff checked the forms when the system reopened."},
            choices=(
                "when the system reopened",
                "the forms",
                "checked the forms when the system reopened",
                "The staff checked the forms",
            ),
            answer="The staff checked the forms",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The auditor signed the letter after the corrections were made."},
            choices=(
                "after the corrections were made",
                "the letter",
                "signed the letter after the corrections were made",
                "The auditor signed the letter",
            ),
            answer="The auditor signed the letter",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The team waited in the lobby until the doors opened."},
            choices=(
                "until the doors opened",
                "the lobby",
                "waited in the lobby until the doors opened",
                "The team waited in the lobby",
            ),
            answer="The team waited in the lobby",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The office sent the notice because the deadline changed."},
            choices=(
                "because the deadline changed",
                "the notice",
                "sent the notice because the deadline changed",
                "The office sent the notice",
            ),
            answer="The office sent the notice",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The supervisor called the applicant once the file was ready."},
            choices=(
                "once the file was ready",
                "the applicant",
                "called the applicant once the file was ready",
                "The supervisor called the applicant",
            ),
            answer="The supervisor called the applicant",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The trainer explained the rules while the class settled down."},
            choices=(
                "while the class settled down",
                "the rules",
                "explained the rules while the class settled down",
                "The trainer explained the rules",
            ),
            answer="The trainer explained the rules",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The branch closed early since the storm was severe."},
            choices=(
                "since the storm was severe",
                "the storm",
                "closed early since the storm was severe",
                "The branch closed early",
            ),
            answer="The branch closed early",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
        _scene(
            values={"sentence": "The assistant logged the request after the call ended."},
            choices=(
                "after the call ended",
                "the request",
                "logged the request after the call ended",
                "The assistant logged the request",
            ),
            answer="The assistant logged the request",
            explanation="It has a subject and a verb and expresses a complete thought.",
            tags=("independent-clause", "main-clause"),
        ),
    ]
    return _expand_family("independent-clause-identification", scenes)


def _build_dependent_clause_identification() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "Because the office was closed, the clerk went home."},
            choices=(
                "Because the office was closed",
                "the clerk went home",
                "the office was closed",
                "the clerk",
            ),
            answer="Because the office was closed",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "When the meeting ended, the team filed out."},
            choices=(
                "When the meeting ended",
                "the team filed out",
                "the meeting ended",
                "the team",
            ),
            answer="When the meeting ended",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "Although the forms were late, the manager approved them."},
            choices=(
                "Although the forms were late",
                "the manager approved them",
                "the forms were late",
                "the manager",
            ),
            answer="Although the forms were late",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "If the printer jams, the assistant will call for help."},
            choices=(
                "If the printer jams",
                "the assistant will call for help",
                "the printer jams",
                "the assistant",
            ),
            answer="If the printer jams",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "While the reviewer waited, the clerk checked the file."},
            choices=(
                "While the reviewer waited",
                "the clerk checked the file",
                "the reviewer waited",
                "the clerk",
            ),
            answer="While the reviewer waited",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "Since the memo was short, the office sent a reply."},
            choices=(
                "Since the memo was short",
                "the office sent a reply",
                "the memo was short",
                "the office",
            ),
            answer="Since the memo was short",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "Before the branch opened, the staff arranged the chairs."},
            choices=(
                "Before the branch opened",
                "the staff arranged the chairs",
                "the branch opened",
                "the staff",
            ),
            answer="Before the branch opened",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "Unless the director arrives, the meeting will start."},
            choices=(
                "Unless the director arrives",
                "the meeting will start",
                "the director arrives",
                "the meeting",
            ),
            answer="Unless the director arrives",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "As soon as the bell rang, the trainees sat down."},
            choices=(
                "As soon as the bell rang",
                "the trainees sat down",
                "the bell rang",
                "the trainees",
            ),
            answer="As soon as the bell rang",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
        _scene(
            values={"sentence": "After the audit finished, the supervisor signed the report."},
            choices=(
                "After the audit finished",
                "the supervisor signed the report",
                "the audit finished",
                "the supervisor",
            ),
            answer="After the audit finished",
            explanation="It has a subject and a verb but cannot stand alone as a complete thought.",
            tags=("dependent-clause", "subordinate-clause"),
        ),
    ]
    return _expand_family("dependent-clause-identification", scenes)


def _build_sentence_type_classification() -> list[dict[str, object]]:
    sentence_types = (
        "Simple sentence",
        "Compound sentence",
        "Complex sentence",
        "Compound-complex sentence",
    )
    scenes = [
        _scene(
            values={"sentence": "The clerk filed the report."},
            choices=sentence_types,
            answer="Simple sentence",
            explanation="It has one independent clause and no dependent clause.",
            tags=("simple",),
        ),
        _scene(
            values={"sentence": "The clerk filed the report, and the manager approved it."},
            choices=sentence_types,
            answer="Compound sentence",
            explanation="It has two independent clauses joined by a coordinating conjunction.",
            tags=("compound", "coordinating-conjunction"),
        ),
        _scene(
            values={"sentence": "Because the office was closed, the clerk went home."},
            choices=sentence_types,
            answer="Complex sentence",
            explanation="It has one independent clause and one dependent clause.",
            tags=("complex", "dependent-clause"),
        ),
        _scene(
            values={"sentence": "Because the office was closed, the clerk went home, and the manager locked the door."},
            choices=sentence_types,
            answer="Compound-complex sentence",
            explanation="It has a dependent clause and two independent clauses.",
            tags=("compound-complex", "dependent-clause"),
        ),
        _scene(
            values={"sentence": "The staff waited in the lobby."},
            choices=sentence_types,
            answer="Simple sentence",
            explanation="It has one independent clause and no dependent clause.",
            tags=("simple",),
        ),
        _scene(
            values={"sentence": "The supervisor called the applicant, but the line was busy."},
            choices=sentence_types,
            answer="Compound sentence",
            explanation="It has two independent clauses joined by a coordinating conjunction.",
            tags=("compound", "coordinating-conjunction"),
        ),
        _scene(
            values={"sentence": "When the meeting ended, the team filed out."},
            choices=sentence_types,
            answer="Complex sentence",
            explanation="It has one independent clause and one dependent clause.",
            tags=("complex", "dependent-clause"),
        ),
        _scene(
            values={"sentence": "The branch reopened, and the visitors returned."},
            choices=sentence_types,
            answer="Compound sentence",
            explanation="It has two independent clauses joined by a coordinating conjunction.",
            tags=("compound", "coordinating-conjunction"),
        ),
        _scene(
            values={"sentence": "If the printer jams, the assistant will call for help, and the clerk will notify IT."},
            choices=sentence_types,
            answer="Compound-complex sentence",
            explanation="It has a dependent clause and two independent clauses.",
            tags=("compound-complex", "dependent-clause"),
        ),
        _scene(
            values={"sentence": "The office sent the memo."},
            choices=sentence_types,
            answer="Simple sentence",
            explanation="It has one independent clause and no dependent clause.",
            tags=("simple",),
        ),
    ]
    return _expand_family("sentence-type-classification", scenes)


def _build_clause_vs_phrase_classification() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={
                "set_name": "the office-closure set",
                "target_label": "dependent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "because the office was closed",
                "before lunch",
                "the clerk went home",
                "the office",
            ),
            answer="because the office was closed",
            explanation="It has a subject and a verb and begins with a marker, so it is a dependent clause.",
            tags=("dependent-clause", "phrase-contrast"),
        ),
        _scene(
            values={
                "set_name": "the clerk-home set",
                "target_label": "independent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "the clerk went home",
                "because the office was closed",
                "before lunch",
                "the office",
            ),
            answer="the clerk went home",
            explanation="It has a subject and a verb and can stand alone, so it is an independent clause.",
            tags=("independent-clause", "phrase-contrast"),
        ),
        _scene(
            values={
                "set_name": "the lunch-break set",
                "target_label": "phrase",
                "contrast_label": "clause",
            },
            choices=(
                "before lunch",
                "because the office was closed",
                "the clerk went home",
                "the office",
            ),
            answer="before lunch",
            explanation="It does not contain both a subject and a verb, so it is a phrase.",
            tags=("phrase", "clause-contrast"),
        ),
        _scene(
            values={
                "set_name": "the meeting-ending set",
                "target_label": "dependent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "when the meeting ended",
                "the meeting ended",
                "after the meeting",
                "the team filed out",
            ),
            answer="when the meeting ended",
            explanation="It has a subject and a verb and begins with a marker, so it is a dependent clause.",
            tags=("dependent-clause", "phrase-contrast"),
        ),
        _scene(
            values={
                "set_name": "the team-exit set",
                "target_label": "independent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "The team filed out",
                "when the meeting ended",
                "after the meeting",
                "the meeting",
            ),
            answer="The team filed out",
            explanation="It has a subject and a verb and can stand alone, so it is an independent clause.",
            tags=("independent-clause", "phrase-contrast"),
        ),
        _scene(
            values={
                "set_name": "the after-meeting set",
                "target_label": "phrase",
                "contrast_label": "clause",
            },
            choices=(
                "after the meeting",
                "when the meeting ended",
                "The team filed out",
                "the team",
            ),
            answer="after the meeting",
            explanation="It does not contain both a subject and a verb, so it is a phrase.",
            tags=("phrase", "clause-contrast"),
        ),
        _scene(
            values={
                "set_name": "the printer-jam set",
                "target_label": "dependent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "if the printer jams",
                "the printer jams",
                "the assistant will call",
                "the printer",
            ),
            answer="if the printer jams",
            explanation="It has a subject and a verb and begins with a marker, so it is a dependent clause.",
            tags=("dependent-clause", "phrase-contrast"),
        ),
        _scene(
            values={
                "set_name": "the assistant-call set",
                "target_label": "independent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "the assistant will call",
                "if the printer jams",
                "because the forms were late",
                "the assistant",
            ),
            answer="the assistant will call",
            explanation="It has a subject and a verb and can stand alone, so it is an independent clause.",
            tags=("independent-clause", "phrase-contrast"),
        ),
        _scene(
            values={
                "set_name": "the assistant-only set",
                "target_label": "phrase",
                "contrast_label": "clause",
            },
            choices=(
                "the assistant",
                "because the forms were late",
                "if the printer jams",
                "the assistant will call",
            ),
            answer="the assistant",
            explanation="It does not contain both a subject and a verb, so it is a phrase.",
            tags=("phrase", "clause-contrast"),
        ),
        _scene(
            values={
                "set_name": "the memo-delay set",
                "target_label": "dependent clause",
                "contrast_label": "phrase",
            },
            choices=(
                "because the forms were late",
                "the forms were late",
                "The office sent the memo",
                "the forms",
            ),
            answer="because the forms were late",
            explanation="It has a subject and a verb and begins with a marker, so it is a dependent clause.",
            tags=("dependent-clause", "phrase-contrast"),
        ),
    ]
    return _expand_family("clause-vs-phrase-classification", scenes)


def _build_noun_clause_identification() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "What the committee decided mattered to everyone.", "role": "subject"},
            choices=(
                "What the committee decided",
                "the committee decided",
                "because the committee decided",
                "the decided committee",
            ),
            answer="What the committee decided",
            explanation="It has a subject and a verb and functions as a noun, so it is a noun clause.",
            tags=("noun-clause", "subject"),
        ),
        _scene(
            values={"sentence": "The manager knew that the report was late.", "role": "object"},
            choices=(
                "that the report was late",
                "the report was late",
                "the late report",
                "because the report was late",
            ),
            answer="that the report was late",
            explanation="It has a subject and a verb and functions as the object of knew.",
            tags=("noun-clause", "object"),
        ),
        _scene(
            values={"sentence": "The problem is that the files were missing.", "role": "complement"},
            choices=(
                "that the files were missing",
                "the files were missing",
                "the missing files",
                "because the files were missing",
            ),
            answer="that the files were missing",
            explanation="It completes the linking verb is, so it works as a noun clause.",
            tags=("noun-clause", "complement"),
        ),
        _scene(
            values={"sentence": "Please tell me where the office kept the forms.", "role": "object"},
            choices=(
                "where the office kept the forms",
                "the office kept the forms",
                "the office forms",
                "because the office kept the forms",
            ),
            answer="where the office kept the forms",
            explanation="It functions as the object of tell.",
            tags=("noun-clause", "object"),
        ),
        _scene(
            values={"sentence": "We depended on whoever arrived first.", "role": "object of the preposition"},
            choices=(
                "whoever arrived first",
                "who arrived first",
                "the first arrival",
                "because whoever arrived first",
            ),
            answer="whoever arrived first",
            explanation="It follows the preposition on and acts as its object.",
            tags=("noun-clause", "preposition-object"),
        ),
        _scene(
            values={"sentence": "I asked whether the meeting would continue.", "role": "object"},
            choices=(
                "whether the meeting would continue",
                "the meeting would continue",
                "the continuing meeting",
                "because the meeting would continue",
            ),
            answer="whether the meeting would continue",
            explanation="It functions as the object of asked.",
            tags=("noun-clause", "object"),
        ),
        _scene(
            values={"sentence": "She explained why the memo was delayed.", "role": "object"},
            choices=(
                "why the memo was delayed",
                "the memo was delayed",
                "the delayed memo",
                "because the memo was delayed",
            ),
            answer="why the memo was delayed",
            explanation="It functions as the object of explained.",
            tags=("noun-clause", "object"),
        ),
        _scene(
            values={"sentence": "The issue is how the clerk should respond.", "role": "complement"},
            choices=(
                "how the clerk should respond",
                "the clerk should respond",
                "the clerk's response",
                "because the clerk should respond",
            ),
            answer="how the clerk should respond",
            explanation="It completes the linking verb is, so it works as a noun clause.",
            tags=("noun-clause", "complement"),
        ),
        _scene(
            values={"sentence": "They discussed when the branch should reopen.", "role": "object"},
            choices=(
                "when the branch should reopen",
                "the branch should reopen",
                "the reopening branch",
                "because the branch should reopen",
            ),
            answer="when the branch should reopen",
            explanation="It functions as the object of discussed.",
            tags=("noun-clause", "object"),
        ),
        _scene(
            values={"sentence": "Whoever calls first gets the slot.", "role": "subject"},
            choices=(
                "Whoever calls first",
                "calls first",
                "the first caller",
                "because whoever calls first",
            ),
            answer="Whoever calls first",
            explanation="It has a subject and a verb and functions as the subject of the sentence.",
            tags=("noun-clause", "subject"),
        ),
    ]
    return _expand_family("noun-clause-identification", scenes)


def _build_adjective_clause_identification() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "The memo that the clerk revised was approved."},
            choices=(
                "that the clerk revised",
                "the clerk revised",
                "the revised memo",
                "because the clerk revised it",
            ),
            answer="that the clerk revised",
            explanation="It modifies the noun memo, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The supervisor who signed the order left early."},
            choices=(
                "who signed the order",
                "the signed order",
                "the order",
                "because the supervisor signed",
            ),
            answer="who signed the order",
            explanation="It modifies the noun supervisor, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The office where the files were stored was locked."},
            choices=(
                "where the files were stored",
                "the files were stored",
                "the stored files",
                "because the files were stored",
            ),
            answer="where the files were stored",
            explanation="It modifies the noun office, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "Ms. Cruz, who manages the branch, arrived early."},
            choices=(
                "who manages the branch",
                "the branch manager",
                "the branch",
                "because Ms. Cruz manages the branch",
            ),
            answer="who manages the branch",
            explanation="It adds extra information about Ms. Cruz, so it is an adjective clause.",
            tags=("adjective-clause", "nonrestrictive"),
        ),
        _scene(
            values={"sentence": "The folder whose cover was torn was replaced."},
            choices=(
                "whose cover was torn",
                "the torn cover",
                "the folder cover",
                "because the cover was torn",
            ),
            answer="whose cover was torn",
            explanation="It modifies the noun folder, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The report which the auditor reviewed was filed."},
            choices=(
                "which the auditor reviewed",
                "the auditor reviewed",
                "the reviewed report",
                "because the auditor reviewed it",
            ),
            answer="which the auditor reviewed",
            explanation="It modifies the noun report, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The file that had the wrong date was corrected."},
            choices=(
                "that had the wrong date",
                "the wrong date",
                "the corrected file",
                "because it had the wrong date",
            ),
            answer="that had the wrong date",
            explanation="It modifies the noun file, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The room where the team met was quiet."},
            choices=(
                "where the team met",
                "the team met",
                "the quiet room",
                "because the team met there",
            ),
            answer="where the team met",
            explanation="It modifies the noun room, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The clerk whom the manager praised smiled."},
            choices=(
                "whom the manager praised",
                "the manager praised",
                "the praised clerk",
                "because the manager praised the clerk",
            ),
            answer="whom the manager praised",
            explanation="It modifies the noun clerk, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
        _scene(
            values={"sentence": "The policy that the office adopted saved time."},
            choices=(
                "that the office adopted",
                "the office adopted",
                "the adopted policy",
                "because the office adopted it",
            ),
            answer="that the office adopted",
            explanation="It modifies the noun policy, so it is an adjective clause.",
            tags=("adjective-clause", "restrictive"),
        ),
    ]
    return _expand_family("adjective-clause-identification", scenes)


def _build_adverb_clause_identification() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "Because the roads were flooded, the bus was late.", "relation": "reason"},
            choices=(
                "Because the roads were flooded",
                "the roads were flooded",
                "the bus was late",
                "the flooded roads",
            ),
            answer="Because the roads were flooded",
            explanation="It modifies the verb phrase by showing reason, so it is an adverb clause.",
            tags=("adverb-clause", "reason"),
        ),
        _scene(
            values={"sentence": "When the office reopened, the clerk filed the memo.", "relation": "time"},
            choices=(
                "When the office reopened",
                "the office reopened",
                "the clerk filed the memo",
                "the reopened office",
            ),
            answer="When the office reopened",
            explanation="It modifies the verb phrase by showing time, so it is an adverb clause.",
            tags=("adverb-clause", "time"),
        ),
        _scene(
            values={"sentence": "Although the file was found, the staff kept searching.", "relation": "contrast"},
            choices=(
                "Although the file was found",
                "the file was found",
                "the staff kept searching",
                "the found file",
            ),
            answer="Although the file was found",
            explanation="It modifies the verb phrase by showing contrast, so it is an adverb clause.",
            tags=("adverb-clause", "contrast"),
        ),
        _scene(
            values={"sentence": "If the manager approves, we will print the notice.", "relation": "condition"},
            choices=(
                "If the manager approves",
                "the manager approves",
                "we will print the notice",
                "the approving manager",
            ),
            answer="If the manager approves",
            explanation="It modifies the verb phrase by showing condition, so it is an adverb clause.",
            tags=("adverb-clause", "condition"),
        ),
        _scene(
            values={"sentence": "While the team waited, the supervisor called.", "relation": "time"},
            choices=(
                "While the team waited",
                "the team waited",
                "the supervisor called",
                "the waiting team",
            ),
            answer="While the team waited",
            explanation="It modifies the verb phrase by showing time, so it is an adverb clause.",
            tags=("adverb-clause", "time"),
        ),
        _scene(
            values={"sentence": "Since the printer jammed, the copies were delayed.", "relation": "reason"},
            choices=(
                "Since the printer jammed",
                "the printer jammed",
                "the copies were delayed",
                "the jammed printer",
            ),
            answer="Since the printer jammed",
            explanation="It modifies the verb phrase by showing reason, so it is an adverb clause.",
            tags=("adverb-clause", "reason"),
        ),
        _scene(
            values={"sentence": "Before the meeting began, the staff took seats.", "relation": "time"},
            choices=(
                "Before the meeting began",
                "the meeting began",
                "the staff took seats",
                "the beginning meeting",
            ),
            answer="Before the meeting began",
            explanation="It modifies the verb phrase by showing time, so it is an adverb clause.",
            tags=("adverb-clause", "time"),
        ),
        _scene(
            values={"sentence": "After the audit ended, the office closed.", "relation": "time"},
            choices=(
                "After the audit ended",
                "the audit ended",
                "the office closed",
                "the ended audit",
            ),
            answer="After the audit ended",
            explanation="It modifies the verb phrase by showing time, so it is an adverb clause.",
            tags=("adverb-clause", "time"),
        ),
        _scene(
            values={"sentence": "Unless the form is signed, the request will pause.", "relation": "condition"},
            choices=(
                "Unless the form is signed",
                "the form is signed",
                "the request will pause",
                "the signed form",
            ),
            answer="Unless the form is signed",
            explanation="It modifies the verb phrase by showing condition, so it is an adverb clause.",
            tags=("adverb-clause", "condition"),
        ),
        _scene(
            values={"sentence": "As soon as the clerk arrived, the team started the review.", "relation": "time"},
            choices=(
                "As soon as the clerk arrived",
                "the clerk arrived",
                "the team started the review",
                "the arriving clerk",
            ),
            answer="As soon as the clerk arrived",
            explanation="It modifies the verb phrase by showing time, so it is an adverb clause.",
            tags=("adverb-clause", "time"),
        ),
    ]
    return _expand_family("adverb-clause-identification", scenes)


def _build_relative_clause_repair() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"original": "The report that the clerk revised was approved."},
            choices=(
                "The report that the clerk revised was approved.",
                "The report, which the clerk revised, was approved.",
                "The report that the clerk revised, was approved.",
                "The report which the clerk revised was approved.",
            ),
            answer="The report that the clerk revised was approved.",
            explanation="The restrictive clause should stay with that and no commas.",
            tags=("relative-clause", "restrictive"),
        ),
        _scene(
            values={"original": "The supervisor, who arrived early, opened the office."},
            choices=(
                "The supervisor, who arrived early, opened the office.",
                "The supervisor who arrived early opened the office.",
                "The supervisor, that arrived early, opened the office.",
                "The supervisor, who arrived early opened the office.",
            ),
            answer="The supervisor, who arrived early, opened the office.",
            explanation="The nonrestrictive clause needs commas and who, not that.",
            tags=("relative-clause", "nonrestrictive"),
        ),
        _scene(
            values={"original": "The forms that were signed were archived."},
            choices=(
                "The forms that were signed were archived.",
                "The forms, that were signed, were archived.",
                "The forms which were signed were archived.",
                "The forms that were signed, were archived.",
            ),
            answer="The forms that were signed were archived.",
            explanation="The restrictive clause should stay with that and no commas.",
            tags=("relative-clause", "restrictive"),
        ),
        _scene(
            values={"original": "The office, which was reopened yesterday, welcomed visitors."},
            choices=(
                "The office, which was reopened yesterday, welcomed visitors.",
                "The office which was reopened yesterday welcomed visitors.",
                "The office, that was reopened yesterday, welcomed visitors.",
                "The office, which was reopened yesterday welcomed visitors.",
            ),
            answer="The office, which was reopened yesterday, welcomed visitors.",
            explanation="The nonrestrictive clause needs commas and which.",
            tags=("relative-clause", "nonrestrictive"),
        ),
        _scene(
            values={"original": "The file that had the wrong date was corrected."},
            choices=(
                "The file that had the wrong date was corrected.",
                "The file, which had the wrong date, was corrected.",
                "The file that had the wrong date, was corrected.",
                "The file which had the wrong date was corrected.",
            ),
            answer="The file that had the wrong date was corrected.",
            explanation="The restrictive clause should stay with that and no commas.",
            tags=("relative-clause", "restrictive"),
        ),
        _scene(
            values={"original": "The trainer, whose notes were clear, explained the policy."},
            choices=(
                "The trainer, whose notes were clear, explained the policy.",
                "The trainer whose notes were clear explained the policy.",
                "The trainer, who's notes were clear, explained the policy.",
                "The trainer, whose notes were clear explained the policy.",
            ),
            answer="The trainer, whose notes were clear, explained the policy.",
            explanation="The nonrestrictive clause needs commas and whose.",
            tags=("relative-clause", "nonrestrictive"),
        ),
        _scene(
            values={"original": "The clerk who answered first received the badge."},
            choices=(
                "The clerk who answered first received the badge.",
                "The clerk, who answered first, received the badge.",
                "The clerk whom answered first received the badge.",
                "The clerk who answered first, received the badge.",
            ),
            answer="The clerk who answered first received the badge.",
            explanation="The restrictive clause should stay without commas and with who.",
            tags=("relative-clause", "restrictive"),
        ),
        _scene(
            values={"original": "The meeting, which ended early, allowed everyone to leave."},
            choices=(
                "The meeting, which ended early, allowed everyone to leave.",
                "The meeting which ended early allowed everyone to leave.",
                "The meeting, that ended early, allowed everyone to leave.",
                "The meeting, which ended early allowed everyone to leave.",
            ),
            answer="The meeting, which ended early, allowed everyone to leave.",
            explanation="The nonrestrictive clause needs commas and which.",
            tags=("relative-clause", "nonrestrictive"),
        ),
        _scene(
            values={"original": "The packets that the supervisor checked were missing."},
            choices=(
                "The packets that the supervisor checked were missing.",
                "The packets, that the supervisor checked, were missing.",
                "The packets which the supervisor checked were missing.",
                "The packets that the supervisor checked, were missing.",
            ),
            answer="The packets that the supervisor checked were missing.",
            explanation="The restrictive clause should stay with that and no commas.",
            tags=("relative-clause", "restrictive"),
        ),
        _scene(
            values={"original": "The branch, where the records were kept, stayed open."},
            choices=(
                "The branch, where the records were kept, stayed open.",
                "The branch where the records were kept stayed open.",
                "The branch, that the records were kept, stayed open.",
                "The branch, where the records were kept stayed open.",
            ),
            answer="The branch, where the records were kept, stayed open.",
            explanation="The nonrestrictive clause needs commas and where.",
            tags=("relative-clause", "nonrestrictive"),
        ),
    ]
    return _expand_family("relative-clause-repair", scenes)


def _build_introductory_dependent_clause_comma() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"original": "Because the office was closed the clerk went home."},
            choices=(
                "Because the office was closed, the clerk went home.",
                "Because the office was closed; the clerk went home.",
                "Because, the office was closed, the clerk went home.",
                "Because the office was closed the clerk, went home.",
            ),
            answer="Because the office was closed, the clerk went home.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "When the meeting ended the team filed out."},
            choices=(
                "When the meeting ended, the team filed out.",
                "When the meeting ended; the team filed out.",
                "When, the meeting ended, the team filed out.",
                "When the meeting ended the team, filed out.",
            ),
            answer="When the meeting ended, the team filed out.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "After the audit finished the supervisor signed the report."},
            choices=(
                "After the audit finished, the supervisor signed the report.",
                "After the audit finished; the supervisor signed the report.",
                "After, the audit finished, the supervisor signed the report.",
                "After the audit finished the supervisor, signed the report.",
            ),
            answer="After the audit finished, the supervisor signed the report.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "Although the forms were late the manager approved them."},
            choices=(
                "Although the forms were late, the manager approved them.",
                "Although the forms were late; the manager approved them.",
                "Although, the forms were late, the manager approved them.",
                "Although the forms were late the manager, approved them.",
            ),
            answer="Although the forms were late, the manager approved them.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "If the printer jams the assistant will call for help."},
            choices=(
                "If the printer jams, the assistant will call for help.",
                "If the printer jams; the assistant will call for help.",
                "If, the printer jams, the assistant will call for help.",
                "If the printer jams the assistant, will call for help.",
            ),
            answer="If the printer jams, the assistant will call for help.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "Since the memo was short the office sent a reply."},
            choices=(
                "Since the memo was short, the office sent a reply.",
                "Since the memo was short; the office sent a reply.",
                "Since, the memo was short, the office sent a reply.",
                "Since the memo was short the office, sent a reply.",
            ),
            answer="Since the memo was short, the office sent a reply.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "Before the branch opened the staff arranged the chairs."},
            choices=(
                "Before the branch opened, the staff arranged the chairs.",
                "Before the branch opened; the staff arranged the chairs.",
                "Before, the branch opened, the staff arranged the chairs.",
                "Before the branch opened the staff, arranged the chairs.",
            ),
            answer="Before the branch opened, the staff arranged the chairs.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "While the reviewer waited the clerk checked the file."},
            choices=(
                "While the reviewer waited, the clerk checked the file.",
                "While the reviewer waited; the clerk checked the file.",
                "While, the reviewer waited, the clerk checked the file.",
                "While the reviewer waited the clerk, checked the file.",
            ),
            answer="While the reviewer waited, the clerk checked the file.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "Unless the director arrives the meeting will start."},
            choices=(
                "Unless the director arrives, the meeting will start.",
                "Unless the director arrives; the meeting will start.",
                "Unless, the director arrives, the meeting will start.",
                "Unless the director arrives the meeting, will start.",
            ),
            answer="Unless the director arrives, the meeting will start.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
        _scene(
            values={"original": "As soon as the bell rang the trainees sat down."},
            choices=(
                "As soon as the bell rang, the trainees sat down.",
                "As soon as the bell rang; the trainees sat down.",
                "As soon as, the bell rang, the trainees sat down.",
                "As soon as the bell rang the trainees, sat down.",
            ),
            answer="As soon as the bell rang, the trainees sat down.",
            explanation="The introductory dependent clause should be followed by a comma.",
            tags=("introductory-clause", "comma"),
        ),
    ]
    return _expand_family("introductory-dependent-clause-comma", scenes)


def _build_clause_joining_comma_conjunction() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"original": "The clerk filed the memo the supervisor signed it."},
            choices=(
                "The clerk filed the memo, and the supervisor signed it.",
                "The clerk filed the memo; the supervisor signed it.",
                "The clerk filed the memo, the supervisor signed it.",
                "The clerk filed the memo the supervisor signed it.",
            ),
            answer="The clerk filed the memo, and the supervisor signed it.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The report was late the manager apologized."},
            choices=(
                "The report was late, so the manager apologized.",
                "The report was late; the manager apologized.",
                "The report was late, the manager apologized.",
                "The report was late the manager apologized.",
            ),
            answer="The report was late, so the manager apologized.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The office was quiet the lights were off."},
            choices=(
                "The office was quiet, and the lights were off.",
                "The office was quiet; the lights were off.",
                "The office was quiet, the lights were off.",
                "The office was quiet the lights were off.",
            ),
            answer="The office was quiet, and the lights were off.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The forms were ready the assistant sorted them."},
            choices=(
                "The forms were ready, so the assistant sorted them.",
                "The forms were ready; the assistant sorted them.",
                "The forms were ready, the assistant sorted them.",
                "The forms were ready the assistant sorted them.",
            ),
            answer="The forms were ready, so the assistant sorted them.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The memo was clear the supervisor asked questions."},
            choices=(
                "The memo was clear, but the supervisor asked questions.",
                "The memo was clear; the supervisor asked questions.",
                "The memo was clear, the supervisor asked questions.",
                "The memo was clear the supervisor asked questions.",
            ),
            answer="The memo was clear, but the supervisor asked questions.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The team finished early the office closed soon after."},
            choices=(
                "The team finished early, yet the office closed soon after.",
                "The team finished early; the office closed soon after.",
                "The team finished early, the office closed soon after.",
                "The team finished early the office closed soon after.",
            ),
            answer="The team finished early, yet the office closed soon after.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The staff waited patiently the trainer arrived late."},
            choices=(
                "The staff waited patiently, and the trainer arrived late.",
                "The staff waited patiently; the trainer arrived late.",
                "The staff waited patiently, the trainer arrived late.",
                "The staff waited patiently the trainer arrived late.",
            ),
            answer="The staff waited patiently, and the trainer arrived late.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The branch reopened the visitors returned."},
            choices=(
                "The branch reopened, and the visitors returned.",
                "The branch reopened; the visitors returned.",
                "The branch reopened, the visitors returned.",
                "The branch reopened the visitors returned.",
            ),
            answer="The branch reopened, and the visitors returned.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The clerk checked the log the assistant copied the notes."},
            choices=(
                "The clerk checked the log, and the assistant copied the notes.",
                "The clerk checked the log; the assistant copied the notes.",
                "The clerk checked the log, the assistant copied the notes.",
                "The clerk checked the log the assistant copied the notes.",
            ),
            answer="The clerk checked the log, and the assistant copied the notes.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
        _scene(
            values={"original": "The office stayed open the manager handled the calls."},
            choices=(
                "The office stayed open, and the manager handled the calls.",
                "The office stayed open; the manager handled the calls.",
                "The office stayed open, the manager handled the calls.",
                "The office stayed open the manager handled the calls.",
            ),
            answer="The office stayed open, and the manager handled the calls.",
            explanation="Two independent clauses should be joined with a comma and coordinating conjunction.",
            tags=("coordination", "comma"),
        ),
    ]
    return _expand_family("clause-joining-comma-conjunction", scenes)


def _build_clause_joining_semicolon() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"original": "The memo was late the clerk apologized."},
            choices=(
                "The memo was late; the clerk apologized.",
                "The memo was late, and the clerk apologized.",
                "The memo was late, the clerk apologized.",
                "The memo was late the clerk apologized.",
            ),
            answer="The memo was late; the clerk apologized.",
            explanation="Two independent clauses may be linked with a semicolon.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The office was busy the staff kept working."},
            choices=(
                "The office was busy; therefore, the staff kept working.",
                "The office was busy, so the staff kept working.",
                "The office was busy, the staff kept working.",
                "The office was busy the staff kept working.",
            ),
            answer="The office was busy; therefore, the staff kept working.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The printer jammed the copies were delayed."},
            choices=(
                "The printer jammed; consequently, the copies were delayed.",
                "The printer jammed, so the copies were delayed.",
                "The printer jammed, the copies were delayed.",
                "The printer jammed the copies were delayed.",
            ),
            answer="The printer jammed; consequently, the copies were delayed.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The report was clear the director approved it."},
            choices=(
                "The report was clear; the director approved it.",
                "The report was clear, and the director approved it.",
                "The report was clear, the director approved it.",
                "The report was clear the director approved it.",
            ),
            answer="The report was clear; the director approved it.",
            explanation="Two independent clauses may be linked with a semicolon.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The team arrived early the doors were still locked."},
            choices=(
                "The team arrived early; however, the doors were still locked.",
                "The team arrived early, but the doors were still locked.",
                "The team arrived early, the doors were still locked.",
                "The team arrived early the doors were still locked.",
            ),
            answer="The team arrived early; however, the doors were still locked.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The forms were complete the assistant submitted them."},
            choices=(
                "The forms were complete; then, the assistant submitted them.",
                "The forms were complete, and the assistant submitted them.",
                "The forms were complete, the assistant submitted them.",
                "The forms were complete the assistant submitted them.",
            ),
            answer="The forms were complete; then, the assistant submitted them.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The clock struck noon the meeting ended."},
            choices=(
                "The clock struck noon; meanwhile, the meeting ended.",
                "The clock struck noon, and the meeting ended.",
                "The clock struck noon, the meeting ended.",
                "The clock struck noon the meeting ended.",
            ),
            answer="The clock struck noon; meanwhile, the meeting ended.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The files were sorted the branch closed for lunch."},
            choices=(
                "The files were sorted; afterward, the branch closed for lunch.",
                "The files were sorted, and the branch closed for lunch.",
                "The files were sorted, the branch closed for lunch.",
                "The files were sorted the branch closed for lunch.",
            ),
            answer="The files were sorted; afterward, the branch closed for lunch.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The supervisor answered the call the trainee took notes."},
            choices=(
                "The supervisor answered the call; meanwhile, the trainee took notes.",
                "The supervisor answered the call, and the trainee took notes.",
                "The supervisor answered the call, the trainee took notes.",
                "The supervisor answered the call the trainee took notes.",
            ),
            answer="The supervisor answered the call; meanwhile, the trainee took notes.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
        _scene(
            values={"original": "The room was quiet the lights were off."},
            choices=(
                "The room was quiet; nevertheless, the lights were off.",
                "The room was quiet, and the lights were off.",
                "The room was quiet, the lights were off.",
                "The room was quiet the lights were off.",
            ),
            answer="The room was quiet; nevertheless, the lights were off.",
            explanation="Two independent clauses may be linked with a semicolon and a conjunctive adverb.",
            tags=("coordination", "semicolon"),
        ),
    ]
    return _expand_family("clause-joining-semicolon", scenes)


def _build_dependent_clause_fragment_diagnosis() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"fragment": "Because the files were late."},
            choices=(
                "Because the files were late.",
                "The clerk apologized for the delay.",
                "The office closed on time.",
                "The report was filed.",
            ),
            answer="Because the files were late.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "When the office reopened."},
            choices=(
                "When the office reopened.",
                "The team returned to work.",
                "The manager signed the memo.",
                "The staff waited.",
            ),
            answer="When the office reopened.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "Although the report was long."},
            choices=(
                "Although the report was long.",
                "The report was long.",
                "The manager approved it.",
                "The clerk filed the forms.",
            ),
            answer="Although the report was long.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "If the supervisor approves."},
            choices=(
                "If the supervisor approves.",
                "The supervisor approved the memo.",
                "The memo was printed.",
                "The office closed early.",
            ),
            answer="If the supervisor approves.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "Since the printer jammed."},
            choices=(
                "Since the printer jammed.",
                "The copies were delayed.",
                "The staff fixed the machine.",
                "The office was busy.",
            ),
            answer="Since the printer jammed.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "After the meeting ended."},
            choices=(
                "After the meeting ended.",
                "The assistant sent the notice.",
                "The team left the room.",
                "The branch closed for lunch.",
            ),
            answer="After the meeting ended.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "While the team waited."},
            choices=(
                "While the team waited.",
                "The supervisor called the clerk.",
                "The file was ready.",
                "The lights were off.",
            ),
            answer="While the team waited.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "Before the forms were signed."},
            choices=(
                "Before the forms were signed.",
                "The office sent a reply.",
                "The trainer explained the rule.",
                "The clerk checked the file.",
            ),
            answer="Before the forms were signed.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "Unless the memo is revised."},
            choices=(
                "Unless the memo is revised.",
                "The memo was revised.",
                "The supervisor approved it.",
                "The staff waited.",
            ),
            answer="Unless the memo is revised.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "As soon as the clerk arrived."},
            choices=(
                "As soon as the clerk arrived.",
                "The team started the review.",
                "The branch reopened.",
                "The assistant filed the report.",
            ),
            answer="As soon as the clerk arrived.",
            explanation="It has a subject and a verb but cannot stand alone as a complete sentence.",
            tags=("fragment", "dependent-clause"),
        ),
    ]
    return _expand_family("dependent-clause-fragment-diagnosis", scenes)


def _build_run_on_diagnosis() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "The clerk filed the memo, the supervisor signed it."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="comma splice",
            explanation="The sentence joins two independent clauses with only a comma.",
            tags=("run-on", "comma-splice"),
        ),
        _scene(
            values={"sentence": "The clerk filed the memo the supervisor signed it."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="fused sentence",
            explanation="The sentence joins two independent clauses with no punctuation at all.",
            tags=("run-on", "fused-sentence"),
        ),
        _scene(
            values={"sentence": "The report was late, the manager apologized."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="comma splice",
            explanation="The sentence joins two independent clauses with only a comma.",
            tags=("run-on", "comma-splice"),
        ),
        _scene(
            values={"sentence": "The report was late the manager apologized."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="fused sentence",
            explanation="The sentence joins two independent clauses with no punctuation at all.",
            tags=("run-on", "fused-sentence"),
        ),
        _scene(
            values={"sentence": "The office opened early, the staff prepared the room."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="comma splice",
            explanation="The sentence joins two independent clauses with only a comma.",
            tags=("run-on", "comma-splice"),
        ),
        _scene(
            values={"sentence": "The office opened early the staff prepared the room."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="fused sentence",
            explanation="The sentence joins two independent clauses with no punctuation at all.",
            tags=("run-on", "fused-sentence"),
        ),
        _scene(
            values={"sentence": "The forms were ready, the assistant sorted them."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="comma splice",
            explanation="The sentence joins two independent clauses with only a comma.",
            tags=("run-on", "comma-splice"),
        ),
        _scene(
            values={"sentence": "The forms were ready the assistant sorted them."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="fused sentence",
            explanation="The sentence joins two independent clauses with no punctuation at all.",
            tags=("run-on", "fused-sentence"),
        ),
        _scene(
            values={"sentence": "The trainer finished the lesson, the students asked questions."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="comma splice",
            explanation="The sentence joins two independent clauses with only a comma.",
            tags=("run-on", "comma-splice"),
        ),
        _scene(
            values={"sentence": "The trainer finished the lesson the students asked questions."},
            choices=("comma splice", "fused sentence", "fragment", "correct sentence"),
            answer="fused sentence",
            explanation="The sentence joins two independent clauses with no punctuation at all.",
            tags=("run-on", "fused-sentence"),
        ),
    ]
    return _expand_family("run-on-diagnosis", scenes)


def _build_clause_repair_complete_sentence() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"fragment": "Because the files were late"},
            choices=(
                "Because the files were late, the clerk apologized.",
                "Because the files were late; the clerk apologized.",
                "Because the files were late the clerk apologized.",
                "Because the files were late, the clerk apologized",
            ),
            answer="Because the files were late, the clerk apologized.",
            explanation="The dependent clause needs a comma before the independent clause.",
            tags=("repair", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "The clerk filed the memo the supervisor signed it"},
            choices=(
                "The clerk filed the memo, and the supervisor signed it.",
                "The clerk filed the memo, the supervisor signed it.",
                "The clerk filed the memo the supervisor signed it.",
                "The clerk filed the memo; and the supervisor signed it.",
            ),
            answer="The clerk filed the memo, and the supervisor signed it.",
            explanation="Two independent clauses need a comma and coordinating conjunction.",
            tags=("repair", "run-on"),
        ),
        _scene(
            values={"fragment": "When the office reopened"},
            choices=(
                "When the office reopened, the staff filed the forms.",
                "When the office reopened; the staff filed the forms.",
                "When the office reopened the staff filed the forms.",
                "When the office reopened, the staff filed the forms",
            ),
            answer="When the office reopened, the staff filed the forms.",
            explanation="The dependent clause needs a comma before the independent clause.",
            tags=("repair", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "The memo was late the clerk apologized"},
            choices=(
                "The memo was late; the clerk apologized.",
                "The memo was late, the clerk apologized.",
                "The memo was late the clerk apologized.",
                "The memo was late; and the clerk apologized.",
            ),
            answer="The memo was late; the clerk apologized.",
            explanation="Two independent clauses can be linked with a semicolon.",
            tags=("repair", "semicolon"),
        ),
        _scene(
            values={"fragment": "Although the report was long"},
            choices=(
                "Although the report was long, the manager approved it.",
                "Although the report was long; the manager approved it.",
                "Although the report was long the manager approved it.",
                "Although the report was long, the manager approved it",
            ),
            answer="Although the report was long, the manager approved it.",
            explanation="The dependent clause needs a comma before the independent clause.",
            tags=("repair", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "The team reviewed the forms, the supervisor signed them"},
            choices=(
                "The team reviewed the forms, and the supervisor signed them.",
                "The team reviewed the forms; the supervisor signed them.",
                "The team reviewed the forms the supervisor signed them.",
                "The team reviewed the forms, the supervisor signed them.",
            ),
            answer="The team reviewed the forms, and the supervisor signed them.",
            explanation="Two independent clauses need a comma and coordinating conjunction.",
            tags=("repair", "run-on"),
        ),
        _scene(
            values={"fragment": "After the meeting ended"},
            choices=(
                "After the meeting ended, the assistant sent the notice.",
                "After the meeting ended; the assistant sent the notice.",
                "After the meeting ended the assistant sent the notice.",
                "After the meeting ended, the assistant sent the notice",
            ),
            answer="After the meeting ended, the assistant sent the notice.",
            explanation="The dependent clause needs a comma before the independent clause.",
            tags=("repair", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "The office was quiet the lights were off"},
            choices=(
                "The office was quiet; the lights were off.",
                "The office was quiet, the lights were off.",
                "The office was quiet the lights were off.",
                "The office was quiet; and the lights were off.",
            ),
            answer="The office was quiet; the lights were off.",
            explanation="Two independent clauses can be linked with a semicolon.",
            tags=("repair", "semicolon"),
        ),
        _scene(
            values={"fragment": "If the supervisor approves"},
            choices=(
                "If the supervisor approves, we will print the memo.",
                "If the supervisor approves; we will print the memo.",
                "If the supervisor approves we will print the memo.",
                "If the supervisor approves, we will print the memo",
            ),
            answer="If the supervisor approves, we will print the memo.",
            explanation="The dependent clause needs a comma before the independent clause.",
            tags=("repair", "dependent-clause"),
        ),
        _scene(
            values={"fragment": "Since the printer jammed"},
            choices=(
                "Since the printer jammed, the copies were delayed.",
                "Since the printer jammed; the copies were delayed.",
                "Since the printer jammed the copies were delayed.",
                "Since the printer jammed, the copies were delayed",
            ),
            answer="Since the printer jammed, the copies were delayed.",
            explanation="The dependent clause needs a comma before the independent clause.",
            tags=("repair", "dependent-clause"),
        ),
    ]
    return _expand_family("clause-repair-complete-sentence", scenes)


def _build_true_subject_clause_distractor() -> list[dict[str, object]]:
    scenes = [
        _scene(
            values={"sentence": "Although the stack of reports on the desk was missing, the clerk apologized."},
            choices=("clerk", "stack", "reports", "desk"),
            answer="clerk",
            explanation="The head noun clerk is the subject that controls the verb apologized.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "When the bundle of forms in the tray was incomplete, the manager waited."},
            choices=("manager", "bundle", "forms", "tray"),
            answer="manager",
            explanation="The head noun manager is the subject that controls the verb waited.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "Because the row of chairs near the wall was moved, the team noticed."},
            choices=("team", "row", "chairs", "wall"),
            answer="team",
            explanation="The head noun team is the subject that controls the verb noticed.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "After the list of requested documents from the client was checked, the office responded."},
            choices=("office", "list", "documents", "client"),
            answer="office",
            explanation="The head noun office is the subject that controls the verb responded.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "Since the packet of letters beside the printer was sealed, the supervisor signed."},
            choices=("supervisor", "packet", "letters", "printer"),
            answer="supervisor",
            explanation="The head noun supervisor is the subject that controls the verb signed.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "While the set of revised notes on the table was helpful, the reviewer kept reading."},
            choices=("reviewer", "set", "notes", "table"),
            answer="reviewer",
            explanation="The head noun reviewer is the subject that controls the verb kept reading.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "Before the series of checks before the meeting was finished, the trainer paused."},
            choices=("trainer", "series", "checks", "meeting"),
            answer="trainer",
            explanation="The head noun trainer is the subject that controls the verb paused.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "Unless the folder of invoices under the counter was found, the branch closed."},
            choices=("branch", "folder", "invoices", "counter"),
            answer="branch",
            explanation="The head noun branch is the subject that controls the verb closed.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "After the pile of files beside the printer was sorted, the assistant left."},
            choices=("assistant", "pile", "files", "printer"),
            answer="assistant",
            explanation="The head noun assistant is the subject that controls the verb left.",
            tags=("true-subject", "head-noun"),
        ),
        _scene(
            values={"sentence": "Because the schedule of meetings for the week was changed, the officer emailed everyone."},
            choices=("officer", "schedule", "meetings", "week"),
            answer="officer",
            explanation="The head noun officer is the subject that controls the verb emailed.",
            tags=("true-subject", "head-noun"),
        ),
    ]
    return _expand_family("true-subject-clause-distractor", scenes)


def _build_questions() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    family_builders = [
        _build_independent_clause_identification,
        _build_dependent_clause_identification,
        _build_sentence_type_classification,
        _build_clause_vs_phrase_classification,
        _build_noun_clause_identification,
        _build_adjective_clause_identification,
        _build_adverb_clause_identification,
        _build_relative_clause_repair,
        _build_introductory_dependent_clause_comma,
        _build_clause_joining_comma_conjunction,
        _build_clause_joining_semicolon,
        _build_dependent_clause_fragment_diagnosis,
        _build_run_on_diagnosis,
        _build_clause_repair_complete_sentence,
        _build_true_subject_clause_distractor,
    ]
    for builder in family_builders:
        questions.extend(builder())
    return questions



def _validate_questions(questions: list[dict[str, object]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, found {len(questions)}")

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
    OUTPUT_PATH.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


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


if __name__ == "__main__":
    raise SystemExit(main())
