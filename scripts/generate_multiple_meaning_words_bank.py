"""Generate the Verbal Ability / Word Meanings / Multiple Meaning Words bank.

The generator uses Open English Wordnet for multi-sense lemmas and the
FrequencyWords list for a simple difficulty ladder. Each item targets one
word with at least four clean senses, and the four answer choices are the
four senses shown for that word.

That keeps the bank tightly aligned to the lesson: every item is really a
context-and-sense question, not a generic synonym drill.
"""

from __future__ import annotations

import io
import json
import random
import re
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

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
    / "multiple-meaning-words"
    / "questions.json"
)

WORDNET_URL = "https://en-word.net/static/english-wordnet-2025.zip"
FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Multiple Meaning Words"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_TO_SENSE_INDEX = {"Easy": 0, "Medium": 1, "Hard": 2, "Ultra": 3}

WORD_RE = re.compile(r"^[a-z]+$")
SPLIT_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

CONTENT_POS = {"adj", "n", "v", "adv"}
POS_PRIORITY = ("adj", "v", "n", "adv")

STOP_WORDS = {
    "a",
    "an",
    "the",
    "and",
    "or",
    "but",
    "to",
    "of",
    "in",
    "on",
    "for",
    "with",
    "as",
    "by",
    "from",
    "at",
    "into",
    "over",
    "under",
    "up",
    "down",
    "about",
    "against",
    "between",
    "among",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "near",
    "than",
    "then",
    "that",
    "this",
    "these",
    "those",
    "be",
    "been",
    "being",
    "is",
    "am",
    "are",
    "was",
    "were",
    "do",
    "does",
    "did",
    "doing",
    "done",
    "have",
    "has",
    "had",
    "having",
    "can",
    "could",
    "may",
    "might",
    "must",
    "will",
    "would",
    "should",
    "shall",
    "not",
    "no",
    "nor",
    "so",
    "yet",
    "very",
    "more",
    "most",
    "less",
    "least",
    "each",
    "every",
    "some",
    "any",
    "all",
    "both",
    "few",
    "many",
    "much",
    "such",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
    "ten",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "who",
    "whom",
    "whose",
    "which",
    "what",
    "if",
    "else",
    "your",
    "yours",
    "our",
    "ours",
    "their",
    "theirs",
    "his",
    "her",
    "hers",
    "its",
    "my",
    "mine",
    "i",
    "you",
    "he",
    "she",
    "it",
    "we",
    "they",
    "me",
    "us",
    "them",
}

GENERIC_DISPLAY_HEADS = {
    "thing",
    "stuff",
    "object",
    "entity",
    "matter",
    "way",
    "sort",
    "type",
    "kind",
    "process",
    "state",
    "condition",
    "act",
    "action",
    "unit",
    "person",
    "someone",
    "something",
}

BAD_DISPLAY_TOKENS = {
    "someone",
    "something",
    "somebody",
    "contingencies",
    "claimed",
    "whatever",
    "whichever",
    "wherever",
    "whoever",
}

NATURAL_CATEGORIES = {
    "finance",
    "river",
    "animal",
    "object",
    "time",
    "quality",
    "communication",
    "action",
    "body",
    "sport",
    "light",
}

QUESTION_TEMPLATES = {
    "direct": [
        lambda q: f'What does "{q["word"]}" mean in "{q["sentence"]}"?',
        lambda q: f'What is the meaning of "{q["word"]}" in "{q["sentence"]}"?',
    ],
    "restatement": [
        lambda q: f'Which meaning of "{q["word"]}" is restated in "{q["sentence"]}"?',
        lambda q: f'What meaning of "{q["word"]}" is being restated in "{q["sentence"]}"?',
    ],
    "contrast": [
        lambda q: f'Which meaning of "{q["word"]}" is shown by the contrast in "{q["sentence"]}"?',
        lambda q: f'What meaning of "{q["word"]}" is contrasted in "{q["sentence"]}"?',
    ],
    "context": [
        lambda q: f'Choose the meaning of "{q["word"]}" that fits "{q["sentence"]}".',
        lambda q: f'Which meaning of "{q["word"]}" best fits "{q["sentence"]}"?',
        lambda q: f'In "{q["sentence"]}", how is "{q["word"]}" used?',
    ],
}

