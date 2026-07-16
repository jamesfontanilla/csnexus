"""Generate the Fragments and Run-ons question bank."""

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
    / "fragments-and-run-ons"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Fragments and Run-ons"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

BASE_FAMILIES = (
    "complete-sentence",
    "subjectless-fragment",
    "verbless-fragment",
    "dependent-clause-fragment",
    "phrase-fragment",
    "fused-run-on",
    "comma-splice",
    "fix-subjectless",
    "fix-verbless",
    "fix-dependent-clause",
    "fix-phrase-fragment",
    "split-period",
    "join-semicolon",
    "join-comma-conjunction",
    "join-subordinator",
)

DIAG_CONTEXTS = (
    "filing-desk set",
    "morning memo set",
    "branch update set",
    "training note set",
    "office reminder set",
    "report excerpt set",
    "noticeboard set",
    "shift log set",
    "supervisor memo set",
    "workplace bulletin set",
)

SUBJECTS = (
    "The clerk",
    "The supervisor",
    "The manager",
    "The officer",
    "The team",
    "The assistant",
    "The reviewer",
    "The trainer",
    "The branch",
    "The office",
)

VERBS = (
    "filed",
    "reviewed",
    "signed",
    "checked",
    "prepared",
    "posted",
    "updated",
    "sent",
    "organized",
    "delivered",
)

OBJECTS = (
    "the memo",
    "the report",
    "the forms",
    "the schedule",
    "the notice",
    "the packet",
    "the log",
    "the summary",
    "the files",
    "the announcement",
)

GERUNDS = (
    "Reviewing",
    "Checking",
    "Signing",
    "Preparing",
    "Posting",
    "Updating",
    "Sending",
    "Organizing",
    "Delivering",
    "Filing",
)

EVENTS = (
    "the briefing ended",
    "the meeting closed",
    "the audit finished",
    "the shift ended",
    "the workshop started",
    "the review began",
    "the call ended",
    "the deadline passed",
    "the training resumed",
    "the office reopened",
)

ADVERBIALS = (
    "before lunch",
    "after the briefing",
    "during the shift",
    "after the audit",
    "before the deadline",
    "at noon",
    "after the meeting",
    "during the review",
    "before the workshop",
    "after the call",
)

PLACES = (
    "front desk",
    "filing room",
    "branch office",
    "records shelf",
    "reception area",
    "counter",
    "training table",
    "supervisor's desk",
    "work station",
    "notice board",
)

SUBJECTLESS_SCENARIOS = (
    ("Reviewing the memo before lunch", "The clerk", "reviewed", "the memo", "before lunch"),
    ("Checking the report after the briefing", "The supervisor", "checked", "the report", "after the briefing"),
    ("Signing the forms during the shift", "The manager", "signed", "the forms", "during the shift"),
    ("Preparing the schedule after the audit", "The officer", "prepared", "the schedule", "after the audit"),
    ("Posting the notice before the deadline", "The team", "posted", "the notice", "before the deadline"),
    ("Updating the packet at noon", "The assistant", "updated", "the packet", "at noon"),
    ("Sending the log after the meeting", "The reviewer", "sent", "the log", "after the meeting"),
    ("Organizing the summary during the review", "The trainer", "organized", "the summary", "during the review"),
    ("Delivering the files before the workshop", "The branch", "delivered", "the files", "before the workshop"),
    ("Filing the announcement after the call", "The office", "filed", "the announcement", "after the call"),
)

SUBORDINATORS = (
    "Because",
    "After",
    "When",
    "Since",
    "Although",
    "While",
    "If",
    "Until",
    "Before",
    "As soon as",
)


