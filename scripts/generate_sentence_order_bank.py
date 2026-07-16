"""Generate the Verbal Ability / Paragraph Organization / Sentence Order question bank.

The bank uses 15 curated paragraph scenarios. Each scenario yields 10
sentence-order question types across four difficulty bands for a total of 600
unique items.
"""

from __future__ import annotations

import json
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "paragraph-organization"
    / "sentence-order"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Paragraph Organization"
SUBTOPIC = "Sentence Order"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
QUESTION_TYPES = (
    "sequence_general_specific",
    "sequence_chronological",
    "sequence_cause_effect",
    "sequence_problem_solution",
    "first_sentence",
    "last_sentence",
    "before_sentence",
    "after_sentence",
    "pronoun_reference",
    "off_topic",
)


STEMS: dict[str, dict[str, str]] = {
    "sequence_general_specific": {
        "Easy": "Which order best follows a general-to-specific pattern in the paragraph about {topic}?",
        "Medium": "Which sequence arranges the sentences into a general-to-specific paragraph about {topic}?",
        "Hard": "Which order best moves from the broad idea to the supporting details in the paragraph about {topic}?",
        "Ultra": "Which sequence most clearly shows a general-to-specific flow in the paragraph about {topic}?",
    },
    "sequence_chronological": {
        "Easy": "Which order best shows the time sequence in the paragraph about {topic}?",
        "Medium": "Which sequence best follows the chronological flow of the paragraph about {topic}?",
        "Hard": "Which order places the sentences in the time sequence used in the paragraph about {topic}?",
        "Ultra": "Which sequence gives the most logical time order for the paragraph about {topic}?",
    },
    "sequence_cause_effect": {
        "Easy": "Which order best shows cause and effect in the paragraph about {topic}?",
        "Medium": "Which sequence best follows the cause-and-effect flow of the paragraph about {topic}?",
        "Hard": "Which order shows the reason before the result in the paragraph about {topic}?",
        "Ultra": "Which sequence most clearly moves from action to effect in the paragraph about {topic}?",
    },
    "sequence_problem_solution": {
        "Easy": "Which order best shows the problem and solution in the paragraph about {topic}?",
        "Medium": "Which sequence best follows the problem-to-solution flow of the paragraph about {topic}?",
        "Hard": "Which order shows the need before the answer in the paragraph about {topic}?",
        "Ultra": "Which sequence most clearly moves from a problem to its solution in the paragraph about {topic}?",
    },
    "first_sentence": {
        "Easy": "Which sentence should come first in the paragraph about {topic}?",
        "Medium": "Which sentence is the best opening sentence for the paragraph about {topic}?",
        "Hard": "Which sentence best begins the paragraph about {topic}?",
        "Ultra": "Which opening sentence best fits the paragraph about {topic}?",
    },
    "last_sentence": {
        "Easy": "Which sentence should come last in the paragraph about {topic}?",
        "Medium": "Which sentence is the best closing sentence for the paragraph about {topic}?",
        "Hard": "Which sentence best ends the paragraph about {topic}?",
        "Ultra": "Which closing sentence best fits the paragraph about {topic}?",
    },
    "before_sentence": {
        "Easy": "Which sentence should come immediately before the sentence '{clue}'?",
        "Medium": "Which sentence belongs just before the sentence '{clue}'?",
        "Hard": "Which sentence must come directly before the sentence '{clue}'?",
        "Ultra": "Which sentence best leads into the sentence '{clue}'?",
    },
    "after_sentence": {
        "Easy": "Which sentence should come immediately after the sentence '{clue}'?",
        "Medium": "Which sentence belongs just after the sentence '{clue}'?",
        "Hard": "Which sentence must come directly after the sentence '{clue}'?",
        "Ultra": "Which sentence best follows the sentence '{clue}'?",
    },
    "pronoun_reference": {
        "Easy": "In the paragraph about {topic}, what does '{pronoun}' refer to?",
        "Medium": "In the paragraph about {topic}, what is the antecedent of '{pronoun}'?",
        "Hard": "What does '{pronoun}' point back to in the paragraph about {topic}?",
        "Ultra": "Which noun phrase is the antecedent of '{pronoun}' in the paragraph about {topic}?",
    },
    "off_topic": {
        "Easy": "Which sentence does not belong in the paragraph about {topic}?",
        "Medium": "Which sentence is off-topic for the paragraph about {topic}?",
        "Hard": "Which choice should be removed because it breaks the paragraph's flow on {topic}?",
        "Ultra": "Which sentence is least related to the paragraph about {topic}?",
    },
}


