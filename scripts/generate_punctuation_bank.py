"""Generate the Punctuation question bank."""

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
    / "punctuation"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Error Recognition"
SUBTOPIC = "Punctuation"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TAGS = {
    "Easy": "easy",
    "Medium": "medium",
    "Hard": "hard",
    "Ultra": "ultra",
}

SENTENCE_STYLE_FAMILIES = {
    "introductory-comma",
    "nonessential-comma",
    "series-comma",
    "coordinate-adjectives",
    "compound-sentence-comma",
    "direct-address-comma",
    "contrast-comma",
    "semicolon-independent",
    "semicolon-series",
    "colon-list",
    "colon-explanation",
    "quotation-sequence",
}

SENTENCE_PROMPTS: dict[str, dict[str, str]] = {
    "introductory-comma": {
        "Easy": "Which sentence correctly sets off the introductory phrase",
        "Medium": "Which revision correctly sets off the introductory phrase",
        "Hard": "Which sentence best handles the introductory phrase",
        "Ultra": "Which revision is most accurate for the introductory phrase",
    },
    "nonessential-comma": {
        "Easy": "Which sentence correctly sets off the nonessential information",
        "Medium": "Which revision correctly sets off the nonessential information",
        "Hard": "Which sentence best handles the nonessential information",
        "Ultra": "Which revision is most accurate for the nonessential information",
    },
    "series-comma": {
        "Easy": "Which sentence correctly punctuates the series",
        "Medium": "Which revision correctly punctuates the series",
        "Hard": "Which sentence best handles the list punctuation",
        "Ultra": "Which revision is most accurate for the series punctuation",
    },
    "coordinate-adjectives": {
        "Easy": "Which sentence correctly uses a comma between the coordinate adjectives",
        "Medium": "Which revision correctly uses a comma between the coordinate adjectives",
        "Hard": "Which sentence best separates the coordinate adjectives",
        "Ultra": "Which revision is most accurate for the coordinate adjectives",
    },
    "compound-sentence-comma": {
        "Easy": "Which sentence correctly joins the independent clauses with a comma",
        "Medium": "Which revision correctly joins the independent clauses with a comma",
        "Hard": "Which sentence best joins the independent clauses",
        "Ultra": "Which revision is most accurate for joining the independent clauses",
    },
    "direct-address-comma": {
        "Easy": "Which sentence correctly punctuates the direct address",
        "Medium": "Which revision correctly punctuates the direct address",
        "Hard": "Which sentence best sets off the direct address",
        "Ultra": "Which revision is most accurate for direct address punctuation",
    },
    "contrast-comma": {
        "Easy": "Which sentence correctly places the comma before the contrast clause",
        "Medium": "Which revision correctly places the comma before the contrast clause",
        "Hard": "Which sentence best marks the contrast with a comma",
        "Ultra": "Which revision is most accurate for the contrast comma",
    },
    "semicolon-independent": {
        "Easy": "Which sentence correctly uses a semicolon to join the clauses",
        "Medium": "Which revision correctly uses a semicolon to join the clauses",
        "Hard": "Which sentence best links the clauses with a semicolon",
        "Ultra": "Which revision is most accurate for the semicolon between clauses",
    },
    "semicolon-series": {
        "Easy": "Which sentence correctly separates the complex list items with semicolons",
        "Medium": "Which revision correctly separates the complex list items with semicolons",
        "Hard": "Which sentence best uses semicolons in the list",
        "Ultra": "Which revision is most accurate for semicolons in the list",
    },
    "colon-list": {
        "Easy": "Which sentence correctly introduces the list with a colon",
        "Medium": "Which revision correctly introduces the list with a colon",
        "Hard": "Which sentence best introduces the list",
        "Ultra": "Which revision is most accurate for the colon before the list",
    },
    "colon-explanation": {
        "Easy": "Which sentence correctly introduces the explanation with a colon",
        "Medium": "Which revision correctly introduces the explanation with a colon",
        "Hard": "Which sentence best introduces the explanation",
        "Ultra": "Which revision is most accurate for the colon before the explanation",
    },
    "quotation-sequence": {
        "Easy": "Which sentence correctly uses quotation marks and end punctuation",
        "Medium": "Which revision correctly uses quotation marks and end punctuation",
        "Hard": "Which sentence best closes the quotation",
        "Ultra": "Which revision is most accurate for quotation punctuation",
    },
}

