"""
Generate 600 part-whole and classification relationship analogy questions.
200 Easy / 200 Medium / 200 Hard
Output: data/seed/questions/analytical-ability/word-analogy/
        part-whole-and-classification-relationships/questions.json

Strategy: Build questions programmatically from relationship data tables,
then supplement with hand-crafted items for variety.
"""
import json
import random
from pathlib import Path

OUTPUT = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions" / "analytical-ability"
    / "word-analogy" / "part-whole-and-classification-relationships"
    / "questions.json"
)

BASE = {
    "subtest": "Analytical Ability",
    "module": "Word Analogy",
    "subtopic": "Part\u2013Whole and Classification Relationships",
    "category": ["Professional", "Sub-Professional"],
    "language": "English",
}

random.seed(42)

# fmt: off

# ============================================================
# DATA POOLS
# ============================================================

# Part-to-Whole pairs: (part, whole)
PART_WHOLE_EASY = [
    ("wheel", "car"), ("page", "book"), ("finger", "hand"), ("petal", "flower"),
    ("key", "keyboard"), ("room", "house"), ("wing", "bird"), ("screen", "phone"),
    ("blade", "fan"), ("engine", "car"), ("branch", "tree"), ("drawer", "cabinet"),
    ("step", "staircase"), ("handle", "door"), ("eye", "face"), ("seed", "fruit"),
    ("verse", "song"), ("button", "shirt"), ("spoke", "wheel"), ("leg", "table"),
    ("brick", "wall"), ("slice", "pizza"), ("tooth", "comb"), ("string", "guitar"),
    ("tile", "roof"), ("feather", "bird"), ("scale", "fish"), ("horn", "bull"),
    ("tail", "dog"), ("root", "plant"), ("shell", "egg"), ("lid", "jar"),
    ("sleeve", "jacket"), ("pocket", "pants"), ("heel", "shoe"), ("knob", "door"),
    ("fender", "car"), ("mast", "ship"), ("chimney", "house"), ("antenna", "radio"),
]

PART_WHOLE_MEDIUM = [
    ("chapter", "novel"), ("stanza", "poem"), ("lens", "camera"), ("wing", "airplane"),
    ("paragraph", "essay"), ("scene", "play"), ("episode", "series"), ("pedal", "bicycle"),
    ("rudder", "ship"), ("propeller", "helicopter"), ("cabin", "aircraft"),
    ("hull", "ship"), ("foundation", "building"), ("corridor", "hospital"),
    ("turret", "castle"), ("minaret", "mosque"), ("aisle", "church"),
    ("cockpit", "airplane"), ("deck", "ship"), ("bumper", "car"),
    ("motherboard", "computer"), ("hard drive", "computer"), ("carburetor", "engine"),
    ("filament", "bulb"), ("wick", "candle"), ("bristle", "brush"),
    ("fret", "guitar"), ("valve", "trumpet"), ("reed", "clarinet"),
    ("shutter", "camera"), ("dial", "watch"), ("crown", "tooth"),
    ("iris", "eye"), ("ventricle", "heart"), ("lobe", "brain"),
    ("cortex", "brain"), ("vertebra", "spine"), ("tendon", "muscle"),
    ("cartilage", "joint"), ("pupil", "eye"),
]

PART_WHOLE_HARD = [
    ("clause", "contract"), ("amendment", "constitution"), ("provision", "legislation"),
    ("preamble", "constitution"), ("article", "treaty"), ("section", "statute"),
    ("module", "curriculum"), ("syllabus", "course"), ("abstract", "thesis"),
    ("appendix", "dissertation"), ("footnote", "manuscript"), ("index", "textbook"),
    ("bureau", "department"), ("division", "bureau"), ("section", "division"),
    ("barangay", "municipality"), ("municipality", "province"), ("province", "region"),
    ("precinct", "district"), ("ward", "city"), ("parish", "diocese"),
    ("neuron", "brain"), ("pixel", "screen"), ("chromosome", "cell"),
    ("mitochondria", "cell"), ("nucleotide", "DNA"), ("isotope", "element"),
    ("stamen", "flower"), ("cortex", "kidney"), ("alveolus", "lung"),
    ("synapse", "nervous system"), ("capillary", "circulatory system"),
    ("transistor", "microchip"), ("capacitor", "circuit"), ("resistor", "circuit"),
    ("actuator", "robot"), ("sensor", "drone"), ("algorithm", "program"),
    ("subroutine", "program"), ("variable", "equation"), ("axiom", "theorem"),
]