EXPLANATIONS: dict[str, str] = {
    "sequence_general_specific": "The answer moves from a broad idea to supporting details in the correct order.",
    "sequence_chronological": "The answer follows time order.",
    "sequence_cause_effect": "The answer places the cause before the result.",
    "sequence_problem_solution": "The answer puts the need or problem before the solution.",
    "first_sentence": "The answer gives the broad opening idea.",
    "last_sentence": "The answer gives the closing thought.",
    "before_sentence": "The answer is the sentence that logically leads into the clue sentence.",
    "after_sentence": "The answer is the sentence that logically follows the clue sentence.",
    "pronoun_reference": "The answer is the noun phrase the pronoun points back to.",
    "off_topic": "The answer breaks the paragraph's flow.",
}


TYPE_TAGS: dict[str, list[str]] = {
    "sequence_general_specific": ["paragraph-organization", "sequence_general_specific", "sequence"],
    "sequence_chronological": ["paragraph-organization", "sequence_chronological", "sequence"],
    "sequence_cause_effect": ["paragraph-organization", "sequence_cause_effect", "sequence"],
    "sequence_problem_solution": ["paragraph-organization", "sequence_problem_solution", "sequence"],
    "first_sentence": ["paragraph-organization", "first_sentence", "opening"],
    "last_sentence": ["paragraph-organization", "last_sentence", "closing"],
    "before_sentence": ["paragraph-organization", "before_sentence", "coherence"],
    "after_sentence": ["paragraph-organization", "after_sentence", "coherence"],
    "pronoun_reference": ["paragraph-organization", "pronoun_reference", "reference"],
    "off_topic": ["paragraph-organization", "off_topic", "coherence"],
}


@dataclass(frozen=True)
class TopicSpec:
    key: str
    topic: str
    sentences: tuple[str, str, str, str, str]
    off_topic: str
    pronoun: str
    pronoun_answer: str
    pronoun_distractor_1: str
    pronoun_distractor_2: str
    pronoun_distractor_3: str

    @property
    def paragraph_sentences(self) -> tuple[str, str, str, str, str]:
        return self.sentences


TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec(
        key="fire-drill-practice",
        topic="fire drill practice",
        sentences=(
            "A fire drill helps students leave the building safely and quickly.",
            "Teachers point to the nearest exits before the drill begins.",
            "Students walk in line to the assembly area.",
            "This practice reduces panic if a real alarm sounds.",
            "Repeated drills make the response automatic.",
        ),
        off_topic="The cafeteria served mango shakes after lunch.",
        pronoun="this",
        pronoun_answer="the fire drill",
        pronoun_distractor_1="the assembly area",
        pronoun_distractor_2="the exits",
        pronoun_distractor_3="the cafeteria",
    ),
    TopicSpec(
        key="classroom-recycling",
        topic="classroom recycling routine",
        sentences=(
            "A classroom recycling routine helps students keep the room tidy and reduce waste.",
            "Students separate paper, plastic, and metal into labeled bins.",
            "They save used worksheets in one tray for collection.",
            "This habit keeps the classroom cleaner and makes disposal easier.",
            "The teacher sees fewer mixed trash bags at the end of the week.",
        ),
        off_topic="The principal bought new curtains for the office.",
        pronoun="they",
        pronoun_answer="students",
        pronoun_distractor_1="the bins",
        pronoun_distractor_2="used worksheets",
        pronoun_distractor_3="the teacher",
    ),
    TopicSpec(
        key="clinic-appointment-board",
        topic="clinic appointment board",
        sentences=(
            "A clinic appointment board helps patients get care without long waits.",
            "Staff write each patient's name, time, and reason for the visit.",
            "Morning slots are reserved for checkups.",
            "Patients are called in the order listed on the board.",
            "This clear schedule keeps the waiting room from becoming crowded.",
        ),
        off_topic="The pharmacy displayed a poster about summer classes.",
        pronoun="this",
        pronoun_answer="the clear schedule",
        pronoun_distractor_1="the waiting room",
        pronoun_distractor_2="the board",
        pronoun_distractor_3="the poster",
    ),
    TopicSpec(
        key="bus-queue-etiquette",
        topic="bus queue etiquette",
        sentences=(
            "Good queue etiquette at a bus stop keeps riders orderly and safe.",
            "Passengers line up behind the painted mark.",
            "They wait until the bus stops completely.",
            "A neat line prevents pushing and confusion.",
            "Simple courtesy makes public transport easier for everyone.",
        ),
        off_topic="The newsstand sold comic books.",
        pronoun="they",
        pronoun_answer="passengers",
        pronoun_distractor_1="the bus",
        pronoun_distractor_2="the painted mark",
        pronoun_distractor_3="the newsstand",
    ),
    TopicSpec(
        key="canteen-cleanliness",
        topic="school canteen cleanliness",
        sentences=(
            "Clean canteen habits help keep food safe for students.",
            "Workers wipe tables after each lunch period.",
            "They sort trash before the floor is mopped.",
            "A clean area reduces germs and spills.",
            "Regular cleaning makes the canteen healthier and more pleasant.",
        ),
        off_topic="The library added a comic book shelf.",
        pronoun="they",
        pronoun_answer="workers",
        pronoun_distractor_1="the tables",
        pronoun_distractor_2="the trash",
        pronoun_distractor_3="the library",
    ),
    TopicSpec(
        key="library-return-policy",
        topic="library return policy",
        sentences=(
            "A clear book return policy helps a library keep materials available.",
            "Books are due back by a fixed date printed on the card.",
            "Borrowers return them before the next reader needs them.",
            "Late returns delay other readers who need the same book.",
            "When everyone follows the rule, more people can borrow books.",
        ),
        off_topic="The library bought new curtains for the lobby.",
        pronoun="them",
        pronoun_answer="books",
        pronoun_distractor_1="borrowers",
        pronoun_distractor_2="the card",
        pronoun_distractor_3="the lobby",
    ),
    TopicSpec(
        key="emergency-contact-card",
        topic="emergency contact card",
        sentences=(
            "An emergency contact card helps adults reach the right people quickly.",
            "The card lists names and phone numbers.",
            "It includes a parent, a guardian, and a neighbor.",
            "The information saves time during accidents or sudden illness.",
            "Keeping the card updated makes it more useful.",
        ),
        off_topic="The class painted a mural about summer.",
        pronoun="it",
        pronoun_answer="the emergency contact card",
        pronoun_distractor_1="the parent",
        pronoun_distractor_2="the neighbor",
        pronoun_distractor_3="the phone numbers",
    ),
    TopicSpec(
        key="drainage-cleanup",
        topic="drainage cleanup",
        sentences=(
            "Cleaning neighborhood drains helps prevent flooding during heavy rain.",
            "Residents remove leaves, mud, and plastic from the channels.",
            "They clear the drain near the corner store first.",
            "Open drains allow water to flow away from the street.",
            "Regular cleanup protects homes and sidewalks.",
        ),
        off_topic="The bakery made a larger birthday cake.",
        pronoun="they",
        pronoun_answer="residents",
        pronoun_distractor_1="the channels",
        pronoun_distractor_2="heavy rain",
        pronoun_distractor_3="the street",
    ),
    TopicSpec(
        key="farm-composting",
        topic="farm composting",
        sentences=(
            "Composting on a farm turns waste into useful fertilizer.",
            "Farmers pile leaves, stalks, and scraps in one area.",
            "They mix fruit peels with dry grass.",
            "The decaying material returns nutrients to the soil.",
            "What was once waste becomes a resource for planting.",
        ),
        off_topic="The store sold umbrellas by the entrance.",
        pronoun="they",
        pronoun_answer="farmers",
        pronoun_distractor_1="the soil",
        pronoun_distractor_2="the scraps",
        pronoun_distractor_3="the fertilizer",
    ),
    TopicSpec(
        key="seedling-nursery",
        topic="seedling nursery",
        sentences=(
            "A seedling nursery helps young plants grow strong before they are transplanted.",
            "Workers water the trays each morning.",
            "They shade fragile leaves from harsh sun.",
            "Gentle care gives the roots time to strengthen.",
            "Careful nursery work leads to better planting later.",
        ),
        off_topic="The shopkeeper stacked bottled drinks near the door.",
        pronoun="they",
        pronoun_answer="workers",
        pronoun_distractor_1="the trays",
        pronoun_distractor_2="young plants",
        pronoun_distractor_3="the sun",
    ),
    TopicSpec(
        key="community-mural-project",
        topic="community mural project",
        sentences=(
            "A blank wall can become a brighter public space when neighbors work together.",
            "Residents sketch ideas on a shared wall.",
            "Children paint small leaves around the border.",
            "More neighbors stop to take part when they see the design taking shape.",
            "The finished mural shows shared effort and local pride.",
        ),
        off_topic="The market closed early because of rain.",
        pronoun="they",
        pronoun_answer="neighbors",
        pronoun_distractor_1="residents",
        pronoun_distractor_2="children",
        pronoun_distractor_3="the design",
    ),
    TopicSpec(
        key="vegetable-stall-display",
        topic="vegetable stall display",
        sentences=(
            "A vegetable stall at the market attracts buyers with fresh produce and neat displays.",
            "Tomatoes are stacked by size and color.",
            "Carrots are bundled in small bunches for easy buying.",
            "They find what they need quickly.",
            "Good presentation helps the stall sell more produce.",
        ),
        off_topic="The tricycle driver changed the route yesterday.",
        pronoun="they",
        pronoun_answer="shoppers",
        pronoun_distractor_1="tomatoes",
        pronoun_distractor_2="carrots",
        pronoun_distractor_3="the market",
    ),
    TopicSpec(
        key="meeting-agenda",
        topic="meeting agenda",
        sentences=(
            "A meeting agenda helps a team cover important topics in order.",
            "The list shows the welcome, report, and action items.",
            "The chair can check off each item as it is discussed.",
            "This clear order prevents people from repeating the same points.",
            "An agenda keeps the meeting focused and efficient.",
        ),
        off_topic="The janitor polished the hallway floor.",
        pronoun="this",
        pronoun_answer="the clear order",
        pronoun_distractor_1="the chair",
        pronoun_distractor_2="the meeting",
        pronoun_distractor_3="the hallway floor",
    ),
    TopicSpec(
        key="coastal-barrier",
        topic="coastal barrier",
        sentences=(
            "A coastal barrier helps slow erosion and protect the shoreline.",
            "It weakens waves before they hit the sand.",
            "Rocks placed along the coast absorb force.",
            "After the barrier is built, the beach loses less sand.",
            "Barriers help preserve the coast over time.",
        ),
        off_topic="The village held a karaoke contest.",
        pronoun="it",
        pronoun_answer="the coastal barrier",
        pronoun_distractor_1="the beach",
        pronoun_distractor_2="the rocks",
        pronoun_distractor_3="the shoreline",
    ),
    TopicSpec(
        key="computer-lab-rules",
        topic="computer lab rules",
        sentences=(
            "Computer lab rules help students use equipment carefully and respectfully.",
            "Students log off before leaving the station.",
            "They keep food and drinks outside the lab.",
            "Careful habits protect the computers from damage.",
            "Rules keep the lab safe and usable for the next class.",
        ),
        off_topic="The basketball court was repainted blue.",
        pronoun="they",
        pronoun_answer="students",
        pronoun_distractor_1="the computers",
        pronoun_distractor_2="the station",
        pronoun_distractor_3="the lab",
    ),
)