QUESTION_WEIGHTS = {
    "Easy": ("direct", "context", "restatement", "direct"),
    "Medium": ("context", "restatement", "contrast", "direct"),
    "Hard": ("contrast", "context", "restatement", "direct"),
    "Ultra": ("contrast", "restatement", "context", "direct"),
}

FINANCE_WORDS = {
    "financial",
    "money",
    "bank",
    "deposit",
    "loan",
    "credit",
    "cash",
    "account",
    "payment",
    "fund",
    "funds",
    "currency",
    "treasury",
}

RIVER_WORDS = {
    "river",
    "shore",
    "edge",
    "bank",
    "coast",
    "slope",
    "water",
    "stream",
    "embankment",
}

ANIMAL_WORDS = {
    "animal",
    "mammal",
    "bird",
    "fish",
    "insect",
    "reptile",
    "creature",
    "beast",
}

OBJECT_WORDS = {
    "tool",
    "instrument",
    "device",
    "implement",
    "apparatus",
    "machine",
    "utensil",
    "object",
    "item",
    "piece",
}

TIME_WORDS = {
    "season",
    "time",
    "period",
    "moment",
    "year",
    "month",
    "day",
    "hour",
    "spring",
    "summer",
    "fall",
    "winter",
}

QUALITY_WORDS = {
    "heavy",
    "bright",
    "dark",
    "good",
    "bad",
    "fine",
    "soft",
    "hard",
    "clear",
    "sharp",
    "straight",
    "light",
    "weak",
    "strong",
}

COMMUNICATION_WORDS = {
    "message",
    "report",
    "speech",
    "remark",
    "statement",
    "note",
    "letter",
    "signal",
    "say",
    "tell",
    "speak",
    "call",
}

GROUP_WORDS = {
    "group",
    "set",
    "series",
    "row",
    "line",
    "collection",
    "pile",
    "batch",
    "heap",
    "cluster",
    "pack",
}

ACTION_WORDS = {
    "move",
    "make",
    "cause",
    "put",
    "place",
    "take",
    "turn",
    "set",
    "run",
    "strike",
    "hit",
    "file",
    "watch",
    "spring",
    "light",
}

FOOD_WORDS = {
    "food",
    "fruit",
    "grain",
    "seed",
    "plant",
    "leaf",
    "root",
    "meat",
    "dish",
    "meal",
}

BODY_WORDS = {
    "head",
    "hand",
    "arm",
    "leg",
    "foot",
    "mouth",
    "eye",
    "ear",
    "nose",
    "face",
    "back",
    "body",
}

SPORT_WORDS = {
    "game",
    "sport",
    "bat",
    "match",
    "play",
    "ball",
    "score",
    "team",
}

LEGAL_WORDS = {
    "law",
    "court",
    "rule",
    "official",
    "order",
    "charge",
    "fine",
    "case",
    "justice",
    "authority",
}

NATURAL_TEMPLATES = {
    "finance": {
        "n": [
            "She deposited her paycheck at the {word} before lunch.",
            "The teller at the {word} helped her open an account.",
        ]
    },
    "river": {
        "n": [
            "The hikers rested on the {word} beside the river.",
            "The boat drifted close to the {word} after the rain.",
        ]
    },
    "animal": {
        "n": [
            "A {word} flew out of the cave at dusk.",
            "The {word} moved quietly through the dark trees.",
        ]
    },
    "object": {
        "n": [
            "He used the {word} to open the crate.",
            "The {word} was kept in the drawer with the other tools.",
        ]
    },
    "time": {
        "n": [
            "We will travel in the {word} when the flowers bloom.",
            "The meeting was planned for the {word} after winter.",
        ]
    },
    "quality": {
        "adj": [
            "The box was {word} enough to carry with one hand.",
            "The room felt {word} after the long shift.",
        ]
    },
    "communication": {
        "n": [
            "The report included a short {word} from the mayor.",
            "The letter contained an important {word} from the office.",
        ],
        "v": [
            "She tried to {word} the news clearly.",
            "They will {word} the report to the public.",
        ],
    },
    "group": {
        "n": [
            "The teacher sorted the {word} into neat piles.",
            "The staff arranged the {word} by topic.",
        ]
    },
    "action": {
        "v": [
            "The editor asked the team to {word} the draft before noon.",
            "They will {word} the records after the meeting.",
        ]
    },
    "body": {
        "n": [
            "He injured his {word} while climbing the stairs.",
            "The doctor checked his {word} carefully.",
        ]
    },
    "sport": {
        "n": [
            "He swung the {word} and hit the ball.",
            "The coach handed him the {word} before practice.",
        ]
    },
    "legal": {
        "n": [
            "The new rule became the {word} for everyone in the office.",
            "The court issued a strict {word} yesterday.",
        ]
    },
    "food": {
        "n": [
            "The farmer stored the {word} in a dry basket.",
            "The chef used the {word} in the soup.",
        ]
    },
    "direction": {
        "adj": [
            "Turn {word} at the corner.",
            "The sign pointed {word} toward the gate.",
        ]
    },
    "default": {
        "n": [
            "The {word} was mentioned in the memo.",
            "They discussed the {word} during the meeting.",
        ],
        "v": [
            "They will {word} the draft before lunch.",
            "The manager asked them to {word} the report.",
        ],
        "adj": [
            "The report seemed {word} after review.",
            "The room felt {word} to the staff.",
        ],
        "adv": [
            "He spoke {word} during the briefing.",
            "She answered {word} during the interview.",
        ],
    },
}


