"""Generate the Verbal Ability / Sentence Structure / Phrases question bank."""

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
    / "phrases"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Phrases"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "phrases"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

FAMILY_ORDER = (
    "prepositional-phrase-identification",
    "prepositional-phrase-function",
    "noun-phrase-identification",
    "appositive-phrase-identification",
    "appositive-comma-check",
    "participial-phrase-identification",
    "participial-modifier-repair",
    "gerund-phrase-identification",
    "infinitive-phrase-identification",
    "absolute-phrase-identification",
    "phrase-vs-clause-classification",
    "introductory-phrase-comma",
    "phrase-fragment-diagnosis",
    "phrase-repair-complete-sentence",
    "true-subject-prepositional-distractor",
)

FAMILY_EXTRA_TAGS = {
    "prepositional-phrase-identification": "prepositional-phrase",
    "prepositional-phrase-function": "prepositional-function",
    "noun-phrase-identification": "noun-phrase",
    "appositive-phrase-identification": "appositive-phrase",
    "appositive-comma-check": "appositive-comma",
    "participial-phrase-identification": "participial-phrase",
    "participial-modifier-repair": "participial-repair",
    "gerund-phrase-identification": "gerund-phrase",
    "infinitive-phrase-identification": "infinitive-phrase",
    "absolute-phrase-identification": "absolute-phrase",
    "phrase-vs-clause-classification": "phrase-vs-clause",
    "introductory-phrase-comma": "intro-comma",
    "phrase-fragment-diagnosis": "fragment-diagnosis",
    "phrase-repair-complete-sentence": "fragment-repair",
    "true-subject-prepositional-distractor": "true-subject",
}


QUESTION_STEMS: dict[str, dict[str, str]] = {
    "prepositional-phrase-identification": {
        "Easy": 'Which option is the prepositional phrase that shows {focus} in "{sentence}"?',
        "Medium": 'In "{sentence}", which option is the prepositional phrase that shows {focus}?',
        "Hard": 'Which phrase in "{sentence}" is the prepositional phrase that shows {focus}?',
        "Ultra": 'Which choice names the prepositional phrase showing {focus} in "{sentence}"?',
    },
    "prepositional-phrase-function": {
        "Easy": 'What function does "{phrase}" serve in "{sentence}"?',
        "Medium": 'In "{sentence}", what function does "{phrase}" serve?',
        "Hard": 'Which role does "{phrase}" play in "{sentence}"?',
        "Ultra": 'In "{sentence}", which function best describes "{phrase}"?',
    },
    "noun-phrase-identification": {
        "Easy": 'Which option is the full noun phrase serving as the subject in "{sentence}"?',
        "Medium": 'In "{sentence}", which option names the full noun phrase acting as the subject?',
        "Hard": 'Which phrase in "{sentence}" is the subject noun phrase?',
        "Ultra": 'Which choice is the complete noun phrase that works as the subject in "{sentence}"?',
    },
    "appositive-phrase-identification": {
        "Easy": 'Which option is the appositive phrase in "{sentence}"?',
        "Medium": 'In "{sentence}", which phrase renames the noun before it?',
        "Hard": 'Which choice is the appositive phrase that adds extra information in "{sentence}"?',
        "Ultra": 'Which phrase in "{sentence}" is the nonessential appositive?',
    },
    "appositive-comma-check": {
        "Easy": 'Which revision correctly punctuates the nonessential appositive in "{original}"?',
        "Medium": 'Which sentence uses commas correctly around the appositive in "{original}"?',
        "Hard": 'Which choice correctly sets off the added appositive information in "{original}"?',
        "Ultra": 'Which revision is punctuated correctly for the appositive phrase in "{original}"?',
    },
    "participial-phrase-identification": {
        "Easy": 'Which option is the participial phrase in "{sentence}"?',
        "Medium": 'In "{sentence}", which phrase is the participial phrase?',
        "Hard": 'Which phrase in "{sentence}" begins with a participle and describes a noun?',
        "Ultra": 'Which choice is the participial phrase that modifies the subject in "{sentence}"?',
    },
    "participial-modifier-repair": {
        "Easy": 'Which revision correctly repairs the dangling participial phrase in "{original}"?',
        "Medium": 'Which sentence fixes the misplaced modifier in "{original}"?',
        "Hard": 'Which choice attaches the participial phrase to the right subject in "{original}"?',
        "Ultra": 'Which revision most cleanly corrects the dangling participial phrase in "{original}"?',
    },
    "gerund-phrase-identification": {
        "Easy": 'Which option is the gerund phrase in "{sentence}"?',
        "Medium": 'In "{sentence}", which phrase works as the gerund phrase?',
        "Hard": 'Which choice is the gerund phrase acting as a noun in "{sentence}"?',
        "Ultra": 'Which phrase in "{sentence}" is a gerund phrase rather than a clause?',
    },
    "infinitive-phrase-identification": {
        "Easy": 'Which option is the infinitive phrase in "{sentence}"?',
        "Medium": 'In "{sentence}", which phrase begins with to + base verb?',
        "Hard": 'Which choice is the infinitive phrase that functions as a noun, adjective, or adverb in "{sentence}"?',
        "Ultra": 'Which phrase in "{sentence}" is the infinitive phrase?',
    },
    "absolute-phrase-identification": {
        "Easy": 'Which option is the absolute phrase in "{sentence}"?',
        "Medium": 'In "{sentence}", which phrase is the absolute phrase?',
        "Hard": 'Which choice is the detached absolute phrase that adds background detail in "{sentence}"?',
        "Ultra": 'Which phrase in "{sentence}" is the absolute phrase made of a noun plus participle?',
    },
    "phrase-vs-clause-classification": {
        "Easy": 'Which option is a {target_label}, not a {contrast_label}, in the {set_name} set?',
        "Medium": 'In the {set_name} set, which option is a {target_label} and not a {contrast_label}?',
        "Hard": 'Which choice is a {target_label} rather than a {contrast_label} in the {set_name} set?',
        "Ultra": 'Which option matches the {target_label} classification in the {set_name} set?',
    },
    "introductory-phrase-comma": {
        "Easy": 'Which revision correctly adds the comma after the introductory phrase in "{original}"?',
        "Medium": 'Which sentence is punctuated correctly after the introductory phrase in "{original}"?',
        "Hard": 'Which choice correctly places the comma after the opening phrase in "{original}"?',
        "Ultra": 'Which revision correctly punctuates the introductory phrase in "{original}"?',
    },
    "phrase-fragment-diagnosis": {
        "Easy": 'Which sentence is only a phrase and cannot stand alone in the {set_name} set?',
        "Medium": 'In the {set_name} set, which sentence is only a phrase?',
        "Hard": 'Which option is the phrase fragment in the {set_name} set?',
        "Ultra": 'Which choice is not a complete sentence because it is only a phrase in the {set_name} set?',
    },
    "phrase-repair-complete-sentence": {
        "Easy": 'Which revision turns "{fragment}" into a complete sentence?',
        "Medium": 'Which sentence repairs the fragment "{fragment}"?',
        "Hard": 'Which choice most accurately turns "{fragment}" into a complete thought?',
        "Ultra": 'Which revision correctly fixes the phrase fragment "{fragment}"?',
    },
    "true-subject-prepositional-distractor": {
        "Easy": 'What is the true subject in "{sentence}" after you ignore the prepositional phrase?',
        "Medium": 'After crossing out the prepositional phrase, what is the subject of "{sentence}"?',
        "Hard": 'Which word is the true subject of "{sentence}"?',
        "Ultra": 'What noun actually controls the verb in "{sentence}"?',
    },
}


