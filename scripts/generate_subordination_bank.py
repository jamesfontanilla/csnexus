"""Generate the Verbal Ability / Sentence Structure / Subordination question bank."""

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
    / "subordination"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Subordination"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "subordination"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

SENTENCE_TYPE_CHOICES = (
    "simple sentence",
    "compound sentence",
    "complex sentence",
    "compound-complex sentence",
)
CLAUSE_FUNCTION_CHOICES = (
    "adverb clause",
    "adjective clause",
    "noun clause",
    "independent clause",
)
RELATIVE_PRONOUN_CHOICES = ("who", "that", "where", "when")


@dataclass(frozen=True)
class Scene:
    context: str
    intro_sentence: str
    intro_missing_comma_sentence: str
    postposed_sentence: str
    postposed_with_comma_sentence: str
    compound_sentence: str
    compound_complex_sentence: str
    simple_sentence: str
    dependent_clause: str
    fragment_sentence: str
    repaired_fragment_sentence: str
    comma_splice_sentence: str
    fused_sentence: str
    fill_blank_sentence: str
    sentence_type_sentence: str
    sentence_type_answer: str
    clause_function_sentence: str
    clause_function_answer: str
    relative_sentence: str
    relative_pronoun: str
    subordinator: str
    subordinator_choices: tuple[str, str, str, str]
    relation: str
    relation_prompt: str
    no_correction_sentence: str


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
        "intro_sentence": scene.intro_sentence,
        "intro_missing_comma_sentence": scene.intro_missing_comma_sentence,
        "postposed_sentence": scene.postposed_sentence,
        "postposed_with_comma_sentence": scene.postposed_with_comma_sentence,
        "compound_sentence": scene.compound_sentence,
        "compound_complex_sentence": scene.compound_complex_sentence,
        "simple_sentence": scene.simple_sentence,
        "dependent_clause": scene.dependent_clause,
        "fragment_sentence": scene.fragment_sentence,
        "repaired_fragment_sentence": scene.repaired_fragment_sentence,
        "comma_splice_sentence": scene.comma_splice_sentence,
        "fused_sentence": scene.fused_sentence,
        "fill_blank_sentence": scene.fill_blank_sentence,
        "sentence_type_sentence": scene.sentence_type_sentence,
        "sentence_type_answer": scene.sentence_type_answer,
        "clause_function_sentence": scene.clause_function_sentence,
        "clause_function_answer": scene.clause_function_answer,
        "relative_sentence": scene.relative_sentence,
        "relative_pronoun": scene.relative_pronoun,
        "subordinator": scene.subordinator,
        "relation": scene.relation,
        "relation_prompt": scene.relation_prompt,
        "no_correction_sentence": scene.no_correction_sentence,
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


