"""Generate the Verbal Ability / Word Meanings / Word Families question bank.

The bank is built from a curated family roster. Each family gets four question
styles so the final output has a balanced 150 / 150 / 150 / 150 difficulty
split while staying focused on the shared base word and meaning carried by the
family.

Usage:
    python scripts/generate_word_families_bank.py
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
    / "word-families"
    / "questions.json"
)

FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)
DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Word Families"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

WORD_RE = re.compile(r"^[a-z]+$")

SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=2))
SESSION.mount("http://", HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=2))

ROOT_FAMILIES = [
    ("help", "help", "to give aid; make easier", [
        "help",
        "helpful",
        "helpless",
        "helper",
        "helpfulness",
    ]),
    ("care", "care", "to feel concern; to look after", [
        "care",
        "careful",
        "careless",
        "caring",
        "carefully",
    ]),
    ("play", "play", "to take part in an activity for fun", [
        "play",
        "playful",
        "player",
        "playfulness",
        "replay",
    ]),
    ("work", "work", "to do a job or task", [
        "work",
        "worker",
        "workable",
        "working",
        "overwork",
    ]),
    ("move", "move", "to go from one place to another", [
        "move",
        "movement",
        "movable",
        "mover",
        "remove",
    ]),
    ("use", "use", "to put something into action; to employ", [
        "use",
        "useful",
        "useless",
        "user",
        "reuse",
    ]),
    ("hope", "hope", "to want something with expectation", [
        "hope",
        "hopeful",
        "hopeless",
        "hopefully",
        "hoped",
    ]),
    ("kind", "kind", "having a friendly or good nature", [
        "kind",
        "kindness",
        "kindly",
        "unkind",
        "kindhearted",
    ]),
    ("friend", "friend", "a person who is close and supportive", [
        "friend",
        "friendly",
        "friendship",
        "friendless",
        "unfriendly",
    ]),
    ("power", "power", "the ability or strength to act", [
        "power",
        "powerful",
        "powerless",
        "empower",
        "overpower",
    ]),
    ("read", "read", "to look at and understand written words", [
        "read",
        "reader",
        "readable",
        "unread",
        "reread",
    ]),
    ("write", "write", "to form words or text on a surface", [
        "write",
        "writer",
        "writing",
        "rewrite",
        "writable",
    ]),
    ("learn", "learn", "to gain knowledge or skill", [
        "learn",
        "learner",
        "learning",
        "relearn",
        "unlearn",
    ]),
    ("teach", "teach", "to give knowledge or instruction", [
        "teach",
        "teacher",
        "teaching",
        "teachable",
        "reteach",
    ]),
    ("act", "act", "to do something; to take action", [
        "act",
        "action",
        "active",
        "actor",
        "activity",
    ]),
    ("create", "create", "to make something new", [
        "create",
        "creator",
        "creation",
        "creative",
        "recreate",
    ]),
    ("protect", "protect", "to keep safe from harm", [
        "protect",
        "protection",
        "protective",
        "protector",
        "unprotected",
    ]),
    ("decide", "decide", "to make a choice or settle a matter", [
        "decide",
        "decision",
        "decisive",
        "indecisive",
        "undecided",
    ]),
    ("clear", "clear", "easy to see or understand; free from confusion", [
        "clear",
        "clearer",
        "clearest",
        "clearly",
        "unclear",
    ]),
    ("strong", "strong", "having great power or force", [
        "strong",
        "stronger",
        "strongest",
        "strength",
        "strongly",
    ]),
    ("safe", "safe", "free from danger", [
        "safe",
        "safety",
        "safer",
        "safely",
        "unsafe",
    ]),
    ("happy", "happy", "feeling glad or pleased", [
        "happy",
        "happiness",
        "unhappy",
        "happily",
        "happier",
    ]),
    ("bright", "bright", "giving out a lot of light; smart and lively", [
        "bright",
        "brightness",
        "brighten",
        "brightly",
        "brightest",
    ]),
    ("dark", "dark", "having little light", [
        "dark",
        "darkness",
        "darken",
        "darkly",
        "darkest",
    ]),
    ("warm", "warm", "having or giving a comfortable heat", [
        "warm",
        "warmth",
        "warmer",
        "warmly",
        "warming",
    ]),
    ("clean", "clean", "free from dirt or mess", [
        "clean",
        "cleaner",
        "cleanliness",
        "cleanly",
        "unclean",
    ]),
    ("quick", "quick", "moving or happening fast", [
        "quick",
        "quicker",
        "quickest",
        "quickly",
        "quickness",
    ]),
    ("slow", "slow", "moving or happening at a low speed", [
        "slow",
        "slower",
        "slowest",
        "slowly",
        "slowness",
    ]),
    ("nation", "nation", "a country or people with shared identity", [
        "nation",
        "national",
        "nationality",
        "international",
        "multinational",
    ]),
    ("respect", "respect", "esteem or regard for someone or something", [
        "respect",
        "respectful",
        "respectable",
        "disrespect",
        "disrespectful",
    ]),
]

# Some words have noisy first dictionary senses. Pin the clue text to a more
# CSE-friendly sense so the ultra questions stay accurate and readable.
DEFINITION_OVERRIDES: dict[str, str] = {
    "creation": "the act of making something new",
    "disrespect": "a lack of respect; rude or discourteous behavior",
    "decisive": "quick and firm in making a decision",
    "friendless": "without friends",
    "friendly": "showing the qualities of a good friend",
    "kindly": "in a kind or friendly way",
    "quicker": "moving or happening faster than something else",
    "quickest": "moving or happening with the greatest speed",
    "respectful": "showing respect; courteous",
    "reuse": "to use something again",
    "relearn": "to learn again",
    "user": "a person who uses something",
    "stronger": "having more physical force than something else",
    "strongest": "having the greatest physical force",
    "warmer": "having more warmth than something else",
    "warm": "having a comfortable moderate heat",
    "use": "to put something into action; to employ",
    "unlearn": "to forget or stop using a learned habit",
    "writable": "able to be written on or into",
    "indecisive": "unable to decide easily",
}

BASE_WORDS = {
    "help",
    "care",
    "play",
    "work",
    "move",
    "use",
    "hope",
    "kind",
    "friend",
    "power",
    "read",
    "write",
    "learn",
    "teach",
    "act",
    "create",
    "protect",
    "decide",
    "clear",
    "strong",
    "safe",
    "happy",
    "bright",
    "dark",
    "warm",
    "clean",
    "quick",
    "slow",
    "nation",
    "respect",
}

COMPARATIVE_FORMS = {
    "clearer",
    "cleaner",
    "happier",
    "quicker",
    "safer",
    "slower",
    "stronger",
    "warmer",
}

SUPERLATIVE_FORMS = {
    "brightest",
    "clearest",
    "cleanest",
    "darkest",
    "happiest",
    "quickest",
    "slowest",
    "strongest",
}

ADVERB_FORMS = {
    "brightly",
    "carefully",
    "cleanly",
    "clearly",
    "darkly",
    "happily",
    "kindly",
    "quickly",
    "safely",
    "slowly",
    "strongly",
    "warmly",
    "hopefully",
}

NOUN_FORMS = {
    "action",
    "activity",
    "cleanliness",
    "creation",
    "decision",
    "darkness",
    "friendship",
    "happiness",
    "helpfulness",
    "kindness",
    "movement",
    "nationality",
    "playfulness",
    "protection",
    "quickness",
    "readability",
    "respect",
    "safety",
    "slowness",
    "strength",
    "teachability",
    "teaching",
    "use",
    "warmth",
    "writing",
}

AGENT_NOUNS = {
    "creator",
    "friend",
    "helper",
    "learner",
    "mover",
    "player",
    "protector",
    "reader",
    "teacher",
    "user",
    "worker",
    "writer",
}

VERB_FORMS = {
    "brighten",
    "decide",
    "empower",
    "hoped",
    "learning",
    "overpower",
    "overwork",
    "read",
    "recreate",
    "readable",
    "relearn",
    "remove",
    "replay",
    "respect",
    "reteach",
    "rewrite",
    "reuse",
    "teach",
    "teaching",
    "unlearn",
    "working",
    "warming",
    "write",
}

ADJECTIVE_FORMS = {
    "careful",
    "careless",
    "caring",
    "creative",
    "decisive",
    "disrespectful",
    "friendly",
    "friendless",
    "helpful",
    "helpless",
    "hopeless",
    "hopeful",
    "indecisive",
    "kindhearted",
    "multinational",
    "national",
    "overworked",
    "powerful",
    "powerless",
    "protective",
    "readable",
    "respectable",
    "respectful",
    "strongly",
    "teachabe",
    "teachable",
    "unclear",
    "unclean",
    "unfriendly",
    "unhappy",
    "unprotected",
    "unsafe",
    "useless",
    "useful",
    "writable",
    "workable",
    "quick",
    "bright",
    "dark",
    "slow",
    "warm",
    "clean",
    "moveable",
    "movable",
}


def _word_kind(word: str) -> str:
    if word in BASE_WORDS:
        return "base word"
    if word in COMPARATIVE_FORMS:
        return "comparative form"
    if word in SUPERLATIVE_FORMS:
        return "superlative form"
    if word in ADVERB_FORMS:
        return "adverb form"
    if word in AGENT_NOUNS:
        return "agent noun"
    if word in NOUN_FORMS:
        return "noun form"
    if word in VERB_FORMS:
        return "verb form"
    if word in ADJECTIVE_FORMS:
        return "adjective form"
    return "family form"


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
                f'Which base word is shared by "{record.word}"?',
                f'What word family does "{record.word}" belong to?',
                f'Identify the base word in "{record.word}".',
            ]
        )
        answer = record.root_label
        choices = _build_choices(answer, root_label_pool, rng)
        explanation = (
            f'The word belongs to the {record.root_label} family, and that base idea means {record.root_meaning}.'
        )
        tags = ["family", "base_word", "word-meaning", "cse", record.family_key]
    elif difficulty == "Medium":
        question = rng.choice(
            [
                f'What does the base word in "{record.word}" usually mean?',
                f'Which meaning best fits the base word in "{record.word}"?',
                f'Pick the core meaning of the family base in "{record.word}".',
            ]
        )
        answer = record.root_meaning
        choices = _build_choices(answer, meaning_pool, rng)
        explanation = f'The word family {record.root_label} usually carries the meaning {record.root_meaning}.'
        tags = ["family", "family_meaning", "word-meaning", "cse", record.family_key]
    elif difficulty == "Hard":
        question = rng.choice(
            [
                f'Which word below comes from the same family as "{record.word}"?',
                f'Pick the best match from the same word family as "{record.word}".',
                f'Which option belongs to the same word family as "{record.word}"?',
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
        tags = ["family", "family_match", "word-meaning", "cse", record.family_key]
    else:
        definition = record.definition or f'word related to {record.root_meaning}'
        kind = _word_kind(record.word)
        question = rng.choice(
            [
                f'Which {kind} best matches this definition: "{definition}"?',
                f'Pick the {kind} that matches this short meaning: "{definition}".',
                f'Which option is closest to the meaning "{definition}" for this {kind}?',
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
            f'The clue points to "{record.word}", and the word family {record.root_label} supports that meaning.'
        )
        tags = ["family", "definition", "word-meaning", "cse", record.family_key]

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
    print("Selected family words:")
    for family_key, root_label, _meaning, _words in ROOT_FAMILIES:
        family_words = [record.word for record in records if record.family_key == family_key]
        preview = ", ".join(family_words[:5])
        print(f"  {root_label:>12} ({family_summary[family_key]:>2}): {preview}")

    questions = _build_bank(records)
    _validate_bank(questions, records)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    print(f"Selected {len(records)} words across {len(ROOT_FAMILIES)} word families")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