@dataclass(frozen=True, slots=True)
class SenseRecord:
    word: str
    pos: str
    gloss: str
    display: str
    source_index: int


@dataclass(slots=True)
class WordSummary:
    word: str
    frequency: int
    senses: list[SenseRecord]


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _truncate_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(",;:.!?") + "..."


def _sanitize_text(text: str) -> str:
    return _normalize_whitespace(
        text.replace("\u2018", "'")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
    )


def _sanitize_lemma(raw: str) -> str | None:
    lemma = raw.lower().strip()
    if not lemma or "_" in lemma or "-" in lemma or "'" in lemma:
        return None
    if not WORD_RE.fullmatch(lemma):
        return None
    if lemma in STOP_WORDS:
        return None
    return lemma


def _normalize_pos(pos: str) -> str:
    return {"a": "adj", "s": "adj", "n": "n", "v": "v", "r": "adv"}.get(pos, pos)


def _sanitize_gloss(gloss: str) -> str:
    text = _normalize_whitespace(gloss)
    text = re.sub(r"^\([^)]*\)\s*", "", text)
    text = text.split(";", 1)[0]
    text = re.sub(r"\s*\([^)]*\)\s*$", "", text)
    text = text.split('"', 1)[0]
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = _truncate_words(text, 14)
    return text.strip(" ,;:.")


def _simplify_display(gloss: str, pos: str, word: str) -> str:
    text = _sanitize_gloss(gloss)
    if not text:
        return ""
    text = re.sub(r"^(?:a|an|the)\s+", "", text, flags=re.I)
    if pos == "v" and text.lower().startswith("to "):
        text = text[3:]
    lower = text.lower()
    for separator in (" that ", " or ", " when ", " where ", " which ", " who ", " whom "):
        if separator in lower and len(text.split()) > 4:
            text = text.split(separator, 1)[0]
            lower = text.lower()
            break
    text = _truncate_words(text, 8)
    while text and text.split()[-1].lower() in {"or", "and", "of", "to", "with", "for", "as", "in", "on", "by", "at", "from"}:
        text = " ".join(text.split()[:-1]).strip()
    text = text.strip(" ,;:.")
    if not text:
        return ""
    lowered = text.lower()
    if lowered == word or lowered.startswith(f"{word} ") or lowered.endswith(f" {word}"):
        return ""
    if _sense_keywords(lowered) & BAD_DISPLAY_TOKENS:
        return ""
    head = lowered.split()[0]
    if head in GENERIC_DISPLAY_HEADS and len(lowered.split()) == 1:
        return ""
    return text


def _dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _get(url: str, **kwargs: object) -> requests.Response:
    retries = 3
    backoff = 0.5
    for attempt in range(retries + 1):
        response = SESSION.get(url, **kwargs)
        if response.status_code in {429, 503} and attempt < retries:
            import time

            time.sleep(backoff * (2**attempt))
            continue
        response.raise_for_status()
        return response
    response.raise_for_status()
    return response


SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(pool_connections=24, pool_maxsize=24, max_retries=2))
SESSION.mount("http://", HTTPAdapter(pool_connections=24, pool_maxsize=24, max_retries=2))