# Whole-to-Part pairs: (whole, part)
WHOLE_PART_EASY = [
    ("tree", "branch"), ("house", "room"), ("hand", "finger"), ("book", "chapter"),
    ("clock", "hand"), ("car", "engine"), ("face", "eye"), ("year", "month"),
    ("flower", "petal"), ("school", "classroom"), ("pizza", "slice"),
    ("necklace", "bead"), ("garden", "plant"), ("forest", "tree"),
    ("rainbow", "color"), ("deck", "card"), ("bouquet", "flower"),
    ("calendar", "date"), ("dictionary", "word"), ("building", "floor"),
    ("body", "arm"), ("week", "day"), ("alphabet", "letter"),
    ("chain", "link"), ("fence", "post"), ("ladder", "rung"),
    ("piano", "key"), ("comb", "tooth"), ("rake", "prong"),
    ("skeleton", "bone"), ("galaxy", "star"), ("crowd", "person"),
    ("herd", "cow"), ("bunch", "grape"), ("fleet", "car"),
    ("toolbox", "tool"), ("wardrobe", "clothes"), ("wallet", "card"),
    ("basket", "fruit"), ("shelf", "book"),
]

WHOLE_PART_MEDIUM = [
    ("orchestra", "violin"), ("computer", "processor"), ("government", "agency"),
    ("university", "college"), ("archipelago", "island"), ("library", "book"),
    ("fleet", "ship"), ("constellation", "star"), ("anthology", "essay"),
    ("atlas", "map"), ("encyclopedia", "article"), ("portfolio", "document"),
    ("curriculum", "subject"), ("menu", "dish"), ("catalog", "item"),
    ("playlist", "song"), ("database", "record"), ("network", "node"),
    ("ecosystem", "organism"), ("solar system", "planet"),
    ("continent", "country"), ("ocean", "current"), ("atmosphere", "layer"),
    ("spectrum", "color"), ("periodic table", "element"),
    ("genome", "gene"), ("vocabulary", "word"), ("repertoire", "piece"),
    ("inventory", "product"), ("registry", "entry"), ("directory", "listing"),
    ("mosaic", "tile"), ("quilt", "patch"), ("tapestry", "thread"),
    ("symphony", "movement"), ("opera", "act"), ("trilogy", "volume"),
    ("archipelago", "atoll"), ("mountain range", "peak"),
    ("nervous system", "nerve"), ("digestive system", "organ"),
]

WHOLE_PART_HARD = [
    ("constitution", "article"), ("corporation", "subsidiary"),
    ("legislature", "committee"), ("judiciary", "court"),
    ("bureaucracy", "bureau"), ("federation", "state"),
    ("conglomerate", "company"), ("consortium", "member firm"),
    ("parliament", "chamber"), ("cabinet", "ministry"),
    ("diocese", "parish"), ("empire", "province"),
    ("biome", "ecosystem"), ("genome", "chromosome"),
    ("proteome", "protein"), ("microbiome", "bacterium"),
    ("lithosphere", "tectonic plate"), ("hydrosphere", "water body"),
    ("magnetosphere", "radiation belt"), ("ionosphere", "layer"),
    ("lexicon", "morpheme"), ("syntax", "clause"),
    ("phonology", "phoneme"), ("semantics", "meaning unit"),
    ("infrastructure", "utility"), ("superstructure", "ideology"),
    ("framework", "module"), ("architecture", "component"),
    ("ontology", "concept"), ("taxonomy", "taxon"),
    ("hierarchy", "level"), ("matrix", "element"),
    ("manifold", "dimension"), ("tensor", "component"),
    ("algorithm", "subroutine"), ("protocol", "handshake"),
    ("blockchain", "block"), ("neural network", "layer"),
    ("operating system", "kernel"), ("compiler", "parser"),
]


