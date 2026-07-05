"""Generate the Verbal Ability / Word Meanings / Root Words question bank.

The bank is built from a curated root-family roster. Each root family gets
four question styles so the final output has a balanced 150 / 150 / 150 / 150
difficulty split while staying focused on the core meaning carried by roots.

Usage:
    python scripts/generate_root_words_bank.py
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "word-meaning"
    / "root-words"
    / "questions.json"
)

FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)
DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Root Words"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

WORD_RE = re.compile(r"^[a-z]+$")

SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=2))
SESSION.mount("http://", HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=2))

ROOT_FAMILIES = [
    ("aud", "aud", "hear; listen", [
        "audio",
        "audience",
        "audible",
        "audition",
        "auditorium",
    ]),
    ("bene", "bene", "good; well", [
        "benefit",
        "beneficial",
        "benefactor",
        "benevolent",
        "beneficiary",
    ]),
    ("cent", "cent", "hundred", [
        "century",
        "centennial",
        "percent",
        "centipede",
        "centurion",
    ]),
    ("circum", "circum", "around", [
        "circumference",
        "circumstance",
        "circumstantial",
        "circumvent",
        "circumlocution",
    ]),
    ("dict", "dict", "say; speak", [
        "dictate",
        "dictionary",
        "dictator",
        "predict",
        "verdict",
    ]),
    ("duc", "duc/duct", "lead; carry", [
        "conduct",
        "induce",
        "produce",
        "reduce",
        "deduct",
    ]),
    ("form", "form", "shape; form", [
        "conform",
        "reform",
        "transform",
        "uniform",
        "formation",
    ]),
    ("fract", "fract", "break", [
        "fraction",
        "fragment",
        "fracture",
        "infraction",
        "refract",
    ]),
    ("ject", "ject", "throw", [
        "project",
        "reject",
        "inject",
        "eject",
        "interject",
    ]),
    ("jud", "jud", "judge", [
        "judge",
        "judicial",
        "prejudice",
        "judiciary",
        "judgment",
    ]),
    ("mal", "mal", "bad; evil", [
        "malicious",
        "malfunction",
        "malady",
        "malevolent",
        "malice",
    ]),
    ("mit", "mit", "send", [
        "transmit",
        "admit",
        "permit",
        "submit",
        "remit",
    ]),
    ("mort", "mort", "death", [
        "mortal",
        "immortal",
        "mortality",
        "mortician",
        "mortuary",
    ]),
    ("multi", "multi", "many", [
        "multiple",
        "multiply",
        "multitude",
        "multinational",
        "multipurpose",
    ]),
    ("port", "port", "carry", [
        "transport",
        "portable",
        "import",
        "export",
        "porter",
    ]),
    ("rupt", "rupt", "break", [
        "corrupt",
        "bankrupt",
        "erupt",
        "disrupt",
        "interrupt",
    ]),
    ("scrib", "scrib/script", "write", [
        "describe",
        "prescribe",
        "subscribe",
        "script",
        "manuscript",
    ]),
    ("sect", "sect/sec", "cut", [
        "section",
        "sector",
        "dissect",
        "insect",
        "intersection",
    ]),
    ("spect", "spect", "look; see", [
        "inspect",
        "respect",
        "spectator",
        "spectacle",
        "retrospect",
    ]),
    ("struct", "struct", "build", [
        "structure",
        "construct",
        "destruction",
        "instruction",
        "infrastructure",
    ]),
    ("vid", "vid/vis", "see", [
        "visible",
        "vision",
        "revise",
        "envision",
        "video",
    ]),
    ("voc", "voc", "voice; call", [
        "vocal",
        "vocation",
        "advocate",
        "invoke",
        "revoke",
    ]),
    ("auto", "auto", "self", [
        "automatic",
        "autobiography",
        "automobile",
        "autonomy",
        "autograph",
    ]),
    ("bio", "bio", "life", [
        "biology",
        "biography",
        "biodegradable",
        "biosphere",
        "antibiotic",
    ]),
    ("chron", "chron", "time", [
        "chronological",
        "chronicle",
        "chronic",
        "synchronize",
        "anachronism",
    ]),
    ("graph", "graph", "write", [
        "graphic",
        "photograph",
        "telegraph",
        "paragraph",
        "diagram",
    ]),
    ("hydr", "hydr", "water", [
        "hydrate",
        "hydration",
        "hydraulic",
        "hydrant",
        "dehydration",
    ]),
    ("logy", "logy", "study of", [
        "anthropology",
        "ecology",
        "mythology",
        "neurology",
        "sociology",
    ]),
    ("meter", "meter/metr", "measure", [
        "thermometer",
        "perimeter",
        "kilometer",
        "diameter",
        "metric",
    ]),
    ("micro", "micro", "small", [
        "microscope",
        "microphone",
        "microbe",
        "microchip",
        "microcosm",
    ]),
]

# Some words have noisy first dictionary senses. Pin the clue text to a more
# CSE-friendly sense so the ultra questions stay accurate and readable.
DEFINITION_OVERRIDES: dict[str, str] = {
    "chronic": "lasting for a long time or recurring often",
    "biodegradable": "able to break down naturally by living organisms",
    "beneficiary": "a person who receives a benefit or advantage",
    "corrupt": "dishonest or immoral; made bad",
    "admit": "to allow someone to enter or to accept as true",
    "deduct": "to take away or subtract",
    "dissect": "to cut apart or examine by cutting apart",
    "fracture": "a break or crack in something",
    "fragment": "a small broken piece",
    "eject": "to force out or throw out",
    "inject": "to put or force something into something else",
    "immortal": "living forever or not able to die",
    "instruction": "information that tells you how to do something",
    "judge": "to form an opinion or decide after careful consideration",
    "judgment": "the ability to form an opinion or decision",
    "judicial": "relating to courts or judges",
    "judiciary": "the system of courts and judges",
    "antibiotic": "a substance that kills or stops bacteria",
    "chronological": "arranged in the order that things happened",
    "conform": "to act according to rules or expectations",
    "formation": "the act of forming or arranging something",
    "malady": "an illness or disease",
    "malevolent": "having or showing a wish to do harm",
    "malfunction": "to fail to work properly",
    "mortician": "a person who prepares bodies for burial",
    "mortuary": "a place where bodies are kept before burial",
    "fraction": "a small part of a whole",
    "mortal": "subject to death",
    "permit": "to allow someone to do something",
    "multiple": "having more than one part or element",
    "multiply": "to increase in number",
    "reform": "to improve by making changes",
    "reduce": "to make smaller or less",
    "uniform": "the same in all cases; consistent",
    "neurology": "the study of the nervous system",
    "transmit": "to send from one place to another",
    "transform": "to change greatly in form or appearance",
    "hydration": "the act of adding or absorbing water",
    "automatic": "working by itself with little or no direct control",
    "portable": "able to be carried easily",
    "interrupt": "to stop something temporarily",
    "vision": "the ability to see",
    "sector": "a division or part of something larger",
    "export": "to carry or send goods out",
    "import": "to carry or bring goods in",
    "project": "to throw or cast forward",
    "invoke": "to call on for help or authority",
    "transport": "to carry people or goods from one place to another",
    "insect": "a small animal with six legs and three main body parts",
}


@dataclass
class WordRecord:
    word: str
    family_key: str
    root_label: str
    root_meaning: str
    frequency: int
    definition: str = ""


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _truncate(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(",;:.!?") + "..."


def _download_frequency_map() -> dict[str, int]:
    response = requests.get(FREQUENCY_URL, timeout=60)
    response.raise_for_status()

    frequency_map: dict[str, int] = {}
    for raw_line in response.text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        word = parts[0].lower()
        if not WORD_RE.fullmatch(word):
            continue
        try:
            frequency = int(parts[1])
        except ValueError:
            continue
        frequency_map[word] = frequency
    return frequency_map


def _fetch_definition(word: str) -> str:
    try:
        response = SESSION.get(DICTIONARY_URL.format(word=word), timeout=20)
    except requests.RequestException:
        return ""
    if response.status_code != 200:
        return ""
    try:
        payload = response.json()
    except ValueError:
        return ""
    if not isinstance(payload, list) or not payload:
        return ""

    for entry in payload:
        meanings = entry.get("meanings", [])
        for meaning in meanings:
            definitions = meaning.get("definitions", [])
            for definition in definitions:
                text = _normalize(str(definition.get("definition", "")))
                if text:
                    text = text.replace('"', "'")
                    return _truncate(text, 14).rstrip(".")
    return ""


def _build_records(frequency_map: dict[str, int]) -> list[WordRecord]:
    records: list[WordRecord] = []
    for family_key, root_label, root_meaning, words in ROOT_FAMILIES:
        for word in words:
            records.append(
                WordRecord(
                    word=word,
                    family_key=family_key,
                    root_label=root_label,
                    root_meaning=root_meaning,
                    frequency=frequency_map.get(word, 0),
                )
            )
    return records


def _hydrate_definitions(records: list[WordRecord]) -> None:
    with cf.ThreadPoolExecutor(max_workers=12) as executor:
        future_map = {
            executor.submit(_fetch_definition, record.word): record for record in records
        }
        for future in cf.as_completed(future_map):
            record = future_map[future]
            try:
                definition = future.result()
            except Exception:
                definition = ""

            # Retry missing entries one by one. The dictionary API is reliable
            # for these words, but the concurrent pass can occasionally hit a
            # transient failure or rate limit.
            if not definition:
                definition = _fetch_definition(record.word)

            definition = _normalize(definition.replace('"', "'")) if definition else ""
            definition = _truncate(definition, 14).rstrip(".") if definition else ""

            override = DEFINITION_OVERRIDES.get(record.word)
            record.definition = override or definition or f'word related to {record.root_meaning}'


def _build_family_groups(records: list[WordRecord]) -> dict[str, list[str]]:
    groups: dict[str, list[tuple[int, str]]] = defaultdict(list)
    for record in records:
        groups[record.family_key].append((record.frequency, record.word))

    ordered: dict[str, list[str]] = {}
    for family_key, items in groups.items():
        ordered[family_key] = [
            word for _frequency, word in sorted(items, key=lambda item: (-item[0], len(item[1]), item[1]))
        ]
    return ordered


def _root_label_pool() -> list[str]:
    return _dedupe([root_label for _family_key, root_label, _meaning, _words in ROOT_FAMILIES])


def _meaning_pool() -> list[str]:
    return _dedupe([meaning for _family_key, _root_label, meaning, _words in ROOT_FAMILIES])


def _word_pool(records: list[WordRecord]) -> list[str]:
    return _dedupe([record.word for record in records])


def _build_choices(answer: str, pool: list[str], rng: random.Random) -> list[str]:
    options = [item for item in pool if item != answer]
    rng.shuffle(options)
    choices = [answer, *options[:3]]
    if len(choices) < 4:
        raise RuntimeError(f"not enough distractors for {answer!r}")
    rng.shuffle(choices)
    if len(set(choices)) != 4:
        raise RuntimeError(f"duplicate choices for {answer!r}")
    return choices


def _pick_family_peer(record: WordRecord, family_groups: dict[str, list[str]], rng: random.Random) -> str:
    peers = [word for word in family_groups[record.family_key] if word != record.word]
    if not peers:
        raise RuntimeError(f"no family peers available for {record.word}")
    return rng.choice(peers)


def _build_question(
    record: WordRecord,
    difficulty: str,
    family_groups: dict[str, list[str]],
    root_label_pool: list[str],
    meaning_pool: list[str],
    word_pool: list[str],
) -> dict[str, object]:
    rng = random.Random(f"{difficulty}:{record.word}")

    if difficulty == "Easy":
        question = rng.choice(
            [
                f'Which root family appears in "{record.word}"?',
                f'What root family is used in "{record.word}"?',
                f'Identify the root family in "{record.word}".',
            ]
        )
        answer = record.root_label
        choices = _build_choices(answer, root_label_pool, rng)
        explanation = (
            f'The word belongs to the {record.root_label} family, which means {record.root_meaning}.'
        )
        tags = ["root", "root_id", "word-meaning", "cse", record.family_key]
    elif difficulty == "Medium":
        question = rng.choice(
            [
                f'What does the root family in "{record.word}" usually mean?',
                f'Which meaning best fits the root in "{record.word}"?',
                f'Pick the core meaning of the root in "{record.word}".',
            ]
        )
        answer = record.root_meaning
        choices = _build_choices(answer, meaning_pool, rng)
        explanation = f'The root family {record.root_label} usually means {record.root_meaning}.'
        tags = ["root", "root_meaning", "word-meaning", "cse", record.family_key]
    elif difficulty == "Hard":
        question = rng.choice(
            [
                f'Which word below comes from the same root family as "{record.word}"?',
                f'Pick the best match from the same root family as "{record.word}".',
                f'Which option belongs to the same root cluster as "{record.word}"?',
            ]
        )
        answer = _pick_family_peer(record, family_groups, rng)
        distractors = [word for word in word_pool if word not in family_groups[record.family_key] and word != answer]
        rng.shuffle(distractors)
        choices = [answer, *distractors[:3]]
        rng.shuffle(choices)
        if len(set(choices)) != 4:
            raise RuntimeError(f"duplicate hard choices for {record.word!r}")
        explanation = f'"{record.word}" and "{answer}" are both part of the {record.root_label} family.'
        tags = ["root", "root_family", "word-meaning", "cse", record.family_key]
    else:
        definition = record.definition or f'word related to {record.root_meaning}'
        question = rng.choice(
            [
                f'Which word best matches this definition: "{definition}"?',
                f'Pick the word that matches this short meaning: "{definition}".',
                f'Which option is closest to the meaning "{definition}"?',
            ]
        )
        answer = record.word
        distractors = [word for word in word_pool if word not in family_groups[record.family_key] and word != answer]
        rng.shuffle(distractors)
        choices = [answer, *distractors[:3]]
        rng.shuffle(choices)
        if len(set(choices)) != 4:
            raise RuntimeError(f"duplicate ultra choices for {record.word!r}")
        explanation = (
            f'The clue points to "{record.word}", and the root family {record.root_label} supports that meaning.'
        )
        tags = ["root", "definition", "word-meaning", "cse", record.family_key]

    if answer not in choices:
        raise RuntimeError(f"answer missing for {record.word!r}")

    return {
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": _dedupe(tags),
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _build_bank(records: list[WordRecord]) -> list[dict[str, object]]:
    family_groups = _build_family_groups(records)
    root_label_pool = _root_label_pool()
    meaning_pool = _meaning_pool()
    word_pool = _word_pool(records)

    questions: list[dict[str, object]] = []
    question_id = 1
    for difficulty in DIFFICULTY_ORDER:
        for record in records:
            question = _build_question(
                record,
                difficulty,
                family_groups,
                root_label_pool,
                meaning_pool,
                word_pool,
            )
            question["id"] = question_id
            questions.append(question)
            question_id += 1
    return questions


def _validate_bank(questions: list[dict[str, object]], records: list[WordRecord]) -> None:
    if len(questions) != 600:
        raise RuntimeError(f"expected 600 questions, got {len(questions)}")

    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise RuntimeError("question ids are not sequential from 1 to 600")

    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise RuntimeError(f"unexpected difficulty distribution: {dict(counts)}")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise RuntimeError("question texts are not unique")

    words = [record.word for record in records]
    if len(words) != len(set(words)):
        raise RuntimeError("target words are not unique")

    seen_questions: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        choices = [str(choice) for choice in question["choices"]]  # type: ignore[assignment]
        if len(choices) != 4:
            raise RuntimeError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise RuntimeError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise RuntimeError(f"answer missing from choices for question {question['id']}")
        key = (str(question["question"]), tuple(sorted(choices)))
        if key in seen_questions:
            raise RuntimeError(f"duplicate question and choice set at id {question['id']}")
        seen_questions.add(key)


def main() -> int:
    frequency_map = _download_frequency_map()
    records = _build_records(frequency_map)
    _hydrate_definitions(records)
    records = sorted(records, key=lambda item: (-item.frequency, len(item.word), item.word))

    family_summary = Counter(record.family_key for record in records)
    print("Selected root words:")
    for family_key, root_label, _meaning, _words in ROOT_FAMILIES:
        family_words = [record.word for record in records if record.family_key == family_key]
        preview = ", ".join(family_words[:5])
        print(f"  {root_label:>12} ({family_summary[family_key]:>2}): {preview}")

    questions = _build_bank(records)
    _validate_bank(questions, records)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    print(f"Selected {len(records)} words across {len(ROOT_FAMILIES)} root families")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
