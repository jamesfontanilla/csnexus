"""Generate the Verbal Ability / Paragraph Organization / Main Idea question bank.

The bank is built from a small set of carefully curated paragraph scenarios.
Each scenario yields 10 CSE-style question types across four difficulty bands,
for a total of 600 unique items.
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
    / "main-idea"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Paragraph Organization"
SUBTOPIC = "Main Idea"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
QUESTION_TYPES = (
    "main_idea",
    "title",
    "summary",
    "topic_sentence",
    "support_detail",
    "off_topic",
    "sequence",
    "concluding_sentence",
    "scope_broad",
    "scope_narrow",
)


STEMS: dict[str, dict[str, str]] = {
    "main_idea": {
        "Easy": "What is the main idea of the paragraph about {topic}?",
        "Medium": "Which choice best states the central idea of the paragraph about {topic}?",
        "Hard": "Which statement best captures the controlling idea of the paragraph about {topic}?",
        "Ultra": "Which option most accurately expresses the controlling idea of the paragraph about {topic}?",
    },
    "title": {
        "Easy": "Which title best fits the paragraph about {topic}?",
        "Medium": "Which title best matches the paragraph about {topic}?",
        "Hard": "Which title best captures the paragraph about {topic}?",
        "Ultra": "Which title best reflects the controlling idea of the paragraph about {topic}?",
    },
    "summary": {
        "Easy": "Which sentence best summarizes the paragraph about {topic}?",
        "Medium": "Which choice gives the best summary of the paragraph about {topic}?",
        "Hard": "Which statement best summarizes the paragraph about {topic}?",
        "Ultra": "Which option best condenses the paragraph about {topic} without losing its main point?",
    },
    "topic_sentence": {
        "Easy": "Which sentence would make the best topic sentence for the paragraph about {topic}?",
        "Medium": "Which sentence would best open the paragraph about {topic} as a topic sentence?",
        "Hard": "Which sentence is the best topic sentence for the paragraph about {topic}?",
        "Ultra": "Which opening sentence best establishes the controlling idea of the paragraph about {topic}?",
    },
    "support_detail": {
        "Easy": "Which sentence best supports the main idea of the paragraph about {topic}?",
        "Medium": "Which sentence is the best supporting detail for the paragraph about {topic}?",
        "Hard": "Which choice most directly supports the main idea of the paragraph about {topic}?",
        "Ultra": "Which option most clearly stays within the scope of the paragraph about {topic}?",
    },
    "off_topic": {
        "Easy": "Which sentence does not belong in the paragraph about {topic}?",
        "Medium": "Which sentence is off-topic for the paragraph about {topic}?",
        "Hard": "Which choice should be removed because it does not fit the paragraph about {topic}?",
        "Ultra": "Which sentence breaks the paragraph's focus on {topic}?",
    },
    "sequence": {
        "Easy": "Choose the best order and sequence of the sentences to form a well-organized paragraph about {topic}.",
        "Medium": "Which sequence arranges the sentences into the best paragraph about {topic}?",
        "Hard": "Which order makes the passage about {topic} flow logically?",
        "Ultra": "Which sequence gives the most coherent paragraph about {topic}?",
    },
    "concluding_sentence": {
        "Easy": "Which sentence best concludes the paragraph about {topic}?",
        "Medium": "Which sentence is the best closing sentence for the paragraph about {topic}?",
        "Hard": "Which choice would be the strongest concluding sentence for the paragraph about {topic}?",
        "Ultra": "Which option best wraps up the paragraph about {topic} without introducing a new idea?",
    },
    "scope_broad": {
        "Easy": "Which choice is too broad to serve as the main idea of the paragraph about {topic}?",
        "Medium": "Which sentence is too broad for the main idea of the paragraph about {topic}?",
        "Hard": "Which option covers more than the paragraph about {topic} actually explains?",
        "Ultra": "Which choice is broader than the paragraph's controlling idea about {topic}?",
    },
    "scope_narrow": {
        "Easy": "Which choice is too narrow to serve as the main idea of the paragraph about {topic}?",
        "Medium": "Which sentence is too narrow for the main idea of the paragraph about {topic}?",
        "Hard": "Which option focuses on only one detail instead of the full paragraph about {topic}?",
        "Ultra": "Which choice is narrower than the paragraph's controlling idea about {topic}?",
    },
}

EXPLANATIONS: dict[str, str] = {
    "main_idea": "The answer is the broad point that the other sentences support.",
    "title": "The answer matches the paragraph's main point and scope.",
    "summary": "The answer condenses the paragraph without drifting into one detail.",
    "topic_sentence": "The answer is broad enough to open the paragraph and support the details that follow.",
    "support_detail": "The answer is a supporting detail, not the whole point.",
    "off_topic": "The answer breaks the paragraph's focus.",
    "sequence": "The answer orders the sentences from the general idea to the details and closing idea.",
    "concluding_sentence": "The answer wraps up the paragraph without introducing a new idea.",
    "scope_broad": "The answer is broader than the paragraph's actual focus.",
    "scope_narrow": "The answer is narrower than the paragraph's actual focus.",
}

TYPE_TAGS: dict[str, list[str]] = {
    "main_idea": ["paragraph-organization", "main_idea", "direct"],
    "title": ["paragraph-organization", "title", "direct"],
    "summary": ["paragraph-organization", "summary", "direct"],
    "topic_sentence": ["paragraph-organization", "topic_sentence", "direct"],
    "support_detail": ["paragraph-organization", "support_detail", "detail"],
    "off_topic": ["paragraph-organization", "off_topic", "coherence"],
    "sequence": ["paragraph-organization", "sequence", "sequence"],
    "concluding_sentence": ["paragraph-organization", "concluding_sentence", "coherence"],
    "scope_broad": ["paragraph-organization", "scope_broad", "broad"],
    "scope_narrow": ["paragraph-organization", "scope_narrow", "narrow"],
}


@dataclass(frozen=True)
class TopicSpec:
    key: str
    topic: str
    main_idea: str
    support: tuple[str, str, str]
    off_topic: str
    broad: str
    narrow: str
    title: str
    title_broad: str
    title_narrow: str
    title_off: str
    summary: str
    summary_detail: str
    closing: str

    @property
    def paragraph_sentences(self) -> tuple[str, str, str, str, str]:
        return (self.main_idea, *self.support, self.closing)


TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec(
        key="community-garden",
        topic="community garden",
        main_idea="A community garden helps neighbors share space, food, and responsibility.",
        support=(
            "Volunteers water the beds and clear the paths.",
            "Children learn how vegetables grow from seeds to harvest.",
            "Families bring compost, tools, and extra seedlings.",
        ),
        off_topic="The city painted the bus terminal red.",
        broad="Community projects can improve neighborhoods.",
        narrow="The garden has three raised beds.",
        title="A Garden That Brings People Together",
        title_broad="Why Shared Projects Matter",
        title_narrow="Watering the Garden Beds",
        title_off="Painting the Bus Terminal",
        summary="The paragraph explains that a community garden gives neighbors a shared project that teaches and helps the neighborhood.",
        summary_detail="The paragraph focuses on watering the beds and clearing the paths.",
        closing="Together, these details show that the garden turns an unused lot into a useful shared space.",
    ),
    TopicSpec(
        key="reading-club",
        topic="library reading club",
        main_idea="A library reading club helps students build confidence, vocabulary, and discussion skills.",
        support=(
            "Members read the same book and talk about unfamiliar words.",
            "They practice sharing opinions aloud.",
            "The club gives students a regular time to read together.",
        ),
        off_topic="The librarian ordered new curtains for the office.",
        broad="Reading activities can help students grow.",
        narrow="The club meets every Tuesday afternoon.",
        title="Why a Reading Club Matters",
        title_broad="Why Reading Matters",
        title_narrow="Talking About Unfamiliar Words",
        title_off="The Office Curtain Order",
        summary="The paragraph shows that a reading club helps students read more carefully and speak more confidently.",
        summary_detail="The paragraph focuses on reading the same book and practicing discussion.",
        closing="The club helps students turn reading into a shared habit.",
    ),
    TopicSpec(
        key="recycling-drive",
        topic="school recycling drive",
        main_idea="A school recycling drive teaches students to sort waste and reduce trash.",
        support=(
            "Bins are labeled paper, plastic, and metal.",
            "Students collect bottles from classrooms.",
            "Classes track how much waste they divert.",
        ),
        off_topic="The principal bought new basketballs.",
        broad="Schools can teach responsibility.",
        narrow="The paper bin is next to the cafeteria.",
        title="How a Recycling Drive Works at School",
        title_broad="Why School Responsibility Matters",
        title_narrow="Sorting Paper and Plastic",
        title_off="Buying New Basketballs",
        summary="The paragraph explains that a recycling drive turns disposal into a lesson about responsibility.",
        summary_detail="The paragraph focuses on labeled bins and collecting bottles.",
        closing="The drive helps students see how small habits reduce waste.",
    ),
    TopicSpec(
        key="neighborhood-watch",
        topic="neighborhood watch",
        main_idea="A neighborhood watch can make a street feel safer and more connected.",
        support=(
            "Neighbors report unusual activity.",
            "Volunteers check streetlights.",
            "Residents share emergency contacts.",
        ),
        off_topic="The bakery changed the color of its menu.",
        broad="Communities need ways to stay safe.",
        narrow="The watch team meets on Thursday evenings.",
        title="Building Safety Through Neighbor Cooperation",
        title_broad="Why Community Safety Matters",
        title_narrow="Sharing Emergency Contacts",
        title_off="The Bakery Menu Change",
        summary="The paragraph shows that a watch group improves safety by keeping people alert and in contact.",
        summary_detail="The paragraph focuses on neighbors reporting activity and checking lights.",
        closing="The group helps neighbors look out for one another.",
    ),
    TopicSpec(
        key="transit-schedule",
        topic="public transit schedule",
        main_idea="A clear transit schedule helps riders plan trips and avoid delays.",
        support=(
            "It shows exact departure times.",
            "It lists transfer points.",
            "It notes when buses run less often.",
        ),
        off_topic="The station sold souvenirs near the entrance.",
        broad="Good transportation saves time.",
        narrow="The first bus leaves at 6:10 a.m.",
        title="Why Transit Schedules Matter",
        title_broad="Why Public Transit Matters",
        title_narrow="Transfer Points on the Route",
        title_off="Buying Souvenirs at the Station",
        summary="The paragraph explains that a schedule makes travel easier because riders can plan ahead.",
        summary_detail="The paragraph focuses on exact departure times and transfer points.",
        closing="A good schedule keeps travel predictable.",
    ),
    TopicSpec(
        key="handwashing",
        topic="hospital handwashing",
        main_idea="Careful handwashing helps prevent the spread of infection in hospitals.",
        support=(
            "Staff clean hands before patient contact.",
            "Soap removes germs from skin.",
            "Reminders appear near sinks.",
        ),
        off_topic="The cafeteria began serving mango shakes.",
        broad="Hospitals must protect health.",
        narrow="Nurses use warm water.",
        title="Why Clean Hands Protect Patients",
        title_broad="Why Hospital Safety Matters",
        title_narrow="Cleaning Hands Before Patient Contact",
        title_off="Mango Shakes in the Cafeteria",
        summary="The paragraph shows that handwashing keeps patients safer by lowering the chance of infection.",
        summary_detail="The paragraph focuses on staff cleaning hands before patient contact and soap removing germs.",
        closing="Clean hands protect both patients and staff.",
    ),
    TopicSpec(
        key="farmers-market",
        topic="farmers market",
        main_idea="A farmers market gives shoppers fresh food and supports local growers.",
        support=(
            "Produce is picked close to market day.",
            "Farmers keep more of the sale.",
            "Shoppers can ask how food is grown.",
        ),
        off_topic="The parking lot was repaved last summer.",
        broad="Local food systems can strengthen a community.",
        narrow="One vendor sells sweet corn on Saturdays.",
        title="Benefits of Buying at a Farmers Market",
        title_broad="Why Local Food Matters",
        title_narrow="Fresh Produce Near Market Day",
        title_off="Repaving the Parking Lot",
        summary="The paragraph explains that a farmers market helps both shoppers and farmers.",
        summary_detail="The paragraph focuses on fresh food, local growers, and shopper questions.",
        closing="The market connects fresh food with the people who grow it.",
    ),
    TopicSpec(
        key="storm-preparedness",
        topic="storm preparedness",
        main_idea="Preparing for a storm helps families stay calm and safe when bad weather arrives.",
        support=(
            "Households store water and flashlights.",
            "They secure loose items outside.",
            "They know evacuation routes.",
        ),
        off_topic="The school painted the library door green.",
        broad="Weather can change quickly.",
        narrow="The family keeps candles in a drawer.",
        title="Getting Ready Before a Storm",
        title_broad="Why Weather Preparation Matters",
        title_narrow="Storing Water and Flashlights",
        title_off="Painting the Library Door Green",
        summary="The paragraph shows that preparation reduces panic and damage during severe weather.",
        summary_detail="The paragraph focuses on storing supplies and knowing evacuation routes.",
        closing="Preparation turns a storm from a surprise into a plan.",
    ),
    TopicSpec(
        key="filing-system",
        topic="office filing system",
        main_idea="A filing system helps workers find records quickly and avoid mistakes.",
        support=(
            "Folders are labeled by date.",
            "Papers are kept in one place.",
            "Old files are archived in order.",
        ),
        off_topic="The office installed a new coffee machine.",
        broad="Organization improves office work.",
        narrow="The red folder holds payroll forms.",
        title="Why an Organized Filing System Helps",
        title_broad="Why Office Organization Matters",
        title_narrow="Labeling and Archiving Files",
        title_off="The New Coffee Machine",
        summary="The paragraph explains that a filing system saves time because documents are easier to locate.",
        summary_detail="The paragraph focuses on labeled folders and archived files.",
        closing="An orderly system makes the office more efficient.",
    ),
    TopicSpec(
        key="volunteer-tutoring",
        topic="volunteer tutoring",
        main_idea="Volunteer tutoring gives students extra practice and personal encouragement.",
        support=(
            "Tutors review homework.",
            "They explain difficult lessons slowly.",
            "They praise small improvements.",
        ),
        off_topic="The gym replaced the broken mirror.",
        broad="Extra help can improve learning.",
        narrow="The tutor meets the class after school.",
        title="How Volunteer Tutors Support Students",
        title_broad="Why Extra Help Matters",
        title_narrow="Explaining Difficult Lessons Slowly",
        title_off="Replacing the Broken Mirror",
        summary="The paragraph shows that tutoring helps students understand lessons and stay motivated.",
        summary_detail="The paragraph focuses on homework review, slow explanations, and praise.",
        closing="The extra attention helps learners keep up and gain confidence.",
    ),
    TopicSpec(
        key="coastal-cleanup",
        topic="coastal cleanup",
        main_idea="A coastal cleanup protects marine life and keeps the shore pleasant for visitors.",
        support=(
            "Volunteers collect plastic from the sand.",
            "They sort recyclable items before disposal.",
            "They remove fishing line that can hurt animals.",
        ),
        off_topic="The town built a new fountain downtown.",
        broad="Keeping beaches clean is important.",
        narrow="The cleanup starts near the pier.",
        title="Why Cleaning the Shore Matters",
        title_broad="Why Coastal Care Matters",
        title_narrow="Removing Plastic and Fishing Line",
        title_off="A New Fountain Downtown",
        summary="The paragraph explains that cleaning the coast protects animals and improves the shoreline.",
        summary_detail="The paragraph focuses on collecting trash and protecting animals.",
        closing="The cleanup helps both the environment and the people who use the beach.",
    ),
    TopicSpec(
        key="science-fair",
        topic="science fair",
        main_idea="A science fair helps students investigate questions and explain their findings.",
        support=(
            "They test ideas with simple experiments.",
            "They record results carefully.",
            "They present conclusions to visitors.",
        ),
        off_topic="The cafeteria served adobo for lunch.",
        broad="Science helps students learn.",
        narrow="The display board uses blue lettering.",
        title="What Students Learn from a Science Fair",
        title_broad="Why Student Science Matters",
        title_narrow="Testing Ideas and Sharing Results",
        title_off="Adobo for Lunch",
        summary="The paragraph shows that a science fair builds research, writing, and speaking skills.",
        summary_detail="The paragraph focuses on experiments, recording results, and presenting conclusions.",
        closing="The fair teaches students how to think like young researchers.",
    ),
    TopicSpec(
        key="mobile-payment-safety",
        topic="mobile payment safety",
        main_idea="Using mobile payments safely means checking details before confirming a transaction.",
        support=(
            "Users verify the recipient name.",
            "They review the amount.",
            "They keep login information private.",
        ),
        off_topic="The phone case was delivered in a red box.",
        broad="Digital tools can simplify buying and selling.",
        narrow="The app has a blue home screen.",
        title="Staying Safe with Mobile Payments",
        title_broad="Why Digital Payment Habits Matter",
        title_narrow="Checking the Recipient Before Paying",
        title_off="A Red Phone Case",
        summary="The paragraph explains that careful checking prevents payment mistakes and fraud.",
        summary_detail="The paragraph focuses on verifying recipient names, amounts, and privacy.",
        closing="Careful checking protects money and personal information.",
    ),
    TopicSpec(
        key="park-maintenance",
        topic="park maintenance",
        main_idea="Regular park maintenance keeps public spaces clean, safe, and pleasant.",
        support=(
            "Workers trim overgrown grass.",
            "They empty trash bins.",
            "They inspect playground equipment.",
        ),
        off_topic="The city opened a new art gallery.",
        broad="Public spaces need regular care.",
        narrow="The bench near the entrance was repainted.",
        title="The Value of Keeping Parks in Good Shape",
        title_broad="Why Public Spaces Matter",
        title_narrow="Trimming Grass and Emptying Bins",
        title_off="The New Art Gallery",
        summary="The paragraph shows that maintenance makes parks safer and more enjoyable.",
        summary_detail="The paragraph focuses on trimming grass, emptying bins, and inspecting equipment.",
        closing="Ongoing upkeep keeps the park useful for everyone.",
    ),
    TopicSpec(
        key="farm-irrigation",
        topic="farm irrigation",
        main_idea="A reliable irrigation system helps crops get water even when rain is scarce.",
        support=(
            "Channels carry water to dry soil.",
            "Timers control when pumps run.",
            "Farmers adjust flow to match plant needs.",
        ),
        off_topic="The farmhouse gained a bigger porch.",
        broad="Farming depends on many systems.",
        narrow="The irrigation pump sits near the field gate.",
        title="Why Irrigation Matters on a Farm",
        title_broad="Why Farm Water Systems Matter",
        title_narrow="Watering Crops When Rain Is Scarce",
        title_off="The Bigger Porch",
        summary="The paragraph explains that irrigation supports plant growth by supplying water on schedule.",
        summary_detail="The paragraph focuses on channels, timers, and matching water flow to plant needs.",
        closing="Consistent watering helps crops stay healthy.",
    ),
)


def _title_case(text: str) -> str:
    return " ".join(part.capitalize() for part in text.split())


def _normalize_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def _paragraph_text(topic: TopicSpec, difficulty: str) -> str:
    if difficulty == "Easy":
        sentences = topic.paragraph_sentences[:3]
    elif difficulty == "Medium":
        sentences = topic.paragraph_sentences[:4]
    else:
        sentences = topic.paragraph_sentences
    return " ".join(sentences)


def _sequence_display(topic: TopicSpec, difficulty: str, *, rng: random.Random) -> tuple[str, str]:
    if difficulty in {"Easy", "Medium"}:
        sentences = topic.paragraph_sentences[:4]
    else:
        sentences = topic.paragraph_sentences

    display_sentences = list(sentences)
    rng.shuffle(display_sentences)

    labels = [chr(ord("A") + index) for index in range(len(display_sentences))]
    display_lines = [f"{label}. {sentence}" for label, sentence in zip(labels, display_sentences)]
    display_text = "\n".join(display_lines)

    label_by_sentence = {sentence: label for label, sentence in zip(labels, display_sentences)}
    correct_sequence = "-".join(label_by_sentence[sentence] for sentence in sentences)
    return display_text, correct_sequence


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


def _summary_distractors(topic: TopicSpec) -> tuple[str, str, str]:
    return (
        topic.summary_detail,
        topic.broad,
        topic.off_topic,
    )


def _choice_sets(
    topic: TopicSpec, difficulty: str, qtype: str, *, rng: random.Random
) -> tuple[list[str], str, list[str]]:
    if qtype == "main_idea":
        correct = topic.main_idea
        distractors = (topic.broad, topic.narrow, topic.off_topic)
    elif qtype == "title":
        correct = topic.title
        distractors = (topic.title_broad, topic.title_narrow, topic.title_off)
    elif qtype == "summary":
        correct = topic.summary
        distractors = _summary_distractors(topic)
    elif qtype == "topic_sentence":
        correct = topic.main_idea
        distractors = (topic.support[0], topic.narrow, topic.off_topic)
    elif qtype == "support_detail":
        correct = topic.support[0]
        distractors = (topic.main_idea, topic.broad, topic.off_topic)
    elif qtype == "off_topic":
        correct = topic.off_topic
        distractors = (topic.main_idea, topic.support[0], topic.support[1])
    elif qtype == "sequence":
        display_text, correct = _sequence_display(topic, difficulty, rng=rng)
        distractors = _sequence_distractors(correct, rng)
        return [display_text], correct, list(distractors)
    elif qtype == "concluding_sentence":
        correct = topic.closing
        distractors = (topic.support[2], topic.broad, topic.off_topic)
    elif qtype == "scope_broad":
        correct = topic.broad
        distractors = (topic.main_idea, topic.narrow, topic.off_topic)
    elif qtype == "scope_narrow":
        correct = topic.narrow
        distractors = (topic.main_idea, topic.broad, topic.off_topic)
    else:
        raise ValueError(f"unsupported question type: {qtype}")

    return [], correct, list(distractors)


def _sequence_distractors(correct: str, rng: random.Random) -> tuple[str, str, str]:
    parts = correct.split("-")
    if len(parts) == 4:
        a, b, c, d = parts
        candidates = (
            f"{a}-{c}-{b}-{d}",
            f"{b}-{a}-{c}-{d}",
            f"{a}-{b}-{d}-{c}",
        )
    elif len(parts) == 5:
        a, b, c, d, e = parts
        candidates = (
            f"{a}-{c}-{b}-{d}-{e}",
            f"{b}-{a}-{c}-{d}-{e}",
            f"{a}-{b}-{d}-{c}-{e}",
        )
    else:
        raise ValueError(f"unexpected sequence length: {correct}")

    ordered = list(candidates)
    rng.shuffle(ordered)
    return tuple(ordered[:3])


def _question_stem(topic: TopicSpec, difficulty: str, qtype: str) -> str:
    stem = STEMS[qtype][difficulty].format(topic=topic.topic)
    if qtype == "sequence":
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

    if qtype == "sequence":
        display_text = prefix[0]
        stem = f"{display_text}\n\n{stem}"

    choices = _shuffle_choices(correct, distractors, seed=f"{topic.key}:{difficulty}:{qtype}:{index}")

    if qtype == "sequence":
        explanation = EXPLANATIONS[qtype]
    else:
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

    expected_types = {difficulty: 150 for difficulty in DIFFICULTIES}
    if difficulty_counts != expected_types:
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