# Item-to-Category pairs: (item, category)
ITEM_CATEGORY_EASY = [
    ("eagle", "bird"), ("rose", "flower"), ("hammer", "tool"), ("apple", "fruit"),
    ("guitar", "instrument"), ("basketball", "sport"), ("shirt", "clothing"),
    ("oak", "tree"), ("dog", "animal"), ("piano", "instrument"),
    ("truck", "vehicle"), ("red", "color"), ("circle", "shape"),
    ("English", "language"), ("rice", "grain"), ("January", "month"),
    ("gold", "metal"), ("diamond", "gemstone"), ("Mars", "planet"),
    ("novel", "book"), ("sparrow", "bird"), ("ant", "insect"),
    ("oxygen", "gas"), ("soccer", "sport"), ("whale", "mammal"),
    ("cobra", "reptile"), ("salmon", "fish"), ("carrot", "vegetable"),
    ("peso", "currency"), ("Monday", "day"), ("violin", "instrument"),
    ("sedan", "car"), ("tulip", "flower"), ("pine", "tree"),
    ("iron", "metal"), ("ruby", "gemstone"), ("tennis", "sport"),
    ("dolphin", "mammal"), ("frog", "amphibian"), ("daisy", "flower"),
]

ITEM_CATEGORY_MEDIUM = [
    ("lawyer", "profession"), ("democracy", "government system"),
    ("sonnet", "poem"), ("tsunami", "natural disaster"),
    ("algebra", "mathematics"), ("typhoon", "weather phenomenon"),
    ("laptop", "technology device"), ("memorandum", "document"),
    ("nurse", "medical professional"), ("judge", "judicial officer"),
    ("mayor", "public official"), ("governor", "executive official"),
    ("biology", "science"), ("psychology", "social science"),
    ("economics", "discipline"), ("chemistry", "natural science"),
    ("microscope", "scientific instrument"), ("stethoscope", "medical instrument"),
    ("thermometer", "measuring instrument"), ("telescope", "optical instrument"),
    ("scalpel", "surgical instrument"), ("compass", "navigation tool"),
    ("waltz", "dance"), ("opera", "musical genre"), ("haiku", "poetry form"),
    ("fresco", "painting technique"), ("sculpture", "art form"),
    ("capitalism", "economic system"), ("monarchy", "government type"),
    ("Buddhism", "religion"), ("Tagalog", "language"),
    ("archipelago", "landform"), ("peninsula", "landform"),
    ("plateau", "landform"), ("glacier", "geological formation"),
    ("tornado", "weather phenomenon"), ("drought", "climate event"),
    ("inflation", "economic phenomenon"), ("recession", "economic condition"),
    ("photosynthesis", "biological process"), ("osmosis", "biological process"),
]

