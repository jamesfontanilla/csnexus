"""Generate the Verbal Ability / Sentence Structure / Coordination question bank."""

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
    / "coordination"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Coordination"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "coordination"
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
    word_coordination: str
    phrase_coordination: str
    sentence_type_sentence: str
    sentence_type_answer: str
    correlative_correct: str
    correlative_parallel_wrong_choices: tuple[str, str, str]
    correlative_blank: str
    correlative_pair_label: str
    correlative_pair_choices: tuple[str, str, str, str]
    correlative_fill_choices: tuple[str, str, str, str]
    correlative_fill_answer: str
    no_correction: str
    conjunction: str
    conjunction_choices: tuple[str, str, str, str]
    relation: str
    relation_prompt: str
    subordinator: str


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
        "word_coordination": scene.word_coordination,
        "phrase_coordination": scene.phrase_coordination,
        "sentence_type_sentence": scene.sentence_type_sentence,
        "sentence_type_answer": scene.sentence_type_answer,
        "correlative_correct": scene.correlative_correct,
        "correlative_blank": scene.correlative_blank,
        "correlative_pair_label": scene.correlative_pair_label,
        "correlative_fill_answer": scene.correlative_fill_answer,
        "no_correction": scene.no_correction,
        "conjunction": scene.conjunction,
        "relation": scene.relation,
        "relation_prompt": scene.relation_prompt,
        "subordinator": scene.subordinator,
        "conjunction_blank": scene.compound.replace(f", {scene.conjunction} ", ", ____ ", 1),
    }


def _choices_from_fields(*fields: str) -> Callable[[Scene], list[str]]:
    def builder(scene: Scene) -> list[str]:
        choices: list[str] = []
        for field in fields:
            value = getattr(scene, field)
            if isinstance(value, (list, tuple)):
                choices.extend(str(item) for item in value)
            else:
                choices.append(str(value))
        return choices

    return builder


def _fixed_choices(*choices: str) -> Callable[[Scene], list[str]]:
    def builder(_: Scene) -> list[str]:
        return list(choices)

    return builder


def _answer_field(field: str) -> Callable[[Scene], str]:
    def builder(scene: Scene) -> str:
        return str(getattr(scene, field))

    return builder


def _answer_value(value: str) -> Callable[[Scene], str]:
    def builder(_: Scene) -> str:
        return value

    return builder