PROMPT_PREFIXES: dict[str, dict[str, str]] = {
    "complete-sentence": {
        "Easy": "Which sentence is complete as written in the {context}",
        "Medium": "Which sentence can stand alone as a complete sentence in the {context}",
        "Hard": "Which sentence is neither a fragment nor a run-on in the {context}",
        "Ultra": "Which sentence is the only complete sentence in the {context}",
    },
    "subjectless-fragment": {
        "Easy": "Which sentence is a fragment because it lacks a subject in the {context}",
        "Medium": "Which sentence is the subjectless fragment in the {context}",
        "Hard": "Which sentence best shows a missing subject in the {context}",
        "Ultra": "Which sentence is the clear subjectless fragment in the {context}",
    },
    "verbless-fragment": {
        "Easy": "Which sentence is a fragment because it lacks a verb in the {context}",
        "Medium": "Which sentence is the verbless fragment in the {context}",
        "Hard": "Which sentence best shows a missing verb in the {context}",
        "Ultra": "Which sentence is the clear verbless fragment in the {context}",
    },
    "dependent-clause-fragment": {
        "Easy": "Which sentence is a fragment because it is only a dependent clause in the {context}",
        "Medium": "Which sentence is the dependent-clause fragment in the {context}",
        "Hard": "Which sentence best shows a dependent clause that cannot stand alone in the {context}",
        "Ultra": "Which sentence is the clear dependent-clause fragment in the {context}",
    },
    "phrase-fragment": {
        "Easy": "Which sentence is a fragment because it is only a phrase in the {context}",
        "Medium": "Which sentence is the phrase fragment in the {context}",
        "Hard": "Which sentence best shows a phrase that cannot stand alone in the {context}",
        "Ultra": "Which sentence is the clear phrase fragment in the {context}",
    },
    "fused-run-on": {
        "Easy": "Which sentence is a fused run-on in the {context}",
        "Medium": "Which sentence shows a fused run-on in the {context}",
        "Hard": "Which sentence best shows two clauses pushed together with no break in the {context}",
        "Ultra": "Which sentence is the clear fused run-on in the {context}",
    },
    "comma-splice": {
        "Easy": "Which sentence is a comma splice in the {context}",
        "Medium": "Which sentence shows a comma splice in the {context}",
        "Hard": "Which sentence best shows two complete clauses joined by only a comma in the {context}",
        "Ultra": "Which sentence is the clear comma splice in the {context}",
    },
    "fix-subjectless": {
        "Easy": "Which revision correctly adds the missing subject",
        "Medium": "Which revision best adds the missing subject",
        "Hard": "Which choice best repairs the subjectless fragment",
        "Ultra": "Which revision is most accurate for the subjectless fragment",
    },
    "fix-verbless": {
        "Easy": "Which revision correctly adds the missing verb",
        "Medium": "Which revision best adds the missing verb",
        "Hard": "Which choice best repairs the verbless fragment",
        "Ultra": "Which revision is most accurate for the verbless fragment",
    },
    "fix-dependent-clause": {
        "Easy": "Which revision correctly turns the dependent clause into one complete sentence",
        "Medium": "Which revision best turns the dependent clause into a complete sentence",
        "Hard": "Which choice best repairs the dependent-clause fragment",
        "Ultra": "Which revision is most accurate for the dependent-clause fragment",
    },
    "fix-phrase-fragment": {
        "Easy": "Which revision correctly turns the phrase fragment into a complete sentence",
        "Medium": "Which revision best turns the phrase fragment into a complete sentence",
        "Hard": "Which choice best repairs the phrase fragment",
        "Ultra": "Which revision is most accurate for the phrase fragment",
    },
    "split-period": {
        "Easy": "Which revision correctly splits the fused sentence into two sentences",
        "Medium": "Which revision best splits the fused sentence into two sentences",
        "Hard": "Which choice best fixes the fused sentence with two clear sentences",
        "Ultra": "Which revision is most accurate for separating the fused sentence",
    },
    "join-semicolon": {
        "Easy": "Which revision correctly joins the clauses with a semicolon",
        "Medium": "Which revision best joins the clauses with a semicolon",
        "Hard": "Which choice best fixes the sentence with a semicolon",
        "Ultra": "Which revision is most accurate for the semicolon join",
    },
    "join-comma-conjunction": {
        "Easy": "Which revision correctly joins the clauses with a comma and a coordinating conjunction",
        "Medium": "Which revision best joins the clauses with a comma and a coordinating conjunction",
        "Hard": "Which choice best fixes the sentence with a comma and conjunction",
        "Ultra": "Which revision is most accurate for the comma-and-conjunction join",
    },
    "join-subordinator": {
        "Easy": "Which revision correctly joins the ideas by making one clause dependent",
        "Medium": "Which revision best joins the ideas by making one clause dependent",
        "Hard": "Which choice best fixes the run-on with a subordinating conjunction",
        "Ultra": "Which revision is most accurate for the subordinated join",
    },
}