QUESTION_STEMS: dict[str, dict[str, str]] = {
    "complex-sentence-identification": {
        "Easy": "Which sentence in the {context} is the complex sentence?",
        "Medium": "From the {context}, pick the sentence that contains one independent clause and one dependent clause.",
        "Hard": "In the {context}, which option is a complex sentence rather than a compound or simple one?",
        "Ultra": "Select the line from the {context} that shows one main clause joined to one subordinate clause.",
    },
    "dependent-clause-identification": {
        "Easy": "Which clause in the {context} is dependent?",
        "Medium": "From the {context}, choose the clause that cannot stand alone.",
        "Hard": "In the {context}, which option is the subordinate clause?",
        "Ultra": "Select the fragment in the {context} that still needs a main clause to finish the thought.",
    },
    "subordinating-conjunction-identification": {
        "Easy": "Which word in \"{intro_sentence}\" is the subordinating conjunction?",
        "Medium": "In \"{intro_sentence}\", which word begins the dependent clause?",
        "Hard": "Which subordinating conjunction appears in the {context} sentence?",
        "Ultra": "Identify the word that makes the clause subordinate in \"{intro_sentence}\".",
    },
    "relation-based-subordinator-choice": {
        "Easy": "Which subordinating conjunction best shows {relation} in the {context}?",
        "Medium": "The {context} item needs a connector for {relation}. Which one fits?",
        "Hard": "Choose the subordinating conjunction that matches the {relation_prompt} relationship in the {context} example.",
        "Ultra": "Which subordinate marker expresses {relation_prompt} most precisely in the {context} example?",
    },
    "subordinator-fill-in": {
        "Easy": "Fill the blank in \"{fill_blank_sentence}\".",
        "Medium": "Complete the dependent clause in \"{fill_blank_sentence}\".",
        "Hard": "Which word belongs in the blank so the relationship stays clear: \"{fill_blank_sentence}\"?",
        "Ultra": "Insert the correct subordinating conjunction into \"{fill_blank_sentence}\".",
    },
    "introductory-comma-revision": {
        "Easy": "Which revision correctly uses a comma after the introductory dependent clause in the {context}?",
        "Medium": "Choose the sentence that fixes the introductory-clause punctuation in the {context} example.",
        "Hard": "Select the revision that places the comma in the correct spot for the opening dependent clause in the {context} example.",
        "Ultra": "Which option gives the clean introductory-clause form for the {context}?",
    },
    "postposed-clause-revision": {
        "Easy": "Which revision correctly places the dependent clause after the main clause in the {context}?",
        "Medium": "Choose the sentence that keeps the main clause first and the dependent clause second in the {context} example.",
        "Hard": "Select the revision that uses the postposed dependent clause without adding an unnecessary comma in the {context} example.",
        "Ultra": "Which sentence shows the best main-clause-first order in the {context} example?",
    },
    "sentence-type-classification": {
        "Easy": "What sentence type is \"{sentence_type_sentence}\"?",
        "Medium": "Which label best fits \"{sentence_type_sentence}\"?",
        "Hard": "Classify \"{sentence_type_sentence}\" by sentence structure.",
        "Ultra": "Name the sentence type of \"{sentence_type_sentence}\".",
    },
    "clause-function-classification": {
        "Easy": "What is the function of the clause in \"{clause_function_sentence}\"?",
        "Medium": "Which clause function fits \"{clause_function_sentence}\"?",
        "Hard": "Classify the subordinate clause in \"{clause_function_sentence}\".",
        "Ultra": "Select the grammatical role played by the subordinate clause in \"{clause_function_sentence}\".",
    },
    "relative-pronoun-identification": {
        "Easy": "Which word introduces the relative clause in \"{relative_sentence}\"?",
        "Medium": "In \"{relative_sentence}\", which word begins the adjective clause?",
        "Hard": "Which relative word appears in the {context} example?",
        "Ultra": "Identify the relative pronoun or relative adverb in \"{relative_sentence}\".",
    },
    "relative-clause-identification": {
        "Easy": "Which sentence in the {context} uses a relative clause?",
        "Medium": "From the {context}, choose the sentence that describes a noun with a subordinate clause.",
        "Hard": "In the {context}, which option contains a relative clause?",
        "Ultra": "Select the line from the {context} that uses a relative clause to modify a noun.",
    },
    "fragment-repair": {
        "Easy": "Which revision turns \"{fragment_sentence}\" into a complete sentence?",
        "Medium": "Choose the sentence that repairs the fragment in the {context}.",
        "Hard": "Select the option that adds the missing main clause to the {context} fragment.",
        "Ultra": "Which revision gives the complete thought without changing the meaning in the {context}?",
    },
    "coordination-vs-subordination-classification": {
        "Easy": "Which sentence in the {context} uses subordination rather than coordination?",
        "Medium": "Choose the option in the {context} that relies on a dependent clause.",
        "Hard": "In the {context}, which sentence is complex because one clause depends on another?",
        "Ultra": "Select the line from the {context} that shows unequal clause rank.",
    },
    "clause-order-revision": {
        "Easy": "Which revision correctly moves the dependent clause to the front in the {context}?",
        "Medium": "Choose the sentence in the {context} that starts with the subordinate clause and ends with the main clause.",
        "Hard": "Select the revision that flips the clause order without losing the relationship in the {context} example.",
        "Ultra": "Which option front-loads the dependent clause and keeps the sentence grammatically complete in the {context} example?",
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
        context="weather-delay set",
        intro_sentence="Because the roads were flooded, the bus arrived late.",
        intro_missing_comma_sentence="Because the roads were flooded the bus arrived late.",
        postposed_sentence="The bus arrived late because the roads were flooded.",
        postposed_with_comma_sentence="The bus arrived late, because the roads were flooded.",
        compound_sentence="The roads were flooded, so the bus arrived late.",
        compound_complex_sentence="Because the roads were flooded, the bus arrived late, and the passengers waited quietly.",
        simple_sentence="The bus arrived late.",
        dependent_clause="Because the roads were flooded",
        fragment_sentence="Because the roads were flooded.",
        repaired_fragment_sentence="Because the roads were flooded, the bus arrived late.",
        comma_splice_sentence="Because the roads were flooded, the bus arrived late, the passengers waited quietly.",
        fused_sentence="Because the roads were flooded the bus arrived late and the passengers waited quietly.",
        fill_blank_sentence="The bus arrived late ____ the roads were flooded.",
        sentence_type_sentence="Because the roads were flooded, the bus arrived late.",
        sentence_type_answer="complex sentence",
        clause_function_sentence="Because the roads were flooded, the bus arrived late.",
        clause_function_answer="adverb clause",
        relative_sentence="The bus that arrived late left the station.",
        relative_pronoun="that",
        subordinator="because",
        subordinator_choices=("because", "although", "if", "after"),
        relation="cause",
        relation_prompt="cause",
        no_correction_sentence="The bus arrived late because the roads were flooded.",
    ),
    Scene(
        context="office contrast set",
        intro_sentence="Although the office was busy, the clerk stayed calm.",
        intro_missing_comma_sentence="Although the office was busy the clerk stayed calm.",
        postposed_sentence="The clerk stayed calm although the office was busy.",
        postposed_with_comma_sentence="The clerk stayed calm, although the office was busy.",
        compound_sentence="The office was busy, but the clerk stayed calm.",
        compound_complex_sentence="Although the office was busy, the clerk stayed calm, and the manager reviewed the report.",
        simple_sentence="The office was busy all morning.",
        dependent_clause="Although the office was busy",
        fragment_sentence="Although the office was busy.",
        repaired_fragment_sentence="Although the office was busy, the clerk stayed calm.",
        comma_splice_sentence="Although the office was busy, the clerk stayed calm, the manager reviewed the report.",
        fused_sentence="Although the office was busy the clerk stayed calm and the manager reviewed the report.",
        fill_blank_sentence="The clerk stayed calm ____ the office was busy.",
        sentence_type_sentence="The office was busy, but the clerk stayed calm.",
        sentence_type_answer="compound sentence",
        clause_function_sentence="Although the office was busy, the clerk stayed calm.",
        clause_function_answer="adverb clause",
        relative_sentence="The clerk who stayed calm answered the phone.",
        relative_pronoun="who",
        subordinator="although",
        subordinator_choices=("although", "because", "if", "when"),
        relation="contrast",
        relation_prompt="contrast",
        no_correction_sentence="Although the office was busy, the clerk stayed calm.",
    ),
    Scene(
        context="report condition set",
        intro_sentence="Unless the report is ready, do not send it.",
        intro_missing_comma_sentence="Unless the report is ready do not send it.",
        postposed_sentence="Do not send it unless the report is ready.",
        postposed_with_comma_sentence="Do not send it, unless the report is ready.",
        compound_sentence="The report is ready, so send it now.",
        compound_complex_sentence="Unless the report is ready, do not send it, and keep the file open.",
        simple_sentence="Do not send it now.",
        dependent_clause="Unless the report is ready",
        fragment_sentence="Unless the report is ready.",
        repaired_fragment_sentence="Unless the report is ready, do not send it.",
        comma_splice_sentence="Unless the report is ready, do not send it, keep the file open.",
        fused_sentence="Unless the report is ready do not send it keep the file open.",
        fill_blank_sentence="Do not send it ____ the report is ready.",
        sentence_type_sentence="Do not send it now.",
        sentence_type_answer="simple sentence",
        clause_function_sentence="Unless the report is ready, do not send it.",
        clause_function_answer="adverb clause",
        relative_sentence="The report that the assistant checked is ready.",
        relative_pronoun="that",
        subordinator="unless",
        subordinator_choices=("unless", "if", "because", "after"),
        relation="condition",
        relation_prompt="condition",
        no_correction_sentence="Do not send it unless the report is ready.",
    ),
    Scene(
        context="meeting time set",
        intro_sentence="After the meeting ended, the assistant sent the notice.",
        intro_missing_comma_sentence="After the meeting ended the assistant sent the notice.",
        postposed_sentence="The assistant sent the notice after the meeting ended.",
        postposed_with_comma_sentence="The assistant sent the notice, after the meeting ended.",
        compound_sentence="The meeting ended, and the assistant sent the notice.",
        compound_complex_sentence="After the meeting ended, the assistant sent the notice, and the clerk archived the notes.",
        simple_sentence="The assistant sent the notice.",
        dependent_clause="After the meeting ended",
        fragment_sentence="After the meeting ended.",
        repaired_fragment_sentence="After the meeting ended, the assistant sent the notice.",
        comma_splice_sentence="After the meeting ended, the assistant sent the notice, the clerk archived the notes.",
        fused_sentence="After the meeting ended the assistant sent the notice the clerk archived the notes.",
        fill_blank_sentence="The assistant sent the notice ____ the meeting ended.",
        sentence_type_sentence="The meeting ended, and the assistant sent the notice.",
        sentence_type_answer="compound sentence",
        clause_function_sentence="After the meeting ended, the assistant sent the notice.",
        clause_function_answer="adverb clause",
        relative_sentence="The notice that the assistant sent was brief.",
        relative_pronoun="that",
        subordinator="after",
        subordinator_choices=("after", "before", "because", "although"),
        relation="time",
        relation_prompt="time",
        no_correction_sentence="The assistant sent the notice after the meeting ended.",
    ),
    Scene(
        context="bridge purpose set",
        intro_sentence="So that the bridge could open safely, the crew worked carefully.",
        intro_missing_comma_sentence="So that the bridge could open safely the crew worked carefully.",
        postposed_sentence="The crew worked carefully so that the bridge could open safely.",
        postposed_with_comma_sentence="The crew worked carefully, so that the bridge could open safely.",
        compound_sentence="The crew worked carefully, and the bridge opened safely.",
        compound_complex_sentence="So that the bridge could open safely, the crew worked carefully, and the engineer checked the bolts.",
        simple_sentence="The crew worked carefully.",
        dependent_clause="So that the bridge could open safely",
        fragment_sentence="So that the bridge could open safely.",
        repaired_fragment_sentence="So that the bridge could open safely, the crew worked carefully.",
        comma_splice_sentence="So that the bridge could open safely, the crew worked carefully, the engineer checked the bolts.",
        fused_sentence="So that the bridge could open safely the crew worked carefully the engineer checked the bolts.",
        fill_blank_sentence="The crew worked carefully ____ the bridge could open safely.",
        sentence_type_sentence="So that the bridge could open safely, the crew worked carefully, and the engineer checked the bolts.",
        sentence_type_answer="compound-complex sentence",
        clause_function_sentence="So that the bridge could open safely, the crew worked carefully.",
        clause_function_answer="adverb clause",
        relative_sentence="The bridge that the crew repaired reopened.",
        relative_pronoun="that",
        subordinator="so that",
        subordinator_choices=("so that", "because", "if", "when"),
        relation="purpose",
        relation_prompt="purpose",
        no_correction_sentence="So that the bridge could open safely, the crew worked carefully.",
    ),
    Scene(
        context="campus place set",
        intro_sentence="Where the notes were kept, the shelf was empty.",
        intro_missing_comma_sentence="Where the notes were kept the shelf was empty.",
        postposed_sentence="The shelf was empty where the notes were kept.",
        postposed_with_comma_sentence="The shelf was empty, where the notes were kept.",
        compound_sentence="The notes were kept there, and the shelf was empty.",
        compound_complex_sentence="Where the notes were kept, the shelf was empty, and the librarian checked the drawers.",
        simple_sentence="The shelf was empty.",
        dependent_clause="Where the notes were kept",
        fragment_sentence="Where the notes were kept.",
        repaired_fragment_sentence="Where the notes were kept, the shelf was empty.",
        comma_splice_sentence="Where the notes were kept, the shelf was empty, the librarian checked the drawers.",
        fused_sentence="Where the notes were kept the shelf was empty the librarian checked the drawers.",
        fill_blank_sentence="The shelf was empty ____ the notes were kept there.",
        sentence_type_sentence="The shelf was empty.",
        sentence_type_answer="simple sentence",
        clause_function_sentence="The shelf where the notes were kept was empty.",
        clause_function_answer="adjective clause",
        relative_sentence="The shelf where the notes were kept was empty.",
        relative_pronoun="where",
        subordinator="where",
        subordinator_choices=("where", "when", "because", "although"),
        relation="place",
        relation_prompt="place",
        no_correction_sentence="The shelf where the notes were kept was empty.",
    ),
    Scene(
        context="teacher note set",
        intro_sentence="When the memo was ready, the clerk filed it.",
        intro_missing_comma_sentence="When the memo was ready the clerk filed it.",
        postposed_sentence="The clerk filed it when the memo was ready.",
        postposed_with_comma_sentence="The clerk filed it, when the memo was ready.",
        compound_sentence="The memo was ready, and the clerk filed it.",
        compound_complex_sentence="When the memo was ready, the clerk filed it, and the supervisor signed it.",
        simple_sentence="The clerk filed it.",
        dependent_clause="When the memo was ready",
        fragment_sentence="When the memo was ready.",
        repaired_fragment_sentence="When the memo was ready, the clerk filed it.",
        comma_splice_sentence="When the memo was ready, the clerk filed it, the supervisor signed it.",
        fused_sentence="When the memo was ready the clerk filed it the supervisor signed it.",
        fill_blank_sentence="I know ____ the memo is ready.",
        sentence_type_sentence="I know that the memo is ready.",
        sentence_type_answer="complex sentence",
        clause_function_sentence="I know that the memo is ready.",
        clause_function_answer="noun clause",
        relative_sentence="The memo that the clerk checked was ready.",
        relative_pronoun="that",
        subordinator="when",
        subordinator_choices=("when", "that", "because", "after"),
        relation="time",
        relation_prompt="time",
        no_correction_sentence="I know that the memo is ready.",
    ),
    Scene(
        context="gardener-relative set",
        intro_sentence="Because the gardener was late, the plants needed water.",
        intro_missing_comma_sentence="Because the gardener was late the plants needed water.",
        postposed_sentence="The plants needed water because the gardener was late.",
        postposed_with_comma_sentence="The plants needed water, because the gardener was late.",
        compound_sentence="The gardener was late, so the plants needed water.",
        compound_complex_sentence="Because the gardener was late, the plants needed water, and the assistant opened the gate.",
        simple_sentence="The plants needed water.",
        dependent_clause="Because the gardener was late",
        fragment_sentence="Because the gardener was late.",
        repaired_fragment_sentence="Because the gardener was late, the plants needed water.",
        comma_splice_sentence="Because the gardener was late, the plants needed water, the assistant opened the gate.",
        fused_sentence="Because the gardener was late the plants needed water the assistant opened the gate.",
        fill_blank_sentence="The plants needed water ____ the gardener was late.",
        sentence_type_sentence="The gardener who watered the plants left early.",
        sentence_type_answer="complex sentence",
        clause_function_sentence="The gardener who watered the plants left early.",
        clause_function_answer="adjective clause",
        relative_sentence="The gardener who watered the plants left early.",
        relative_pronoun="who",
        subordinator="because",
        subordinator_choices=("because", "although", "if", "when"),
        relation="cause",
        relation_prompt="cause",
        no_correction_sentence="The gardener who watered the plants left early.",
    ),
    Scene(
        context="clinic wait set",
        intro_sentence="Until the nurse calls, the patient waits.",
        intro_missing_comma_sentence="Until the nurse calls the patient waits.",
        postposed_sentence="The patient waits until the nurse calls.",
        postposed_with_comma_sentence="The patient waits, until the nurse calls.",
        compound_sentence="The nurse has not called, so the patient waits.",
        compound_complex_sentence="Until the nurse calls, the patient waits, and the clerk updates the chart.",
        simple_sentence="The patient waits.",
        dependent_clause="Until the nurse calls",
        fragment_sentence="Until the nurse calls.",
        repaired_fragment_sentence="Until the nurse calls, the patient waits.",
        comma_splice_sentence="Until the nurse calls, the patient waits, the clerk updates the chart.",
        fused_sentence="Until the nurse calls the patient waits the clerk updates the chart.",
        fill_blank_sentence="The patient waits ____ the nurse calls.",
        sentence_type_sentence="The patient waits until the nurse calls.",
        sentence_type_answer="complex sentence",
        clause_function_sentence="Until the nurse calls, the patient waits.",
        clause_function_answer="adverb clause",
        relative_sentence="The patient who waited quietly left.",
        relative_pronoun="who",
        subordinator="until",
        subordinator_choices=("until", "when", "because", "although"),
        relation="time",
        relation_prompt="time",
        no_correction_sentence="The patient waits until the nurse calls.",
    ),
    Scene(
        context="market plan set",
        intro_sentence="Since the prices changed, the buyer revised the plan.",
        intro_missing_comma_sentence="Since the prices changed the buyer revised the plan.",
        postposed_sentence="The buyer revised the plan since the prices changed.",
        postposed_with_comma_sentence="The buyer revised the plan, since the prices changed.",
        compound_sentence="The prices changed, so the buyer revised the plan.",
        compound_complex_sentence="Since the prices changed, the buyer revised the plan, and the manager approved it.",
        simple_sentence="The buyer revised the plan.",
        dependent_clause="Since the prices changed",
        fragment_sentence="Since the prices changed.",
        repaired_fragment_sentence="Since the prices changed, the buyer revised the plan.",
        comma_splice_sentence="Since the prices changed, the buyer revised the plan, the manager approved it.",
        fused_sentence="Since the prices changed the buyer revised the plan the manager approved it.",
        fill_blank_sentence="The buyer revised the plan ____ the prices changed.",
        sentence_type_sentence="Since the prices changed, the buyer revised the plan, and the manager approved it.",
        sentence_type_answer="compound-complex sentence",
        clause_function_sentence="Since the prices changed, the buyer revised the plan.",
        clause_function_answer="adverb clause",
        relative_sentence="The plan that the buyer revised was simple.",
        relative_pronoun="that",
        subordinator="since",
        subordinator_choices=("since", "because", "after", "unless"),
        relation="cause",
        relation_prompt="cause",
        no_correction_sentence="The buyer revised the plan since the prices changed.",
    ),
)