WORD_PROMPTS: dict[str, dict[str, str]] = {
    "possessive-singular": {
        "Easy": "Which form shows singular possession correctly",
        "Medium": "Which revision correctly shows singular possession",
        "Hard": "Which form best shows singular possession",
        "Ultra": "Which revision is most accurate for singular possession",
    },
    "possessive-plural": {
        "Easy": "Which form shows plural possession correctly",
        "Medium": "Which revision correctly shows plural possession",
        "Hard": "Which form best shows plural possession",
        "Ultra": "Which revision is most accurate for plural possession",
    },
    "contraction": {
        "Easy": "Which form correctly contracts `it is`",
        "Medium": "Which revision correctly contracts `it is`",
        "Hard": "Which form best contracts `it is`",
        "Ultra": "Which revision is most accurate for the contraction of `it is`",
    },
}


@dataclass(frozen=True)
class Frame:
    before: str
    after: str
    terminal: str = "."


@dataclass(frozen=True)
class FamilySpec:
    base_family: str
    kind: str
    answer: str
    choices: tuple[str, str, str, str]
    frames: tuple[Frame, ...]
    explanation: str
    tags: tuple[str, ...]
    question_wrap: str = "double"


def frames(*pairs: tuple[str, str], terminal: str = ".") -> tuple[Frame, ...]:
    return tuple(Frame(before=before, after=after, terminal=terminal) for before, after in pairs)


def _compose_sentence(frame: Frame) -> str:
    before = " ".join(frame.before.split())
    after = " ".join(frame.after.split())
    if before and after:
        sentence = f"{before} ____ {after}"
    elif before:
        sentence = f"{before} ____"
    elif after:
        sentence = f"____ {after}"
    else:
        sentence = "____"
    if frame.terminal:
        sentence = f"{sentence}{frame.terminal}"
    return sentence


def _wrap_sentence(question_wrap: str, sentence: str) -> str:
    if question_wrap == "single":
        return f"'{sentence}'"
    if question_wrap == "double":
        return f'"{sentence}"'
    return sentence


def _rotate_choices(choices: list[str], question_id: int, frame_index: int) -> list[str]:
    rotation = (question_id + frame_index) % len(choices)
    return choices[rotation:] + choices[:rotation]


def _sentence_option_family(base_family: str, frame: Frame) -> tuple[str, str, list[str]]:
    before = " ".join(frame.before.split())
    after = " ".join(frame.after.split())
    terminal = frame.terminal or "."

    if base_family == "introductory-comma":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}; {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "nonessential-comma":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}, {after}",
            "No correction needed",
        ]

    if base_family == "series-comma":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}; {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "coordinate-adjectives":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}; {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "compound-sentence-comma":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}, {after}",
            "No correction needed",
        ]

    if base_family == "direct-address-comma":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}; {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "contrast-comma":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}, {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before} {after}{terminal}",
            f"{before}, {after}",
            "No correction needed",
        ]

    if base_family == "semicolon-independent":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}; {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before}, {after}{terminal}",
            f"{before} and {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "semicolon-series":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}; {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before}, {after}{terminal}",
            f"{before}; and {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "colon-list":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}: {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before}, {after}{terminal}",
            f"{before}; {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "colon-explanation":
        prompt = f"{before} {after}{terminal}"
        correct = f"{before}: {after}{terminal}"
        return prompt, correct, [
            correct,
            f"{before}, {after}{terminal}",
            f"{before}; {after}{terminal}",
            "No correction needed",
        ]

    if base_family == "quotation-sequence":
        prompt = f'{before}".'
        correct = f'{before}."'
        return prompt, correct, [
            correct,
            f'{before}"',
            f'{before}, "',
            "No correction needed",
        ]

    raise ValueError(f"unsupported sentence family: {base_family}")


