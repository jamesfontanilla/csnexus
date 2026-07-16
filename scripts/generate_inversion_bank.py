"""Generate the Verbal Ability / Sentence Structure / Inversion question bank."""

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
    / "inversion"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Structure"
SUBTOPIC = "Inversion"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

ROOT_TAG = "inversion"
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
    question_sentence: str
    question_auxiliary: str
    question_auxiliary_choices: tuple[str, str, str, str]
    subject_question_sentence: str
    object_question_sentence: str
    inversion_sentence: str
    normal_sentence: str
    wrong_sentence: str
    fixed_sentence: str
    negative_sentence: str
    negative_auxiliary: str
    negative_auxiliary_choices: tuple[str, str, str, str]
    negative_fill_sentence: str
    negative_normal_sentence: str
    locative_sentence: str
    locative_normal_sentence: str
    restrictive_sentence: str
    restrictive_normal_sentence: str
    emphatic_sentence: str
    emphatic_normal_sentence: str
    response_prompt: str
    response_answer: str
    response_so_sentence: str
    response_neither_sentence: str
    response_plain_sentence: str
    response_choices: tuple[str, str, str, str]
    hardly_sentence: str
    hardly_normal_sentence: str
    fronted_place_sentence: str
    fronted_place_normal_sentence: str
    trigger_answer: str
    trigger_choices: tuple[str, str, str, str]
    type_answer: str
    type_choices: tuple[str, str, str, str]
    no_correction_sentence: str
    no_correction_choices: tuple[str, str, str, str]


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
        "question_sentence": scene.question_sentence,
        "question_auxiliary": scene.question_auxiliary,
        "subject_question_sentence": scene.subject_question_sentence,
        "object_question_sentence": scene.object_question_sentence,
        "inversion_sentence": scene.inversion_sentence,
        "normal_sentence": scene.normal_sentence,
        "wrong_sentence": scene.wrong_sentence,
        "fixed_sentence": scene.fixed_sentence,
        "negative_sentence": scene.negative_sentence,
        "negative_auxiliary": scene.negative_auxiliary,
        "negative_fill_sentence": scene.negative_fill_sentence,
        "negative_normal_sentence": scene.negative_normal_sentence,
        "locative_sentence": scene.locative_sentence,
        "locative_normal_sentence": scene.locative_normal_sentence,
        "restrictive_sentence": scene.restrictive_sentence,
        "restrictive_normal_sentence": scene.restrictive_normal_sentence,
        "emphatic_sentence": scene.emphatic_sentence,
        "emphatic_normal_sentence": scene.emphatic_normal_sentence,
        "response_prompt": scene.response_prompt,
        "response_answer": scene.response_answer,
        "response_so_sentence": scene.response_so_sentence,
        "response_neither_sentence": scene.response_neither_sentence,
        "response_plain_sentence": scene.response_plain_sentence,
        "hardly_sentence": scene.hardly_sentence,
        "hardly_normal_sentence": scene.hardly_normal_sentence,
        "fronted_place_sentence": scene.fronted_place_sentence,
        "fronted_place_normal_sentence": scene.fronted_place_normal_sentence,
        "trigger_answer": scene.trigger_answer,
        "type_answer": scene.type_answer,
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


def _answer_field(field: str) -> Callable[[Scene], str]:
    def builder(scene: Scene) -> str:
        return str(getattr(scene, field))

    return builder