def _download_frequency_map() -> dict[str, int]:
    response = _get(FREQUENCY_URL, timeout=60)
    frequency_map: dict[str, int] = {}
    for raw_line in response.text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            continue
        word = parts[0].lower().strip()
        if not WORD_RE.fullmatch(word):
            continue
        try:
            frequency = int(parts[1])
        except ValueError:
            continue
        frequency_map[word] = frequency
    return frequency_map


def _parse_wordnet_entry(
    line: str,
) -> tuple[str, str, list[str], list[tuple[str, str, str, str]], str] | None:
    if not re.match(r"^\d{8}\s", line):
        return None
    left, sep, gloss = line.partition("|")
    if not sep:
        return None
    tokens = left.split()
    if len(tokens) < 7:
        return None

    try:
        offset = tokens[0]
        pos = tokens[2]
        word_count = int(tokens[3], 16)
        index = 4
        words: list[str] = []
        for _ in range(word_count):
            if index + 1 >= len(tokens):
                return None
            words.append(tokens[index])
            index += 2
        if index >= len(tokens):
            return None
        pointer_count = int(tokens[index], 16)
        index += 1
        pointers: list[tuple[str, str, str, str]] = []
        for _ in range(pointer_count):
            if index + 3 >= len(tokens):
                return None
            pointers.append(
                (tokens[index], tokens[index + 1], tokens[index + 2], tokens[index + 3])
            )
            index += 4
    except (IndexError, ValueError):
        return None

    return offset, pos, words, pointers, _sanitize_gloss(gloss)


def _load_wordnet_source() -> bytes:
    response = _get(WORDNET_URL, timeout=120)
    return response.content


def _build_records(
    archive: zipfile.ZipFile,
    frequency_map: dict[str, int],
) -> dict[str, list[SenseRecord]]:
    files = [
        "oewn2025/data.adj",
        "oewn2025/data.verb",
        "oewn2025/data.noun",
        "oewn2025/data.adv",
    ]

    records_by_word: dict[str, list[SenseRecord]] = defaultdict(list)

    for file_rank, filename in enumerate(files):
        with archive.open(filename) as handle:
            for line_index, raw_line in enumerate(handle):
                line = raw_line.decode("utf-8", errors="replace").strip()
                parsed = _parse_wordnet_entry(line)
                if parsed is None:
                    continue
                offset, pos, words, _pointers, gloss = parsed
                norm_pos = _normalize_pos(pos)
                if norm_pos not in CONTENT_POS:
                    continue
                for raw_word in words:
                    word = _sanitize_lemma(raw_word)
                    if word is None or frequency_map.get(word, 0) <= 0:
                        continue
                    display = _simplify_display(gloss, norm_pos, word)
                    if not display:
                        continue
                    records_by_word[word].append(
                        SenseRecord(
                            word=word,
                            pos=norm_pos,
                            gloss=gloss,
                            display=display,
                            source_index=file_rank * 100000 + line_index,
                        )
                    )

    cleaned: dict[str, list[SenseRecord]] = {}
    for word, senses in records_by_word.items():
        senses = sorted(senses, key=lambda item: (item.source_index, len(item.display), item.display))
        unique: list[SenseRecord] = []
        seen_displays: set[str] = set()
        for sense in senses:
            key = sense.display.lower()
            if key in seen_displays:
                continue
            seen_displays.add(key)
            unique.append(sense)
        if len(unique) >= 4:
            cleaned[word] = unique
    return cleaned


def _choose_sense(word_senses: list[SenseRecord], difficulty: str) -> SenseRecord:
    index = DIFFICULTY_TO_SENSE_INDEX[difficulty]
    if index >= len(word_senses):
        index = len(word_senses) - 1
    return word_senses[index]


def _sense_keywords(text: str) -> set[str]:
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z]+", text)
        if len(token) > 1 and token.lower() not in STOP_WORDS
    }