def _build_question(
    *,
    question_id: int,
    spec: FamilySpec,
    family_name: str,
    frame: Frame,
    frame_index: int,
    difficulty: str,
) -> dict:
    if spec.base_family in SENTENCE_STYLE_FAMILIES:
        stem = SENTENCE_PROMPTS[spec.base_family][difficulty]
        prompt_sentence, answer, choices = _sentence_option_family(spec.base_family, frame)
        question = f'{stem}: "{prompt_sentence}"'
    else:
        stem = WORD_PROMPTS.get(
            spec.base_family,
            {
                "Easy": "Which form best completes the sentence",
                "Medium": "Which revision best completes the sentence",
                "Hard": "Which form is most accurate for the sentence",
                "Ultra": "Which revision is most accurate for the sentence",
            }[difficulty],
        )[difficulty]
        sentence = _compose_sentence(frame)
        wrapped_sentence = _wrap_sentence(spec.question_wrap, sentence)
        question = f"{stem}: {wrapped_sentence}"
        choices = list(spec.choices)
        answer = spec.answer

    choices = _rotate_choices(list(choices), question_id, frame_index)
    if answer not in choices:
        raise ValueError(f"answer {answer!r} not present in choices for {family_name}")

    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": spec.explanation,
        "tags": [
            "punctuation",
            family_name,
            DIFFICULTY_TAGS[difficulty],
            spec.base_family,
            spec.kind,
            *spec.tags,
        ],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _family_specs() -> tuple[FamilySpec, ...]:
    return (
        FamilySpec(
            base_family="introductory-comma",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("After the briefing", "the clerk filed the forms"),
                ("Before the office opened", "the supervisor checked the log"),
                ("During the inspection", "the staff organized the desk"),
                ("At the end of the shift", "the team left the room"),
                ("Early on Monday morning", "the manager reviewed the schedule"),
                ("Without a doubt", "the branch remained quiet"),
                ("When the lights came back", "the workers reopened the file"),
                ("After the final review", "the office sent the memo"),
                ("In the middle of the meeting", "the speaker paused"),
                ("For the new employee", "the trainer explained the process"),
            ),
            explanation="Introductory clauses and phrases are normally followed by a comma.",
            tags=("comma", "introductory", "opener"),
        ),
        FamilySpec(
            base_family="nonessential-comma",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("The manager, who arrived late", "approved the schedule"),
                ("The report, which was revised yesterday", "was still accepted"),
                ("The clerk, wearing a blue jacket", "handed over the papers"),
                ("The memo, prepared by the assistant", "reached the director"),
                ("The officer, who was on duty", "checked the gate"),
                ("The branch, located near the station", "stayed open longer"),
                ("The applicant, already seated", "answered the call"),
                ("The form, signed by the supervisor", "was filed on time"),
                ("The guide, speaking softly", "explained the route"),
                ("The file, marked in red", "was returned to the folder"),
            ),
            explanation="Nonessential information is set off with commas.",
            tags=("comma", "nonessential", "set-off"),
        ),
        FamilySpec(
            base_family="series-comma",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("The office ordered paper, folders", "and staplers"),
                ("The team packed pens, notebooks", "and name tags"),
                ("The branch bought chairs, desks", "and lamps"),
                ("The clerk sorted forms, receipts", "and invoices"),
                ("The manager packed masks, gloves", "and sanitizer"),
                ("The staff prepared letters, notices", "and envelopes"),
                ("The reviewer checked logs, charts", "and tables"),
                ("The office stocked ink, toner", "and paper clips"),
                ("The group collected files, folders", "and binders"),
                ("The clerk gathered stamps, seals", "and trays"),
            ),
            explanation="Items in a series are separated by commas.",
            tags=("comma", "series", "list"),
        ),
        FamilySpec(
            base_family="coordinate-adjectives",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("The clerk handled a careful", "detailed report"),
                ("The office sent a brief", "clear memo"),
                ("The team prepared a long", "detailed summary"),
                ("The manager wrote a plain", "polite reminder"),
                ("The branch filed a neat", "organized form"),
                ("The report was a small", "useful guide"),
                ("The memo carried a warm", "sincere note"),
                ("The form had a simple", "clean layout"),
                ("The file became a clear", "readable copy"),
                ("The room held a bright", "open space"),
            ),
            explanation="Coordinate adjectives that modify the same noun are separated by a comma.",
            tags=("comma", "coordinate-adjectives", "modifiers"),
        ),
        FamilySpec(
            base_family="compound-sentence-comma",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("The supervisor approved the forms", "and the staff filed them"),
                ("The clerk checked the log", "and the manager signed it"),
                ("The report was complete", "and the office submitted it"),
                ("The branch opened early", "and the line formed outside"),
                ("The memo was delayed", "and the deadline had passed"),
                ("The officer finished the review", "and the team left"),
                ("The staff closed the office", "and the lights were turned off"),
                ("The director signed the notice", "and the clerk posted it"),
                ("The team gathered the files", "and the supervisor sorted them"),
                ("The assistant copied the document", "and the reviewer archived it"),
            ),
            explanation="Independent clauses joined by a coordinating conjunction normally take a comma before the conjunction.",
            tags=("comma", "compound-sentence", "coordination"),
        ),
        FamilySpec(
            base_family="direct-address-comma",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("Maria", "please bring the files"),
                ("Officer Cruz", "please check the log"),
                ("Sir", "the report is ready"),
                ("Doctor Reyes", "please sign the form"),
                ("Ms. Santos", "please review the memo"),
                ("Team", "please stay alert"),
                ("Ana", "please open the door"),
                ("Mr. Lopez", "please read the notice"),
                ("Counsel", "please answer the question"),
                ("Carla", "please wait here"),
            ),
            explanation="Direct address is usually set off with a comma.",
            tags=("comma", "direct-address", "vocative"),
        ),
        FamilySpec(
            base_family="contrast-comma",
            kind="mark",
            answer="comma",
            choices=("comma", "semicolon", "colon", "period"),
            frames=frames(
                ("The office was busy", "but the clerk stayed calm"),
                ("The weather was harsh", "but the team kept working"),
                ("The file was old", "but the information was still useful"),
                ("The room was small", "but the lights were bright"),
                ("The plan was risky", "but the branch moved ahead"),
                ("The schedule was tight", "but the staff finished on time"),
                ("The instructions were clear", "but the result was still confusing"),
                ("The task was difficult", "but the clerk finished it"),
                ("The hallway was crowded", "but the desk was quiet"),
                ("The test was short", "but the questions were tricky"),
            ),
            explanation="A comma can separate contrasted or shifted ideas before a coordinating conjunction.",
            tags=("comma", "contrast", "shift"),
        ),
        FamilySpec(
            base_family="semicolon-independent",
            kind="mark",
            answer="semicolon",
            choices=("semicolon", "comma", "colon", "period"),
            frames=frames(
                ("The clerk was late", "the meeting started on time"),
                ("The memo was revised", "the staff sent it again"),
                ("The branch was crowded", "another counter opened"),
                ("The report was finished", "the director approved it"),
                ("The office was quiet", "the phones still rang"),
                ("The light was dim", "the next room stayed dark"),
                ("The staff was ready", "the line moved quickly"),
                ("The file was missing", "the drawer was still empty"),
                ("The supervisor was busy", "the deadline was close"),
                ("The room was warm", "the window stayed open"),
            ),
            explanation="A semicolon can join two closely related independent clauses.",
            tags=("semicolon", "independent-clauses", "compound"),
        ),
        FamilySpec(
            base_family="semicolon-series",
            kind="mark",
            answer="semicolon",
            choices=("semicolon", "comma", "colon", "period"),
            frames=frames(
                ("The trip included Manila, Philippines", "Cebu City, Cebu"),
                ("The schedule listed Dr. Santos, the director", "Ms. Gomez, the assistant"),
                ("The report mentioned April 3, 2026", "May 7, 2026"),
                ("The class visited Baguio City, Benguet", "Davao City, Davao"),
                ("The memo named Mr. Cruz, the manager", "Mr. Lim, the supervisor"),
                ("The agenda covered San Fernando, La Union", "Laoag City, Ilocos Norte"),
                ("The route crossed Iloilo City, Iloilo", "Taguig City, Metro Manila"),
                ("The file recorded Jan. 12, 2026", "Feb. 9, 2026"),
                ("The guide included Cagayan de Oro, Misamis Oriental", "Tacloban City, Leyte"),
                ("The roster listed Ms. Reyes, the coordinator", "Dr. Alba, the officer"),
            ),
            explanation="Semicolons can separate complex series items that already contain commas.",
            tags=("semicolon", "series", "complex-list"),
        ),
        FamilySpec(
            base_family="colon-list",
            kind="mark",
            answer="colon",
            choices=("colon", "semicolon", "comma", "period"),
            frames=frames(
                ("The office needed three supplies", "paper, toner, and clips"),
                ("The team packed four supplies", "paper, pens, notebooks, and labels"),
                ("The branch stocked three materials", "forms, stamps, and envelopes"),
                ("The class reviewed three topics", "rules, examples, and exceptions"),
                ("The memo listed three deadlines", "Monday, Wednesday, and Friday"),
                ("The report named three goals", "speed, accuracy, and fairness"),
                ("The kit included four parts", "a pen, a ruler, a stapler, and tape"),
                ("The folder held three forms", "receipts, notes, and logs"),
                ("The schedule showed four steps", "planning, drafting, revising, and checking"),
                ("The project needed three features", "clarity, accuracy, and brevity"),
            ),
            explanation="A colon can introduce a list after a complete clause.",
            tags=("colon", "list", "introduction"),
        ),
        FamilySpec(
            base_family="colon-explanation",
            kind="mark",
            answer="colon",
            choices=("colon", "semicolon", "comma", "period"),
            frames=frames(
                ("The supervisor had one request", "finish the report before noon"),
                ("The memo had one purpose", "explain the policy clearly"),
                ("The applicant had one goal", "pass the screening test"),
                ("The trainer had one warning", "stay alert during the drill"),
                ("The office had one rule", "submit the forms on time"),
                ("The director had one message", "keep the records organized"),
                ("The clerk had one explanation", "check the totals again"),
                ("The branch had one answer", "wait for the final approval"),
                ("The manager had one reminder", "bring the receipt to the desk"),
                ("The report had one conclusion", "check the figures carefully"),
            ),
            explanation="A colon can introduce an explanation after a complete clause.",
            tags=("colon", "explanation", "formal"),
        ),
        FamilySpec(
            base_family="possessive-singular",
            kind="word",
            answer="manager's",
            choices=("manager's", "managers'", "manager", "managers"),
            frames=frames(
                ("The", "memo was approved yesterday"),
                ("The", "desk was empty"),
                ("The", "schedule changed at noon"),
                ("The", "report was filed on time"),
                ("The", "notes were helpful"),
                ("The", "key was missing"),
                ("The", "office was quiet"),
                ("The", "signature was clear"),
                ("The", "proposal was accepted"),
                ("The", "folder was on the table"),
            ),
            explanation="A singular possessive takes an apostrophe plus s.",
            tags=("apostrophe", "possessive", "singular"),
        ),
        FamilySpec(
            base_family="possessive-plural",
            kind="word",
            answer="teachers'",
            choices=("teachers'", "teacher's", "teachers", "teacher"),
            frames=frames(
                ("The", "desks were arranged neatly"),
                ("The", "reports were stacked on the table"),
                ("The", "files were updated yesterday"),
                ("The", "offices were locked at noon"),
                ("The", "schedules were posted early"),
                ("The", "notebooks were collected"),
                ("The", "notes were shared after class"),
                ("The", "uniforms were cleaned"),
                ("The", "seats were reserved"),
                ("The", "folders were returned"),
            ),
            explanation="A plural possessive usually adds the apostrophe after the plural s.",
            tags=("apostrophe", "possessive", "plural"),
        ),
        FamilySpec(
            base_family="contraction",
            kind="word",
            answer="it's",
            choices=("it's", "its", "its'", "it is"),
            frames=frames(
                ("It", "time to leave"),
                ("It", "been approved"),
                ("It", "raining outside"),
                ("It", "a good idea to wait"),
                ("It", "ready for review"),
                ("It", "already late"),
                ("It", "not difficult to see"),
                ("It", "the only way forward"),
                ("It", "possible to finish today"),
                ("It", "okay to ask questions"),
            ),
            explanation="It's is the contraction of it is.",
            tags=("apostrophe", "contraction", "it-is"),
        ),
        FamilySpec(
            base_family="quotation-sequence",
            kind="quote",
            answer="period inside the quote",
            choices=(
                "period inside the quote",
                "comma inside the quote",
                "question mark inside the quote",
                "exclamation point inside the quote",
            ),
            frames=frames(
                ("The clerk said, \"The files are ready", ""),
                ("The manager wrote, \"The report is complete", ""),
                ("The officer announced, \"The room is open", ""),
                ("The guide replied, \"The forms are here", ""),
                ("The supervisor explained, \"The schedule is final", ""),
                ("The teacher noted, \"The answer is correct", ""),
                ("The speaker added, \"The meeting is over", ""),
                ("The assistant confirmed, \"The memo is revised", ""),
                ("The director stated, \"The office is closed", ""),
                ("The clerk reported, \"The documents are sorted", ""),
                terminal="",
            ),
            explanation="In American English, a period usually stays inside the closing quotation mark.",
            tags=("quotation-marks", "terminal-punctuation", "direct-speech"),
            question_wrap="single",
        ),
    )