QUESTION_STEMS: dict[str, dict[str, str]] = {
    "inversion-identification": {
        "Easy": "Which sentence in the {context} set shows inversion?",
        "Medium": "From the {context} set, pick the line that reverses the usual subject-verb order.",
        "Hard": "In the {context} set, which option uses inverted word order instead of an ordinary statement?",
        "Ultra": "Select the sentence from the {context} set where the verb or auxiliary appears before the subject.",
    },
    "question-auxiliary-identification": {
        "Easy": "Which auxiliary appears before the subject in \"{question_sentence}\"?",
        "Medium": "In \"{question_sentence}\", which helping verb has been moved in front of the subject?",
        "Hard": "Which form is the fronted auxiliary in \"{question_sentence}\"?",
        "Ultra": "Identify the auxiliary that carries the inversion in \"{question_sentence}\".",
    },
    "wh-subject-no-inversion-identification": {
        "Easy": "Which question in the {context} set keeps normal order because the wh-word is the subject?",
        "Medium": "From the {context} set, pick the question that does not move an auxiliary before the subject.",
        "Hard": "In the {context} set, which line is a subject question rather than an inverted wh-question?",
        "Ultra": "Select the question from the {context} set where the wh-word itself acts as the subject.",
    },
    "negative-adverb-inversion-identification": {
        "Easy": "Which sentence in the {context} set uses inversion after a fronted negative word?",
        "Medium": "From the {context} set, choose the line that begins with a negative trigger and then inverts the order.",
        "Hard": "In the {context} set, which option shows formal negative inversion?",
        "Ultra": "Select the sentence from the {context} set where a negative trigger brings the auxiliary ahead of the subject.",
    },
    "negative-adverb-auxiliary-choice": {
        "Easy": "Which auxiliary completes the inverted negative pattern in \"{negative_fill_sentence}\"?",
        "Medium": "In \"{negative_fill_sentence}\", which helping verb belongs after the fronted negative trigger?",
        "Hard": "Choose the auxiliary that keeps the negative inversion correct in \"{negative_fill_sentence}\".",
        "Ultra": "Which fronted-negative structure in \"{negative_fill_sentence}\" needs the missing auxiliary?",
    },
    "locative-inversion-identification": {
        "Easy": "Which sentence in the {context} set shows place inversion?",
        "Medium": "From the {context} set, pick the line that starts with a place phrase and then inverts the order.",
        "Hard": "In the {context} set, which option places the verb before the subject after a location phrase?",
        "Ultra": "Select the line from the {context} set that uses locative inversion rather than ordinary order.",
    },
    "so-such-inversion-identification": {
        "Easy": "Which sentence in the {context} set uses so/such inversion for emphasis?",
        "Medium": "From the {context} set, pick the line where a fronted so or such phrase creates inversion.",
        "Hard": "In the {context} set, which option uses emphatic inversion with so or such?",
        "Ultra": "Select the sentence from the {context} set where emphasis pushes the verb ahead of the subject.",
    },
    "restrictive-fronting-inversion-identification": {
        "Easy": "Which sentence in the {context} set uses a fronted restrictive phrase and inversion?",
        "Medium": "From the {context} set, choose the line that begins with only, not until, or a similar trigger and then inverts the order.",
        "Hard": "In the {context} set, which option shows restrictive inversion?",
        "Ultra": "Select the sentence from the {context} set where the restrictive opener forces inversion.",
    },
    "response-inversion-identification": {
        "Easy": "Which short reply in the {context} set shows {response_prompt} with inversion?",
        "Medium": "From the {context} set, pick the brief response that uses inversion to show {response_prompt}.",
        "Hard": "In the {context} set, which reply is the correct inverted form for {response_prompt}?",
        "Ultra": "Select the short response from the {context} set that matches the earlier statement through inversion and shows {response_prompt}.",
    },
    "inversion-revision": {
        "Easy": "Which revision fixes the inversion error in \"{wrong_sentence}\"?",
        "Medium": "Choose the corrected version of \"{wrong_sentence}\" in the {context} set.",
        "Hard": "Select the sentence that repairs \"{wrong_sentence}\" without changing the meaning.",
        "Ultra": "Which revision restores the correct inverted pattern in \"{wrong_sentence}\"?",
    },
    "incorrect-inversion-diagnosis": {
        "Easy": "Which sentence in the {context} set is wrongly formed?",
        "Medium": "From the {context} set, pick the line that breaks the inversion rule.",
        "Hard": "In the {context} set, which option contains the inversion mistake?",
        "Ultra": "Select the sentence from the {context} set that would need repair.",
    },
    "normal-order-rewrite": {
        "Easy": "Which rewrite returns \"{inversion_sentence}\" to normal order?",
        "Medium": "Choose the plain-order version of \"{inversion_sentence}\" in the {context} set.",
        "Hard": "Select the sentence that keeps the same meaning but restores ordinary word order for \"{inversion_sentence}\".",
        "Ultra": "Which option rewrites \"{inversion_sentence}\" in standard declarative order?",
    },
    "trigger-word-choice": {
        "Easy": "Which opening word or phrase triggers the inversion in \"{inversion_sentence}\"?",
        "Medium": "In \"{inversion_sentence}\", which opening element makes the sentence invert?",
        "Hard": "Which trigger begins the inverted pattern in \"{inversion_sentence}\"?",
        "Ultra": "Identify the opening word or phrase that forces inversion in \"{inversion_sentence}\".",
    },
    "inversion-type-classification": {
        "Easy": "What kind of inversion is \"{inversion_sentence}\"?",
        "Medium": "Which label best describes the inversion pattern in \"{inversion_sentence}\"?",
        "Hard": "Classify \"{inversion_sentence}\" by inversion type.",
        "Ultra": "Name the inversion type shown in \"{inversion_sentence}\".",
    },
    "no-correction-needed": {
        "Easy": "Which sentence in the {context} set is already correct?",
        "Medium": "Choose the option in the {context} set that needs no revision.",
        "Hard": "Select the sentence in the {context} set that can stay exactly as written.",
        "Ultra": "Which line in the {context} set is already acceptable as it stands?",
    },
}