@dataclass(frozen=True)
class Frame:
    stems: dict[str, str]
    choices: tuple[str, str, str, str]
    answer: str
    explanation: str
    tags: tuple[str, ...]


def _lower_first(text: str) -> str:
    if not text:
        return text
    return text[:1].lower() + text[1:]


def _make_stems(family: str, **values: str) -> dict[str, str]:
    return {
        difficulty: template.format(**values)
        for difficulty, template in QUESTION_STEMS[family].items()
    }


def _rotate_choices(choices: list[str], question_id: int) -> list[str]:
    rotation = question_id % len(choices)
    return choices[rotation:] + choices[:rotation]


def _frame(
    family: str,
    *,
    choices: tuple[str, str, str, str],
    answer: str,
    explanation: str,
    tags: tuple[str, ...],
    **stem_values: str,
) -> Frame:
    return Frame(
        stems=_make_stems(family, **stem_values),
        choices=choices,
        answer=answer,
        explanation=explanation,
        tags=tags,
    )


def _build_prepositional_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "The clerk filed the forms in the cabinet before lunch.",
            "in the cabinet",
            "location",
            ("the forms", "filed the forms", "The clerk filed the forms"),
            ("prepositional", "location"),
        ),
        (
            "The supervisor shared updates with the team after the briefing.",
            "with the team",
            "companionship",
            ("the team", "shared updates", "The supervisor shared updates"),
            ("prepositional", "companionship"),
        ),
        (
            "The assistant pinned the notice on the board near the elevator.",
            "on the board",
            "location",
            ("the notice", "pinned the notice", "The assistant pinned the notice"),
            ("prepositional", "location"),
        ),
        (
            "The courier sent the package to the branch by noon.",
            "to the branch",
            "destination",
            ("the package", "sent the package", "The courier sent the package"),
            ("prepositional", "destination"),
        ),
        (
            "The archivist stored the file under the tray before closing.",
            "under the tray",
            "location",
            ("the file", "stored the file", "The archivist stored the file"),
            ("prepositional", "location"),
        ),
        (
            "The assistant placed the forms beside the printer after lunch.",
            "beside the printer",
            "location",
            ("the forms", "placed the forms", "The assistant placed the forms"),
            ("prepositional", "location"),
        ),
        (
            "The manager delivered the report to the branch on Monday.",
            "to the branch",
            "destination",
            ("the report", "delivered the report", "The manager delivered the report"),
            ("prepositional", "destination"),
        ),
        (
            "The team kept the receipts in the folder during the audit.",
            "in the folder",
            "location",
            ("the receipts", "kept the receipts", "The team kept the receipts"),
            ("prepositional", "location"),
        ),
        (
            "The porter carried the box across the hall before the meeting.",
            "across the hall",
            "path",
            ("the box", "carried the box", "The porter carried the box"),
            ("prepositional", "path"),
        ),
        (
            "The clerk returned the keys to the guard at dusk.",
            "to the guard",
            "destination",
            ("the keys", "returned the keys", "The clerk returned the keys"),
            ("prepositional", "destination"),
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, focus, distractors, extra_tags in scenes:
        frames.append(
            _frame(
                "prepositional-phrase-identification",
                choices=(answer, *distractors),
                answer=answer,
                explanation="It begins with a preposition and ends with its object, so it is a prepositional phrase.",
                tags=extra_tags,
                sentence=sentence,
                focus=focus,
            )
        )
    return tuple(frames)


def _build_prepositional_phrase_function() -> tuple[Frame, ...]:
    scenes = (
        (
            "The memo on the desk was revised.",
            "on the desk",
            "adjective phrase",
            ("adjective phrase", "adverb phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adjective"),
        ),
        (
            "The staff met after lunch.",
            "after lunch",
            "adverb phrase",
            ("adverb phrase", "adjective phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adverb"),
        ),
        (
            "The folder beside the printer held the receipts.",
            "beside the printer",
            "adjective phrase",
            ("adjective phrase", "adverb phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adjective"),
        ),
        (
            "The team gathered in the lobby.",
            "in the lobby",
            "adverb phrase",
            ("adverb phrase", "adjective phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adverb"),
        ),
        (
            "The notice from the branch manager was clear.",
            "from the branch manager",
            "adjective phrase",
            ("adjective phrase", "adverb phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adjective"),
        ),
        (
            "The courier arrived from the regional office.",
            "from the regional office",
            "adverb phrase",
            ("adverb phrase", "adjective phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adverb"),
        ),
        (
            "The key under the notebook opened the drawer.",
            "under the notebook",
            "adjective phrase",
            ("adjective phrase", "adverb phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adjective"),
        ),
        (
            "The inspectors waited at the front desk.",
            "at the front desk",
            "adverb phrase",
            ("adverb phrase", "adjective phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adverb"),
        ),
        (
            "The policy for the new shift was posted.",
            "for the new shift",
            "adjective phrase",
            ("adjective phrase", "adverb phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adjective"),
        ),
        (
            "The manager spoke with confidence.",
            "with confidence",
            "adverb phrase",
            ("adverb phrase", "adjective phrase", "noun phrase", "absolute phrase"),
            ("prepositional", "adverb"),
        ),
    )

    frames: list[Frame] = []
    for sentence, phrase, answer, choices, extra_tags in scenes:
        frames.append(
            _frame(
                "prepositional-phrase-function",
                choices=choices,
                answer=answer,
                explanation=f'The phrase "{phrase}" functions as an {answer} in the sentence.',
                tags=extra_tags,
                sentence=sentence,
                phrase=phrase,
            )
        )
    return tuple(frames)


def _build_noun_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "The newly approved work schedule delayed the meeting.",
            "The newly approved work schedule",
            "delayed the meeting",
            "at the branch office",
            "because the schedule changed",
        ),
        (
            "The records officer at the front desk answered the call.",
            "The records officer at the front desk",
            "answered the call",
            "at the front desk",
            "because the call rang again",
        ),
        (
            "The blue folder with the missing forms sat on the counter.",
            "The blue folder with the missing forms",
            "sat on the counter",
            "on the counter",
            "because the folder was blue",
        ),
        (
            "The revised safety memo reached the staff.",
            "The revised safety memo",
            "reached the staff",
            "to the staff",
            "because the memo was revised",
        ),
        (
            "The senior auditor from Manila reviewed the report.",
            "The senior auditor from Manila",
            "reviewed the report",
            "from Manila",
            "because the report needed review",
        ),
        (
            "The long line outside the office moved slowly.",
            "The long line outside the office",
            "moved slowly",
            "outside the office",
            "because the line was long",
        ),
        (
            "The new filing system for the branch saved time.",
            "The new filing system for the branch",
            "saved time",
            "for the branch",
            "because time was saved",
        ),
        (
            "The polite request for an extension surprised the manager.",
            "The polite request for an extension",
            "surprised the manager",
            "for an extension",
            "because the request was polite",
        ),
        (
            "The stack of printed notices near the door disappeared.",
            "The stack of printed notices near the door",
            "disappeared",
            "near the door",
            "because the notices were printed",
        ),
        (
            "The written explanation from the trainee helped the team.",
            "The written explanation from the trainee",
            "helped the team",
            "from the trainee",
            "because the trainee explained it",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, verb_phrase, prep_phrase, clause in scenes:
        frames.append(
            _frame(
                "noun-phrase-identification",
                choices=(answer, verb_phrase, prep_phrase, clause),
                answer=answer,
                explanation="It names the subject and includes its modifiers, so it is a noun phrase.",
                tags=("noun-phrase", "subject"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _build_appositive_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "Maya, the branch coordinator, approved the memo.",
            "the branch coordinator",
            "approved the memo",
            "the memo",
            "in the branch office",
        ),
        (
            "Mr. Santos, the senior auditor, reviewed the folder.",
            "the senior auditor",
            "reviewed the folder",
            "the folder",
            "at the desk",
        ),
        (
            "Aisha, our training officer, explained the schedule.",
            "our training officer",
            "explained the schedule",
            "the schedule",
            "during the briefing",
        ),
        (
            "Daniel, the lead clerk, sorted the files.",
            "the lead clerk",
            "sorted the files",
            "the files",
            "in the filing room",
        ),
        (
            "Mrs. Cruz, the records supervisor, checked the log.",
            "the records supervisor",
            "checked the log",
            "the log",
            "after the audit",
        ),
        (
            "Rafael, the assistant cashier, counted the receipts.",
            "the assistant cashier",
            "counted the receipts",
            "the receipts",
            "at the counter",
        ),
        (
            "Leah, the new team leader, opened the meeting.",
            "the new team leader",
            "opened the meeting",
            "the meeting",
            "before lunch",
        ),
        (
            "Nina, the compliance specialist, signed the notice.",
            "the compliance specialist",
            "signed the notice",
            "the notice",
            "for the policy",
        ),
        (
            "Omar, the senior inspector, closed the case.",
            "the senior inspector",
            "closed the case",
            "the case",
            "by noon",
        ),
        (
            "Paula, the office manager, answered the questions.",
            "the office manager",
            "answered the questions",
            "the questions",
            "after the session",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, clause, object_phrase, prep_phrase in scenes:
        frames.append(
            _frame(
                "appositive-phrase-identification",
                choices=(answer, clause, object_phrase, prep_phrase),
                answer=answer,
                explanation="The phrase renames the noun just before it, so it is an appositive.",
                tags=("appositive", "identification"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _build_appositive_comma_check() -> tuple[Frame, ...]:
    scenes = (
        ("Maya", "the branch coordinator", "approved", "the memo"),
        ("Mr. Santos", "the senior auditor", "reviewed", "the folder"),
        ("Aisha", "our training officer", "explained", "the schedule"),
        ("Daniel", "the lead clerk", "sorted", "the files"),
        ("Mrs. Cruz", "the records supervisor", "checked", "the log"),
        ("Rafael", "the assistant cashier", "counted", "the receipts"),
        ("Leah", "the new team leader", "opened", "the meeting"),
        ("Nina", "the compliance specialist", "signed", "the notice"),
        ("Omar", "the senior inspector", "closed", "the case"),
        ("Paula", "the office manager", "answered", "the questions"),
    )

    frames: list[Frame] = []
    for name, appositive, verb, obj in scenes:
        original = f"{name} {appositive} {verb} {obj}."
        correct = f"{name}, {appositive}, {verb} {obj}."
        wrong1 = f"{name}, {appositive} {verb} {obj}."
        wrong2 = f"{name} {appositive}, {verb} {obj}."
        wrong3 = f"{name} {appositive} {verb} {obj}."
        frames.append(
            _frame(
                "appositive-comma-check",
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A nonessential appositive adds extra information and should be set off with commas.",
                tags=("appositive", "comma"),
                original=original,
            )
        )
    return tuple(frames)


def _build_participial_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "Smiling at the visitors, the clerk opened the door.",
            "Smiling at the visitors",
            "the clerk opened the door",
            "at the visitors",
            "the clerk",
        ),
        (
            "Hidden behind the desk, the key escaped notice.",
            "Hidden behind the desk",
            "the key escaped notice",
            "behind the desk",
            "the key",
        ),
        (
            "Carrying the heavy box, the assistant paused at the elevator.",
            "Carrying the heavy box",
            "the assistant paused at the elevator",
            "at the elevator",
            "the assistant",
        ),
        (
            "Reviewed by the manager, the memo was returned to the team.",
            "Reviewed by the manager",
            "the memo was returned to the team",
            "to the team",
            "the memo",
        ),
        (
            "Tucked inside the folder, the note stayed safe.",
            "Tucked inside the folder",
            "the note stayed safe",
            "inside the folder",
            "the note",
        ),
        (
            "Arriving early, the inspectors prepared the room.",
            "Arriving early",
            "the inspectors prepared the room",
            "the room",
            "the inspectors",
        ),
        (
            "Supported by new evidence, the claim was accepted.",
            "Supported by new evidence",
            "the claim was accepted",
            "by new evidence",
            "the claim",
        ),
        (
            "Holding the schedule, the coordinator answered the phone.",
            "Holding the schedule",
            "the coordinator answered the phone",
            "the phone",
            "the coordinator",
        ),
        (
            "Printed before noon, the notices were posted on the board.",
            "Printed before noon",
            "the notices were posted on the board",
            "on the board",
            "the notices",
        ),
        (
            "Frustrated by delays, the staff asked for help.",
            "Frustrated by delays",
            "the staff asked for help",
            "for help",
            "the staff",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, clause, prep_phrase, noun_phrase in scenes:
        frames.append(
            _frame(
                "participial-phrase-identification",
                choices=(answer, clause, prep_phrase, noun_phrase),
                answer=answer,
                explanation="The phrase begins with a participle and modifies the noun that follows or is understood as its subject.",
                tags=("participial", "identification"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _build_participial_modifier_repair() -> tuple[Frame, ...]:
    scenes = (
        ("Walking to the office", "the clerk", "slipped on the wet pavement", "the rain"),
        ("Checking the ledger", "the manager", "found a missing total", "the numbers"),
        ("Reading the memo", "the supervisor", "spotted the error", "the memo"),
        ("Carrying the files", "the assistant", "kept the stack steady", "the box"),
        ("Opening the envelope", "the auditor", "found a signed receipt", "the letter"),
        ("Looking at the screen", "the reviewer", "noticed the typo", "the report"),
        ("Listening to the announcement", "the staff", "heard the schedule change", "the loudspeaker"),
        ("Waiting at the counter", "the customer", "received a token", "the counter"),
        ("Using the checklist", "the inspector", "finished early", "the checklist"),
        ("Following the instructions", "the trainee", "completed the form correctly", "the instructions"),
    )

    frames: list[Frame] = []
    for phrase, subject, revision_tail, wrong_subject in scenes:
        original = f"{phrase}, {wrong_subject} {revision_tail}."
        correct = f"{phrase}, {subject} {revision_tail}."
        wrong1 = f"{phrase} {subject} {revision_tail}."
        wrong2 = f"{subject} {revision_tail}, {phrase.lower()}."
        wrong3 = f"{phrase}. {subject.capitalize()} {revision_tail}."
        frames.append(
            _frame(
                "participial-modifier-repair",
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="The participial phrase must modify the noun that performs the action, so the subject has to match the phrase.",
                tags=("participial", "repair"),
                original=original,
            )
        )
    return tuple(frames)


def _build_gerund_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "Reviewing the memo carefully helped the team avoid errors.",
            "Reviewing the memo carefully",
            "to review the memo carefully",
            "during the review",
            "The team avoided errors",
        ),
        (
            "Submitting the forms early pleased the supervisor.",
            "Submitting the forms early",
            "to submit the forms early",
            "before the deadline",
            "The supervisor pleased the forms",
        ),
        (
            "Keeping accurate records saves time.",
            "Keeping accurate records",
            "to keep accurate records",
            "with accurate records",
            "Records save time",
        ),
        (
            "Checking the figures twice reduced mistakes.",
            "Checking the figures twice",
            "to check the figures twice",
            "after the check",
            "The figures reduced mistakes",
        ),
        (
            "Sending the report before noon earned praise.",
            "Sending the report before noon",
            "to send the report before noon",
            "before noon",
            "The report earned praise",
        ),
        (
            "Following the checklist prevented delays.",
            "Following the checklist",
            "to follow the checklist",
            "through the checklist",
            "The checklist prevented delays",
        ),
        (
            "Answering the phone during lunch distracted the clerk.",
            "Answering the phone during lunch",
            "to answer the phone during lunch",
            "during lunch",
            "The phone distracted the clerk",
        ),
        (
            "Updating the log at once was required.",
            "Updating the log at once",
            "to update the log at once",
            "at once",
            "The log was required",
        ),
        (
            "Meeting the deadline took patience.",
            "Meeting the deadline",
            "to meet the deadline",
            "before the deadline",
            "The deadline took patience",
        ),
        (
            "Using the new format simplified filing.",
            "Using the new format",
            "to use the new format",
            "with the new format",
            "The new format simplified filing",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, infinitive_phrase, prep_phrase, clause in scenes:
        frames.append(
            _frame(
                "gerund-phrase-identification",
                choices=(answer, infinitive_phrase, prep_phrase, clause),
                answer=answer,
                explanation="The -ing phrase acts as a noun here, so it is a gerund phrase.",
                tags=("gerund", "identification"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _build_infinitive_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "The team decided to finish the report before noon.",
            "to finish the report before noon",
            "The team decided",
            "before noon",
            "finishing the report",
        ),
        (
            "The office wanted to reduce waiting time.",
            "to reduce waiting time",
            "The office wanted",
            "waiting time",
            "reducing waiting time",
        ),
        (
            "The clerk tried to locate the missing file.",
            "to locate the missing file",
            "The clerk tried",
            "the missing file",
            "locating the file",
        ),
        (
            "The manager planned to meet the interns.",
            "to meet the interns",
            "The manager planned",
            "the interns",
            "meeting the interns",
        ),
        (
            "The trainers began to explain the new policy.",
            "to explain the new policy",
            "The trainers began",
            "the new policy",
            "explaining the policy",
        ),
        (
            "The staff hoped to avoid the delay.",
            "to avoid the delay",
            "The staff hoped",
            "the delay",
            "avoiding the delay",
        ),
        (
            "The auditor needed to verify the totals.",
            "to verify the totals",
            "The auditor needed",
            "the totals",
            "verifying the totals",
        ),
        (
            "The team agreed to revise the notice.",
            "to revise the notice",
            "The team agreed",
            "the notice",
            "revising the notice",
        ),
        (
            "The assistant learned to use the archive system.",
            "to use the archive system",
            "The assistant learned",
            "the archive system",
            "using the archive system",
        ),
        (
            "The branch aimed to open earlier.",
            "to open earlier",
            "The branch aimed",
            "earlier",
            "opening earlier",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, clause, prep_phrase, gerund_phrase in scenes:
        frames.append(
            _frame(
                "infinitive-phrase-identification",
                choices=(answer, clause, prep_phrase, gerund_phrase),
                answer=answer,
                explanation="The phrase begins with to + base verb, so it is an infinitive phrase.",
                tags=("infinitive", "identification"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _build_absolute_phrase_identification() -> tuple[Frame, ...]:
    scenes = (
        (
            "Her hands folded, the director listened in silence.",
            "Her hands folded",
            "the director listened in silence",
            "in silence",
            "the director",
        ),
        (
            "The schedules arranged by color, the clerk filed them quickly.",
            "The schedules arranged by color",
            "the clerk filed them quickly",
            "quickly",
            "the clerk",
        ),
        (
            "Their voices lowered, the reviewers continued the meeting.",
            "Their voices lowered",
            "the reviewers continued the meeting",
            "the meeting",
            "the reviewers",
        ),
        (
            "The forms stacked neatly, the assistant closed the drawer.",
            "The forms stacked neatly",
            "the assistant closed the drawer",
            "the drawer",
            "the assistant",
        ),
        (
            "His work complete, the officer clocked out.",
            "His work complete",
            "the officer clocked out",
            "out",
            "the officer",
        ),
        (
            "The agenda finalized, the committee adjourned.",
            "The agenda finalized",
            "the committee adjourned",
            "the committee",
            "adjourned",
        ),
        (
            "The printer silent, the office felt calm.",
            "The printer silent",
            "the office felt calm",
            "calm",
            "the office",
        ),
        (
            "The notes spread across the table, the team compared answers.",
            "The notes spread across the table",
            "the team compared answers",
            "across the table",
            "the team",
        ),
        (
            "Their bags packed, the trainees waited in the lobby.",
            "Their bags packed",
            "the trainees waited in the lobby",
            "in the lobby",
            "the trainees",
        ),
        (
            "The checklist ready, the inspector started the round.",
            "The checklist ready",
            "the inspector started the round",
            "the round",
            "the inspector",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, clause, prep_phrase, noun_phrase in scenes:
        frames.append(
            _frame(
                "absolute-phrase-identification",
                choices=(answer, clause, prep_phrase, noun_phrase),
                answer=answer,
                explanation="The phrase has a noun plus a participle or adjective, so it is an absolute phrase.",
                tags=("absolute", "identification"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _build_phrase_vs_clause_classification() -> tuple[Frame, ...]:
    scenes = (
        ("memo", "phrase", "under the new policy", "because the schedule changed", "when the office reopened", "after the report was filed"),
        ("records", "clause", "because the schedule changed", "under the new policy", "in the filing room", "after the meeting"),
        ("audit", "phrase", "after the briefing", "because the audit ended", "when the inspector arrived", "the staff filed out"),
        ("schedule", "clause", "since the office reopened", "before lunch", "on the desk", "in the new schedule"),
        ("branch", "phrase", "in the records room", "after the forms were checked", "because the clerk left", "to the branch"),
        ("mail", "clause", "while the courier waited", "during the delivery", "with the package", "near the mail bin"),
        ("meeting", "phrase", "across the hall", "because the meeting ended", "when the team arrived", "inside the branch office"),
        ("reception", "clause", "after the supervisor signed", "before the counter", "at the front desk", "near the elevator"),
        ("training", "phrase", "for the new shift", "because the trainer arrived", "while the staff watched", "after the session"),
        ("policy", "clause", "if the policy changes", "with the forms ready", "under the old rule", "during the audit"),
    )

    frames: list[Frame] = []
    for set_name, target_label, answer, c1, c2, c3 in scenes:
        if target_label == "phrase":
            choices = (answer, c1, c2, c3)
            explanation = "The correct option has no subject plus finite verb, so it is only a phrase."
            contrast_label = "clause"
            tags = ("phrase-vs-clause", "phrase")
        else:
            choices = (answer, c1, c2, c3)
            explanation = "The correct option has a subject and a finite verb, so it is a clause."
            contrast_label = "phrase"
            tags = ("phrase-vs-clause", "clause")

        frames.append(
            _frame(
                "phrase-vs-clause-classification",
                choices=choices,
                answer=answer,
                explanation=explanation,
                tags=tags,
                set_name=set_name,
                target_label=target_label,
                contrast_label=contrast_label,
            )
        )
    return tuple(frames)


def _build_introductory_phrase_comma() -> tuple[Frame, ...]:
    scenes = (
        ("After the briefing", "the staff", "filed", "out"),
        ("Before lunch", "the clerk", "checked", "the forms"),
        ("In the records room", "the assistant", "sorted", "files"),
        ("To save time", "the manager", "used", "a checklist"),
        ("Working without a break", "the reviewers", "finished", "on time"),
        ("Hoping to avoid delays", "the team", "arrived", "early"),
        ("With the notes ready", "the presenter", "began", "the talk"),
        ("Once the meeting ended", "the officers", "left", "the hall"),
        ("Although tired", "the clerk", "kept", "typing"),
        ("After checking the log", "the auditor", "signed", "the report"),
    )

    frames: list[Frame] = []
    for intro, subject, verb, obj in scenes:
        original = f"{intro} {subject} {verb} {obj}."
        correct = f"{intro}, {subject} {verb} {obj}."
        wrong1 = f"{intro} {subject}, {verb} {obj}."
        wrong2 = f"{intro}; {subject} {verb} {obj}."
        wrong3 = f"{intro}, {subject} {verb}, {obj}."
        frames.append(
            _frame(
                "introductory-phrase-comma",
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="An introductory phrase at the start is usually followed by a comma when it opens the sentence.",
                tags=("introductory", "comma"),
                original=original,
            )
        )
    return tuple(frames)


def _build_phrase_fragment_diagnosis() -> tuple[Frame, ...]:
    scenes = (
        (
            "filing",
            "Near the records shelf.",
            "The files sat near the records shelf.",
            "The clerk sorted the files near the records shelf.",
            "The records shelf held the files.",
        ),
        (
            "briefing",
            "After the briefing.",
            "The staff filed out after the briefing.",
            "The staff filed out before lunch.",
            "The briefing ended at noon.",
        ),
        (
            "deadline",
            "To finish the report on time.",
            "The team stayed late to finish the report on time.",
            "The report was finished on time.",
            "The team finished the report before noon.",
        ),
        (
            "visitor",
            "Smiling at the visitors.",
            "The clerk smiled at the visitors as she opened the door.",
            "The clerk greeted the visitors warmly.",
            "The visitors smiled back.",
        ),
        (
            "manager",
            "The new branch manager.",
            "The new branch manager approved the memo.",
            "The manager approved the memo.",
            "The branch opened on Monday.",
        ),
        (
            "policy",
            "With the forms ready.",
            "The assistant waited with the forms ready.",
            "The forms were ready by noon.",
            "The assistant prepared the forms.",
        ),
        (
            "audit",
            "Reviewed by the auditor.",
            "The report was reviewed by the auditor.",
            "The auditor reviewed the report.",
            "The report needed review.",
        ),
        (
            "hall",
            "Across the hall.",
            "The offices were across the hall.",
            "The team moved across the hall.",
            "The hall was across the office.",
        ),
        (
            "records",
            "For the office records.",
            "The file box was for the office records.",
            "The office kept the records.",
            "The records were filed yesterday.",
        ),
        (
            "meeting",
            "Before the meeting.",
            "The staff arrived before the meeting.",
            "The meeting began at noon.",
            "The staff met after lunch.",
        ),
    )

    frames: list[Frame] = []
    for set_name, fragment, complete1, complete2, complete3 in scenes:
        frames.append(
            _frame(
                "phrase-fragment-diagnosis",
                choices=(fragment, complete1, complete2, complete3),
                answer=fragment,
                explanation="It is only a phrase, so it cannot stand alone as a complete sentence.",
                tags=("fragment", "diagnosis"),
                set_name=set_name,
            )
        )
    return tuple(frames)


def _build_phrase_repair_complete_sentence() -> tuple[Frame, ...]:
    scenes = (
        (
            "Near the records shelf",
            "The files were stored near the records shelf.",
            "Near the records shelf, the files.",
            "The files near the records shelf were.",
            "Near the records shelf the files stored.",
        ),
        (
            "After the briefing",
            "The staff filed out after the briefing.",
            "After the briefing, the staff.",
            "The briefing after the staff filed out.",
            "The staff filed out, after the briefing.",
        ),
        (
            "To finish the report on time",
            "The team stayed late to finish the report on time.",
            "To finish the report on time, the team.",
            "The team to finish the report on time stayed late.",
            "The report on time to finish the team stayed late.",
        ),
        (
            "Smiling at the visitors",
            "Smiling at the visitors, the clerk opened the door.",
            "Smiling at the visitors the clerk opened the door.",
            "The clerk opened the door smiling at the visitors.",
            "Smiling at the visitors, opened the door the clerk.",
        ),
        (
            "The new branch manager",
            "The new branch manager approved the memo.",
            "The new branch manager.",
            "Approved the memo the new branch manager.",
            "The new branch manager, approved the memo.",
        ),
        (
            "With the forms ready",
            "With the forms ready, the assistant waited quietly.",
            "With the forms ready the assistant waited quietly.",
            "The assistant waited quietly with the forms ready.",
            "With the forms ready, waited quietly the assistant.",
        ),
        (
            "Reviewed by the auditor",
            "Reviewed by the auditor, the report was filed.",
            "Reviewed by the auditor the report was filed.",
            "The report was filed reviewed by the auditor.",
            "The report, reviewed by the auditor, was filed.",
        ),
        (
            "Across the hall",
            "The offices were across the hall.",
            "Across the hall the offices were.",
            "The offices across the hall were.",
            "Across the hall, were the offices.",
        ),
        (
            "For the office records",
            "The file box was kept for the office records.",
            "For the office records the file box was kept.",
            "The file box for the office records kept.",
            "The file box was, for the office records, kept.",
        ),
        (
            "Before the meeting",
            "The staff arrived before the meeting.",
            "Before the meeting the staff arrived.",
            "The meeting before the staff arrived.",
            "Before the meeting, arrived the staff.",
        ),
    )

    frames: list[Frame] = []
    for fragment, correct, wrong1, wrong2, wrong3 in scenes:
        frames.append(
            _frame(
                "phrase-repair-complete-sentence",
                choices=(correct, wrong1, wrong2, wrong3),
                answer=correct,
                explanation="A complete sentence needs a subject and a finite verb, so the phrase must be expanded into a full clause.",
                tags=("fragment", "repair"),
                fragment=fragment,
            )
        )
    return tuple(frames)


def _build_true_subject_prepositional_distractor() -> tuple[Frame, ...]:
    scenes = (
        (
            "The stack of reports on the desk was missing.",
            "stack",
            "reports",
            "desk",
            "was",
        ),
        (
            "The bundle of forms in the tray was signed.",
            "bundle",
            "forms",
            "tray",
            "was",
        ),
        (
            "The row of chairs near the wall was empty.",
            "row",
            "chairs",
            "wall",
            "was",
        ),
        (
            "The list of requested documents from the client was incomplete.",
            "list",
            "documents",
            "client",
            "was",
        ),
        (
            "The group of applicants at the door was waiting.",
            "group",
            "applicants",
            "door",
            "was",
        ),
        (
            "The box of invoices under the counter was lost.",
            "box",
            "invoices",
            "counter",
            "was",
        ),
        (
            "The set of revised notes on the table was helpful.",
            "set",
            "notes",
            "table",
            "was",
        ),
        (
            "The series of checks before the meeting was thorough.",
            "series",
            "checks",
            "meeting",
            "was",
        ),
        (
            "The packet of letters from the office was sealed.",
            "packet",
            "letters",
            "office",
            "was",
        ),
        (
            "The pile of files beside the printer was tall.",
            "pile",
            "files",
            "printer",
            "was",
        ),
    )

    frames: list[Frame] = []
    for sentence, answer, distractor1, distractor2, distractor3 in scenes:
        frames.append(
            _frame(
                "true-subject-prepositional-distractor",
                choices=(answer, distractor1, distractor2, distractor3),
                answer=answer,
                explanation="Cross out the prepositional phrase and keep the main noun that controls the verb.",
                tags=("subject", "prepositional-distractor"),
                sentence=sentence,
            )
        )
    return tuple(frames)


def _family_specs() -> tuple[tuple[str, callable], ...]:
    return (
        ("prepositional-phrase-identification", _build_prepositional_phrase_identification),
        ("prepositional-phrase-function", _build_prepositional_phrase_function),
        ("noun-phrase-identification", _build_noun_phrase_identification),
        ("appositive-phrase-identification", _build_appositive_phrase_identification),
        ("appositive-comma-check", _build_appositive_comma_check),
        ("participial-phrase-identification", _build_participial_phrase_identification),
        ("participial-modifier-repair", _build_participial_modifier_repair),
        ("gerund-phrase-identification", _build_gerund_phrase_identification),
        ("infinitive-phrase-identification", _build_infinitive_phrase_identification),
        ("absolute-phrase-identification", _build_absolute_phrase_identification),
        ("phrase-vs-clause-classification", _build_phrase_vs_clause_classification),
        ("introductory-phrase-comma", _build_introductory_phrase_comma),
        ("phrase-fragment-diagnosis", _build_phrase_fragment_diagnosis),
        ("phrase-repair-complete-sentence", _build_phrase_repair_complete_sentence),
        ("true-subject-prepositional-distractor", _build_true_subject_prepositional_distractor),
    )


def _build_bank() -> list[dict[str, object]]:
    questions: list[dict[str, object]] = []
    question_id = 1

    for difficulty in DIFFICULTIES:
        for family, builder in _family_specs():
            frames = builder()
            if len(frames) != 10:
                raise ValueError(f"family {family} must generate 10 frames, got {len(frames)}")
            for frame in frames:
                question_text = frame.stems[difficulty]
                rotated_choices = _rotate_choices(list(frame.choices), question_id)
                if frame.answer not in rotated_choices:
                    raise ValueError(f"answer {frame.answer!r} missing from choices for id {question_id}")
                questions.append(
                    {
                        "id": question_id,
                        "subtest": SUBTEST,
                        "module": MODULE,
                        "subtopic": SUBTOPIC,
                        "difficulty": difficulty,
                        "question": question_text,
                        "choices": rotated_choices,
                        "answer": frame.answer,
                        "explanation": frame.explanation,
                        "tags": [
                            ROOT_TAG,
                            family,
                            DIFFICULTY_TAGS[difficulty],
                            FAMILY_EXTRA_TAGS[family],
                            *frame.tags,
                        ],
                        "category": CATEGORY,
                        "language": LANGUAGE,
                    }
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

    family_counts = Counter(str(question["tags"][1]) for question in questions)  # type: ignore[index]
    expected_family_counts = {family: 40 for family in FAMILY_ORDER}
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


def _write_bank(questions: list[dict[str, object]]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(questions)} questions to {OUTPUT_PATH}")


def main() -> int:
    questions = _build_bank()
    _validate_bank(questions)
    _write_bank(questions)

    difficulty_summary = Counter(str(question["difficulty"]) for question in questions)
    family_summary = Counter(str(question["tags"][1]) for question in questions)  # type: ignore[index]
    print(f"Difficulty summary: {dict(difficulty_summary)}")
    print(f"Family summary: {dict(family_summary)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