def _generate() -> list[dict]:
    items: list[dict] = []
    question_id = 1

    for difficulty in DIFFICULTIES:
        for spec in _family_specs():
            family_name = f"{difficulty.lower()}-{spec.base_family}"
            for frame_index, frame in enumerate(spec.frames):
                items.append(
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
    return items


def _validate_bank(items: list[dict]) -> None:
    if len(items) != 600:
        raise ValueError(f"expected 600 questions, found {len(items)}")

    expected_difficulties = {difficulty: 150 for difficulty in DIFFICULTIES}
    actual_difficulties: dict[str, int] = {difficulty: 0 for difficulty in DIFFICULTIES}
    actual_families: Counter[str] = Counter()
    seen_questions: set[str] = set()

    for index, item in enumerate(items, start=1):
        if item.get("id") != index:
            raise ValueError(
                f"question ids must be sequential; found {item.get('id')} at position {index}"
            )

        if item.get("subtest") != SUBTEST:
            raise ValueError(f"invalid subtest at id {index}")
        if item.get("module") != MODULE:
            raise ValueError(f"invalid module at id {index}")
        if item.get("subtopic") != SUBTOPIC:
            raise ValueError(f"invalid subtopic at id {index}")
        if item.get("category") != CATEGORY:
            raise ValueError(f"invalid category at id {index}")
        if item.get("language") != LANGUAGE:
            raise ValueError(f"invalid language at id {index}")

        difficulty = str(item.get("difficulty", "")).strip()
        if difficulty not in actual_difficulties:
            raise ValueError(f"invalid difficulty {difficulty!r} at id {index}")
        actual_difficulties[difficulty] += 1

        question = str(item.get("question", "")).strip()
        if not question:
            raise ValueError(f"blank question text at id {index}")
        if "  " in question:
            raise ValueError(f"double space found in question text at id {index}")
        if question in seen_questions:
            raise ValueError(f"duplicate question text at id {index}")
        seen_questions.add(question)

        choices = item.get("choices")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"invalid choices at id {index}")
        normalized = [str(choice).strip() for choice in choices]
        if any(not choice for choice in normalized):
            raise ValueError(f"blank choice at id {index}")
        if len(set(normalized)) != len(normalized):
            raise ValueError(f"duplicate choices at id {index}")

        answer = str(item.get("answer", "")).strip()
        if answer not in normalized:
            raise ValueError(f"answer {answer!r} not present in choices at id {index}")

        explanation = str(item.get("explanation", "")).strip()
        if not explanation:
            raise ValueError(f"blank explanation at id {index}")

        tags = item.get("tags")
        if not isinstance(tags, list) or len(tags) < 5:
            raise ValueError(f"invalid tags at id {index}")
        if tags[0] != "punctuation":
            raise ValueError(f"invalid root tag at id {index}")
        actual_families[str(tags[1])] += 1

    if actual_difficulties != expected_difficulties:
        raise ValueError(f"unexpected difficulty counts: {actual_difficulties}")

    expected_families = {
        f"{difficulty.lower()}-{spec.base_family}": 10
        for difficulty in DIFFICULTIES
        for spec in _family_specs()
    }
    family_mismatches = {
        family: count
        for family, count in actual_families.items()
        if expected_families.get(family) != count
    }
    if family_mismatches or len(actual_families) != len(expected_families):
        raise ValueError(
            "unexpected family counts: "
            f"{dict(actual_families)} expected {expected_families}"
        )


def main() -> None:
    items = _generate()
    _validate_bank(items)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(items, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