SCENES: tuple[Scene, ...] = (
    Scene(
        context="classroom question",
        question_sentence="Did the teacher finish the quiz?",
        question_auxiliary="did",
        question_auxiliary_choices=("did", "had", "was", "can"),
        subject_question_sentence="Who finished the quiz?",
        object_question_sentence="What did the teacher finish?",
        inversion_sentence="Did the teacher finish the quiz?",
        normal_sentence="The teacher finished the quiz.",
        wrong_sentence="Did the teacher finished the quiz?",
        fixed_sentence="Did the teacher finish the quiz?",
        negative_sentence="Never had the teacher seen such silence.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "did", "was", "can"),
        negative_fill_sentence="Never ____ the teacher seen such silence.",
        negative_normal_sentence="The teacher had never seen such silence.",
        locative_sentence="On the front desk lay the answer key.",
        locative_normal_sentence="The answer key lay on the front desk.",
        restrictive_sentence="Only after the bell rang did the class leave.",
        restrictive_normal_sentence="The class left only after the bell rang.",
        emphatic_sentence="So quiet was the room that every pencil sounded loud.",
        emphatic_normal_sentence="The room was so quiet that every pencil sounded loud.",
        response_prompt="agreement",
        response_answer="So do I.",
        response_so_sentence="So do I.",
        response_neither_sentence="Neither can we.",
        response_plain_sentence="I do too.",
        response_choices=("So do I.", "I do too.", "So I do.", "Do I so?"),
        hardly_sentence="Hardly had the quiz started when the fire alarm sounded.",
        hardly_normal_sentence="The fire alarm sounded soon after the quiz started.",
        fronted_place_sentence="Down the hallway came the principal.",
        fronted_place_normal_sentence="The principal came down the hallway.",
        trigger_answer="did",
        trigger_choices=("did", "had", "never", "so quiet"),
        type_answer="question inversion",
        type_choices=("question inversion", "negative inversion", "locative inversion", "response inversion"),
        no_correction_sentence="Did the teacher finish the quiz?",
        no_correction_choices=(
            "Did the teacher finish the quiz?",
            "Did the teacher finished the quiz?",
            "The teacher did finished the quiz?",
            "Did teacher the finish the quiz?",
        ),
    ),
    Scene(
        context="newsroom negative",
        question_sentence="Has the editor approved the draft?",
        question_auxiliary="has",
        question_auxiliary_choices=("has", "did", "had", "was"),
        subject_question_sentence="Who approved the draft?",
        object_question_sentence="What has the editor approved?",
        inversion_sentence="Never had the editor seen such a draft.",
        normal_sentence="The editor had never seen such a draft.",
        wrong_sentence="Never the editor had seen such a draft.",
        fixed_sentence="Never had the editor seen such a draft.",
        negative_sentence="Never had the editor seen such a draft.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "has", "did", "was"),
        negative_fill_sentence="Never ____ the editor seen such a draft.",
        negative_normal_sentence="The editor had never seen such a draft.",
        locative_sentence="Across the monitor flashed the headline.",
        locative_normal_sentence="The headline flashed across the monitor.",
        restrictive_sentence="Only after the editor signed off did the issue go to print.",
        restrictive_normal_sentence="The issue went to print only after the editor signed off.",
        emphatic_sentence="So sharp was the deadline that everyone skipped lunch.",
        emphatic_normal_sentence="The deadline was so sharp that everyone skipped lunch.",
        response_prompt="disagreement",
        response_answer="Neither can we.",
        response_so_sentence="So do I.",
        response_neither_sentence="Neither can we.",
        response_plain_sentence="We cannot either.",
        response_choices=("Neither can we.", "We cannot either.", "Neither we can.", "Can neither we?"),
        hardly_sentence="Hardly had the editor opened the email when another alert sounded.",
        hardly_normal_sentence="Another alert sounded soon after the editor opened the email.",
        fronted_place_sentence="Across the monitor flashed the headline.",
        fronted_place_normal_sentence="The headline flashed across the monitor.",
        trigger_answer="never",
        trigger_choices=("never", "has", "on the monitor", "so sharp"),
        type_answer="negative inversion",
        type_choices=("negative inversion", "question inversion", "locative inversion", "emphatic inversion"),
        no_correction_sentence="The editor had never seen such a draft.",
        no_correction_choices=(
            "The editor had never seen such a draft.",
            "Never the editor had seen such a draft.",
            "Never had the editor see such a draft.",
            "Never had editor the seen such a draft.",
        ),
    ),
    Scene(
        context="archive shelf",
        question_sentence="Was the librarian searching for the file?",
        question_auxiliary="was",
        question_auxiliary_choices=("was", "did", "had", "can"),
        subject_question_sentence="Who found the file?",
        object_question_sentence="What was the librarian searching for?",
        inversion_sentence="On the top shelf lay the file.",
        normal_sentence="The file lay on the top shelf.",
        wrong_sentence="On the top shelf the file lay.",
        fixed_sentence="On the top shelf lay the file.",
        negative_sentence="Rarely had the librarian found a file so quickly.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "did", "was", "can"),
        negative_fill_sentence="Rarely ____ the librarian found a file so quickly.",
        negative_normal_sentence="The librarian had rarely found a file so quickly.",
        locative_sentence="On the top shelf lay the file.",
        locative_normal_sentence="The file lay on the top shelf.",
        restrictive_sentence="Only after the card was stamped did the file move out.",
        restrictive_normal_sentence="The file moved out only after the card was stamped.",
        emphatic_sentence="So old was the archive that the labels faded.",
        emphatic_normal_sentence="The archive was so old that the labels faded.",
        response_prompt="agreement",
        response_answer="So was I.",
        response_so_sentence="So was I.",
        response_neither_sentence="Neither had they.",
        response_plain_sentence="I was too.",
        response_choices=("So was I.", "I was too.", "So I was.", "Was I so?"),
        hardly_sentence="Hardly had the librarian opened the cabinet when the power failed.",
        hardly_normal_sentence="The power failed soon after the librarian opened the cabinet.",
        fronted_place_sentence="At the far end stood the index cabinet.",
        fronted_place_normal_sentence="The index cabinet stood at the far end.",
        trigger_answer="on the top shelf",
        trigger_choices=("on the top shelf", "rarely", "only after", "so old"),
        type_answer="locative inversion",
        type_choices=("locative inversion", "negative inversion", "question inversion", "response inversion"),
        no_correction_sentence="On the top shelf lay the file.",
        no_correction_choices=(
            "On the top shelf lay the file.",
            "On the top shelf the file lay.",
            "On the top shelf layed the file.",
            "The file was lay on the top shelf.",
        ),
    ),
    Scene(
        context="office deadline",
        question_sentence="Had the manager signed the memo?",
        question_auxiliary="had",
        question_auxiliary_choices=("had", "did", "was", "can"),
        subject_question_sentence="Who signed the memo?",
        object_question_sentence="What had the manager signed?",
        inversion_sentence="Only after the manager signed the memo did the office close.",
        normal_sentence="The office closed only after the manager signed the memo.",
        wrong_sentence="Only after the manager signed the memo the office close.",
        fixed_sentence="Only after the manager signed the memo did the office close.",
        negative_sentence="Seldom had the office stayed open past the deadline.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "did", "was", "can"),
        negative_fill_sentence="Seldom ____ the office stayed open past the deadline.",
        negative_normal_sentence="The office had seldom stayed open past the deadline.",
        locative_sentence="At the reception desk stood the schedule.",
        locative_normal_sentence="The schedule stood at the reception desk.",
        restrictive_sentence="Only after the manager signed the memo did the office close.",
        restrictive_normal_sentence="The office closed only after the manager signed the memo.",
        emphatic_sentence="So strict was the deadline that nobody joked about it.",
        emphatic_normal_sentence="The deadline was so strict that nobody joked about it.",
        response_prompt="disagreement",
        response_answer="Neither had they.",
        response_so_sentence="So did the crowd.",
        response_neither_sentence="Neither had they.",
        response_plain_sentence="They had not either.",
        response_choices=("Neither had they.", "They had not either.", "Neither they had.", "Had neither they?"),
        hardly_sentence="No sooner had the manager signed the memo than the office closed.",
        hardly_normal_sentence="The office closed soon after the manager signed the memo.",
        fronted_place_sentence="In the filing room waited the final copy.",
        fronted_place_normal_sentence="The final copy waited in the filing room.",
        trigger_answer="only after",
        trigger_choices=("only after", "had", "at the reception desk", "so strict"),
        type_answer="restrictive inversion",
        type_choices=("restrictive inversion", "negative inversion", "locative inversion", "question inversion"),
        no_correction_sentence="Only after the manager signed the memo did the office close.",
        no_correction_choices=(
            "Only after the manager signed the memo did the office close.",
            "Only after the manager signed the memo the office close.",
            "Only after the manager signed the memo did the office closes.",
            "The office close only after the manager signed the memo.",
        ),
    ),
    Scene(
        context="storm emphasis",
        question_sentence="Was the storm fierce?",
        question_auxiliary="was",
        question_auxiliary_choices=("was", "did", "had", "can"),
        subject_question_sentence="What shook the windows?",
        object_question_sentence="What did the storm shake?",
        inversion_sentence="So fierce was the storm that the windows shook.",
        normal_sentence="The storm was so fierce that the windows shook.",
        wrong_sentence="So fierce the storm was that the windows shook.",
        fixed_sentence="So fierce was the storm that the windows shook.",
        negative_sentence="Rarely had the town seen such wind.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "was", "did", "can"),
        negative_fill_sentence="Rarely ____ the town seen such wind.",
        negative_normal_sentence="The town had rarely seen such wind.",
        locative_sentence="On the ridge stood the lookout.",
        locative_normal_sentence="The lookout stood on the ridge.",
        restrictive_sentence="Only after midnight did the wind ease.",
        restrictive_normal_sentence="The wind eased only after midnight.",
        emphatic_sentence="So fierce was the storm that the windows shook.",
        emphatic_normal_sentence="The storm was so fierce that the windows shook.",
        response_prompt="agreement",
        response_answer="So did the crowd.",
        response_so_sentence="So did the crowd.",
        response_neither_sentence="Neither should we.",
        response_plain_sentence="The crowd did too.",
        response_choices=("So did the crowd.", "The crowd did so.", "So the crowd did.", "Did the crowd so?"),
        hardly_sentence="Hardly had the power gone out when the siren sounded.",
        hardly_normal_sentence="The siren sounded soon after the power went out.",
        fronted_place_sentence="Down the hill rolled the storm clouds.",
        fronted_place_normal_sentence="The storm clouds rolled down the hill.",
        trigger_answer="so fierce",
        trigger_choices=("so fierce", "was", "on the ridge", "rarely"),
        type_answer="emphatic inversion",
        type_choices=("emphatic inversion", "negative inversion", "locative inversion", "question inversion"),
        no_correction_sentence="So fierce was the storm that the windows shook.",
        no_correction_choices=(
            "So fierce was the storm that the windows shook.",
            "So fierce the storm was that the windows shook.",
            "So fierce was the storm, the windows shook.",
            "The windows shook so fierce was the storm.",
        ),
    ),
    Scene(
        context="hallway agreement",
        question_sentence="Do you hear the announcement?",
        question_auxiliary="do",
        question_auxiliary_choices=("do", "did", "was", "had"),
        subject_question_sentence="Who heard the announcement?",
        object_question_sentence="What do you hear?",
        inversion_sentence="So do I.",
        normal_sentence="I do too.",
        wrong_sentence="So I do.",
        fixed_sentence="So do I.",
        negative_sentence="Hardly had the speaker begun when the crowd settled down.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "do", "was", "can"),
        negative_fill_sentence="Hardly ____ the speaker begun when the crowd settled down.",
        negative_normal_sentence="The crowd settled down soon after the speaker began.",
        locative_sentence="Down the corridor came the announcement.",
        locative_normal_sentence="The announcement came down the corridor.",
        restrictive_sentence="Only after the bell rang did the students leave.",
        restrictive_normal_sentence="The students left only after the bell rang.",
        emphatic_sentence="So clear was the announcement that everyone stopped talking.",
        emphatic_normal_sentence="The announcement was so clear that everyone stopped talking.",
        response_prompt="agreement",
        response_answer="So do I.",
        response_so_sentence="So do I.",
        response_neither_sentence="Neither can we.",
        response_plain_sentence="I do too.",
        response_choices=("So do I.", "I do too.", "So I do.", "Do I so?"),
        hardly_sentence="Hardly had the speaker begun when the crowd settled down.",
        hardly_normal_sentence="The crowd settled down soon after the speaker began.",
        fronted_place_sentence="Down the corridor came the announcement.",
        fronted_place_normal_sentence="The announcement came down the corridor.",
        trigger_answer="so",
        trigger_choices=("so", "do", "never", "only after"),
        type_answer="response inversion",
        type_choices=("response inversion", "question inversion", "negative inversion", "locative inversion"),
        no_correction_sentence="So do I.",
        no_correction_choices=(
            "So do I.",
            "So I do.",
            "I do so.",
            "Do I so?",
        ),
    ),
    Scene(
        context="hallway disagreement",
        question_sentence="Can the team agree to the schedule?",
        question_auxiliary="can",
        question_auxiliary_choices=("can", "did", "had", "was"),
        subject_question_sentence="Who agreed to the schedule?",
        object_question_sentence="What can the team agree to?",
        inversion_sentence="Neither can we.",
        normal_sentence="We cannot either.",
        wrong_sentence="Neither we can.",
        fixed_sentence="Neither can we.",
        negative_sentence="Never had the team seen such a difficult schedule.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "did", "can", "was"),
        negative_fill_sentence="Never ____ the team seen such a difficult schedule.",
        negative_normal_sentence="The team had never seen such a difficult schedule.",
        locative_sentence="At the doorway stood the coach.",
        locative_normal_sentence="The coach stood at the doorway.",
        restrictive_sentence="Only after the survey ended did the group respond.",
        restrictive_normal_sentence="The group responded only after the survey ended.",
        emphatic_sentence="So demanding was the schedule that breaks vanished.",
        emphatic_normal_sentence="The schedule was so demanding that breaks vanished.",
        response_prompt="disagreement",
        response_answer="Neither can we.",
        response_so_sentence="So can I.",
        response_neither_sentence="Neither can we.",
        response_plain_sentence="We cannot either.",
        response_choices=("Neither can we.", "We cannot either.", "Neither we can.", "Can neither we?"),
        hardly_sentence="Hardly had the team arrived when the meeting began.",
        hardly_normal_sentence="The meeting began soon after the team arrived.",
        fronted_place_sentence="Across the room waited the coach.",
        fronted_place_normal_sentence="The coach waited across the room.",
        trigger_answer="neither",
        trigger_choices=("neither", "so", "never", "only after"),
        type_answer="response inversion",
        type_choices=("response inversion", "question inversion", "negative inversion", "locative inversion"),
        no_correction_sentence="Neither can we.",
        no_correction_choices=(
            "Neither can we.",
            "Neither we can.",
            "We can neither.",
            "Can neither we?",
        ),
    ),
    Scene(
        context="gate alarm",
        question_sentence="Did the guard open the gate?",
        question_auxiliary="did",
        question_auxiliary_choices=("did", "had", "was", "can"),
        subject_question_sentence="Who opened the gate?",
        object_question_sentence="What did the guard open?",
        inversion_sentence="Hardly had the guard opened the gate when the alarm sounded.",
        normal_sentence="The alarm sounded soon after the guard opened the gate.",
        wrong_sentence="Hardly the guard had opened the gate when the alarm sounded.",
        fixed_sentence="Hardly had the guard opened the gate when the alarm sounded.",
        negative_sentence="Hardly had the guard opened the gate when the alarm sounded.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "did", "was", "can"),
        negative_fill_sentence="Hardly ____ the guard opened the gate when the alarm sounded.",
        negative_normal_sentence="The alarm sounded soon after the guard opened the gate.",
        locative_sentence="By the gate stood the watchman.",
        locative_normal_sentence="The watchman stood by the gate.",
        restrictive_sentence="Only after the light flashed did the guard move.",
        restrictive_normal_sentence="The guard moved only after the light flashed.",
        emphatic_sentence="So sudden was the alarm that the guard froze.",
        emphatic_normal_sentence="The alarm was so sudden that the guard froze.",
        response_prompt="disagreement",
        response_answer="Neither did the clerk.",
        response_so_sentence="So did the clerk.",
        response_neither_sentence="Neither did the clerk.",
        response_plain_sentence="The clerk did not either.",
        response_choices=("Neither did the clerk.", "The clerk did not either.", "Neither the clerk did.", "Did neither the clerk?"),
        hardly_sentence="Hardly had the guard opened the gate when the alarm sounded.",
        hardly_normal_sentence="The alarm sounded soon after the guard opened the gate.",
        fronted_place_sentence="By the gate stood the watchman.",
        fronted_place_normal_sentence="The watchman stood by the gate.",
        trigger_answer="hardly",
        trigger_choices=("hardly", "did", "by the gate", "so sudden"),
        type_answer="negative inversion",
        type_choices=("negative inversion", "question inversion", "emphatic inversion", "locative inversion"),
        no_correction_sentence="Hardly had the guard opened the gate when the alarm sounded.",
        no_correction_choices=(
            "Hardly had the guard opened the gate when the alarm sounded.",
            "Hardly the guard had opened the gate when the alarm sounded.",
            "Hardly had the guard opened the gate, the alarm sounded.",
            "The alarm sounded when hardly had the guard opened the gate.",
        ),
    ),
    Scene(
        context="parade street",
        question_sentence="Did the parade pass the school?",
        question_auxiliary="did",
        question_auxiliary_choices=("did", "was", "had", "can"),
        subject_question_sentence="Who watched the parade?",
        object_question_sentence="What did the crowd watch?",
        inversion_sentence="Down the road came the parade.",
        normal_sentence="The parade came down the road.",
        wrong_sentence="Down the road the parade came.",
        fixed_sentence="Down the road came the parade.",
        negative_sentence="Rarely had the crowd seen such color.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "did", "was", "can"),
        negative_fill_sentence="Rarely ____ the crowd seen such color.",
        negative_normal_sentence="The crowd had rarely seen such color.",
        locative_sentence="Down the road came the parade.",
        locative_normal_sentence="The parade came down the road.",
        restrictive_sentence="Only after the band arrived did the crowd cheer.",
        restrictive_normal_sentence="The crowd cheered only after the band arrived.",
        emphatic_sentence="So bright was the parade that everyone waved.",
        emphatic_normal_sentence="The parade was so bright that everyone waved.",
        response_prompt="agreement",
        response_answer="So did the parade.",
        response_so_sentence="So did the parade.",
        response_neither_sentence="Neither did the clerk.",
        response_plain_sentence="The parade did too.",
        response_choices=("So did the parade.", "The parade did so.", "So the parade did.", "Did the parade so?"),
        hardly_sentence="Hardly had the parade started when the drums rolled.",
        hardly_normal_sentence="The drums rolled soon after the parade started.",
        fronted_place_sentence="At the corner stood the balloon vendor.",
        fronted_place_normal_sentence="The balloon vendor stood at the corner.",
        trigger_answer="down the road",
        trigger_choices=("down the road", "did", "never", "so bright"),
        type_answer="locative inversion",
        type_choices=("locative inversion", "negative inversion", "question inversion", "emphatic inversion"),
        no_correction_sentence="Down the road came the parade.",
        no_correction_choices=(
            "Down the road came the parade.",
            "Down the road the parade came.",
            "Down the road did come the parade.",
            "The parade did came down the road.",
        ),
    ),
    Scene(
        context="library revision",
        question_sentence="Has the clerk returned the book?",
        question_auxiliary="has",
        question_auxiliary_choices=("has", "did", "was", "can"),
        subject_question_sentence="Who returned the book?",
        object_question_sentence="What has the clerk returned?",
        inversion_sentence="Never had the librarian seen such patience.",
        normal_sentence="The librarian had never seen such patience.",
        wrong_sentence="Never the librarian had seen such patience.",
        fixed_sentence="Never had the librarian seen such patience.",
        negative_sentence="Never had the librarian seen such patience.",
        negative_auxiliary="had",
        negative_auxiliary_choices=("had", "has", "did", "was"),
        negative_fill_sentence="Never ____ the librarian seen such patience.",
        negative_normal_sentence="The librarian had never seen such patience.",
        locative_sentence="On the reading table rested the book.",
        locative_normal_sentence="The book rested on the reading table.",
        restrictive_sentence="Only after the last page was copied did the librarian close the file.",
        restrictive_normal_sentence="The librarian closed the file only after the last page was copied.",
        emphatic_sentence="So quiet was the room that even the clock sounded loud.",
        emphatic_normal_sentence="The room was so quiet that even the clock sounded loud.",
        response_prompt="disagreement",
        response_answer="Neither was the book.",
        response_so_sentence="So was the book.",
        response_neither_sentence="Neither was the book.",
        response_plain_sentence="The book was not either.",
        response_choices=("Neither was the book.", "The book was not either.", "Neither the book was.", "Was neither the book?"),
        hardly_sentence="Hardly had the clerk returned the book when another patron arrived.",
        hardly_normal_sentence="Another patron arrived soon after the clerk returned the book.",
        fronted_place_sentence="At the reference desk waited the catalog.",
        fronted_place_normal_sentence="The catalog waited at the reference desk.",
        trigger_answer="never",
        trigger_choices=("never", "has", "on the reading table", "so quiet"),
        type_answer="negative inversion",
        type_choices=("negative inversion", "question inversion", "locative inversion", "response inversion"),
        no_correction_sentence="Never had the librarian seen such patience.",
        no_correction_choices=(
            "Never had the librarian seen such patience.",
            "Never the librarian had seen such patience.",
            "Never had the librarian see such patience.",
            "The librarian had never seen such patience, never.",
        ),
    ),
)


