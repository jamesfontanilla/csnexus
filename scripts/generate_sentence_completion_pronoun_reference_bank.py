"""Generate the Verbal Ability / Sentence Completion / Pronoun Reference bank.

The bank centers on antecedent tracking and pronoun choice:

- singular and plural reference
- possessive reference
- reflexive reference
- indefinite antecedents
- relative pronouns

Each difficulty band contains 150 items, for 600 items total. The bank is
deterministic and writes directly to the seed tree so the reset script can
pick it up automatically.
"""

from __future__ import annotations

import json
import random
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "sentence-completion"
    / "pronoun-reference"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Pronoun Reference"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "singular-reference",
    "plural-reference",
    "possessive-reference",
    "reflexive-reference",
    "indefinite-reference",
    "relative-reference",
)

QUESTION_STEMS = {
    "singular-reference": [
        "Which pronoun best completes the sentence below",
        "Which choice keeps the reference clear",
        "Which option best fits the pronoun reference",
        "Which pronoun most precisely completes the sentence below",
    ],
    "plural-reference": [
        "Which pronoun best completes the sentence below",
        "Which choice keeps the reference clear",
        "Which option best fits the pronoun reference",
        "Which pronoun most precisely completes the sentence below",
    ],
    "possessive-reference": [
        "Which possessive form best completes the sentence below",
        "Which choice best shows ownership",
        "Which option best fits the pronoun reference",
        "Which possessive word most precisely completes the sentence below",
    ],
    "reflexive-reference": [
        "Which reflexive pronoun best completes the sentence below",
        "Which choice points back to the subject",
        "Which option best fits the pronoun reference",
        "Which reflexive word most precisely completes the sentence below",
    ],
    "indefinite-reference": [
        "Which phrase best completes the sentence below",
        "Which pronoun best fits a singular indefinite antecedent",
        "Which option best matches the pronoun reference",
        "Which expression most precisely completes the sentence below",
    ],
    "relative-reference": [
        "Which relative pronoun best completes the sentence below",
        "Which choice best links the clause to the noun",
        "Which option best fits the pronoun reference",
        "Which relative word most precisely completes the sentence below",
    ],
}

DIFFICULTY_PREFIXES = {
    "Easy": "",
    "Medium": "During a routine review, ",
    "Hard": "During a routine review, after a second check, ",
    "Ultra": "During a routine review, after a second check and a tight deadline, ",
}


@dataclass(frozen=True)
class GroupSpec:
    family: str
    answer: str
    choice_key: str
    note: str
    templates: tuple[str, str, str, str, str]


def _cap_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return text
    return text[0].upper() + text[1:]


def _normalize_sentence(sentence: str) -> str:
    sentence = re.sub(r"\s+", " ", sentence.strip())
    if sentence and sentence[-1] not in ".!?":
        sentence += "."
    return sentence


def _answer_descriptor(answer: str) -> str:
    return "phrase" if " " in answer else "pronoun"


def _build_choices(choice_key: str, rng: random.Random) -> list[str]:
    pool = CHOICE_POOLS.get(choice_key)
    if pool is None:
        raise KeyError(f"missing choice pool for key: {choice_key}")
    choices = list(dict.fromkeys(pool))
    if len(choices) != 4:
        raise ValueError(f"choice pool for {choice_key!r} must contain 4 distinct items")
    rng.shuffle(choices)
    return choices


def _question_stem(family: str, difficulty: str, index: int) -> str:
    stems = QUESTION_STEMS[family]
    stem = stems[(index + DIFFICULTY_ORDER.index(difficulty)) % len(stems)]
    return stem.rstrip("?.!")


def _difficulty_wrap(sentence: str, difficulty: str) -> str:
    prefix = DIFFICULTY_PREFIXES[difficulty]
    if not prefix:
        return _cap_sentence(_normalize_sentence(sentence))
    return _cap_sentence(_normalize_sentence(f"{prefix}{sentence}"))


def _build_explanation(answer: str, note: str) -> str:
    descriptor = _answer_descriptor(answer)
    return f"The sentence needs the {descriptor} {answer} because {note}."