@dataclass(frozen=True)
class Frame:
    context: str
    choices: tuple[str, str, str, str]
    answer: str
    explanation: str
    tags: tuple[str, ...]


@dataclass(frozen=True)
class FamilySpec:
    base_family: str
    mode: str
    frames: tuple[Frame, ...]


def _lower(text: str) -> str:
    return text[:1].lower() + text[1:] if text else text


def _rotate_choices(choices: list[str], question_id: int, frame_index: int) -> list[str]:
    rotation = (question_id + frame_index) % len(choices)
    return choices[rotation:] + choices[:rotation]


def _question_text(base_family: str, difficulty: str, context: str, mode: str) -> str:
    prefix = PROMPT_PREFIXES[base_family][difficulty]
    if mode == "diagnose":
        return f"{prefix.format(context=context)}:"
    return f'{prefix}: "{context}"'


def _build_question(
    *,
    question_id: int,
    spec: FamilySpec,
    family_name: str,
    frame: Frame,
    frame_index: int,
    difficulty: str,
) -> dict:
    question = _question_text(spec.base_family, difficulty, frame.context, spec.mode)
    choices = _rotate_choices(list(frame.choices), question_id, frame_index)
    if frame.answer not in choices:
        raise ValueError(f"answer {frame.answer!r} missing from choices for {family_name}")

    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": frame.answer,
        "explanation": frame.explanation,
        "tags": [
            "fragments-and-run-ons",
            family_name,
            DIFFICULTY_TAGS[difficulty],
            spec.base_family,
            spec.mode,
            *frame.tags,
        ],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _complete_sentence_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        complete = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} {ADVERBIALS[i]}."
        fragment = f"After {EVENTS[i]}."
        dependent = f"Because { _lower(SUBJECTS[i]) } {VERBS[i]} {OBJECTS[i]}."
        fused = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(complete, fragment, dependent, fused),
                answer=complete,
                explanation="A complete sentence needs a subject, a finite verb, and a complete thought.",
                tags=("complete", "sentence-check"),
            )
        )
    return tuple(frames)


def _subjectless_fragment_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i, (fragment_text, subject, verb, object_text, adverbial) in enumerate(SUBJECTLESS_SCENARIOS):
        fragment = f"{fragment_text}."
        complete = f"{subject} {verb} {object_text} {adverbial}."
        dependent = f"Because {_lower(subject)} {verb} {object_text}."
        run_on = (
            f"{subject} {verb} {object_text}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(fragment, complete, dependent, run_on),
                answer=fragment,
                explanation="A subjectless fragment has a verb form but no subject to perform the action.",
                tags=("subjectless", "fragment"),
            )
        )
    return tuple(frames)


def _verbless_fragment_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        fragment = f"{SUBJECTS[i]} at the {PLACES[i]}."
        complete = f"{SUBJECTS[i]} was at the {PLACES[i]}."
        dependent = f"When {_lower(SUBJECTS[i])} was at the {PLACES[i]}."
        run_on = (
            f"{SUBJECTS[i]} was at the {PLACES[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(fragment, complete, dependent, run_on),
                answer=fragment,
                explanation="A verbless fragment has a subject but no finite verb.",
                tags=("verbless", "fragment"),
            )
        )
    return tuple(frames)