FAMILY_SPECS: tuple[FamilySpec, ...] = (
    FamilySpec(
        base_family="inversion-identification",
        choice_builder=_choices_from_fields("inversion_sentence", "subject_question_sentence", "object_question_sentence", "normal_sentence"),
        answer_builder=_answer_field("inversion_sentence"),
        explanation="Inversion is the pattern where the verb or auxiliary appears before the subject.",
        tags=("classification", "word-order"),
    ),
    FamilySpec(
        base_family="question-auxiliary-identification",
        choice_builder=_choices_from_fields("question_auxiliary_choices"),
        answer_builder=_answer_field("question_auxiliary"),
        explanation="Question inversion usually moves the auxiliary in front of the subject.",
        tags=("grammar", "question"),
    ),
    FamilySpec(
        base_family="wh-subject-no-inversion-identification",
        choice_builder=_choices_from_fields("subject_question_sentence", "object_question_sentence", "question_sentence", "normal_sentence"),
        answer_builder=_answer_field("subject_question_sentence"),
        explanation="A wh-word that acts as the subject does not need inversion.",
        tags=("question", "wh-subject"),
    ),
    FamilySpec(
        base_family="negative-adverb-inversion-identification",
        choice_builder=_choices_from_fields("negative_sentence", "question_sentence", "object_question_sentence", "normal_sentence"),
        answer_builder=_answer_field("negative_sentence"),
        explanation="A fronted negative trigger can force inversion in formal English.",
        tags=("negative", "inversion"),
    ),
    FamilySpec(
        base_family="negative-adverb-auxiliary-choice",
        choice_builder=_choices_from_fields("negative_auxiliary_choices"),
        answer_builder=_answer_field("negative_auxiliary"),
        explanation="The auxiliary must move ahead of the subject after the negative trigger.",
        tags=("negative", "auxiliary"),
    ),
    FamilySpec(
        base_family="locative-inversion-identification",
        choice_builder=_choices_from_fields("locative_sentence", "question_sentence", "subject_question_sentence", "normal_sentence"),
        answer_builder=_answer_field("locative_sentence"),
        explanation="Locative inversion starts with a place phrase and then reverses the usual order.",
        tags=("locative", "place"),
    ),
    FamilySpec(
        base_family="so-such-inversion-identification",
        choice_builder=_choices_from_fields("emphatic_sentence", "question_sentence", "object_question_sentence", "normal_sentence"),
        answer_builder=_answer_field("emphatic_sentence"),
        explanation="So and such can trigger inversion when a writer wants emphasis.",
        tags=("emphasis", "style"),
    ),
    FamilySpec(
        base_family="restrictive-fronting-inversion-identification",
        choice_builder=_choices_from_fields("restrictive_sentence", "question_sentence", "object_question_sentence", "normal_sentence"),
        answer_builder=_answer_field("restrictive_sentence"),
        explanation="Restrictive openers such as only after or not until often trigger inversion.",
        tags=("restrictive", "fronting"),
    ),
    FamilySpec(
        base_family="response-inversion-identification",
        choice_builder=_choices_from_fields("response_choices"),
        answer_builder=_answer_field("response_answer"),
        explanation="Short responses such as so do I or neither can we use inversion too.",
        tags=("response", "short-reply"),
    ),
    FamilySpec(
        base_family="inversion-revision",
        choice_builder=_choices_from_fields("fixed_sentence", "wrong_sentence", "subject_question_sentence", "object_question_sentence"),
        answer_builder=_answer_field("fixed_sentence"),
        explanation="The corrected revision must repair the inverted word order without changing the meaning.",
        tags=("revision", "repair"),
    ),
    FamilySpec(
        base_family="incorrect-inversion-diagnosis",
        choice_builder=_choices_from_fields("wrong_sentence", "fixed_sentence", "subject_question_sentence", "object_question_sentence"),
        answer_builder=_answer_field("wrong_sentence"),
        explanation="Only one option contains the inversion error; the others are acceptable forms.",
        tags=("diagnosis", "error"),
    ),
    FamilySpec(
        base_family="normal-order-rewrite",
        choice_builder=_choices_from_fields("normal_sentence", "wrong_sentence", "subject_question_sentence", "object_question_sentence"),
        answer_builder=_answer_field("normal_sentence"),
        explanation="Normal order restores the usual subject-before-verb pattern.",
        tags=("rewrite", "normal-order"),
    ),
    FamilySpec(
        base_family="trigger-word-choice",
        choice_builder=_choices_from_fields("trigger_choices"),
        answer_builder=_answer_field("trigger_answer"),
        explanation="The trigger is the opening word or phrase that causes inversion.",
        tags=("trigger", "selection"),
    ),
    FamilySpec(
        base_family="inversion-type-classification",
        choice_builder=_choices_from_fields("type_choices"),
        answer_builder=_answer_field("type_answer"),
        explanation="Different inversion patterns have different labels, such as question, negative, locative, or response inversion.",
        tags=("classification", "type"),
    ),
    FamilySpec(
        base_family="no-correction-needed",
        choice_builder=_choices_from_fields("no_correction_choices"),
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
            raise ValueError(f"missing explanation at id {index}")

        question_text = str(question.get("question", ""))
        for banned_phrase in banned_phrases:
            if banned_phrase in question_text:
                raise ValueError(f"banned stem detected at id {index}: {banned_phrase}")


def _write_bank(path: Path, questions: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    questions = _build_bank()
    _validate_bank(questions)
    _write_bank(OUTPUT_PATH, questions)
    print(f"Wrote {len(questions)} questions to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