ITEM_CATEGORY_HARD = [
    ("impeachment", "legal proceeding"), ("appropriation", "legislation"),
    ("arbitration", "dispute resolution"), ("epidemiology", "medical science"),
    ("jurisprudence", "legal philosophy"), ("pedagogy", "educational method"),
    ("referendum", "electoral process"), ("filibuster", "legislative tactic"),
    ("subpoena", "legal instrument"), ("injunction", "court order"),
    ("deposition", "legal procedure"), ("arraignment", "court proceeding"),
    ("triage", "medical procedure"), ("dialysis", "medical treatment"),
    ("angioplasty", "surgical procedure"), ("biopsy", "diagnostic procedure"),
    ("audit", "accounting process"), ("amortization", "financial method"),
    ("depreciation", "accounting concept"), ("liquidation", "business process"),
    ("requisition", "procurement process"), ("accreditation", "quality assurance"),
    ("algorithm", "computational method"), ("heuristic", "problem-solving approach"),
    ("syllogism", "logical argument"), ("paradox", "logical construct"),
    ("metaphor", "figure of speech"), ("synecdoche", "rhetorical device"),
    ("gerrymandering", "political strategy"), ("filibuster", "parliamentary procedure"),
    ("embargo", "trade restriction"), ("tariff", "trade policy"),
    ("habeas corpus", "legal right"), ("due process", "constitutional principle"),
    ("eminent domain", "government power"), ("sovereignty", "political concept"),
    ("hegemony", "power structure"), ("oligarchy", "government type"),
    ("meritocracy", "social system"), ("technocracy", "governance model"),
    ("epistemology", "philosophical branch"), ("ontology", "philosophical discipline"),
]


# Member-to-Group pairs: (member, group)
MEMBER_GROUP_EASY = [
    ("soldier", "army"), ("player", "team"), ("student", "class"),
    ("singer", "choir"), ("bee", "swarm"), ("wolf", "pack"),
    ("fish", "school"), ("bird", "flock"), ("cow", "herd"),
    ("sheep", "flock"), ("lion", "pride"), ("ant", "colony"),
    ("sailor", "crew"), ("dancer", "troupe"), ("monk", "monastery"),
    ("nun", "convent"), ("scout", "troop"), ("pilgrim", "caravan"),
    ("worker", "staff"), ("guest", "audience"), ("fan", "crowd"),
    ("pupil", "class"), ("member", "club"), ("resident", "community"),
    ("neighbor", "neighborhood"), ("citizen", "nation"),
    ("passenger", "flight"), ("rider", "convoy"),
    ("swimmer", "relay"), ("runner", "marathon"),
    ("camper", "camp"), ("traveler", "group"),
    ("volunteer", "brigade"), ("firefighter", "squad"),
    ("officer", "platoon"), ("guard", "patrol"),
    ("actor", "cast"), ("musician", "band"),
    ("athlete", "team"), ("singer", "ensemble"),
    ("chef", "kitchen staff"),
]

MEMBER_GROUP_MEDIUM = [
    ("senator", "senate"), ("juror", "jury"), ("musician", "orchestra"),
    ("actor", "ensemble"), ("employee", "workforce"), ("citizen", "electorate"),
    ("athlete", "delegation"), ("diplomat", "corps"),
    ("professor", "faculty"), ("researcher", "team"),
    ("legislator", "congress"), ("representative", "assembly"),
    ("councilor", "council"), ("commissioner", "commission"),
    ("director", "board"), ("trustee", "board of trustees"),
    ("partner", "firm"), ("associate", "consortium"),
    ("delegate", "convention"), ("panelist", "panel"),
    ("witness", "tribunal"), ("arbitrator", "panel"),
    ("monk", "order"), ("friar", "brotherhood"),
    ("knight", "order"), ("samurai", "clan"),
    ("warrior", "battalion"), ("marine", "platoon"),
    ("cadet", "corps"), ("recruit", "cohort"),
    ("parishioner", "parish"), ("congregant", "congregation"),
    ("shareholder", "corporation"), ("stakeholder", "consortium"),
    ("subscriber", "membership"), ("alumnus", "alumni association"),
    ("fellow", "fellowship"), ("apprentice", "guild"),
    ("intern", "cohort"), ("resident", "program"),
    ("constituent", "electorate"), ("voter", "constituency"),
]