def _dependent_clause_fragment_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        fragment = f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}."
        complete = (
            f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        phrase = f"Because of {OBJECTS[i]}."
        run_on = (
            f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(fragment, complete, phrase, run_on),
                answer=fragment,
                explanation="A dependent clause fragment cannot stand alone as a sentence.",
                tags=("dependent-clause", "fragment"),
            )
        )
    return tuple(frames)


def _phrase_fragment_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        fragment = f"At the {PLACES[i]}."
        complete = f"{SUBJECTS[i]} waited at the {PLACES[i]}."
        dependent = f"While {_lower(SUBJECTS[i])} waited at the {PLACES[i]}."
        run_on = f"At the {PLACES[i]} {SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}."
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(fragment, complete, dependent, run_on),
                answer=fragment,
                explanation="A phrase has no main clause, so it cannot stand alone as a sentence.",
                tags=("phrase", "fragment"),
            )
        )
    return tuple(frames)


def _fused_run_on_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        fused = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        comma_splice = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        complete = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} {ADVERBIALS[i]}."
        fragment = f"After {EVENTS[i]}."
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(fused, comma_splice, complete, fragment),
                answer=fused,
                explanation="A fused run-on pushes two independent clauses together without punctuation.",
                tags=("fused", "run-on"),
            )
        )
    return tuple(frames)


def _comma_splice_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        comma_splice = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        fused = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        complete = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} {ADVERBIALS[i]}."
        fragment = f"After {EVENTS[i]}."
        frames.append(
            Frame(
                context=DIAG_CONTEXTS[i],
                choices=(comma_splice, fused, complete, fragment),
                answer=comma_splice,
                explanation="A comma splice joins two complete clauses with only a comma.",
                tags=("comma-splice", "run-on"),
            )
        )
    return tuple(frames)


def _fix_subjectless_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i, (fragment_text, subject, verb, object_text, adverbial) in enumerate(SUBJECTLESS_SCENARIOS):
        original = fragment_text
        correct = f"{subject} {verb} {object_text} {adverbial}."
        wrong1 = f"{fragment_text}, {_lower(subject)}."
        wrong2 = (
            f"{subject} {verb} {object_text}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        wrong3 = f"Because {verb} {object_text} {adverbial}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="Adding a clear subject turns the fragment into a complete sentence.",
                tags=("repair", "subjectless"),
            )
        )
    return tuple(frames)


def _fix_verbless_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = f"{SUBJECTS[i]} at the {PLACES[i]}"
        correct = f"{SUBJECTS[i]} was at the {PLACES[i]}."
        wrong1 = f"{SUBJECTS[i]} at the {PLACES[i]} was."
        wrong2 = f"At the {PLACES[i]}, {_lower(SUBJECTS[i])}."
        wrong3 = f"Because {_lower(SUBJECTS[i])} at the {PLACES[i]}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="Adding a finite verb completes the verbless fragment.",
                tags=("repair", "verbless"),
            )
        )
    return tuple(frames)


def _fix_dependent_clause_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}"
        correct = (
            f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        wrong1 = (
            f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        wrong2 = (
            f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}; "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        wrong3 = (
            f"Because {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}, and "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="The dependent clause needs a main clause to finish the thought.",
                tags=("repair", "dependent-clause"),
            )
        )
    return tuple(frames)


def _fix_phrase_fragment_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = f"At the {PLACES[i]}"
        correct = f"{SUBJECTS[i]} waited at the {PLACES[i]}."
        wrong1 = f"At the {PLACES[i]} waited {_lower(SUBJECTS[i])}."
        wrong2 = f"At the {PLACES[i]}, {_lower(SUBJECTS[i])} waited, and {_lower(SUBJECTS[(i + 1) % 10])}."
        wrong3 = f"{SUBJECTS[i]} at the {PLACES[i]}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A phrase fragment needs a full clause with a subject and verb.",
                tags=("repair", "phrase"),
            )
        )
    return tuple(frames)