QUESTION_STEMS: dict[str, dict[str, str]] = {
    "coordination-identification": {
        "Easy": "Which sentence in the {context} shows coordination at the clause level?",
        "Medium": "From the {context}, pick the sentence that joins equal ideas.",
        "Hard": "In the {context}, which option is a coordinated clause pair rather than a simple or complex sentence?",
        "Ultra": "Select the line from the {context} that keeps both clauses at the same grammatical rank.",
    },
    "coordinating-conjunction-identification": {
        "Easy": "Which word in \"{compound}\" is the coordinating conjunction?",
        "Medium": "In \"{compound}\", which word links the two independent clauses?",
        "Hard": "Which FANBOYS word appears in \"{compound}\"?",
        "Ultra": "Identify the coordinating conjunction that connects the clauses in \"{compound}\".",
    },
    "relation-based-conjunction-choice": {
        "Easy": "Which coordinating conjunction best shows {relation} in the {context}?",
        "Medium": "The {context} item needs a FANBOYS word for {relation}. Which one fits?",
        "Hard": "Choose the conjunction that matches the {relation_prompt} relationship in the {context} example.",
        "Ultra": "Which FANBOYS word expresses {relation_prompt} most precisely in the {context} example?",
    },
    "coordinating-conjunction-fill-in": {
        "Easy": "Fill the blank in \"{conjunction_blank}\".",
        "Medium": "Complete the coordinated clause pair: \"{conjunction_blank}\".",
        "Hard": "Which word belongs in the blank so the sentence stays coordinated: \"{conjunction_blank}\"?",
        "Ultra": "Insert the correct coordinating conjunction into \"{conjunction_blank}\".",
    },
    "comma-conjunction-revision": {
        "Easy": "Which revision correctly uses a comma before the coordinating conjunction in the {context}?",
        "Medium": "Choose the sentence that fixes the comma usage in the {context} item.",
        "Hard": "Select the revision that joins the clauses with the correct comma-and-conjunction pattern in the {context}.",
        "Ultra": "Which option gives the clean coordinated form for the {context} example?",
    },
    "semicolon-revision": {
        "Easy": "Which revision correctly joins the clauses with a semicolon in the {context}?",
        "Medium": "Choose the semicolon revision for the {context} sentence.",
        "Hard": "Select the option that uses a semicolon to link the two independent clauses in the {context} example.",
        "Ultra": "Which sentence shows the best semicolon connection in the {context}?",
    },
    "punctuation-mark-selection": {
        "Easy": "What punctuation mark should come before the coordinating conjunction in the {context} sentence?",
        "Medium": "Which mark belongs before the FANBOYS word in \"{compound}\"?",
        "Hard": "Choose the punctuation mark that coordinated clauses require before the conjunction in the {context} sentence.",
        "Ultra": "What mark correctly separates the first independent clause from the coordinating conjunction in \"{compound}\"?",
    },
    "word-coordination-identification": {
        "Easy": "Which sentence in the {context} coordinates words rather than clauses?",
        "Medium": "From the {context}, choose the option that joins equal words.",
        "Hard": "In the {context} example, which line shows coordination at the word level?",
        "Ultra": "Select the choice in the {context} where the equal units are individual words, not clauses.",
    },
    "phrase-coordination-identification": {
        "Easy": "Which sentence in the {context} coordinates phrases?",
        "Medium": "Choose the option that joins matching phrases in the {context} example.",
        "Hard": "In the {context}, which line shows phrase-level coordination?",
        "Ultra": "Select the sentence in the {context} where the coordinated units are phrases instead of clauses.",
    },
    "coordination-vs-subordination-classification": {
        "Easy": "Which sentence in the {context} uses coordination rather than subordination?",
        "Medium": "Choose the option in the {context} that keeps both ideas at the same grammatical rank.",
        "Hard": "Which sentence is coordinated, not subordinated, in the {context} example?",
        "Ultra": "Select the line in the {context} where the relationship is equal rather than dependent.",
    },
    "sentence-type-classification": {
        "Easy": "What sentence type is \"{sentence_type_sentence}\"?",
        "Medium": "Which label best fits \"{sentence_type_sentence}\"?",
        "Hard": "Classify \"{sentence_type_sentence}\" by sentence structure.",
        "Ultra": "Name the sentence type of \"{sentence_type_sentence}\".",
    },
    "correlative-conjunction-identification": {
        "Easy": "Which correlative pair appears in the {context} example?",
        "Medium": "Identify the paired conjunction used in \"{correlative_correct}\".",
        "Hard": "Which correlative pair matches the balanced structure in the {context}?",
        "Ultra": "Select the correlative pair used in \"{correlative_correct}\".",
    },
    "correlative-conjunction-fill-in": {
        "Easy": "What word completes \"{correlative_blank}\"?",
        "Medium": "Fill the missing correlative word in \"{correlative_blank}\".",
        "Hard": "Which word belongs in the blank of \"{correlative_blank}\" so the pair stays balanced?",
        "Ultra": "Insert the correct paired word into \"{correlative_blank}\".",
    },
    "correlative-parallel-repair": {
        "Easy": "Which revision keeps the correlative pair parallel in the {context}?",
        "Medium": "Choose the sentence that repairs the correlative structure in the {context}.",
        "Hard": "Select the option in the {context} that keeps the paired elements balanced and parallel.",
        "Ultra": "Which sentence in the {context} preserves the correlative pattern without changing the meaning?",
    },
    "no-correction-needed": {
        "Easy": "Which sentence in the {context} is already correct?",
        "Medium": "Choose the option in the {context} that needs no correction.",
        "Hard": "Select the sentence in the {context} that is already acceptable as written.",
        "Ultra": "Which choice in the {context} can stay exactly as it is?",
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
        word_coordination="The clerk and the supervisor filed the memo.",
        phrase_coordination="The memo was filed by hand and with care.",
        sentence_type_sentence="The clerk filed the memo, and the supervisor signed it.",
        sentence_type_answer="compound sentence",
        correlative_correct="Both the clerk and the supervisor signed the memo.",
        correlative_parallel_wrong_choices=(
            "Both the clerk or the supervisor signed the memo.",
            "Both the clerk and the supervisor was signing the memo.",
            "Both the clerk and the supervisor signed memo.",
        ),
        correlative_blank="Both the clerk ____ the supervisor signed the memo.",
        correlative_pair_label="both...and",
        correlative_pair_choices=(
            "both...and",
            "either...or",
            "neither...nor",
            "not only...but also",
        ),
        correlative_fill_choices=("and", "or", "nor", "but"),
        correlative_fill_answer="and",
        no_correction="The clerk filed the memo, and the supervisor signed it.",
        conjunction="and",
        conjunction_choices=("and", "but", "so", "or"),
        relation="addition",
        relation_prompt="addition",
        subordinator="because",
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
        word_coordination="The office and the lobby stayed quiet.",
        phrase_coordination="The clerk stayed calm in the office and at the counter.",
        sentence_type_sentence="Although the office was busy, the clerk stayed calm.",
        sentence_type_answer="complex sentence",
        correlative_correct="Neither the office nor the lobby was quiet.",
        correlative_parallel_wrong_choices=(
            "Neither the office or the lobby was quiet.",
            "Neither the office nor the lobby were quiet.",
            "Neither office nor the lobby was quiet.",
        ),
        correlative_blank="Neither the office ____ the lobby was quiet.",
        correlative_pair_label="neither...nor",
        correlative_pair_choices=(
            "neither...nor",
            "both...and",
            "either...or",
            "not only...but also",
        ),
        correlative_fill_choices=("nor", "or", "and", "but"),
        correlative_fill_answer="nor",
        no_correction="The office was busy, but the clerk stayed calm.",
        conjunction="but",
        conjunction_choices=("but", "and", "so", "or"),
        relation="contrast",
        relation_prompt="contrast",
        subordinator="although",
    ),
    Scene(
        context="printer-jam set",
        compound="The printer jammed, so the staff waited.",
        simple="The staff waited in silence.",
        complex="Because the printer jammed, the staff waited.",
        compound_complex="Because the printer jammed, the staff waited, and the technician arrived.",
        comma_splice="The printer jammed, the staff waited.",
        fused="The printer jammed the staff waited.",
        semicolon="The printer jammed; the staff waited.",
        word_coordination="The staff and the technician fixed the printer.",
        phrase_coordination="The staff worked with speed and with care.",
        sentence_type_sentence="Because the printer jammed, the staff waited.",
        sentence_type_answer="complex sentence",
        correlative_correct="Not only did the printer jam, but the staff also waited.",
        correlative_parallel_wrong_choices=(
            "Not only did the printer jam and the staff also waited.",
            "Not only the printer jam, but the staff also waited.",
            "Not only did the printer jam, and the staff also waited.",
        ),
        correlative_blank="Not only did the printer jam, ____ the staff also waited.",
        correlative_pair_label="not only...but also",
        correlative_pair_choices=(
            "not only...but also",
            "either...or",
            "neither...nor",
            "both...and",
        ),
        correlative_fill_choices=("but", "and", "or", "nor"),
        correlative_fill_answer="but",
        no_correction="The printer jammed, so the staff waited.",
        conjunction="so",
        conjunction_choices=("so", "and", "but", "or"),
        relation="result",
        relation_prompt="result",
        subordinator="because",
    ),
    Scene(
        context="choice set",
        compound="You may call now, or you may send an email later.",
        simple="You may call now.",
        complex="If the office is open, you may call now.",
        compound_complex="If the office is open, you may call now, or you may send an email later.",
        comma_splice="You may call now, you may send an email later.",
        fused="You may call now you may send an email later.",
        semicolon="You may call now; you may send an email later.",
        word_coordination="The clerk or the supervisor will sign the memo.",
        phrase_coordination="The notice was sent by phone or by email.",
        sentence_type_sentence="You may call now.",
        sentence_type_answer="simple sentence",
        correlative_correct="Either the clerk or the supervisor will sign the memo.",
        correlative_parallel_wrong_choices=(
            "Either the clerk and the supervisor will sign the memo.",
            "Either the clerk or the supervisor will signing the memo.",
            "Either the clerk or the supervisor will sign memo.",
        ),
        correlative_blank="Either the clerk ____ the supervisor will sign the memo.",
        correlative_pair_label="either...or",
        correlative_pair_choices=(
            "either...or",
            "both...and",
            "neither...nor",
            "not only...but also",
        ),
        correlative_fill_choices=("or", "and", "nor", "but"),
        correlative_fill_answer="or",
        no_correction="You may call now, or you may send an email later.",
        conjunction="or",
        conjunction_choices=("or", "and", "but", "so"),
        relation="choice",
        relation_prompt="choice",
        subordinator="if",
    ),
    Scene(
        context="night-watch set",
        compound="The team did not delay, nor did it complain.",
        simple="The team stayed silent.",
        complex="Although the team was tired, it did not complain.",
        compound_complex="Although the team was tired, it did not complain, and it kept working.",
        comma_splice="The team did not delay, it did not complain.",
        fused="The team did not delay it did not complain.",
        semicolon="The team did not delay; it did not complain.",
        word_coordination="The team and the manager stayed silent.",
        phrase_coordination="The team waited in silence and with patience.",
        sentence_type_sentence="The team did not delay, nor did it complain.",
        sentence_type_answer="compound sentence",
        correlative_correct="Neither the team nor the manager complained.",
        correlative_parallel_wrong_choices=(
            "Neither the team or the manager complained.",
            "Neither the team nor the manager were complaining.",
            "Neither team nor the manager complained.",
        ),
        correlative_blank="Neither the team ____ the manager complained.",
        correlative_pair_label="neither...nor",
        correlative_pair_choices=(
            "neither...nor",
            "both...and",
            "either...or",
            "not only...but also",
        ),
        correlative_fill_choices=("nor", "or", "and", "but"),
        correlative_fill_answer="nor",
        no_correction="The team did not delay, nor did it complain.",
        conjunction="nor",
        conjunction_choices=("nor", "and", "but", "or"),
        relation="negative addition",
        relation_prompt="negative addition",
        subordinator="although",
    ),
    Scene(
        context="editor deadline set",
        compound="The editor left early, for the deadline was near.",
        simple="The deadline was near.",
        complex="Because the deadline was near, the editor left early.",
        compound_complex="Because the deadline was near, the editor left early, and the assistant closed the file.",
        comma_splice="The editor left early, the deadline was near.",
        fused="The editor left early the deadline was near.",
        semicolon="The editor left early; the deadline was near.",
        word_coordination="The editor and the assistant checked the proof.",
        phrase_coordination="The editor worked with speed and with focus.",
        sentence_type_sentence="Because the deadline was near, the editor left early.",
        sentence_type_answer="complex sentence",
        correlative_correct="The editor would rather leave early than miss the deadline.",
        correlative_parallel_wrong_choices=(
            "The editor would rather leave early and miss the deadline.",
            "The editor would rather leave early than the deadline.",
            "The editor would rather leave early, the deadline.",
        ),
        correlative_blank="The editor would rather leave early ____ miss the deadline.",
        correlative_pair_label="rather...than",
        correlative_pair_choices=(
            "rather...than",
            "both...and",
            "either...or",
            "not only...but also",
        ),
        correlative_fill_choices=("than", "or", "and", "nor"),
        correlative_fill_answer="than",
        no_correction="The editor left early, for the deadline was near.",
        conjunction="for",
        conjunction_choices=("for", "because", "but", "or"),
        relation="reason",
        relation_prompt="reason",
        subordinator="because",
    ),
    Scene(
        context="schedule update set",
        compound="The schedule changed, yet everyone stayed calm.",
        simple="The plan changed.",
        complex="Although the schedule changed, everyone stayed calm.",
        compound_complex="Although the schedule changed, everyone stayed calm, and the team kept working.",
        comma_splice="The schedule changed, everyone stayed calm.",
        fused="The schedule changed everyone stayed calm.",
        semicolon="The schedule changed; everyone stayed calm.",
        word_coordination="The schedule and the plan changed.",
        phrase_coordination="The update arrived by email and by text.",
        sentence_type_sentence="Although the schedule changed, everyone stayed calm.",
        sentence_type_answer="complex sentence",
        correlative_correct="Both the schedule and the plan changed.",
        correlative_parallel_wrong_choices=(
            "Both the schedule or the plan changed.",
            "Both the schedule and the plan was changed.",
            "Both schedule and the plan changed.",
        ),
        correlative_blank="Both the schedule ____ the plan changed.",
        correlative_pair_label="both...and",
        correlative_pair_choices=(
            "both...and",
            "either...or",
            "neither...nor",
            "not only...but also",
        ),
        correlative_fill_choices=("and", "or", "nor", "but"),
        correlative_fill_answer="and",
        no_correction="The schedule changed, yet everyone stayed calm.",
        conjunction="yet",
        conjunction_choices=("yet", "and", "or", "so"),
        relation="contrast",
        relation_prompt="contrast",
        subordinator="although",
    ),
    Scene(
        context="meeting note set",
        compound="The meeting ended at noon, and the assistant sent the notice.",
        simple="The assistant sent the notice.",
        complex="After the meeting ended, the assistant sent the notice.",
        compound_complex="After the meeting ended, the assistant sent the notice, and the clerk archived the notes.",
        comma_splice="The meeting ended at noon, the assistant sent the notice.",
        fused="The meeting ended at noon the assistant sent the notice.",
        semicolon="The meeting ended at noon; the assistant sent the notice.",
        word_coordination="The meeting and the notice were ready.",
        phrase_coordination="The assistant sent the notice by email and by text.",
        sentence_type_sentence="The meeting ended at noon, and the assistant sent the notice.",
        sentence_type_answer="compound sentence",
        correlative_correct="Whether the meeting ends early or late, the assistant will send the notice.",
        correlative_parallel_wrong_choices=(
            "Whether the meeting ends early and late, the assistant will send the notice.",
            "Whether the meeting ends early or the assistant will send the notice.",
            "Whether the meeting ends early, the assistant will send the notice.",
        ),
        correlative_blank="Whether the meeting ends early ____ late, the assistant will send the notice.",
        correlative_pair_label="whether...or",
        correlative_pair_choices=(
            "whether...or",
            "both...and",
            "neither...nor",
            "not only...but also",
        ),
        correlative_fill_choices=("or", "and", "nor", "but"),
        correlative_fill_answer="or",
        no_correction="The meeting ended at noon, and the assistant sent the notice.",
        conjunction="and",
        conjunction_choices=("and", "but", "so", "or"),
        relation="addition",
        relation_prompt="addition",
        subordinator="after",
    ),
    Scene(
        context="server failure set",
        compound="The server failed, so the staff restarted it.",
        simple="The staff restarted it.",
        complex="Because the server failed, the staff restarted it.",
        compound_complex="Because the server failed, the staff restarted it, and the backup came online.",
        comma_splice="The server failed, the staff restarted it.",
        fused="The server failed the staff restarted it.",
        semicolon="The server failed; the staff restarted it.",
        word_coordination="The staff and the backups were ready.",
        phrase_coordination="The staff acted with speed and with focus.",
        sentence_type_sentence="Because the server failed, the staff restarted it.",
        sentence_type_answer="complex sentence",
        correlative_correct="Not only did the server fail, but the backup also failed.",
        correlative_parallel_wrong_choices=(
            "Not only did the server fail and the backup also failed.",
            "Not only the server failed, but the backup also failed.",
            "Not only did the server fail, and the backup also failed.",
        ),
        correlative_blank="Not only did the server fail, ____ the backup also failed.",
        correlative_pair_label="not only...but also",
        correlative_pair_choices=(
            "not only...but also",
            "either...or",
            "neither...nor",
            "both...and",
        ),
        correlative_fill_choices=("but", "and", "or", "nor"),
        correlative_fill_answer="but",
        no_correction="The server failed, so the staff restarted it.",
        conjunction="so",
        conjunction_choices=("so", "and", "but", "or"),
        relation="result",
        relation_prompt="result",
        subordinator="because",
    ),
    Scene(
        context="planning note set",
        compound="The plan looked simple, yet the deadline remained tight.",
        simple="The memo stayed clear.",
        complex="Although the plan looked simple, the deadline remained tight.",
        compound_complex="Although the plan looked simple, the deadline remained tight, and the team kept moving.",
        comma_splice="The plan looked simple, the deadline remained tight.",
        fused="The plan looked simple the deadline remained tight.",
        semicolon="The plan looked simple; the deadline remained tight.",
        word_coordination="The memo and the timeline were clear.",
        phrase_coordination="The team worked with calm and with care.",
        sentence_type_sentence="The memo stayed clear.",
        sentence_type_answer="simple sentence",
        correlative_correct="The plan was as clear as the memo.",
        correlative_parallel_wrong_choices=(
            "The plan was as clear and the memo.",
            "The plan was as clear than the memo.",
            "The plan was clear as the memo.",
        ),
        correlative_blank="The plan was as clear ____ the memo.",
        correlative_pair_label="as...as",
        correlative_pair_choices=(
            "as...as",
            "either...or",
            "both...and",
            "neither...nor",
        ),
        correlative_fill_choices=("as", "or", "and", "than"),
        correlative_fill_answer="as",
        no_correction="The plan looked simple, yet the deadline remained tight.",
        conjunction="yet",
        conjunction_choices=("yet", "and", "or", "so"),
        relation="contrast",
        relation_prompt="contrast",
        subordinator="although",
    ),
)