MEMBER_GROUP_HARD = [
    ("congressman", "congress"), ("commissioner", "COMELEC"),
    ("justice", "supreme court"), ("magistrate", "bench"),
    ("ambassador", "diplomatic corps"), ("envoy", "delegation"),
    ("cardinal", "college of cardinals"), ("bishop", "episcopate"),
    ("elder", "presbytery"), ("deacon", "diaconate"),
    ("senator", "upper house"), ("deputy", "lower house"),
    ("minister", "cabinet"), ("secretary", "secretariat"),
    ("attaché", "embassy"), ("consul", "consulate"),
    ("academician", "academy"), ("laureate", "pantheon"),
    ("fellow", "royal society"), ("member", "intelligentsia"),
    ("oligarch", "oligarchy"), ("patrician", "aristocracy"),
    ("proletarian", "proletariat"), ("bourgeois", "bourgeoisie"),
    ("vassal", "feudal system"), ("serf", "peasantry"),
    ("partisan", "resistance"), ("guerrilla", "insurgency"),
    ("operative", "cell"), ("agent", "network"),
    ("analyst", "think tank"), ("consultant", "advisory board"),
    ("adjudicator", "tribunal"), ("ombudsman", "oversight body"),
    ("regulator", "regulatory body"), ("auditor", "audit commission"),
    ("mediator", "mediation panel"), ("conciliator", "conciliation board"),
    ("rapporteur", "committee"), ("secretary-general", "secretariat"),
    ("comptroller", "audit office"), ("inspector", "inspectorate"),
]


# Distractor pools by category (words that are plausible but wrong)
DISTRACTORS_GENERAL = [
    "large", "small", "fast", "slow", "heavy", "light", "strong", "weak",
    "old", "new", "hot", "cold", "bright", "dark", "hard", "soft",
    "important", "useful", "common", "rare", "beautiful", "simple",
]

DISTRACTORS_PLACES = [
    "office", "market", "park", "street", "city", "country", "village",
    "factory", "station", "airport", "harbor", "museum", "theater",
    "hospital", "school", "church", "temple", "stadium", "arena",
]

DISTRACTORS_ACTIONS = [
    "run", "write", "build", "create", "destroy", "move", "grow",
    "teach", "learn", "work", "play", "fight", "travel", "study",
]

DISTRACTORS_PEOPLE = [
    "teacher", "doctor", "farmer", "driver", "worker", "manager",
    "leader", "student", "artist", "scientist", "engineer", "pilot",
]

# fmt: on


# ============================================================
# QUESTION GENERATION FUNCTIONS
# ============================================================


def _pick_distractors(answer: str, pool: list[str], n: int = 3) -> list[str]:
    """Pick n distractors from pool that aren't the answer."""
    candidates = [w for w in pool if w.lower() != answer.lower()]
    random.shuffle(candidates)
    return candidates[:n]


def _make_choices(answer: str, distractors: list[str]) -> list[str]:
    """Combine answer with distractors and shuffle."""
    choices = [answer] + distractors[:3]
    random.shuffle(choices)
    return choices


def _cap(s: str) -> str:
    """Capitalize first letter of each word for display."""
    return s.title() if len(s) < 30 else s.capitalize()


def generate_part_whole_q(
    pair1: tuple[str, str],
    pair2: tuple[str, str],
    distractors: list[str],
    difficulty: str,
) -> dict:
    """Generate a part-to-whole question from two pairs."""
    part1, whole1 = pair1
    part2, whole2 = pair2
    question = f"{part1.upper()} : {whole1.upper()} :: {part2.upper()} : ?"
    answer = _cap(whole2)
    dist = _pick_distractors(whole2, distractors, 3)
    dist = [_cap(d) for d in dist]
    choices = _make_choices(answer, dist)
    explanation = (
        f"{_cap(part1)} is a part of {_cap(whole1)}. "
        f"{_cap(part2)} is a part of {_cap(whole2)}. "
        f"Both are part-to-whole relationships."
    )
    return {
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["word analogy", "part-whole"],
    }