def _split_period_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}"
        )
        correct = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}. {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong1 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}; {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong2 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, and {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong3 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A period can split the fused sentence into two complete sentences.",
                tags=("repair", "period"),
            )
        )
    return tuple(frames)


def _join_semicolon_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}"
        )
        correct = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}; {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong1 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}. {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong2 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, and {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong3 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A semicolon correctly joins two closely related independent clauses.",
                tags=("repair", "semicolon"),
            )
        )
    return tuple(frames)


def _join_comma_conjunction_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}"
        )
        correct = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, and {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong1 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}. {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong2 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}; {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong3 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A comma and coordinating conjunction correctly join the two independent clauses.",
                tags=("repair", "comma-conjunction"),
            )
        )
    return tuple(frames)


def _join_subordinator_frames() -> tuple[Frame, ...]:
    frames: list[Frame] = []
    for i in range(10):
        original = (
            f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]} "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}"
        )
        subordinator = SUBORDINATORS[i]
        correct = (
            f"{subordinator} {_lower(SUBJECTS[i])} {VERBS[i]} {OBJECTS[i]}, "
            f"{_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        )
        wrong1 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}. {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong2 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}; {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        wrong3 = f"{SUBJECTS[i]} {VERBS[i]} {OBJECTS[i]}, and {_lower(SUBJECTS[(i + 1) % 10])} {VERBS[(i + 1) % 10]} {OBJECTS[(i + 1) % 10]}."
        frames.append(
            Frame(
                context=original,
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A subordinating conjunction can make one clause dependent and eliminate the run-on.",
                tags=("repair", "subordinator"),
            )
        )
    return tuple(frames)


def _family_specs() -> tuple[FamilySpec, ...]:
    return (
        FamilySpec("complete-sentence", "diagnose", _complete_sentence_frames()),
        FamilySpec("subjectless-fragment", "diagnose", _subjectless_fragment_frames()),
        FamilySpec("verbless-fragment", "diagnose", _verbless_fragment_frames()),
        FamilySpec("dependent-clause-fragment", "diagnose", _dependent_clause_fragment_frames()),
        FamilySpec("phrase-fragment", "diagnose", _phrase_fragment_frames()),
        FamilySpec("fused-run-on", "diagnose", _fused_run_on_frames()),
        FamilySpec("comma-splice", "diagnose", _comma_splice_frames()),
        FamilySpec("fix-subjectless", "revise", _fix_subjectless_frames()),
        FamilySpec("fix-verbless", "revise", _fix_verbless_frames()),
        FamilySpec("fix-dependent-clause", "revise", _fix_dependent_clause_frames()),
        FamilySpec("fix-phrase-fragment", "revise", _fix_phrase_fragment_frames()),
        FamilySpec("split-period", "revise", _split_period_frames()),
        FamilySpec("join-semicolon", "revise", _join_semicolon_frames()),
        FamilySpec("join-comma-conjunction", "revise", _join_comma_conjunction_frames()),
        FamilySpec("join-subordinator", "revise", _join_subordinator_frames()),
    )


def _build_bank() -> list[dict]:
    questions: list[dict] = []
    question_id = 1
    for difficulty in DIFFICULTIES:
        for spec in _family_specs():
            family_name = f"{difficulty.lower()}-{spec.base_family}"
            for frame_index, frame in enumerate(spec.frames):
                questions.append(
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
    return questions


def _validate_bank(questions: list[dict]) -> None:
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
        f"{difficulty.lower()}-{family}": 10
        for difficulty in DIFFICULTIES
        for family in BASE_FAMILIES
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