def _make_item(
    *,
    family: str,
    answer: str,
    choice_key: str,
    note: str,
    sentence: str,
    difficulty: str,
    index: int,
) -> dict[str, object]:
    rng = random.Random(f"{family}:{choice_key}:{difficulty}:{index}")
    wrapped_sentence = _difficulty_wrap(sentence, difficulty)
    question = _question_stem(family, difficulty, index)
    question_text = f'{question}: "{wrapped_sentence}"'
    choices = _build_choices(choice_key, rng)
    explanation = _build_explanation(answer, note)
    tags = [family, difficulty.lower(), "pronoun-reference"]

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question_text,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": tags,
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _validate_bank(questions: list[dict[str, object]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [int(question["id"]) for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise ValueError(f"unexpected difficulty distribution: {dict(counts)}")

    family_counts = Counter(str(question["tags"][0]) for question in questions)  # type: ignore[index]
    expected_family_counts = {family: 100 for family in FAMILY_ORDER}
    if family_counts != expected_family_counts:
        raise ValueError(f"unexpected family distribution: {dict(family_counts)}")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise ValueError("question texts are not unique")

    seen_choices: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        choices = [str(choice) for choice in question["choices"]]  # type: ignore[index]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")
        key = (str(question["question"]), tuple(sorted(choices)))
        if key in seen_choices:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_choices.add(key)


def _write_bank(questions: list[dict[str, object]]) -> None:
    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")


def main() -> int:
    questions: list[dict[str, object]] = []
    index = 1
    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for group in GROUPS_BY_FAMILY[family]:
                for template in group.templates:
                    questions.append(
                        _make_item(
                            family=family,
                            answer=group.answer,
                            choice_key=group.choice_key,
                            note=group.note,
                            sentence=template,
                            difficulty=difficulty,
                            index=index,
                        )
                    )
                    index += 1

    _validate_bank(questions)
    _write_bank(questions)
    return 0


CHOICE_POOLS: dict[str, list[str]] = {
    "it": ["it", "he", "she", "they"],
    "he": ["he", "she", "it", "they"],
    "she": ["she", "he", "it", "they"],
    "him_obj": ["him", "her", "them", "it"],
    "her_obj": ["her", "him", "them", "it"],
    "they": ["they", "it", "he", "she"],
    "them": ["them", "him", "her", "it"],
    "their_plural": ["their", "its", "his", "her"],
    "theirs": ["theirs", "their", "its", "his"],
    "themselves": ["themselves", "himself", "herself", "itself"],
    "his": ["his", "her", "their", "its"],
    "her_poss": ["her", "his", "their", "its"],
    "its": ["its", "his", "her", "their"],
    "whose": ["whose", "who", "which", "that"],
    "himself": ["himself", "herself", "itself", "themselves"],
    "herself": ["herself", "himself", "itself", "themselves"],
    "itself": ["itself", "himself", "herself", "themselves"],
    "ourselves": ["ourselves", "themselves", "himself", "herself"],
    "he_or_she": ["he or she", "he", "she", "they"],
    "him_or_her": ["him or her", "him", "her", "them"],
    "his_or_her": ["his or her", "his", "her", "their"],
    "who": ["who", "whom", "whose", "which"],
    "whom": ["whom", "who", "whose", "which"],
    "which": ["which", "who", "whom", "that"],
    "that": ["that", "which", "who", "whom"],
}


GROUPS_BY_FAMILY: dict[str, list[GroupSpec]] = {
    "singular-reference": [
        GroupSpec(
            family="singular-reference",
            answer="it",
            choice_key="it",
            note="the antecedent is a singular thing or idea",
            templates=(
                "the report was inaccurate, so ____ had to be corrected.",
                "the memo was complete, and ____ was filed immediately.",
                "the printer jammed because ____ was overused.",
                "the schedule changed, but ____ still worked well.",
                "the policy was revised, and ____ was posted online.",
            ),
        ),
        GroupSpec(
            family="singular-reference",
            answer="he",
            choice_key="he",
            note="the antecedent is a singular male person",
            templates=(
                "daniel reviewed the records, and ____ signed the memo.",
                "carlos checked the figures because ____ noticed an error.",
                "miguel called the office, and ____ requested a copy.",
                "ben submitted the form, and ____ left the counter.",
                "mr. reyes thanked the clerk after ____ found the missing page.",
            ),
        ),
        GroupSpec(
            family="singular-reference",
            answer="she",
            choice_key="she",
            note="the antecedent is a singular female person",
            templates=(
                "maria reviewed the records, and ____ signed the memo.",
                "sofia checked the figures because ____ noticed an error.",
                "ana called the office, and ____ requested a copy.",
                "angela submitted the form, and ____ left the counter.",
                "ms. cruz thanked the clerk after ____ found the missing page.",
            ),
        ),
        GroupSpec(
            family="singular-reference",
            answer="him",
            choice_key="him_obj",
            note="the pronoun follows a verb and takes object form",
            templates=(
                "the supervisor called daniel and asked the clerk to meet ____ at noon.",
                "the assistant guided carlos to the counter before thanking ____ for waiting.",
                "the officer saw ben outside and invited ____ inside.",
                "the director praised miguel after meeting ____ in the lobby.",
                "the clerk handed mr. reyes the file because the office needed ____ to sign it.",
            ),
        ),
        GroupSpec(
            family="singular-reference",
            answer="her",
            choice_key="her_obj",
            note="the pronoun follows a verb and takes object form",
            templates=(
                "the supervisor called maria and asked the clerk to meet ____ at noon.",
                "the assistant guided sofia to the counter before thanking ____ for waiting.",
                "the officer saw ana outside and invited ____ inside.",
                "the director praised angela after meeting ____ in the lobby.",
                "the clerk handed ms. cruz the file because the office needed ____ to sign it.",
            ),
        ),
    ],
    "plural-reference": [
        GroupSpec(
            family="plural-reference",
            answer="they",
            choice_key="they",
            note="the antecedent is plural and the pronoun is the subject",
            templates=(
                "the officers reviewed the forms, and ____ returned to the office.",
                "the files were sorted, and ____ were sent to storage.",
                "the clerks finished early because ____ worked together.",
                "the teams met in the hall, and ____ discussed the plan.",
                "the reports were revised, and ____ became easier to read.",
            ),
        ),
        GroupSpec(
            family="plural-reference",
            answer="them",
            choice_key="them",
            note="the pronoun follows a verb or preposition and takes object form",
            templates=(
                "the supervisor called the officers and asked the clerk to meet ____ at noon.",
                "the assistant guided the workers to the counter before thanking ____ for waiting.",
                "the officer saw the files outside and moved ____ inside.",
                "the director praised the teams after meeting ____ in the lobby.",
                "the clerk handed the reports to the manager because the office needed to review ____ again.",
            ),
        ),
        GroupSpec(
            family="plural-reference",
            answer="their",
            choice_key="their_plural",
            note="the pronoun shows ownership for a plural antecedent",
            templates=(
                "the officers reviewed ____ forms before leaving.",
                "the workers checked ____ badges at the door.",
                "the teams compared ____ notes after the meeting.",
                "the clerks organized ____ desks before lunch.",
                "the reporters updated ____ drafts at the end of the day.",
            ),
        ),
        GroupSpec(
            family="plural-reference",
            answer="theirs",
            choice_key="theirs",
            note="the pronoun stands alone and shows possession",
            templates=(
                "the blue folders on the shelf are ____.",
                "the awards on the wall are ____.",
                "the two seats near the window are ____.",
                "the copies in the cabinet are ____.",
                "the final summary is ____.",
            ),
        ),
        GroupSpec(
            family="plural-reference",
            answer="themselves",
            choice_key="themselves",
            note="the action returns to the plural subject",
            templates=(
                "the officers prepared the room by ____.",
                "the workers reminded ____ to check the list.",
                "the teams trained ____ before the audit.",
                "the clerks praised ____ for the careful work.",
                "the volunteers congratulated ____ on the success.",
            ),
        ),
    ],
    "possessive-reference": [
        GroupSpec(
            family="possessive-reference",
            answer="his",
            choice_key="his",
            note="the pronoun shows ownership for a singular male antecedent",
            templates=(
                "daniel packed ____ files before leaving.",
                "carlos left ____ badge on the desk.",
                "miguel checked ____ schedule twice.",
                "ben handed over ____ report to the supervisor.",
                "mr. reyes kept ____ notebook in the drawer.",
            ),
        ),
        GroupSpec(
            family="possessive-reference",
            answer="her",
            choice_key="her_poss",
            note="the pronoun shows ownership for a singular female antecedent",
            templates=(
                "maria packed ____ files before leaving.",
                "sofia left ____ badge on the desk.",
                "ana checked ____ schedule twice.",
                "angela handed over ____ report to the supervisor.",
                "ms. cruz kept ____ notebook in the drawer.",
            ),
        ),
        GroupSpec(
            family="possessive-reference",
            answer="its",
            choice_key="its",
            note="the pronoun shows ownership for a singular thing or idea",
            templates=(
                "the printer lost ____ cable after the move.",
                "the report kept ____ original title.",
                "the machine needed cleaning because ____ fan was dusty.",
                "the office misplaced ____ key after lunch.",
                "the policy showed ____ main purpose clearly.",
            ),
        ),
        GroupSpec(
            family="possessive-reference",
            answer="their",
            choice_key="their_plural",
            note="the pronoun shows ownership for a plural antecedent",
            templates=(
                "the officers checked ____ badges at the door.",
                "the workers packed ____ tools before leaving.",
                "the committees sent ____ notes after the meeting.",
                "the teams compared ____ plans before the vote.",
                "the staff organized ____ desks before lunch.",
            ),
        ),
        GroupSpec(
            family="possessive-reference",
            answer="whose",
            choice_key="whose",
            note="the pronoun shows possession inside a relative clause",
            templates=(
                "the clerk, ____ badge was missing, reported the loss.",
                "the analyst, ____ notes were incomplete, asked for time.",
                "the supervisor, ____ file was misplaced, apologized to the director.",
                "the officer, ____ report was delayed, searched the cabinet.",
                "the manager, ____ memo was revised, approved the update.",
            ),
        ),
    ],
    "reflexive-reference": [
        GroupSpec(
            family="reflexive-reference",
            answer="himself",
            choice_key="himself",
            note="the subject and the object are the same male person",
            templates=(
                "daniel prepared the slides by ____.",
                "carlos reminded ____ to check the dates.",
                "miguel organized the files by ____.",
                "ben coached ____ before the interview.",
                "mr. reyes praised ____ for the careful review.",
            ),
        ),
        GroupSpec(
            family="reflexive-reference",
            answer="herself",
            choice_key="herself",
            note="the subject and the object are the same female person",
            templates=(
                "maria prepared the slides by ____.",
                "sofia reminded ____ to check the dates.",
                "ana organized the files by ____.",
                "angela coached ____ before the interview.",
                "ms. cruz praised ____ for the careful review.",
            ),
        ),
        GroupSpec(
            family="reflexive-reference",
            answer="itself",
            choice_key="itself",
            note="the action returns to the same singular thing or machine",
            templates=(
                "the machine reset ____ after the outage.",
                "the door locked ____ after the alarm sounded.",
                "the system updated ____ overnight.",
                "the application closed ____ during the error.",
                "the printer restarted ____ after the jam.",
            ),
        ),
        GroupSpec(
            family="reflexive-reference",
            answer="themselves",
            choice_key="themselves",
            note="the action returns to the plural subject",
            templates=(
                "the officers prepared ____ for the audit.",
                "the workers reminded ____ to check the list.",
                "the teams trained ____ before the review.",
                "the clerks organized ____ before the meeting.",
                "the volunteers congratulated ____ on the success.",
            ),
        ),
        GroupSpec(
            family="reflexive-reference",
            answer="ourselves",
            choice_key="ourselves",
            note="the action returns to the first-person plural subject",
            templates=(
                "we prepared ____ for the briefing.",
                "we reminded ____ to bring the files.",
                "we organized ____ before the review.",
                "we introduced ____ to the new director.",
                "we should trust ____ to do the work.",
            ),
        ),
    ],
    "indefinite-reference": [
        GroupSpec(
            family="indefinite-reference",
            answer="he or she",
            choice_key="he_or_she",
            note="the antecedent is an indefinite singular person in a formal sentence",
            templates=(
                "if an applicant forgets the pass, ____ must report to security.",
                "each visitor who arrives late should wait until ____ is called.",
                "every employee should read the notice before ____ signs it.",
                "whenever a clerk needs help, ____ should ask the supervisor.",
                "each student who enters the room should make sure ____ is ready to begin.",
            ),
        ),
        GroupSpec(
            family="indefinite-reference",
            answer="him or her",
            choice_key="him_or_her",
            note="the pronoun follows a verb and refers to an indefinite singular person",
            templates=(
                "the clerk will call each applicant after meeting ____.",
                "the officer guided every visitor before thanking ____ for coming.",
                "the supervisor checked each worker before greeting ____.",
                "the manager will interview any candidate before inviting ____ back.",
                "the assistant will help the guest after speaking with ____.",
            ),
        ),
        GroupSpec(
            family="indefinite-reference",
            answer="his or her",
            choice_key="his_or_her",
            note="the pronoun shows possession for an indefinite singular person",
            templates=(
                "each applicant should keep ____ identification ready.",
                "every employee must label ____ file clearly.",
                "any clerk should protect ____ password carefully.",
                "each visitor should leave ____ badge at the desk.",
                "every student must bring ____ own notebook.",
            ),
        ),
        GroupSpec(
            family="indefinite-reference",
            answer="they",
            choice_key="they",
            note="modern standard English accepts singular they for an indefinite person",
            templates=(
                "if an applicant forgets the pass, ____ must report to security.",
                "when a visitor arrives late, ____ should check in at the desk.",
                "each person should sign the form before ____ leaves.",
                "if a clerk needs help, ____ can ask the supervisor.",
                "whenever a candidate is called, ____ should respond promptly.",
            ),
        ),
        GroupSpec(
            family="indefinite-reference",
            answer="their",
            choice_key="their_plural",
            note="modern standard English accepts singular their with an indefinite antecedent",
            templates=(
                "each applicant should keep ____ receipt.",
                "every employee must label ____ file clearly.",
                "any clerk should protect ____ password carefully.",
                "each visitor should leave ____ badge at the desk.",
                "every student must bring ____ own notebook.",
            ),
        ),
    ],
    "relative-reference": [
        GroupSpec(
            family="relative-reference",
            answer="who",
            choice_key="who",
            note="the relative pronoun refers to a person acting as the subject",
            templates=(
                "the officer ____ reviewed the file signed the memo.",
                "the clerk ____ called the director explained the delay.",
                "the teacher ____ checked the forms left early.",
                "the manager ____ approved the plan sent a note.",
                "the analyst ____ found the error reported it quickly.",
            ),
        ),
        GroupSpec(
            family="relative-reference",
            answer="whom",
            choice_key="whom",
            note="the relative pronoun refers to a person acting as the object",
            templates=(
                "the clerk ____ the manager called returned the form.",
                "the applicant ____ the officer interviewed was calm.",
                "the assistant ____ the supervisor invited joined the meeting.",
                "the worker ____ the team supported finished the task.",
                "the visitor ____ the guard stopped showed an ID card.",
            ),
        ),
        GroupSpec(
            family="relative-reference",
            answer="whose",
            choice_key="whose",
            note="the relative pronoun shows possession",
            templates=(
                "the analyst, ____ notes were missing, asked for help.",
                "the supervisor, ____ file was misplaced, apologized.",
                "the officer, ____ badge was lost, reported it.",
                "the clerk, ____ report was delayed, explained the issue.",
                "the manager, ____ memo had been revised, approved the update.",
            ),
        ),
        GroupSpec(
            family="relative-reference",
            answer="which",
            choice_key="which",
            note="the relative pronoun refers to a thing or idea",
            templates=(
                "the report, ____ was revised twice, was approved.",
                "the folder, ____ held the records, was moved to storage.",
                "the machine, ____ had been repaired, worked again.",
                "the notice, ____ explained the rule, was posted outside.",
                "the form, ____ needed a signature, was returned.",
            ),
        ),
        GroupSpec(
            family="relative-reference",
            answer="that",
            choice_key="that",
            note="the relative pronoun introduces a restrictive clause",
            templates=(
                "the report ____ the clerk submitted was approved.",
                "the form ____ the officer checked was complete.",
                "the notice ____ the team posted stayed on the wall.",
                "the memo ____ the supervisor wrote was brief.",
                "the file ____ the assistant found was missing a page.",
            ),
        ),
    ],
}


def main() -> int:
    questions: list[dict[str, object]] = []
    index = 1
    for difficulty in DIFFICULTY_ORDER:
        for family in FAMILY_ORDER:
            for group in GROUPS_BY_FAMILY[family]:
                for template in group.templates:
                    questions.append(
                        _make_item(
                            family=family,
                            answer=group.answer,
                            choice_key=group.choice_key,
                            note=group.note,
                            sentence=template,
                            difficulty=difficulty,
                            index=index,
                        )
                    )
                    index += 1

    _validate_bank(questions)
    _write_bank(questions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