def generate_whole_part_q(
    pair1: tuple[str, str],
    pair2: tuple[str, str],
    distractors: list[str],
    difficulty: str,
) -> dict:
    """Generate a whole-to-part question from two pairs."""
    whole1, part1 = pair1
    whole2, part2 = pair2
    question = f"{whole1.upper()} : {part1.upper()} :: {whole2.upper()} : ?"
    answer = _cap(part2)
    dist = _pick_distractors(part2, distractors, 3)
    dist = [_cap(d) for d in dist]
    choices = _make_choices(answer, dist)
    explanation = (
        f"{_cap(whole1)} contains {_cap(part1)}. "
        f"{_cap(whole2)} contains {_cap(part2)}. "
        f"Both are whole-to-part relationships."
    )
    return {
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["word analogy", "whole-to-part"],
    }


def generate_item_category_q(
    pair1: tuple[str, str],
    pair2: tuple[str, str],
    distractors: list[str],
    difficulty: str,
) -> dict:
    """Generate an item-to-category question from two pairs."""
    item1, cat1 = pair1
    item2, cat2 = pair2
    question = f"{item1.upper()} : {cat1.upper()} :: {item2.upper()} : ?"
    answer = _cap(cat2)
    dist = _pick_distractors(cat2, distractors, 3)
    dist = [_cap(d) for d in dist]
    choices = _make_choices(answer, dist)
    explanation = (
        f"{_cap(item1)} is a type of {cat1}. "
        f"{_cap(item2)} is a type of {cat2}. "
        f"Both are item-to-category relationships."
    )
    return {
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["word analogy", "classification"],
    }


def generate_member_group_q(
    pair1: tuple[str, str],
    pair2: tuple[str, str],
    distractors: list[str],
    difficulty: str,
) -> dict:
    """Generate a member-to-group question from two pairs."""
    member1, group1 = pair1
    member2, group2 = pair2
    question = f"{member1.upper()} : {group1.upper()} :: {member2.upper()} : ?"
    answer = _cap(group2)
    dist = _pick_distractors(group2, distractors, 3)
    dist = [_cap(d) for d in dist]
    choices = _make_choices(answer, dist)
    explanation = (
        f"A {member1} is a member of a {group1}. "
        f"A {member2} is a member of a {group2}. "
        f"Both are member-to-group relationships."
    )
    return {
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "difficulty": difficulty,
        "tags": ["word analogy", "member-to-group"],
    }


def generate_questions_from_pool(
    pool: list[tuple[str, str]],
    gen_func,
    distractors: list[str],
    difficulty: str,
    count: int,
) -> list[dict]:
    """Generate `count` questions by pairing items from the pool."""
    questions = []
    pairs = list(pool)
    random.shuffle(pairs)

    # Generate questions by pairing consecutive items
    i = 0
    while len(questions) < count and i + 1 < len(pairs):
        pair1 = pairs[i]
        pair2 = pairs[i + 1]
        q = gen_func(pair1, pair2, distractors, difficulty)
        questions.append(q)
        i += 2

    # If we need more, wrap around with different pairings
    if len(questions) < count:
        random.shuffle(pairs)
        i = 0
        while len(questions) < count and i + 1 < len(pairs):
            pair1 = pairs[i]
            pair2 = pairs[(i + 2) % len(pairs)]
            q = gen_func(pair1, pair2, distractors, difficulty)
            # Avoid exact duplicate questions
            if q["question"] not in {qq["question"] for qq in questions}:
                questions.append(q)
            i += 1

    # Third pass with offset pairings if still short
    if len(questions) < count:
        random.shuffle(pairs)
        for offset in range(3, len(pairs)):
            if len(questions) >= count:
                break
            for i in range(len(pairs)):
                if len(questions) >= count:
                    break
                pair1 = pairs[i]
                pair2 = pairs[(i + offset) % len(pairs)]
                q = gen_func(pair1, pair2, distractors, difficulty)
                if q["question"] not in {qq["question"] for qq in questions}:
                    questions.append(q)

    return questions[:count]