def _sense_category(sense: SenseRecord) -> str:
    tokens = _sense_keywords(f"{sense.display} {sense.gloss}")
    if tokens & FINANCE_WORDS:
        return "finance"
    if tokens & RIVER_WORDS:
        return "river"
    if tokens & ANIMAL_WORDS:
        return "animal"
    if tokens & OBJECT_WORDS:
        return "object"
    if tokens & TIME_WORDS:
        return "time"
    if tokens & COMMUNICATION_WORDS:
        return "communication"
    if tokens & GROUP_WORDS:
        return "group"
    if tokens & BODY_WORDS:
        return "body"
    if tokens & SPORT_WORDS:
        return "sport"
    if tokens & LEGAL_WORDS:
        return "legal"
    if tokens & FOOD_WORDS:
        return "food"
    if tokens & QUALITY_WORDS:
        return "quality"
    if tokens & ACTION_WORDS:
        return "action"
    if tokens & {"left", "right", "north", "south", "east", "west"}:
        return "direction"
    if "light" in tokens or "bright" in tokens or "illumination" in tokens or "glow" in tokens:
        return "light"
    return "default"


def _article_for(phrase: str) -> str:
    first = phrase.strip().lower()[:1]
    return "an" if first in {"a", "e", "i", "o", "u"} else "a"


def _natural_sentence(word: str, sense: SenseRecord) -> str:
    category = _sense_category(sense)
    if category not in NATURAL_CATEGORIES:
        return _definition_sentence(word, sense)
    pool = NATURAL_TEMPLATES.get(category, {})
    templates = pool.get(sense.pos) or pool.get("any") or []
    if not templates:
        templates = NATURAL_TEMPLATES["default"].get(sense.pos, [])
    if not templates:
        return ""
    template = random.Random(f"{word}:{sense.display}:natural").choice(templates)
    sentence = _sanitize_text(template.format(word=word))
    return sentence if sentence.endswith(".") else f"{sentence}."


def _definition_sentence(word: str, sense: SenseRecord) -> str:
    article = _article_for(sense.display)
    if sense.pos == "n":
        sentence = f"The {word}, {article} {sense.display}, was mentioned in the memo."
    elif sense.pos == "v":
        answer = sense.display
        if answer.startswith("to "):
            answer = answer[3:]
        sentence = f"To {word} means to {answer}."
    else:
        sentence = f"The term {word} was used to mean {sense.display}."
    return _sanitize_text(sentence)


def _restatement_sentence(word: str, sense: SenseRecord) -> str:
    article = _article_for(sense.display)
    if sense.pos == "n":
        sentence = f"The {word}, or {article} {sense.display}, was mentioned in the memo."
    elif sense.pos == "v":
        answer = sense.display
        if answer.startswith("to "):
            answer = answer[3:]
        sentence = f"The team needed to {word}, or to {answer}, before noon."
    else:
        sentence = f"The term {word} was restated as {sense.display}."
    return _sanitize_text(sentence)


def _contrast_sentence(word: str, sense: SenseRecord, other: SenseRecord) -> str:
    if sense.pos == "n":
        sentence = f"It was not the {other.display}, but the {sense.display}, that fit the sentence."
    elif sense.pos == "v":
        answer = sense.display[3:] if sense.display.startswith("to ") else sense.display
        other_phrase = other.display[3:] if other.display.startswith("to ") else other.display
        sentence = f"It was not to {other_phrase}, but to {answer}, that fit the sentence."
    else:
        sentence = f"It was not {other.display}, but {sense.display}, that fit the sentence."
    return _sanitize_text(sentence)


def _context_sentence(word: str, sense: SenseRecord) -> str:
    sentence = _natural_sentence(word, sense)
    if sentence:
        return sentence
    return _definition_sentence(word, sense)


def _build_sentence(
    word: str,
    sense: SenseRecord,
    other: SenseRecord,
    variant: str,
) -> str:
    if variant in {"definition", "direct"}:
        return _definition_sentence(word, sense)
    if variant == "restatement":
        return _restatement_sentence(word, sense)
    if variant == "contrast":
        return _contrast_sentence(word, sense, other)
    return _context_sentence(word, sense)


def _build_question_text(word: str, sentence: str, variant: str) -> str:
    template = random.Random(f"{word}:{sentence}:{variant}").choice(QUESTION_TEMPLATES[variant])
    return _sanitize_text(template({"word": word, "sentence": sentence}))


def _build_choices(
    senses: list[SenseRecord],
    correct_index: int,
    rng: random.Random,
) -> tuple[list[str], str]:
    choices = [sense.display for sense in senses[:4]]
    answer = senses[correct_index].display
    if answer not in choices:
        raise ValueError("answer is missing from the generated choice set")
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError("choices are not four unique senses")
    rng.shuffle(choices)
    if answer not in choices:
        raise ValueError("answer dropped out of the shuffled choices")
    return choices, answer


