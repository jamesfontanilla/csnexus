"""Generate the Verbal Ability / Paragraph Organization / Logical Sequence question bank.

This wrapper reuses the validated sentence-order generator logic, but swaps in a
logical-sequence-specific topic set and output path.
"""

from __future__ import annotations

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import generate_sentence_order_bank as base


OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "paragraph-organization"
    / "logical-sequence"
    / "questions.json"
)

SUBTOPIC = "Logical Sequence"


def topic(
    key: str,
    topic_name: str,
    sentences: tuple[str, str, str, str, str],
    off_topic: str,
    pronoun: str,
    pronoun_answer: str,
    pronoun_distractor_1: str,
    pronoun_distractor_2: str,
    pronoun_distractor_3: str,
) -> base.TopicSpec:
    return base.TopicSpec(
        key=key,
        topic=topic_name,
        sentences=sentences,
        off_topic=off_topic,
        pronoun=pronoun,
        pronoun_answer=pronoun_answer,
        pronoun_distractor_1=pronoun_distractor_1,
        pronoun_distractor_2=pronoun_distractor_2,
        pronoun_distractor_3=pronoun_distractor_3,
    )


TOPICS: tuple[base.TopicSpec, ...] = (
    topic(
        "storm-emergency-kit",
        "storm emergency kit",
        (
            "Preparing an emergency kit helps families stay ready during storms.",
            "They pack water, batteries, and a flashlight.",
            "They add medicines and important papers.",
            "The bag stays near the door.",
            "This simple preparation reduces panic when the weather turns bad.",
        ),
        "The school cafeteria served fried noodles.",
        "they",
        "families",
        "the bag",
        "the flashlight",
        "the weather",
    ),
    topic(
        "office-filing-workflow",
        "office filing workflow",
        (
            "An office filing workflow helps workers find records quickly and avoid mistakes.",
            "Papers are sorted by project and date.",
            "Each folder gets a clear label.",
            "Old files are stored in the archive cabinet.",
            "This system saves time for the whole office.",
        ),
        "The basketball court was repainted green.",
        "this",
        "the office filing workflow",
        "the archive cabinet",
        "the office",
        "the project",
    ),
    topic(
        "school-garden-watering-plan",
        "school garden watering plan",
        (
            "A school garden watering plan helps plants stay healthy.",
            "Students check the soil before watering.",
            "They water the beds early in the morning.",
            "The schedule changes when rain is expected.",
            "Regular care helps the plants grow well.",
        ),
        "The principal bought new curtains.",
        "they",
        "students",
        "the soil",
        "the beds",
        "the rain",
    ),
    topic(
        "road-crossing-safety",
        "road crossing safety",
        (
            "Safe road crossing helps students avoid accidents.",
            "They stop at the curb and look both ways.",
            "They wait for traffic to clear.",
            "Crossing with care keeps everyone safer near traffic.",
            "Good habits make the route to school less risky.",
        ),
        "The vendor sold ice candy.",
        "they",
        "students",
        "the curb",
        "traffic",
        "the road",
    ),
    topic(
        "community-library-shelf-system",
        "community library shelf system",
        (
            "A community library shelf system helps readers find books quickly.",
            "Fiction, nonfiction, and reference sections are marked separately.",
            "New books are placed on the correct shelf.",
            "Volunteers check the labels each week.",
            "This arrangement makes the library easier to use.",
        ),
        "The tricycle driver changed the route.",
        "this",
        "the community library shelf system",
        "the labels",
        "the volunteers",
        "the books",
    ),
    topic(
        "kitchen-cleanup-order",
        "kitchen cleanup order",
        (
            "A kitchen cleanup order helps the room stay safe and tidy.",
            "Plates and cups are washed first.",
            "Counters are wiped after the dishes are done.",
            "The floor is swept last.",
            "This order makes the next meal easier to prepare.",
        ),
        "The train arrived late at the station.",
        "this",
        "the kitchen cleanup order",
        "the floor",
        "the dishes",
        "the counters",
    ),
    topic(
        "public-bus-boarding-routine",
        "public bus boarding routine",
        (
            "A public bus boarding routine keeps passengers moving in order.",
            "Riders line up at the stop before the bus arrives.",
            "They wait until the driver opens the doors.",
            "Passengers board one at a time.",
            "An orderly routine prevents pushing and confusion.",
        ),
        "The teacher erased the whiteboard.",
        "they",
        "riders",
        "the bus",
        "the stop",
        "the doors",
    ),
    topic(
        "neighborhood-watch-patrol",
        "neighborhood watch patrol",
        (
            "A neighborhood watch patrol helps residents stay alert.",
            "Volunteers check streetlights and report unusual activity.",
            "They share emergency numbers with one another.",
            "Regular patrols make the street feel safer.",
            "Working together helps the block stay secure.",
        ),
        "The bakery sold purple balloons.",
        "they",
        "volunteers",
        "streetlights",
        "residents",
        "the block",
    ),
    topic(
        "farm-irrigation-schedule",
        "farm irrigation schedule",
        (
            "A farm irrigation schedule helps crops get water on time.",
            "Workers open the valve before sunrise.",
            "Water flows through the field channels.",
            "The schedule changes when rain is expected.",
            "This routine protects the harvest.",
        ),
        "The librarian stamped the new book.",
        "this",
        "the farm irrigation schedule",
        "the field channels",
        "the harvest",
        "the valve",
    ),
    topic(
        "computer-password-safety",
        "computer password safety",
        (
            "Good password safety protects personal information online.",
            "Users create passwords that are hard to guess.",
            "They avoid sharing passwords with other people.",
            "Many accounts also use two-step verification.",
            "Careful habits make online accounts harder to break into.",
        ),
        "The jeepney changed its route yesterday.",
        "they",
        "users",
        "passwords",
        "accounts",
        "the verification",
    ),
    topic(
        "classroom-morning-announcements",
        "classroom morning announcements",
        (
            "A classroom morning announcement helps the day start in order.",
            "The teacher shares the schedule for the morning.",
            "Students listen for reminders about homework and events.",
            "They check for any changes before the first lesson begins.",
            "Clear announcements keep everyone informed.",
        ),
        "The market closed early because of rain.",
        "they",
        "students",
        "the schedule",
        "the teacher",
        "the lesson",
    ),
    topic(
        "market-stall-restocking",
        "market stall restocking",
        (
            "Restocking a market stall keeps fresh goods available.",
            "Unsold vegetables are moved to the cooler.",
            "New produce is arranged by size and color.",
            "Prices are checked before customers arrive.",
            "This tidy arrangement helps shoppers buy quickly.",
        ),
        "The school bell rang after lunch.",
        "this",
        "the market stall restocking",
        "the cooler",
        "the customers",
        "the produce",
    ),
    topic(
        "volunteer-reading-buddy-session",
        "volunteer reading buddy session",
        (
            "A volunteer reading buddy session helps younger learners build confidence.",
            "The older reader chooses a short book.",
            "The pair takes turns reading aloud.",
            "The volunteer asks simple questions about the story.",
            "This practice makes reading feel less stressful.",
        ),
        "The volleyball net was repaired.",
        "this",
        "the volunteer reading buddy session",
        "the short book",
        "the story",
        "the older reader",
    ),
    topic(
        "rainwater-collection-system",
        "rainwater collection system",
        (
            "A rainwater collection system helps save water for dry days.",
            "Gutters guide rain into a storage barrel.",
            "A screen keeps leaves out of the container.",
            "It can later be used for plants.",
            "Saving rainwater reduces waste during dry spells.",
        ),
        "The bus conductor counted the tickets.",
        "it",
        "the collected water",
        "the gutters",
        "the barrel",
        "the plants",
    ),
    topic(
        "school-clinic-triage-desk",
        "school clinic triage desk",
        (
            "A school clinic triage desk helps staff handle students quickly.",
            "Students are asked about their symptoms first.",
            "Serious cases are sent in before minor complaints.",
            "The queue moves more smoothly when each case is sorted.",
            "This process helps the clinic stay organized.",
        ),
        "The playground gate was painted yellow.",
        "this",
        "the triage desk routine",
        "minor complaints",
        "the queue",
        "the symptoms",
    ),
)


def main() -> None:
    base.OUTPUT_PATH = OUTPUT_PATH
    base.SUBTOPIC = SUBTOPIC
    base.TOPICS = TOPICS
    base.main()


if __name__ == "__main__":
    main()