def build_distractor_pool(
    *pools: list[tuple[str, str]],
    extra: list[str] | None = None,
) -> list[str]:
    """Build a distractor pool from all words in the given pair pools."""
    words = set()
    for pool in pools:
        for pair in pool:
            words.add(pair[0])
            words.add(pair[1])
    if extra:
        words.update(extra)
    return list(words)


# ============================================================
# MAIN GENERATION
# ============================================================


def main() -> None:
    # Build distractor pools
    all_wholes = build_distractor_pool(
        PART_WHOLE_EASY, PART_WHOLE_MEDIUM, PART_WHOLE_HARD,
        extra=DISTRACTORS_PLACES + DISTRACTORS_GENERAL,
    )
    all_parts = build_distractor_pool(
        WHOLE_PART_EASY, WHOLE_PART_MEDIUM, WHOLE_PART_HARD,
        extra=DISTRACTORS_GENERAL + DISTRACTORS_ACTIONS,
    )
    all_categories = build_distractor_pool(
        ITEM_CATEGORY_EASY, ITEM_CATEGORY_MEDIUM, ITEM_CATEGORY_HARD,
        extra=DISTRACTORS_PLACES + DISTRACTORS_GENERAL,
    )
    all_groups = build_distractor_pool(
        MEMBER_GROUP_EASY, MEMBER_GROUP_MEDIUM, MEMBER_GROUP_HARD,
        extra=DISTRACTORS_PEOPLE + DISTRACTORS_PLACES,
    )

    # Generate 50 questions per relationship type per difficulty = 200 per difficulty
    # 4 types x 50 = 200 per difficulty level

    easy_questions = []
    easy_questions += generate_questions_from_pool(
        PART_WHOLE_EASY, generate_part_whole_q, all_wholes, "Easy", 50
    )
    easy_questions += generate_questions_from_pool(
        WHOLE_PART_EASY, generate_whole_part_q, all_parts, "Easy", 50
    )
    easy_questions += generate_questions_from_pool(
        ITEM_CATEGORY_EASY, generate_item_category_q, all_categories, "Easy", 50
    )
    easy_questions += generate_questions_from_pool(
        MEMBER_GROUP_EASY, generate_member_group_q, all_groups, "Easy", 50
    )

    medium_questions = []
    medium_questions += generate_questions_from_pool(
        PART_WHOLE_MEDIUM, generate_part_whole_q, all_wholes, "Medium", 50
    )
    medium_questions += generate_questions_from_pool(
        WHOLE_PART_MEDIUM, generate_whole_part_q, all_parts, "Medium", 50
    )
    medium_questions += generate_questions_from_pool(
        ITEM_CATEGORY_MEDIUM, generate_item_category_q, all_categories, "Medium", 50
    )
    medium_questions += generate_questions_from_pool(
        MEMBER_GROUP_MEDIUM, generate_member_group_q, all_groups, "Medium", 50
    )

    hard_questions = []
    hard_questions += generate_questions_from_pool(
        PART_WHOLE_HARD, generate_part_whole_q, all_wholes, "Hard", 50
    )
    hard_questions += generate_questions_from_pool(
        WHOLE_PART_HARD, generate_whole_part_q, all_parts, "Hard", 50
    )
    hard_questions += generate_questions_from_pool(
        ITEM_CATEGORY_HARD, generate_item_category_q, all_categories, "Hard", 50
    )
    hard_questions += generate_questions_from_pool(
        MEMBER_GROUP_HARD, generate_member_group_q, all_groups, "Hard", 50
    )

    # Combine all questions
    all_questions = easy_questions + medium_questions + hard_questions

    # Assign IDs and merge with base metadata
    final = []
    for i, q in enumerate(all_questions, start=1):
        entry = {"id": i, **BASE, **q}
        final.append(entry)

    # Write output
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(final, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Generated {len(final)} questions:")
    print(f"  Easy: {sum(1 for q in final if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in final if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in final if q['difficulty'] == 'Hard')}")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
