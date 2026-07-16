"""Generate the Verbal Ability / Paragraph Organization / Supporting Details question bank.

The bank uses 15 curated paragraph scenarios. Each scenario yields 10 question
types across four difficulty bands for a total of 600 unique items.
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
    / "supporting-details"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Paragraph Organization"
SUBTOPIC = "Supporting Details"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
DIFFICULTIES = ("Easy", "Medium", "Hard", "Ultra")
QUESTION_TYPES = (
    "topic_sentence",
    "support_detail",
    "example_detail",
    "reason_detail",
    "evidence_detail",
    "off_topic",
    "title",
    "summary",
    "sequence",
    "concluding_sentence",
)


STEMS: dict[str, dict[str, str]] = {
    "topic_sentence": {
        "Easy": "Which sentence would best open a paragraph about {topic}?",
        "Medium": "Which sentence is the best topic sentence for the paragraph about {topic}?",
        "Hard": "Which opening sentence best fits the paragraph about {topic}?",
        "Ultra": "Which opening sentence best establishes the paragraph's focus on {topic}?",
    },
    "support_detail": {
        "Easy": "Which sentence best supports the paragraph about {topic}?",
        "Medium": "Which sentence is the strongest supporting detail for the paragraph about {topic}?",
        "Hard": "Which choice most directly supports the topic sentence about {topic}?",
        "Ultra": "Which option gives the clearest support without drifting away from {topic}?",
    },
    "example_detail": {
        "Easy": "Which sentence gives the best example about {topic}?",
        "Medium": "Which sentence is the best illustrative example for the paragraph about {topic}?",
        "Hard": "Which choice best provides an example that supports {topic}?",
        "Ultra": "Which option most clearly illustrates the idea being developed about {topic}?",
    },
    "reason_detail": {
        "Easy": "Which sentence gives a reason why {topic} matters?",
        "Medium": "Which sentence best explains why the idea about {topic} is important?",
        "Hard": "Which choice most clearly states a reason supporting the paragraph about {topic}?",
        "Ultra": "Which option provides the strongest reason for the paragraph's point about {topic}?",
    },
    "evidence_detail": {
        "Easy": "Which sentence gives evidence or proof about {topic}?",
        "Medium": "Which sentence is the best factual support for the paragraph about {topic}?",
        "Hard": "Which choice most clearly adds evidence for the idea about {topic}?",
        "Ultra": "Which option most directly strengthens the paragraph with proof about {topic}?",
    },
    "off_topic": {
        "Easy": "Which sentence does not belong in the paragraph about {topic}?",
        "Medium": "Which sentence is off-topic for the paragraph about {topic}?",
        "Hard": "Which choice should be removed because it breaks the focus on {topic}?",
        "Ultra": "Which sentence is least related to the paragraph's focus on {topic}?",
    },
    "title": {
        "Easy": "Which title best fits the paragraph about {topic}?",
        "Medium": "Which title best matches the paragraph about {topic}?",
        "Hard": "Which title best captures the paragraph about {topic}?",
        "Ultra": "Which title most accurately reflects the paragraph's focus on {topic}?",
    },
    "summary": {
        "Easy": "Which sentence best summarizes the paragraph about {topic}?",
        "Medium": "Which choice gives the best summary of the paragraph about {topic}?",
        "Hard": "Which statement best summarizes the paragraph about {topic}?",
        "Ultra": "Which option best condenses the paragraph about {topic} without losing its support?",
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
        "Ultra": "Which option best wraps up the paragraph about {topic} without adding a new idea?",
    },
}


EXPLANATIONS: dict[str, str] = {
    "topic_sentence": "The answer opens the paragraph with a broad focus that the details can support.",
    "support_detail": "The answer gives a direct supporting detail that develops the topic sentence.",
    "example_detail": "The answer gives a concrete example that illustrates the idea.",
    "reason_detail": "The answer explains why the paragraph's idea matters.",
    "evidence_detail": "The answer adds proof or factual support for the paragraph.",
    "off_topic": "The answer breaks the paragraph's focus and should be removed.",
    "title": "The answer matches the paragraph's central focus without being too broad or too narrow.",
    "summary": "The answer condenses the paragraph without losing its main support.",
    "sequence": "The answer orders the sentences from the broad idea to the details and closing line.",
    "concluding_sentence": "The answer wraps up the paragraph without introducing a new idea.",
}


TYPE_TAGS: dict[str, list[str]] = {
    "topic_sentence": ["paragraph-organization", "topic_sentence", "direct"],
    "support_detail": ["paragraph-organization", "support_detail", "support"],
    "example_detail": ["paragraph-organization", "example_detail", "example"],
    "reason_detail": ["paragraph-organization", "reason_detail", "reason"],
    "evidence_detail": ["paragraph-organization", "evidence_detail", "evidence"],
    "off_topic": ["paragraph-organization", "off_topic", "coherence"],
    "title": ["paragraph-organization", "title", "direct"],
    "summary": ["paragraph-organization", "summary", "direct"],
    "sequence": ["paragraph-organization", "sequence", "sequence"],
    "concluding_sentence": ["paragraph-organization", "concluding_sentence", "coherence"],
}


@dataclass(frozen=True)
class TopicSpec:
    key: str
    topic: str
    opener: str
    detail: str
    example: str
    reason: str
    evidence: str
    closing: str
    off_topic: str
    title: str
    title_broad: str
    title_narrow: str
    title_off: str
    summary: str
    summary_detail: str
    summary_broad: str
    summary_off: str

    @property
    def paragraph_sentences(self) -> tuple[str, str, str, str, str, str]:
        return (self.opener, self.detail, self.example, self.reason, self.evidence, self.closing)


TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec(
        key="classroom-recycling",
        topic="classroom recycling routine",
        opener="A classroom recycling routine helps students keep the room tidy and reduce waste.",
        detail="Students separate paper, plastic, and metal into labeled bins.",
        example="For example, they save used worksheets in one tray for collection.",
        reason="This habit keeps the classroom cleaner and makes disposal easier.",
        evidence="The teacher can see fewer mixed trash bags at the end of the week.",
        closing="A steady routine makes recycling part of daily class life.",
        off_topic="The principal bought new curtains for the office.",
        title="How Recycling Routines Improve Classroom Habits",
        title_broad="Why Schools Need Better Habits",
        title_narrow="Labeled Bins for Paper and Plastic",
        title_off="New Curtains in the Office",
        summary="The paragraph explains that a classroom recycling routine keeps students organized and reduces waste.",
        summary_detail="The paragraph focuses on labeled bins and reused worksheets.",
        summary_broad="Schools need many ways to stay clean.",
        summary_off="The principal changed the office curtains.",
    ),
    TopicSpec(
        key="clinic-appointment-board",
        topic="clinic appointment board",
        opener="A clinic appointment board helps patients get care without long waits.",
        detail="Staff write each patient's name, time, and reason for the visit.",
        example="For example, morning slots are reserved for checkups.",
        reason="A clear schedule keeps the waiting room from becoming crowded.",
        evidence="Patients are called in the order listed on the board.",
        closing="A clear board makes clinic visits run more smoothly.",
        off_topic="The pharmacy displayed a poster about summer classes.",
        title="Why a Clinic Appointment Board Matters",
        title_broad="Why Health Services Need Planning",
        title_narrow="Morning Slots for Checkups",
        title_off="A Poster About Summer Classes",
        summary="The paragraph shows that an appointment board helps patients and staff manage clinic visits efficiently.",
        summary_detail="The paragraph focuses on names, times, and the order of calls.",
        summary_broad="Health services work better with planning.",
        summary_off="A summer classes poster was placed in the pharmacy.",
    ),
    TopicSpec(
        key="library-return-policy",
        topic="library book return policy",
        opener="A clear book return policy helps a library keep materials available.",
        detail="Books are due back by a fixed date printed on the card.",
        example="For example, a borrowed novel may be returned in two weeks.",
        reason="Late returns delay other readers who need the same book.",
        evidence="The librarian can track overdue items in the catalog.",
        closing="When everyone follows the rule, more people can borrow books.",
        off_topic="The library ordered a new set of curtains.",
        title="Why a Library Return Policy Is Important",
        title_broad="How Libraries Stay Organized",
        title_narrow="Returning a Novel in Two Weeks",
        title_off="New Curtains for the Library",
        summary="The paragraph explains that a return policy keeps books moving from one reader to another.",
        summary_detail="The paragraph focuses on due dates and overdue tracking.",
        summary_broad="Libraries need rules to stay organized.",
        summary_off="The library bought new curtains.",
    ),
    TopicSpec(
        key="fire-drill-practice",
        topic="fire drill practice",
        opener="A fire drill prepares students to leave the building safely and quickly.",
        detail="Teachers point to the nearest exit before the drill starts.",
        example="For example, each class practices walking to the assembly area in a line.",
        reason="This practice reduces panic if a real alarm sounds.",
        evidence="Students who know the route can reach the field without stopping.",
        closing="Repeated practice makes the response automatic.",
        off_topic="The cafeteria served noodles at lunch.",
        title="How Fire Drills Help Students Stay Safe",
        title_broad="Why School Safety Matters",
        title_narrow="Walking to the Assembly Area",
        title_off="Lunch in the Cafeteria",
        summary="The paragraph shows that fire drills teach students how to respond calmly in an emergency.",
        summary_detail="The paragraph focuses on exit routes, line formation, and practice.",
        summary_broad="Schools use many ways to protect students.",
        summary_off="The cafeteria served noodles.",
    ),
    TopicSpec(
        key="bus-queue-etiquette",
        topic="bus queue etiquette",
        opener="Good queue etiquette at a bus stop keeps riders orderly and safe.",
        detail="Passengers line up behind the painted mark.",
        example="For example, each rider lets others board in the same order.",
        reason="A neat line prevents pushing and confusion.",
        evidence="The driver can load passengers faster when the line is clear.",
        closing="Simple courtesy makes public transport easier for everyone.",
        off_topic="The newsstand sold comic books.",
        title="Why Bus Stop Queues Matter",
        title_broad="Why Public Transport Needs Courtesy",
        title_narrow="Standing Behind the Painted Mark",
        title_off="Comic Books at the Newsstand",
        summary="The paragraph explains that orderly bus lines make boarding safer and faster.",
        summary_detail="The paragraph focuses on painted marks, turn-taking, and boarding speed.",
        summary_broad="Public transport works better when people are courteous.",
        summary_off="The newsstand sold comic books.",
    ),
    TopicSpec(
        key="canteen-cleanliness",
        topic="school canteen cleanliness",
        opener="Clean canteen habits help keep food safe for students.",
        detail="Workers wipe tables after each lunch period.",
        example="For example, trash is sorted before the floor is mopped.",
        reason="A clean area reduces germs and spills.",
        evidence="Students can sit down without seeing leftover food on the tables.",
        closing="Regular cleaning makes the canteen healthier and more pleasant.",
        off_topic="The library added a comic book shelf.",
        title="Why Clean Canteen Habits Matter",
        title_broad="How Schools Keep Students Healthy",
        title_narrow="Wiping Tables After Lunch",
        title_off="A Comic Book Shelf in the Library",
        summary="The paragraph shows that cleaning the canteen protects food and makes the space pleasant.",
        summary_detail="The paragraph focuses on wiped tables, sorted trash, and fewer spills.",
        summary_broad="Schools need healthy spaces for students.",
        summary_off="The library added a comic book shelf.",
    ),
    TopicSpec(
        key="emergency-contact-card",
        topic="emergency contact card",
        opener="An emergency contact card helps adults reach the right people quickly.",
        detail="The card lists names and phone numbers.",
        example="For example, it includes a parent, a guardian, and a neighbor.",
        reason="The information saves time during accidents or sudden illness.",
        evidence="A teacher can call the correct person without searching.",
        closing="Keeping the card updated makes it more useful.",
        off_topic="The class painted a mural about summer.",
        title="Why Emergency Contact Cards Matter",
        title_broad="Keeping Important Information Ready",
        title_narrow="A Parent and a Guardian",
        title_off="A Mural About Summer",
        summary="The paragraph explains that a contact card helps adults respond quickly in an emergency.",
        summary_detail="The paragraph focuses on names, phone numbers, and fast calling.",
        summary_broad="Useful information should be easy to find.",
        summary_off="The class painted a mural.",
    ),
    TopicSpec(
        key="computer-lab-rules",
        topic="computer lab rules",
        opener="Computer lab rules help students use equipment carefully and respectfully.",
        detail="Students log off before leaving the station.",
        example="For example, food and drinks stay outside the lab.",
        reason="Careful habits protect the computers from damage.",
        evidence="The teacher can see fewer broken keyboards when the rules are followed.",
        closing="Rules keep the lab safe and usable for the next class.",
        off_topic="The basketball court was repainted blue.",
        title="Why Computer Lab Rules Matter",
        title_broad="How Students Care for Shared Equipment",
        title_narrow="Logging Off Before Leaving",
        title_off="A Blue Basketball Court",
        summary="The paragraph shows that lab rules protect equipment and make shared learning possible.",
        summary_detail="The paragraph focuses on logging off, avoiding food, and preventing damage.",
        summary_broad="Shared equipment needs careful use.",
        summary_off="The basketball court was repainted blue.",
    ),
    TopicSpec(
        key="drainage-cleanup",
        topic="neighborhood drainage cleanup",
        opener="Cleaning neighborhood drains helps prevent flooding during heavy rain.",
        detail="Residents remove leaves, mud, and plastic from the channels.",
        example="For example, they clear the drain near the corner store first.",
        reason="Open drains allow water to flow away from the street.",
        evidence="After cleanup, water does not pool as quickly on the road.",
        closing="Regular cleanup protects homes and sidewalks.",
        off_topic="The bakery made a larger birthday cake.",
        title="How Drain Cleanup Helps a Neighborhood",
        title_broad="Why Communities Prepare for Rain",
        title_narrow="Clearing the Drain Near the Corner Store",
        title_off="A Larger Birthday Cake",
        summary="The paragraph explains that clearing drains lowers the risk of flooding.",
        summary_detail="The paragraph focuses on leaves, mud, water flow, and pooling.",
        summary_broad="Communities need many ways to handle rain.",
        summary_off="The bakery made a larger birthday cake.",
    ),
    TopicSpec(
        key="community-mural",
        topic="community mural project",
        opener="A community mural project can make a neighborhood more colorful and united.",
        detail="Residents sketch ideas on a shared wall.",
        example="For example, children paint small leaves around the border.",
        reason="Working together helps people feel proud of the space.",
        evidence="More neighbors stop to take part when they see the design taking shape.",
        closing="The finished mural shows shared effort and local pride.",
        off_topic="The market closed early because of rain.",
        title="How a Mural Brings People Together",
        title_broad="Why Neighborhood Projects Matter",
        title_narrow="Children Painting Small Leaves",
        title_off="The Market Closed Early",
        summary="The paragraph shows that a mural project gives neighbors a shared task and a brighter space.",
        summary_detail="The paragraph focuses on sketches, children's painting, and growing participation.",
        summary_broad="Communities can improve public spaces together.",
        summary_off="The market closed early because of rain.",
    ),
    TopicSpec(
        key="farm-composting",
        topic="farm composting",
        opener="Composting on a farm turns waste into useful fertilizer.",
        detail="Farmers pile leaves, stalks, and scraps in one area.",
        example="For example, fruit peels are mixed with dry grass.",
        reason="The decaying material returns nutrients to the soil.",
        evidence="Crops often grow better in fields that receive compost.",
        closing="What was once waste becomes a resource for planting.",
        off_topic="The store sold umbrellas by the entrance.",
        title="Why Farm Composting Matters",
        title_broad="How Farms Reuse Natural Waste",
        title_narrow="Fruit Peels Mixed with Dry Grass",
        title_off="Umbrellas at the Store Entrance",
        summary="The paragraph explains that composting recycles farm waste into fertilizer.",
        summary_detail="The paragraph focuses on piles of scraps, nutrients, and better crops.",
        summary_broad="Farms benefit when waste is reused.",
        summary_off="The store sold umbrellas.",
    ),
    TopicSpec(
        key="seedling-nursery",
        topic="seedling nursery",
        opener="A seedling nursery helps young plants grow strong before they are transplanted.",
        detail="Workers water the trays each morning.",
        example="For example, shaded nets protect fragile leaves from harsh sun.",
        reason="Gentle care gives the roots time to strengthen.",
        evidence="Healthy seedlings are taller and greener than neglected ones.",
        closing="Careful nursery work leads to better planting later.",
        off_topic="The shopkeeper stacked bottled drinks near the door.",
        title="How a Seedling Nursery Helps Young Plants",
        title_broad="Why Plant Care Matters",
        title_narrow="Watering the Trays Each Morning",
        title_off="Bottled Drinks Near the Door",
        summary="The paragraph shows that a nursery gives seedlings the careful conditions they need to grow.",
        summary_detail="The paragraph focuses on watering, shade, and stronger roots.",
        summary_broad="Plants need care to grow well.",
        summary_off="The shopkeeper stacked bottled drinks.",
    ),
    TopicSpec(
        key="coastal-barrier",
        topic="coastal barrier",
        opener="A coastal barrier helps slow erosion and protect the shoreline.",
        detail="The structure weakens waves before they hit the sand.",
        example="For example, rocks placed along the coast can absorb force.",
        reason="Slower waves carry away less soil.",
        evidence="After the barrier is built, the beach loses less sand.",
        closing="Barriers help preserve the coast over time.",
        off_topic="The village held a karaoke contest.",
        title="Why Coastal Barriers Protect Beaches",
        title_broad="How Communities Protect the Shore",
        title_narrow="Rocks Placed Along the Coast",
        title_off="A Karaoke Contest in the Village",
        summary="The paragraph explains that a coastal barrier reduces wave damage and slows erosion.",
        summary_detail="The paragraph focuses on waves, rocks, and less sand loss.",
        summary_broad="Coastal areas need protection.",
        summary_off="The village held a karaoke contest.",
    ),
    TopicSpec(
        key="meeting-agenda",
        topic="office meeting agenda",
        opener="A meeting agenda helps a team cover important topics in order.",
        detail="The list shows the welcome, report, and action items.",
        example="For example, the budget review comes before new project planning.",
        reason="A clear order prevents people from repeating the same points.",
        evidence="The chair can check off each item as it is discussed.",
        closing="An agenda keeps the meeting focused and efficient.",
        off_topic="The janitor polished the hallway floor.",
        title="Why a Meeting Agenda Matters",
        title_broad="How Teams Stay Organized",
        title_narrow="The Budget Review Comes First",
        title_off="Polishing the Hallway Floor",
        summary="The paragraph shows that an agenda keeps a meeting organized and on task.",
        summary_detail="The paragraph focuses on welcome items, report items, and check marks.",
        summary_broad="Work teams need planning.",
        summary_off="The janitor polished the hallway floor.",
    ),
    TopicSpec(
        key="vegetable-stall",
        topic="vegetable stall",
        opener="A vegetable stall at the market attracts buyers with fresh produce and neat displays.",
        detail="Tomatoes are stacked by size and color.",
        example="For example, carrots are bundled in small bunches for easy buying.",
        reason="A clean layout helps shoppers find what they need quickly.",
        evidence="Customers often stop when the sign shows today's harvest.",
        closing="Good presentation helps the stall sell more produce.",
        off_topic="The tricycle driver changed the route yesterday.",
        title="What Makes a Vegetable Stall Attractive",
        title_broad="Why Market Sellers Care About Presentation",
        title_narrow="Carrots Bundled in Small Bunches",
        title_off="A Route Change by the Tricycle Driver",
        summary="The paragraph explains that neat displays and fresh produce help a market stall draw buyers.",
        summary_detail="The paragraph focuses on stacked tomatoes, bundled carrots, and quick shopping.",
        summary_broad="Market stalls benefit from good presentation.",
        summary_off="The tricycle driver changed the route.",
    ),
)


def _normalize_whitespace(text: str) -> str:
    return " ".join(str(text).split())


def _paragraph_text(topic: TopicSpec, difficulty: str) -> str:
    # Keep the full paragraph available for every question so the supporting
    # detail answers are always visible. Difficulty is expressed through the
    # stem wording and distractor closeness instead.
    return " ".join(topic.paragraph_sentences)


def _sequence_display(topic: TopicSpec, difficulty: str, *, rng: random.Random) -> tuple[str, str]:
    if difficulty == "Easy":
        sentences = topic.paragraph_sentences[:4]
    elif difficulty == "Medium":
        sentences = topic.paragraph_sentences[:5]
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
    elif len(parts) == 6:
        a, b, c, d, e, f = parts
        candidates = [
            f"{a}-{c}-{b}-{d}-{e}-{f}",
            f"{b}-{a}-{c}-{d}-{e}-{f}",
            f"{a}-{b}-{d}-{c}-{e}-{f}",
        ]
    else:
        raise ValueError(f"unexpected sequence length: {correct}")

    rng.shuffle(candidates)
    return tuple(candidates[:3])


def _choice_sets(
    topic: TopicSpec, difficulty: str, qtype: str, *, rng: random.Random
) -> tuple[list[str], str, list[str]]:
    if qtype == "topic_sentence":
        correct = topic.opener
        if difficulty == "Easy":
            distractors = (topic.detail, topic.example, topic.off_topic)
        elif difficulty == "Medium":
            distractors = (topic.detail, topic.reason, topic.off_topic)
        elif difficulty == "Hard":
            distractors = (topic.detail, topic.reason, topic.closing)
        else:
            distractors = (topic.detail, topic.example, topic.closing)
    elif qtype == "support_detail":
        correct = topic.detail
        if difficulty == "Easy":
            distractors = (topic.example, topic.off_topic, topic.opener)
        elif difficulty == "Medium":
            distractors = (topic.example, topic.reason, topic.off_topic)
        elif difficulty == "Hard":
            distractors = (topic.example, topic.reason, topic.evidence)
        else:
            distractors = (topic.example, topic.reason, topic.closing)
    elif qtype == "example_detail":
        correct = topic.example
        if difficulty == "Easy":
            distractors = (topic.detail, topic.off_topic, topic.opener)
        elif difficulty == "Medium":
            distractors = (topic.detail, topic.reason, topic.off_topic)
        elif difficulty == "Hard":
            distractors = (topic.detail, topic.reason, topic.evidence)
        else:
            distractors = (topic.detail, topic.reason, topic.closing)
    elif qtype == "reason_detail":
        correct = topic.reason
        if difficulty == "Easy":
            distractors = (topic.detail, topic.example, topic.off_topic)
        elif difficulty == "Medium":
            distractors = (topic.detail, topic.example, topic.evidence)
        elif difficulty == "Hard":
            distractors = (topic.detail, topic.example, topic.closing)
        else:
            distractors = (topic.detail, topic.example, topic.closing)
    elif qtype == "evidence_detail":
        correct = topic.evidence
        if difficulty == "Easy":
            distractors = (topic.detail, topic.example, topic.off_topic)
        elif difficulty == "Medium":
            distractors = (topic.detail, topic.reason, topic.off_topic)
        elif difficulty == "Hard":
            distractors = (topic.detail, topic.reason, topic.example)
        else:
            distractors = (topic.detail, topic.reason, topic.closing)
    elif qtype == "off_topic":
        correct = topic.off_topic
        if difficulty == "Easy":
            distractors = (topic.detail, topic.example, topic.reason)
        elif difficulty == "Medium":
            distractors = (topic.detail, topic.example, topic.evidence)
        elif difficulty == "Hard":
            distractors = (topic.detail, topic.reason, topic.closing)
        else:
            distractors = (topic.detail, topic.example, topic.closing)
    elif qtype == "title":
        correct = topic.title
        distractors = (topic.title_broad, topic.title_narrow, topic.title_off)
    elif qtype == "summary":
        correct = topic.summary
        distractors = (topic.summary_detail, topic.summary_broad, topic.summary_off)
    elif qtype == "sequence":
        display_text, correct = _sequence_display(topic, difficulty, rng=rng)
        distractors = _sequence_distractors(correct, rng)
        return [display_text], correct, list(distractors)
    elif qtype == "concluding_sentence":
        correct = topic.closing
        if difficulty == "Easy":
            distractors = (topic.detail, topic.example, topic.off_topic)
        elif difficulty == "Medium":
            distractors = (topic.detail, topic.reason, topic.off_topic)
        elif difficulty == "Hard":
            distractors = (topic.detail, topic.example, topic.reason)
        else:
            distractors = (topic.example, topic.reason, topic.evidence)
    else:
        raise ValueError(f"unsupported question type: {qtype}")

    return [], correct, list(distractors)


def _question_stem(topic: TopicSpec, difficulty: str, qtype: str) -> str:
    stem = STEMS[qtype][difficulty].format(topic=topic.topic)
    if qtype == "sequence":
        return stem
    return f"{_paragraph_text(topic, difficulty)}\n\n{stem}"


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