FAMILY_SPECS: tuple[FamilySpec, ...] = (
    FamilySpec(
        base_family="coordination-identification",
        choice_builder=_choices_from_fields("compound", "simple", "complex", "compound_complex"),
        answer_builder=_answer_field("compound"),
        explanation="Coordination joins equal units, so the compound sentence is the correct choice.",
        tags=("classification", "compound"),
    ),
    FamilySpec(
        base_family="coordinating-conjunction-identification",
        choice_builder=_choices_from_fields("conjunction_choices"),
        answer_builder=_answer_field("conjunction"),
        explanation="The coordinating conjunction is the FANBOYS word that links the equal clauses.",
        tags=("grammar", "conjunction"),
    ),
    FamilySpec(
        base_family="relation-based-conjunction-choice",
        choice_builder=_choices_from_fields("conjunction_choices"),
        answer_builder=_answer_field("conjunction"),
        explanation="The conjunction should match the logical relationship between the two coordinated ideas.",
        tags=("selection", "relationship"),
    ),
    FamilySpec(
        base_family="coordinating-conjunction-fill-in",
        choice_builder=_choices_from_fields("conjunction_choices"),
        answer_builder=_answer_field("conjunction"),
        explanation="The blank needs the coordinating conjunction that keeps the clause pair balanced.",
        tags=("completion", "conjunction"),
    ),
    FamilySpec(
        base_family="comma-conjunction-revision",
        choice_builder=_choices_from_fields("compound", "comma_splice", "fused", "semicolon"),
        answer_builder=_answer_field("compound"),
        explanation="A comma belongs before the coordinating conjunction when two independent clauses are joined.",
        tags=("revision", "comma"),
    ),
    FamilySpec(
        base_family="semicolon-revision",
        choice_builder=_choices_from_fields("semicolon", "compound", "comma_splice", "fused"),
        answer_builder=_answer_field("semicolon"),
        explanation="A semicolon can join two closely related independent clauses without a coordinating conjunction.",
        tags=("revision", "semicolon"),
    ),
    FamilySpec(
        base_family="punctuation-mark-selection",
        choice_builder=_fixed_choices("comma", "semicolon", "period", "apostrophe"),
        answer_builder=_answer_value("comma"),
        explanation="A comma comes before a coordinating conjunction that joins two independent clauses.",
        tags=("punctuation", "comma"),
    ),
    FamilySpec(
        base_family="word-coordination-identification",
        choice_builder=_choices_from_fields("word_coordination", "phrase_coordination", "compound", "complex"),
        answer_builder=_answer_field("word_coordination"),
        explanation="Word-level coordination joins individual words, not clauses.",
        tags=("classification", "words"),
    ),
    FamilySpec(
        base_family="phrase-coordination-identification",
        choice_builder=_choices_from_fields("phrase_coordination", "word_coordination", "compound", "complex"),
        answer_builder=_answer_field("phrase_coordination"),
        explanation="Phrase-level coordination joins matching phrases at the same grammatical rank.",
        tags=("classification", "phrases"),
    ),
    FamilySpec(
        base_family="coordination-vs-subordination-classification",
        choice_builder=_choices_from_fields("compound", "complex", "simple", "compound_complex"),
        answer_builder=_answer_field("compound"),
        explanation="Coordination keeps both units equal, while subordination makes one depend on the other.",
        tags=("classification", "coordination"),
    ),
    FamilySpec(
        base_family="sentence-type-classification",
        choice_builder=_fixed_choices(
            "simple sentence",
            "compound sentence",
            "complex sentence",
            "compound-complex sentence",
        ),
        answer_builder=_answer_field("sentence_type_answer"),
        explanation="Sentence-type questions test whether you can distinguish simple, compound, complex, and compound-complex structures.",
        tags=("classification", "sentence-type"),
    ),
    FamilySpec(
        base_family="correlative-conjunction-identification",
        choice_builder=_choices_from_fields("correlative_pair_choices"),
        answer_builder=_answer_field("correlative_pair_label"),
        explanation="Correlative conjunctions appear in matched pairs such as both...and or either...or.",
        tags=("correlative", "pair"),
    ),
    FamilySpec(
        base_family="correlative-conjunction-fill-in",
        choice_builder=_choices_from_fields("correlative_fill_choices"),
        answer_builder=_answer_field("correlative_fill_answer"),
        explanation="The missing word must complete the correlative pair and keep the structure balanced.",
        tags=("correlative", "completion"),
    ),
    FamilySpec(
        base_family="correlative-parallel-repair",
        choice_builder=_choices_from_fields(
            "correlative_correct",
            "correlative_parallel_wrong_choices",
        ),
        answer_builder=_answer_field("correlative_correct"),
        explanation="Correlative pairs must stay parallel, so the balanced revision is the correct choice.",
        tags=("parallel", "correlative"),
    ),
    FamilySpec(
        base_family="no-correction-needed",
        choice_builder=_choices_from_fields("no_correction", "comma_splice", "fused", "complex"),
        answer_builder=_answer_field("no_correction"),
        explanation="When a sentence is already correctly coordinated, no revision is needed.",
        tags=("verification", "no-change"),
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