def _normalize_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def _paragraph_text(topic: TopicSpec, difficulty: str) -> str:
    return " ".join(topic.paragraph_sentences)


def _sequence_subset(topic: TopicSpec, difficulty: str) -> tuple[str, ...]:
    if difficulty in {"Easy", "Medium"}:
        return topic.paragraph_sentences[:4]
    return topic.paragraph_sentences


def _sequence_display(
    topic: TopicSpec, difficulty: str, *, rng: random.Random
) -> tuple[str, str]:
    sentences = list(_sequence_subset(topic, difficulty))
    display_sentences = list(sentences)
    rng.shuffle(display_sentences)

    labels = [chr(ord("A") + index) for index in range(len(display_sentences))]
    display_lines = [f"{label}. {sentence}" for label, sentence in zip(labels, display_sentences)]
    display_text = "\n".join(display_lines)

    label_by_sentence = {sentence: label for label, sentence in zip(labels, display_sentences)}
    correct_sequence = "-".join(label_by_sentence[sentence] for sentence in sentences)
    return display_text, correct_sequence


def _sequence_distractors(correct: str, rng: random.Random) -> tuple[str, str, str]:
    parts = correct.split("-")
    if len(parts) == 4:
        a, b, c, d = parts
        candidates = [
            f"{a}-{c}-{b}-{d}",
            f"{b}-{a}-{c}-{d}",
            f"{a}-{b}-{d}-{c}",
        ]
    elif len(parts) == 5:
        a, b, c, d, e = parts
        candidates = [
            f"{a}-{c}-{b}-{d}-{e}",
            f"{b}-{a}-{c}-{d}-{e}",
            f"{a}-{b}-{d}-{c}-{e}",
        ]
    else:
        raise ValueError(f"unexpected sequence length: {correct}")

    rng.shuffle(candidates)
    return tuple(candidates[:3])


