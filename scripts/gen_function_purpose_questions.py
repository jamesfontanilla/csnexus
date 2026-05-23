"""Generate 600 function-and-purpose relationship analogy questions.

Produces questions for:
- Tool-and-function relationships
- Object-and-purpose relationships
- Occupation-and-task relationships
- Animal-and-action/sound relationships

Distribution: 200 Easy / 200 Medium / 200 Hard

Output: data/seed/questions/analytical-ability/word-analogy/
        function-and-purpose-relationships/questions.json
"""

import json
from pathlib import Path

OUTPUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "seed"
    / "questions"
    / "analytical-ability"
    / "word-analogy"
    / "function-and-purpose-relationships"
)

TEMPLATE = {
    "subtest": "Analytical Ability",
    "module": "Word Analogy",
    "subtopic": "Function and Purpose Relationships",
    "tags": ["word analogy", "function", "purpose relationships"],
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}


def _q(id_: int, difficulty: str, question: str, choices: list[str], answer: str, explanation: str, tags: list[str] | None = None) -> dict:
    entry = {
        "id": id_,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
    }
    entry.update(TEMPLATE)
    if tags:
        entry["tags"] = tags
    return entry


def generate_questions() -> list[dict]:
    questions: list[dict] = []
    id_ = 0

    # =========================================================================
    # EASY QUESTIONS (1-200)
    # =========================================================================

    easy = [
        # Tool-and-Function (Easy) - items 1-50
        ("SCISSORS : CUT :: BROOM : ?", ["Sweep", "Clean", "Floor", "Dust"], "Sweep", "Scissors are used to cut. A broom is used to sweep. Both are tool-to-specific-action relationships."),
        ("KNIFE : CUT :: PEN : ?", ["Ink", "Write", "Paper", "Draw"], "Write", "A knife is used to cut. A pen is used to write. Both are tool-to-function relationships."),
        ("HAMMER : POUND :: SAW : ?", ["Wood", "Cut", "Build", "Carpenter"], "Cut", "A hammer is used to pound. A saw is used to cut. Wood is the material, not the function."),
        ("BROOM : SWEEP :: MOP : ?", ["Floor", "Wipe", "Water", "Clean"], "Wipe", "A broom is used to sweep. A mop is used to wipe. Both are cleaning tool-to-specific-action."),
        ("SHOVEL : DIG :: RAKE : ?", ["Leaves", "Gather", "Garden", "Soil"], "Gather", "A shovel is used to dig. A rake is used to gather leaves. Both are garden tool-to-function."),
        ("PEN : WRITE :: ERASER : ?", ["Pencil", "Remove", "Rubber", "Paper"], "Remove", "A pen is used to write. An eraser is used to remove marks. Both are tool-to-function."),
        ("NEEDLE : SEW :: HAMMER : ?", ["Nail", "Pound", "Build", "Metal"], "Pound", "A needle is used to sew. A hammer is used to pound. Both are tool-to-specific-action."),
        ("AXE : CHOP :: DRILL : ?", ["Hole", "Bore", "Wall", "Electric"], "Bore", "An axe is used to chop. A drill is used to bore holes. Both are tool-to-function."),
        ("RULER : MEASURE :: SCALE : ?", ["Heavy", "Weigh", "Number", "Balance"], "Weigh", "A ruler is used to measure length. A scale is used to weigh objects. Both are instrument-to-function."),
        ("OVEN : BAKE :: STOVE : ?", ["Kitchen", "Cook", "Hot", "Food"], "Cook", "An oven is used to bake. A stove is used to cook. Both are appliance-to-function."),
        ("BRUSH : PAINT :: PEN : ?", ["Ink", "Write", "Paper", "Cap"], "Write", "A brush is used to paint. A pen is used to write. Both are tool-to-function."),
        ("SPOON : STIR :: FORK : ?", ["Eat", "Spear", "Metal", "Plate"], "Spear", "A spoon is used to stir. A fork is used to spear food. Both are utensil-to-function."),
        ("HOSE : SPRAY :: BUCKET : ?", ["Water", "Carry", "Plastic", "Garden"], "Carry", "A hose is used to spray water. A bucket is used to carry water. Both are tool-to-function."),
        ("KEY : UNLOCK :: SWITCH : ?", ["Light", "Activate", "Wall", "Electric"], "Activate", "A key is used to unlock. A switch is used to activate. Both are device-to-function."),
        ("LAMP : ILLUMINATE :: HEATER : ?", ["Hot", "Warm", "Electric", "Winter"], "Warm", "A lamp is used to illuminate. A heater is used to warm. Both are device-to-function."),
        ("CLOCK : TELL TIME :: CALENDAR : ?", ["Days", "Track dates", "Wall", "Month"], "Track dates", "A clock is used to tell time. A calendar is used to track dates. Both are tool-to-function."),
        ("SOAP : CLEAN :: TOWEL : ?", ["Wet", "Dry", "Cloth", "Bath"], "Dry", "Soap is used to clean. A towel is used to dry. Both are item-to-function."),
        ("COMB : UNTANGLE :: BRUSH : ?", ["Hair", "Smooth", "Bristle", "Style"], "Smooth", "A comb is used to untangle hair. A brush is used to smooth hair. Both are grooming tool-to-function."),
        ("STAPLER : BIND :: SCISSORS : ?", ["Paper", "Cut", "Sharp", "Office"], "Cut", "A stapler is used to bind pages. Scissors are used to cut. Both are office tool-to-function."),
        ("MAGNIFYING GLASS : ENLARGE :: BINOCULARS : ?", ["See", "Magnify", "Bird", "Far"], "Magnify", "A magnifying glass is used to enlarge. Binoculars are used to magnify distant objects."),
        ("IRON : PRESS :: WASHING MACHINE : ?", ["Clothes", "Launder", "Water", "Spin"], "Launder", "An iron is used to press clothes. A washing machine is used to launder clothes."),
        ("BLENDER : MIX :: GRINDER : ?", ["Coffee", "Crush", "Electric", "Kitchen"], "Crush", "A blender is used to mix. A grinder is used to crush. Both are appliance-to-function."),
        ("FLASHLIGHT : ILLUMINATE :: WHISTLE : ?", ["Blow", "Signal", "Loud", "Metal"], "Signal", "A flashlight is used to illuminate. A whistle is used to signal. Both are device-to-function."),
        ("CALCULATOR : COMPUTE :: TYPEWRITER : ?", ["Paper", "Type", "Keys", "Office"], "Type", "A calculator is used to compute. A typewriter is used to type. Both are device-to-function."),
        ("THERMOMETER : MEASURE :: BAROMETER : ?", ["Weather", "Gauge", "Pressure", "Mercury"], "Gauge", "A thermometer measures temperature. A barometer gauges pressure. Both are instrument-to-function."),
        ("WRENCH : TIGHTEN :: PLIERS : ?", ["Metal", "Grip", "Tool", "Wire"], "Grip", "A wrench is used to tighten. Pliers are used to grip. Both are hand tool-to-function."),
        ("BROOM : SWEEP :: VACUUM : ?", ["Dirt", "Suction", "Electric", "Suck"], "Suction", "A broom sweeps. A vacuum uses suction to clean. Both are cleaning tool-to-function."),
        ("LIGHTER : IGNITE :: EXTINGUISHER : ?", ["Fire", "Suppress", "Red", "Emergency"], "Suppress", "A lighter is used to ignite. An extinguisher is used to suppress fire. Both are device-to-function."),
        ("PAINTBRUSH : APPLY :: SANDPAPER : ?", ["Rough", "Smooth", "Wood", "Sand"], "Smooth", "A paintbrush is used to apply paint. Sandpaper is used to smooth surfaces."),
        ("FUNNEL : POUR :: SIEVE : ?", ["Holes", "Sift", "Metal", "Flour"], "Sift", "A funnel is used to pour liquids. A sieve is used to sift particles. Both are tool-to-function."),
        ("NAIL : FASTEN :: GLUE : ?", ["Stick", "Bond", "White", "Craft"], "Bond", "A nail is used to fasten. Glue is used to bond materials together. Both are fastener-to-function."),
        ("ANTENNA : RECEIVE :: SPEAKER : ?", ["Sound", "Emit", "Music", "Loud"], "Emit", "An antenna is used to receive signals. A speaker is used to emit sound. Both are device-to-function."),
        ("FILTER : PURIFY :: HEATER : ?", ["Hot", "Warm", "Electric", "Coil"], "Warm", "A filter is used to purify. A heater is used to warm. Both are device-to-function."),
        ("LADDER : CLIMB :: BRIDGE : ?", ["River", "Cross", "Road", "Steel"], "Cross", "A ladder is used to climb. A bridge is used to cross. Both are structure-to-function."),
        ("HOOK : HANG :: SHELF : ?", ["Wood", "Store", "Wall", "Book"], "Store", "A hook is used to hang items. A shelf is used to store items. Both are fixture-to-function."),
        ("ALARM : ALERT :: SIREN : ?", ["Loud", "Warn", "Police", "Sound"], "Warn", "An alarm is used to alert. A siren is used to warn. Both are device-to-function."),
        ("TAPE : SEAL :: ROPE : ?", ["Long", "Bind", "Knot", "Strong"], "Bind", "Tape is used to seal. Rope is used to bind. Both are material-to-function."),
        ("FAN : COOL :: FURNACE : ?", ["Hot", "Heat", "Fire", "Winter"], "Heat", "A fan is used to cool. A furnace is used to heat. Both are appliance-to-function."),
        ("MIRROR : REFLECT :: LENS : ?", ["Glass", "Focus", "Eye", "Round"], "Focus", "A mirror is used to reflect. A lens is used to focus light. Both are optical device-to-function."),
        ("ANCHOR : SECURE :: SAIL : ?", ["Wind", "Propel", "Boat", "Cloth"], "Propel", "An anchor is used to secure a ship. A sail is used to propel a ship. Both are nautical device-to-function."),
        ("PLUG : CONNECT :: SWITCH : ?", ["Wall", "Control", "Electric", "Light"], "Control", "A plug is used to connect to power. A switch is used to control flow. Both are electrical device-to-function."),
        ("ZIPPER : FASTEN :: BUTTON : ?", ["Shirt", "Secure", "Round", "Hole"], "Secure", "A zipper is used to fasten. A button is used to secure clothing. Both are fastener-to-function."),
        ("WHEELBARROW : TRANSPORT :: CRANE : ?", ["Heavy", "Lift", "Steel", "Construction"], "Lift", "A wheelbarrow is used to transport. A crane is used to lift. Both are equipment-to-function."),
        ("SPONGE : ABSORB :: TOWEL : ?", ["Cloth", "Dry", "Soft", "Bath"], "Dry", "A sponge is used to absorb. A towel is used to dry. Both are item-to-function."),
        ("COMPASS : ORIENT :: MAP : ?", ["Paper", "Guide", "Road", "Fold"], "Guide", "A compass is used to orient. A map is used to guide. Both are navigation tool-to-function."),
        ("PADLOCK : SECURE :: CHAIN : ?", ["Metal", "Restrain", "Link", "Heavy"], "Restrain", "A padlock is used to secure. A chain is used to restrain. Both are security device-to-function."),
        ("MEGAPHONE : AMPLIFY :: MICROPHONE : ?", ["Sing", "Capture", "Wire", "Stage"], "Capture", "A megaphone amplifies sound outward. A microphone captures sound. Both are audio device-to-function."),
        ("STRETCHER : CARRY :: WHEELCHAIR : ?", ["Wheel", "Transport", "Hospital", "Sit"], "Transport", "A stretcher is used to carry patients. A wheelchair is used to transport patients. Both are medical device-to-function."),
        ("TONGS : GRIP :: LADLE : ?", ["Soup", "Scoop", "Metal", "Kitchen"], "Scoop", "Tongs are used to grip. A ladle is used to scoop. Both are kitchen tool-to-function."),
        ("DOORBELL : ANNOUNCE :: ALARM CLOCK : ?", ["Time", "Wake", "Ring", "Morning"], "Wake", "A doorbell is used to announce visitors. An alarm clock is used to wake people. Both are device-to-function."),