def _select_words(summaries: list[WordSummary]) -> list[tuple[str, WordSummary]]:
    summaries = sorted(summaries, key=lambda item: (-item.frequency, len(item.word), item.word))
    if len(summaries) < 600:
        raise ValueError(f"expected at least 600 multi-meaning candidates, got {len(summaries)}")

    band_size = len(summaries) // 4
    bands = [
        summaries[:band_size],
        summaries[band_size : band_size * 2],
        summaries[band_size * 2 : band_size * 3],
        summaries[band_size * 3 :],
    ]

    selected: list[tuple[str, WordSummary]] = []
    for difficulty, band in zip(DIFFICULTY_ORDER, bands):
        if len(band) < TARGET_COUNTS[difficulty]:
            raise ValueError(
                f"not enough {difficulty.lower()} candidates: needed {TARGET_COUNTS[difficulty]}, got {len(band)}"
            )
        chosen = band[: TARGET_COUNTS[difficulty]]
        if len(chosen) != TARGET_COUNTS[difficulty]:
            raise ValueError(
                f"expected {TARGET_COUNTS[difficulty]} {difficulty} items, got {len(chosen)}"
            )
        selected.extend((difficulty, summary) for summary in chosen)
    return selected


def _validate_bank(questions: list[dict[str, object]], selected: list[tuple[str, WordSummary]]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    target_words = [summary.word for _difficulty, summary in selected]
    if len(target_words) != len(set(target_words)):
        raise ValueError("target words are not unique")

    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise ValueError(f"unexpected difficulty distribution: {dict(counts)}")

    seen_questions: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        choices = list(question["choices"])  # type: ignore[assignment]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")
        question_key = (
            str(question["question"]),
            tuple(sorted(str(choice) for choice in choices)),
        )
        if question_key in seen_questions:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_questions.add(question_key)


def main() -> int:
    frequency_map = _download_frequency_map()
    archive_bytes = _load_wordnet_source()
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    records_by_word = _build_records(archive, frequency_map)

    summaries: list[WordSummary] = []
    for word, senses in records_by_word.items():
        frequency = frequency_map.get(word, 0)
        if frequency <= 0 or len(word) < 3 or len(senses) < 4:
            continue
        summaries.append(
            WordSummary(
                word=word,
                frequency=frequency,
                senses=senses,
            )
        )

    selected = _select_words(summaries)

    questions: list[dict[str, object]] = []
    for index, (difficulty, summary) in enumerate(selected, start=1):
        rng = random.Random(f"{summary.word}:{difficulty}:{index}")
        senses = summary.senses[:4]
        correct_index = DIFFICULTY_TO_SENSE_INDEX[difficulty]
        if correct_index >= len(senses):
            correct_index = len(senses) - 1

        # Use a sense that is different from the answer sense when making
        # a contrast sentence. This keeps the clue meaningful.
        other_candidates = [sense for i, sense in enumerate(senses) if i != correct_index]
        other = other_candidates[0] if other_candidates else senses[0]

        variant = rng.choice(QUESTION_WEIGHTS[difficulty])
        sentence = _build_sentence(summary.word, senses[correct_index], other, variant)
        question = _build_question_text(summary.word, sentence, variant)
        choices, answer = _build_choices(senses, correct_index, rng)

        explanation: str
        if variant == "definition":
            explanation = f'The direct explanation in the sentence points to "{answer}".'
        elif variant == "restatement":
            explanation = f'The restatement clue points to "{answer}" as the correct sense.'
        elif variant == "contrast":
            explanation = f'The contrast points away from "{other.display}" and toward "{answer}".'
        else:
            explanation = f'The surrounding context shows that "{summary.word}" means "{answer}".'

        tags = [
            senses[correct_index].pos,
            "multiple-meaning",
            "word-meaning",
            difficulty.lower(),
            variant,
        ]
        tags.append(f"senses-{len(senses[:4])}")

        questions.append(
            {
                "id": index,
                "subtest": SUBTEST,
                "module": MODULE,
                "subtopic": SUBTOPIC,
                "difficulty": difficulty,
                "question": question,
                "choices": choices,
                "answer": answer,
                "explanation": explanation,
                "tags": _dedupe_preserve_order(tags),
                "category": CATEGORY,
                "language": LANGUAGE,
            }
        )

    _validate_bank(questions, selected)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
