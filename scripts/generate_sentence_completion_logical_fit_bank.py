"""Generate the Verbal Ability / Sentence Completion / Logical Fit bank.

The bank focuses on the relationship between ideas inside a sentence. It
covers cause and result, contrast, addition, sequence, example and
restatement, and condition and exception. Each difficulty band contains 150
items, for 600 items total.

The script is deterministic and writes directly to the seed tree so the reset
script can pick it up automatically.
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
    / "logical-fit"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Logical Fit"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
FAMILY_ORDER = (
    "cause-effect",
    "contrast",
    "addition",
    "sequence",
    "example-restatement",
    "condition-exception",
)

QUESTION_STEMS = {
    "cause-effect": [
        "Which connector best shows the result",
        "Which word best completes the cause-and-effect link",
        "Which option best fits the sentence logically",
        "Which transition best completes the sentence below",
    ],
    "contrast": [
        "Which connector best signals contrast",
        "Which word best shows an opposite idea",
        "Which option best fits the sentence logically",
        "Which transition best completes the sentence below",
    ],
    "addition": [
        "Which connector best adds another point",
        "Which word best keeps the idea moving in the same direction",
        "Which option best fits the sentence logically",
        "Which transition best completes the sentence below",
    ],
    "sequence": [
        "Which connector best shows order",
        "Which word best marks the next step",
        "Which option best fits the sentence logically",
        "Which transition best completes the sentence below",
    ],
    "example-restatement": [
        "Which phrase best introduces an example",
        "Which phrase best restates the idea",
        "Which option best fits the sentence logically",
        "Which transition best completes the sentence below",
    ],
    "condition-exception": [
        "Which word best shows a condition",
        "Which word best shows an exception",
        "Which option best fits the sentence logically",
        "Which transition best completes the sentence below",
    ],
}

DIFFICULTY_PREFIXES = {
    "Easy": "",
    "Medium": "During a routine review, ",
    "Hard": "During a routine review, after a second check, ",
    "Ultra": "During a routine review, after a second check and a schedule change, ",
}


@dataclass(frozen=True)
class GroupSpec:
    family: str
    answer: str
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


def _build_choices(answer: str, rng: random.Random) -> list[str]:
    pool = CHOICE_POOLS.get(answer)
    if pool is None:
        raise KeyError(f"missing choice pool for answer: {answer}")
    choices = list(dict.fromkeys(pool))
    if answer not in choices:
        raise ValueError(f"answer {answer!r} missing from choice pool")
    if len(choices) != 4:
        raise ValueError(f"choice pool for {answer!r} must contain 4 distinct items")
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
    return f"The sentence needs the connector {answer}; {note}."


def _make_item(
    *,
    family: str,
    answer: str,
    note: str,
    sentence: str,
    difficulty: str,
    index: int,
) -> dict[str, object]:
    rng = random.Random(f"{family}:{answer}:{difficulty}:{index}")
    wrapped_sentence = _difficulty_wrap(sentence, difficulty)
    question = _question_stem(family, difficulty, index)
    question_text = f'{question}: "{wrapped_sentence}"'
    choices = _build_choices(answer, rng)
    explanation = _build_explanation(answer, note)
    tags = [family, difficulty.lower(), "logical-fit"]

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


CHOICE_POOLS: dict[str, list[str]] = {
    "because": ["because", "so", "however", "for example"],
    "so": ["so", "however", "for example", "unless"],
    "therefore": ["therefore", "however", "also", "unless"],
    "thus": ["thus", "however", "also", "for example"],
    "as a result": ["as a result", "however", "also", "unless"],
    "consequently": ["consequently", "however", "for example", "also"],
    "but": ["but", "therefore", "also", "unless"],
    "however": ["however", "so", "also", "for example"],
    "yet": ["yet", "therefore", "also", "unless"],
    "nevertheless": ["nevertheless", "so", "for example", "if"],
    "on the other hand": ["on the other hand", "because", "also", "unless"],
    "also": ["also", "however", "therefore", "unless"],
    "moreover": ["moreover", "but", "unless", "for example"],
    "furthermore": ["furthermore", "yet", "because", "unless"],
    "in addition": ["in addition", "however", "so", "for example"],
    "besides": ["besides", "therefore", "then", "unless"],
    "initially": ["initially", "however", "because", "for example"],
    "next": ["next", "yet", "unless", "however"],
    "then": ["then", "however", "because", "for example"],
    "afterward": ["afterward", "therefore", "also", "unless"],
    "finally": ["finally", "however", "because", "also"],
    "for example": ["for example", "therefore", "however", "unless"],
    "for instance": ["for instance", "also", "yet", "if"],
    "specifically": ["specifically", "however", "moreover", "unless"],
    "in other words": ["in other words", "therefore", "instead", "for example"],
    "namely": ["namely", "however", "also", "unless"],
    "if": ["if", "however", "therefore", "for example"],
    "unless": ["unless", "also", "then", "because"],
    "otherwise": ["otherwise", "however", "moreover", "if"],
    "provided that": ["provided that", "therefore", "instead", "for example"],
    "in case": ["in case", "however", "so", "unless"],
}


GROUPS_BY_FAMILY: dict[str, list[GroupSpec]] = {
    "cause-effect": [
        GroupSpec(
            family="cause-effect",
            answer="because",
            note="the second clause gives the reason for the first",
            templates=(
                "the briefing was moved indoors ____ the rain started early.",
                "the forms were checked twice ____ the office could avoid errors.",
                "the memo was rewritten ____ the first draft was unclear.",
                "the clerk stayed late ____ the backlog was heavy.",
                "the room was quiet ____ the supervisor was speaking.",
            ),
        ),
        GroupSpec(
            family="cause-effect",
            answer="so",
            note="the second clause states the result of the first",
            templates=(
                "the printer jammed, ____ the report was delayed.",
                "the office lost power, ____ the meeting moved indoors.",
                "the files were mixed up, ____ the clerk sorted them again.",
                "the notes were clear, ____ the team finished quickly.",
                "the road was closed, ____ the delivery truck turned back.",
            ),
        ),
        GroupSpec(
            family="cause-effect",
            answer="therefore",
            note="the second clause presents a logical result",
            templates=(
                "the records had missing dates; ____ , the clerk returned them for revision.",
                "the policy was unclear; ____ , employees asked for an explanation.",
                "the schedule changed at the last minute; ____ , the briefing was reset.",
                "the figures did not match; ____ , the report was held.",
                "the forms lacked signatures; ____ , the request was delayed.",
            ),
        ),
        GroupSpec(
            family="cause-effect",
            answer="thus",
            note="the second clause follows as a direct result",
            templates=(
                "the office had enough staff; ____ , the queue moved quickly.",
                "the instructions were simple; ____ , the team finished early.",
                "the data were verified; ____ , the summary was accepted.",
                "the plan was tested; ____ , the errors were caught early.",
                "the system was updated; ____ , the process became smoother.",
            ),
        ),
        GroupSpec(
            family="cause-effect",
            answer="as a result",
            note="the second clause states the outcome of the first",
            templates=(
                "the storm lasted all morning; ____ , the inspection was postponed.",
                "the notice arrived late; ____ , the staff missed the deadline.",
                "the room was overcrowded; ____ , the meeting was moved.",
                "the copy machine failed; ____ , the paperwork piled up.",
                "the clerk double-checked the list; ____ , the final count was accurate.",
            ),
        ),
    ],
    "contrast": [
        GroupSpec(
            family="contrast",
            answer="but",
            note="the second clause presents a contrasting idea",
            templates=(
                "the report was short, ____ it was clear.",
                "the office was busy, ____ the staff stayed calm.",
                "the draft looked simple, ____ it needed careful editing.",
                "the policy was strict, ____ it was fair.",
                "the task was routine, ____ the deadline was tight.",
            ),
        ),
        GroupSpec(
            family="contrast",
            answer="however",
            note="the second clause shifts to an opposite or unexpected point",
            templates=(
                "the report was short; ____ , it was complete.",
                "the draft looked clean; ____ , it still had errors.",
                "the office was ready; ____ , the meeting started late.",
                "the form was easy to read; ____ , many people misunderstood it.",
                "the plan sounded practical; ____ , it was costly.",
            ),
        ),
        GroupSpec(
            family="contrast",
            answer="yet",
            note="the second clause shows an unexpected contrast",
            templates=(
                "the memo was rough, ____ the main point was clear.",
                "the room was small, ____ everyone fit inside.",
                "the task was difficult, ____ the team finished on time.",
                "the form was old, ____ it still worked well.",
                "the rules were strict, ____ the staff followed them well.",
            ),
        ),
        GroupSpec(
            family="contrast",
            answer="nevertheless",
            note="the second clause admits a difficulty but keeps the main point",
            templates=(
                "the deadline was tight; ____ , the team submitted on time.",
                "the draft was imperfect; ____ , it was approved.",
                "the office was noisy; ____ , the clerk focused on the numbers.",
                "the schedule changed; ____ , the meeting went ahead.",
                "the weather was bad; ____ , the inspection continued.",
            ),
        ),
        GroupSpec(
            family="contrast",
            answer="on the other hand",
            note="the second clause presents a different side or opposite case",
            templates=(
                "the first proposal cut costs; ____ , the second improved service.",
                "the city office was crowded; ____ , the district office was quiet.",
                "the initial plan saved time; ____ , it created confusion.",
                "the old system was fast; ____ , the new one was safer.",
                "the short memo was easy to scan; ____ , the long report gave more detail.",
            ),
        ),
    ],
    "addition": [
        GroupSpec(
            family="addition",
            answer="also",
            note="the second clause adds another action in the same direction",
            templates=(
                "the clerk checked the totals and ____ verified the signatures.",
                "the officer filed the report and ____ updated the log.",
                "the team reviewed the plan and ____ checked the dates.",
                "the assistant sorted the papers and ____ labeled the folders.",
                "the supervisor read the memo and ____ signed it.",
            ),
        ),
        GroupSpec(
            family="addition",
            answer="moreover",
            note="the second clause adds a supporting point",
            templates=(
                "the office was short on staff; ____ , it was short on time.",
                "the file was incomplete; ____ , it lacked a signature.",
                "the draft was clear; ____ , it was concise.",
                "the policy was fair; ____ , it was easy to enforce.",
                "the report was useful; ____ , it was well organized.",
            ),
        ),
        GroupSpec(
            family="addition",
            answer="furthermore",
            note="the second clause strengthens the same idea",
            templates=(
                "the plan saved time; ____ , it reduced errors.",
                "the memo was brief; ____ , it was direct.",
                "the office added a backup check; ____ , it improved accuracy.",
                "the forms were standardized; ____ , they were easier to review.",
                "the briefing was short; ____ , it answered the key questions.",
            ),
        ),
        GroupSpec(
            family="addition",
            answer="in addition",
            note="the second clause adds one more point to the first",
            templates=(
                "the clerk reviewed the dates; ____ , she checked the signatures.",
                "the supervisor praised the team; ____ , he thanked the support staff.",
                "the office sent the notice; ____ , it posted a copy on the wall.",
                "the committee approved the plan; ____ , it set a follow-up meeting.",
                "the desk was organized; ____ , the drawers were labeled.",
            ),
        ),
        GroupSpec(
            family="addition",
            answer="besides",
            note="the second clause adds an extra supporting point",
            templates=(
                "the office was already closed; ____ , the forms were missing.",
                "the plan was expensive; ____ , it was hard to explain.",
                "the memo was late; ____ , it was unclear.",
                "the request was unusual; ____ , it arrived without a signature.",
                "the file was old; ____ , it needed extra review.",
            ),
        ),
    ],
    "sequence": [
        GroupSpec(
            family="sequence",
            answer="initially",
            note="the second clause marks the first step in a process",
            templates=(
                "the office had three checks; ____ , it reviewed the forms.",
                "the file had several steps; ____ , it checked the names.",
                "the process had two stages; ____ , it verified the numbers.",
                "the review had many parts; ____ , it scanned the pages.",
                "the workflow began with sorting; ____ , it labeled the folders.",
            ),
        ),
        GroupSpec(
            family="sequence",
            answer="next",
            note="the second clause marks the next step",
            templates=(
                "the clerk sorted the papers; ____ , she stamped each folder.",
                "the team checked the dates; ____ , it confirmed the signatures.",
                "the office read the memo; ____ , it filed the copy.",
                "the inspector reviewed the list; ____ , he counted the forms.",
                "the manager opened the meeting; ____ , she assigned the tasks.",
            ),
        ),
        GroupSpec(
            family="sequence",
            answer="then",
            note="the second clause follows as the next step",
            templates=(
                "the assistant copied the report; ____ , she sent it to the supervisor.",
                "the officer checked the ID; ____ , he let the visitor in.",
                "the clerk logged the request; ____ , she placed it in the file.",
                "the team collected the forms; ____ , it began the review.",
                "the staff finished the draft; ____ , they printed the final copy.",
            ),
        ),
        GroupSpec(
            family="sequence",
            answer="afterward",
            note="the second clause happens later in time",
            templates=(
                "the office met with the staff; ____ , it sent the summary.",
                "the clerk sorted the letters; ____ , she locked the drawer.",
                "the supervisor signed the memo; ____ , he left the room.",
                "the team reviewed the evidence; ____ , it filed the report.",
                "the inspector checked the forms; ____ , he returned to the desk.",
            ),
        ),
        GroupSpec(
            family="sequence",
            answer="finally",
            note="the second clause marks the last step",
            templates=(
                "the clerk checked the names; ____ , she checked the dates.",
                "the team verified the totals; ____ , it filed the report.",
                "the officer sorted the papers; ____ , he locked the cabinet.",
                "the staff compared the copies; ____ , it sent the notice.",
                "the committee reviewed the draft; ____ , it approved the plan.",
            ),
        ),
    ],
    "example-restatement": [
        GroupSpec(
            family="example-restatement",
            answer="for example",
            note="the second clause gives a specific example",
            templates=(
                "the policy covered several checks; ____ , it required two signatures for every release.",
                "the office followed many safety rules; ____ , it kept backup copies of every file.",
                "the report included several details; ____ , it listed the exact dates and times.",
                "the procedure had many steps; ____ , it asked the clerk to verify the ID.",
                "the briefing covered multiple problems; ____ , it mentioned the broken printer.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="for instance",
            note="the second clause gives one specific case",
            templates=(
                "the office used several methods; ____ , it compared dates and signatures.",
                "the memo listed many tasks; ____ , it asked the staff to file the forms.",
                "the policy gave several examples; ____ , it required a second review.",
                "the report noted many issues; ____ , it pointed to the missing page.",
                "the system had several safeguards; ____ , it checked the log twice.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="specifically",
            note="the second clause narrows the idea to one exact point",
            templates=(
                "the guideline named one requirement; ____ , it asked for the signature line.",
                "the notice gave one clear instruction; ____ , it told the clerk to call first.",
                "the memo identified one problem; ____ , it pointed to the wrong date.",
                "the report mentioned one step; ____ , it required a final check.",
                "the policy highlighted one rule; ____ , it limited late filing.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="in other words",
            note="the second clause rephrases the same idea",
            templates=(
                "the supervisor wanted a clearer record; ____ , she needed the file to be easier to read.",
                "the draft was too vague; ____ , it needed more detail.",
                "the process was too slow; ____ , it required fewer steps.",
                "the policy was hard to follow; ____ , it needed simpler language.",
                "the memo lacked focus; ____ , it needed a stronger main point.",
            ),
        ),
        GroupSpec(
            family="example-restatement",
            answer="namely",
            note="the second clause identifies the exact item being discussed",
            templates=(
                "the office had one key task; ____ , it had to verify the names.",
                "the plan had one main goal; ____ , it had to reduce errors.",
                "the report had one central point; ____ , it had to explain the delay.",
                "the request had one specific need; ____ , it had to include the file number.",
                "the notice had one required detail; ____ , it had to show the date.",
            ),
        ),
    ],
    "condition-exception": [
        GroupSpec(
            family="condition-exception",
            answer="if",
            note="the second clause sets the condition for the action",
            templates=(
                "the clerk will resend the form ____ the signature is missing.",
                "the office will delay approval ____ the dates are incomplete.",
                "the team will revise the memo ____ the figures do not match.",
                "the supervisor will call back ____ the report needs changes.",
                "the file will stay open ____ the page is still missing.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="unless",
            note="the second clause shows the exception that prevents the result",
            templates=(
                "the case will remain open ____ the missing page arrives.",
                "the office will not close the file ____ the clerk confirms the dates.",
                "the team will not submit the draft ____ the errors are fixed.",
                "the notice will not go out ____ the manager approves it.",
                "the request will not move forward ____ the signatures are complete.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="otherwise",
            note="the second clause tells what happens if the condition is not met",
            templates=(
                "the clerk must check the names, ____ the list may be wrong.",
                "the team must keep the copies, ____ the report will be incomplete.",
                "the office must post the notice, ____ the staff may miss it.",
                "the supervisor must sign the memo, ____ it will be delayed.",
                "the crew must label the files, ____ they may be misplaced.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="provided that",
            note="the second clause gives the requirement that must be satisfied",
            templates=(
                "the plan will be approved ____ the details are accurate.",
                "the request will move ahead ____ the forms are complete.",
                "the office will release the memo ____ the manager agrees.",
                "the staff may leave early ____ the urgent work is finished.",
                "the file will be accepted ____ the signature line is clear.",
            ),
        ),
        GroupSpec(
            family="condition-exception",
            answer="in case",
            note="the second clause prepares for a possible problem",
            templates=(
                "take an extra copy ____ the printer fails again.",
                "save the email ____ the office needs proof later.",
                "bring the checklist ____ a page is missing.",
                "keep the receipt ____ the clerk asks for it.",
                "carry the backup file ____ the system shuts down.",
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