FAMILY_SPECS: tuple[FamilySpec, ...] = (
    FamilySpec(
        base_family="complex-sentence-identification",
        choice_builder=_choices_from_fields(
            "intro_sentence",
            "simple_sentence",
            "compound_sentence",
            "compound_complex_sentence",
        ),
        answer_builder=_answer_field("intro_sentence"),
        explanation="A complex sentence has one independent clause and one dependent clause.",
        tags=("classification", "complex"),
    ),
    FamilySpec(
        base_family="dependent-clause-identification",
        choice_builder=_choices_from_fields(
            "dependent_clause",
            "simple_sentence",
            "compound_sentence",
            "fragment_sentence",
        ),
        answer_builder=_answer_field("dependent_clause"),
        explanation="The dependent clause cannot stand alone as a complete sentence.",
        tags=("classification", "dependent-clause"),
    ),
    FamilySpec(
        base_family="subordinating-conjunction-identification",
        choice_builder=_choices_from_fields("subordinator_choices"),
        answer_builder=_answer_field("subordinator"),
        explanation="The subordinating conjunction introduces the dependent clause.",
        tags=("grammar", "subordinator"),
    ),
    FamilySpec(
        base_family="relation-based-subordinator-choice",
        choice_builder=_choices_from_fields("subordinator_choices"),
        answer_builder=_answer_field("subordinator"),
        explanation="The conjunction should match the relationship between the two clauses.",
        tags=("selection", "relationship"),
    ),
    FamilySpec(
        base_family="subordinator-fill-in",
        choice_builder=_choices_from_fields("subordinator_choices"),
        answer_builder=_answer_field("subordinator"),
        explanation="The blank needs the subordinating conjunction that fits the sentence relationship.",
        tags=("completion", "subordinator"),
    ),
    FamilySpec(
        base_family="introductory-comma-revision",
        choice_builder=_choices_from_fields(
            "intro_sentence",
            "intro_missing_comma_sentence",
            "comma_splice_sentence",
            "fused_sentence",
        ),
        answer_builder=_answer_field("intro_sentence"),
        explanation="An introductory dependent clause should be followed by a comma.",
        tags=("revision", "comma"),
    ),
    FamilySpec(
        base_family="postposed-clause-revision",
        choice_builder=_choices_from_fields(
            "postposed_sentence",
            "postposed_with_comma_sentence",
            "comma_splice_sentence",
            "fused_sentence",
        ),
        answer_builder=_answer_field("postposed_sentence"),
        explanation="A dependent clause that follows the main clause usually does not need a comma.",
        tags=("revision", "order"),
    ),
    FamilySpec(
        base_family="sentence-type-classification",
        choice_builder=_fixed_choices(*SENTENCE_TYPE_CHOICES),
        answer_builder=_answer_field("sentence_type_answer"),
        explanation="Sentence type depends on the number and relationship of independent and dependent clauses.",
        tags=("classification", "sentence-type"),
    ),
    FamilySpec(
        base_family="clause-function-classification",
        choice_builder=_fixed_choices(*CLAUSE_FUNCTION_CHOICES),
        answer_builder=_answer_field("clause_function_answer"),
        explanation="Subordinate clauses can work as adverb, adjective, or noun clauses.",
        tags=("classification", "clause-function"),
    ),
    FamilySpec(
        base_family="relative-pronoun-identification",
        choice_builder=_fixed_choices(*RELATIVE_PRONOUN_CHOICES),
        answer_builder=_answer_field("relative_pronoun"),
        explanation="Relative words such as who, that, where, and when introduce relative clauses.",
        tags=("grammar", "relative"),
    ),
    FamilySpec(
        base_family="relative-clause-identification",
        choice_builder=_choices_from_fields(
            "relative_sentence",
            "simple_sentence",
            "compound_sentence",
            "intro_sentence",
        ),
        answer_builder=_answer_field("relative_sentence"),
        explanation="A relative clause describes a noun or pronoun.",
        tags=("classification", "relative-clause"),
    ),
    FamilySpec(
        base_family="fragment-repair",
        choice_builder=_choices_from_fields(
            "repaired_fragment_sentence",
            "fragment_sentence",
            "compound_sentence",
            "simple_sentence",
        ),
        answer_builder=_answer_field("repaired_fragment_sentence"),
        explanation="A fragment becomes complete only when it has the missing main clause.",
        tags=("repair", "fragment"),
    ),
    FamilySpec(
        base_family="coordination-vs-subordination-classification",
        choice_builder=_choices_from_fields(
            "intro_sentence",
            "compound_sentence",
            "simple_sentence",
            "compound_complex_sentence",
        ),
        answer_builder=_answer_field("intro_sentence"),
        explanation="Subordination creates unequal clause rank, unlike coordination.",
        tags=("classification", "coordination-vs-subordination"),
    ),
    FamilySpec(
        base_family="clause-order-revision",
        choice_builder=_choices_from_fields(
            "intro_sentence",
            "postposed_sentence",
            "intro_missing_comma_sentence",
            "fused_sentence",
        ),
        answer_builder=_answer_field("intro_sentence"),
        explanation="Moving the dependent clause to the front should preserve the comma pattern.",
        tags=("revision", "clause-order"),
    ),
    FamilySpec(
        base_family="no-correction-needed",
        choice_builder=_choices_from_fields(
            "no_correction_sentence",
            "comma_splice_sentence",
            "fused_sentence",
            "fragment_sentence",
        ),
        answer_builder=_answer_field("no_correction_sentence"),
        explanation="When the sentence is already correct, no revision is needed.",
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