def _shuffle_choices(correct: str, distractors: Iterable[str], *, seed: str) -> list[str]:
    choices = [correct, *distractors]
    unique: list[str] = []
    seen: set[str] = set()
    for choice in choices:
        normalized = _normalize_whitespace(choice)
        if normalized in seen:
            continue
        seen.add(normalized)
        unique.append(normalized)

    if correct not in unique:
        raise ValueError(f"correct answer missing from choice set: {correct!r}")

    rng = random.Random(seed)
    rng.shuffle(unique)
    return unique


def _choice_sets(
    topic: TopicSpec, difficulty: str, qtype: str, *, rng: random.Random
) -> tuple[list[str], str, list[str]]:
    sentences = topic.paragraph_sentences

    if qtype.startswith("sequence_"):
        display_text, correct = _sequence_display(topic, difficulty, rng=rng)
        distractors = _sequence_distractors(correct, rng)
        return [display_text], correct, list(distractors)

    if qtype == "first_sentence":
        correct = sentences[0]
        if difficulty == "Easy":
            distractors = (sentences[1], sentences[2], topic.off_topic)
        elif difficulty == "Medium":
            distractors = (sentences[1], sentences[3], topic.off_topic)
        elif difficulty == "Hard":
            distractors = (sentences[2], sentences[3], topic.off_topic)
        else:
            distractors = (sentences[1], sentences[4], topic.off_topic)
    elif qtype == "last_sentence":
        correct = sentences[-1]
        if difficulty == "Easy":
            distractors = (sentences[2], sentences[3], topic.off_topic)
        elif difficulty == "Medium":
            distractors = (sentences[1], sentences[3], topic.off_topic)
        elif difficulty == "Hard":
            distractors = (sentences[1], sentences[2], topic.off_topic)
        else:
            distractors = (sentences[2], sentences[3], topic.off_topic)
    elif qtype == "before_sentence":
        clue_sentence = sentences[3]
        correct = sentences[2]
        if difficulty == "Easy":
            distractors = (sentences[0], sentences[1], topic.off_topic)
        elif difficulty == "Medium":
            distractors = (sentences[0], sentences[4], topic.off_topic)
        elif difficulty == "Hard":
            distractors = (sentences[1], sentences[4], topic.off_topic)
        else:
            distractors = (sentences[0], sentences[1], sentences[4])
    elif qtype == "after_sentence":
        clue_sentence = sentences[1]
        correct = sentences[2]
        if difficulty == "Easy":
            distractors = (sentences[0], sentences[3], topic.off_topic)
        elif difficulty == "Medium":
            distractors = (sentences[0], sentences[4], topic.off_topic)
        elif difficulty == "Hard":
            distractors = (sentences[3], sentences[4], topic.off_topic)
        else:
            distractors = (sentences[0], sentences[3], sentences[4])
    elif qtype == "pronoun_reference":
        correct = topic.pronoun_answer
        distractors = (
            topic.pronoun_distractor_1,
            topic.pronoun_distractor_2,
            topic.pronoun_distractor_3,
        )
    elif qtype == "off_topic":
        correct = topic.off_topic
        if difficulty == "Easy":
            distractors = (sentences[0], sentences[2], sentences[4])
        elif difficulty == "Medium":
            distractors = (sentences[1], sentences[3], sentences[4])
        elif difficulty == "Hard":
            distractors = (sentences[0], sentences[1], sentences[3])
        else:
            distractors = (sentences[0], sentences[2], sentences[3])
    else:
        raise ValueError(f"unsupported question type: {qtype}")

    return [], correct, list(distractors)


def _question_stem(topic: TopicSpec, difficulty: str, qtype: str) -> str:
    stem = STEMS[qtype][difficulty].format(
        topic=topic.topic,
        pronoun=topic.pronoun,
        clue=topic.sentences[3] if qtype == "before_sentence" else topic.sentences[1] if qtype == "after_sentence" else "",
    )

    if qtype.startswith("sequence_"):
        return stem

    return f"{_paragraph_text(topic, difficulty)}\n\n{stem}"


def _make_record(
    *,
    index: int,
    topic: TopicSpec,
    difficulty: str,
    qtype: str,
    rng: random.Random,
) -> dict[str, object]:
    stem = _question_stem(topic, difficulty, qtype)
    prefix, correct, distractors = _choice_sets(topic, difficulty, qtype, rng=rng)

    if qtype.startswith("sequence_"):
        stem = f"{prefix[0]}\n\n{stem}"

    choices = _shuffle_choices(correct, distractors, seed=f"{topic.key}:{difficulty}:{qtype}:{index}")
    explanation = EXPLANATIONS[qtype]
    tags = [*TYPE_TAGS[qtype], difficulty.lower(), topic.key]

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": stem,
        "choices": choices,
        "answer": correct,
        "explanation": explanation,
        "tags": tags,
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _generate_bank() -> list[dict[str, object]]:
    items: list[dict[str, object]] = []
    question_id = 1

    for difficulty in DIFFICULTIES:
        for topic in TOPICS:
            for qtype in QUESTION_TYPES:
                rng = random.Random(f"{topic.key}:{difficulty}:{qtype}")
                record = _make_record(
                    index=question_id,
                    topic=topic,
                    difficulty=difficulty,
                    qtype=qtype,
                    rng=rng,
                )
                items.append(record)
                question_id += 1

    return items


def _validate_bank(items: list[dict[str, object]]) -> None:
    if len(items) != 600:
        raise ValueError(f"expected 600 questions, found {len(items)}")

    difficulty_counts = {difficulty: 0 for difficulty in DIFFICULTIES}
    type_counts: dict[tuple[str, str], int] = {}
    seen_questions: set[str] = set()

    for expected_id, item in enumerate(items, start=1):
        if item.get("id") != expected_id:
            raise ValueError(f"question ids must be sequential; found {item.get('id')} at position {expected_id}")

        difficulty = str(item.get("difficulty", "")).strip()
        if difficulty not in difficulty_counts:
            raise ValueError(f"unexpected difficulty: {difficulty}")
        difficulty_counts[difficulty] += 1

        question = str(item.get("question", "")).strip()
        if not question:
            raise ValueError(f"blank question text at id {expected_id}")
        if question in seen_questions:
            raise ValueError(f"duplicate question text at id {expected_id}")
        seen_questions.add(question)

        choices = item.get("choices")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError(f"invalid choices at id {expected_id}")
        normalized = [_normalize_whitespace(choice) for choice in choices]
        if any(not choice for choice in normalized):
            raise ValueError(f"blank choice at id {expected_id}")
        if len(set(normalized)) != 4:
            raise ValueError(f"duplicate choices at id {expected_id}")

        answer = _normalize_whitespace(str(item.get("answer", "")))
        if answer not in normalized:
            raise ValueError(f"answer {answer!r} missing from choices at id {expected_id}")

        explanation = str(item.get("explanation", "")).strip()
        if not explanation:
            raise ValueError(f"blank explanation at id {expected_id}")

        tags = item.get("tags")
        if not isinstance(tags, list) or len(tags) < 4:
            raise ValueError(f"invalid tags at id {expected_id}")

        qtype = str(tags[1])
        key = (difficulty, qtype)
        type_counts[key] = type_counts.get(key, 0) + 1

    if difficulty_counts != {difficulty: 150 for difficulty in DIFFICULTIES}:
        raise ValueError(f"unexpected difficulty distribution: {difficulty_counts}")

    for difficulty in DIFFICULTIES:
        per_type = {qtype: type_counts.get((difficulty, qtype), 0) for qtype in QUESTION_TYPES}
        if any(count != 15 for count in per_type.values()):
            raise ValueError(f"unexpected type distribution for {difficulty}: {per_type}")


def main() -> None:
    items = _generate_bank()
    _validate_bank(items)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(items, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {len(items)} questions to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
