"""Generate the Verbal Ability / Word Meanings / Suffixes question bank.

The bank is built from a frequency-backed suffix ladder. Each selected word
appears in four question styles so the final bank has a balanced
150 / 150 / 150 / 150 difficulty split while keeping the vocabulary pool
focused on clear, teachable suffixes.

Usage:
    python scripts/generate_suffixes_bank.py
"""

from __future__ import annotations

import json
import random
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "word-meaning"
    / "suffixes"
    / "questions.json"
)

FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Suffixes"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

WORD_RE = re.compile(r"^[a-z]+$")
TARGET_WORDS = 150
TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

FAMILY_INFO: dict[str, dict[str, str]] = {
    "less": {
        "suffix_form": "-less",
        "meaning": "without; lacking",
        "part_of_speech": "adjective",
    },
    "ful": {
        "suffix_form": "-ful",
        "meaning": "full of; having",
        "part_of_speech": "adjective",
    },
    "ness": {
        "suffix_form": "-ness",
        "meaning": "state; quality; condition",
        "part_of_speech": "noun",
    },
    "ment": {
        "suffix_form": "-ment",
        "meaning": "act; process; result",
        "part_of_speech": "noun",
    },
    "ship": {
        "suffix_form": "-ship",
        "meaning": "state; condition; relationship",
        "part_of_speech": "noun",
    },
    "hood": {
        "suffix_form": "-hood",
        "meaning": "state; condition; period",
        "part_of_speech": "noun",
    },
    "dom": {
        "suffix_form": "-dom",
        "meaning": "state; rank; realm",
        "part_of_speech": "noun",
    },
    "able": {
        "suffix_form": "-able",
        "meaning": "capable of; fit to be",
        "part_of_speech": "adjective",
    },
    "ible": {
        "suffix_form": "-ible",
        "meaning": "capable of; fit to be",
        "part_of_speech": "adjective",
    },
    "ify": {
        "suffix_form": "-ify",
        "meaning": "make; cause to become",
        "part_of_speech": "verb",
    },
}

# Keep the pool focused on transparent suffix examples.
GLOBAL_BLACKLIST = {
    "unless",
    "nevertheless",
    "moment",
    "comment",
    "cement",
    "document",
    "parliament",
    "monument",
    "torment",
    "random",
    "seldom",
    "condom",
    "worship",
    "vegetable",
    "business",
    "witness",
    "eyewitness",
    "baroness",
    "harness",
    "spaceship",
    "likelihood",
    "livelihood",
    "stable",
    "constable",
    "howard",
    "edward",
    "prize",
    "award",
}

FAMILY_BLACKLIST: dict[str, set[str]] = {
    "less": set(),
    "ful": set(),
    "ness": {"business", "witness", "eyewitness", "baroness", "harness"},
    "ment": {
        "moment",
        "comment",
        "cement",
        "document",
        "parliament",
        "monument",
        "torment",
    },
    "ship": {"worship"},
    "hood": set(),
    "dom": {"random", "seldom", "condom", "sodom"},
    "able": {"vegetable", "stable", "constable"},
    "ible": set(),
    "ify": set(),
}

FAMILY_QUOTAS = {
    "less": 18,
    "ful": 18,
    "ness": 22,
    "ment": 25,
    "ship": 12,
    "hood": 8,
    "dom": 6,
    "able": 25,
    "ible": 10,
    "ify": 6,
}

QUESTION_KIND_ORDER = ("suffix_id", "suffix_meaning", "part_of_speech", "family_match")


@dataclass(frozen=True)
class WordRecord:
    word: str
    family_key: str
    suffix_form: str
    suffix_meaning: str
    part_of_speech: str
    frequency: int


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


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


def _detect_family(word: str) -> tuple[str, str] | None:
    matches: list[tuple[int, str, str]] = []
    for family_key, info in FAMILY_INFO.items():
        suffix_form = info["suffix_form"]
        suffix = suffix_form.removeprefix("-")
        if len(word) > len(suffix) + 1 and word.endswith(suffix):
            matches.append((len(suffix), family_key, suffix_form))
    if not matches:
        return None
    _, family_key, suffix_form = sorted(matches, key=lambda item: (-item[0], item[1]))[0]
    return family_key, suffix_form


def _collect_candidates(frequency_map: dict[str, int]) -> list[WordRecord]:
    records: list[WordRecord] = []
    for word, frequency in sorted(
        frequency_map.items(), key=lambda item: (-item[1], len(item[0]), item[0])
    ):
        if word in GLOBAL_BLACKLIST:
            continue
        detected = _detect_family(word)
        if detected is None:
            continue
        family_key, suffix_form = detected
        if word in FAMILY_BLACKLIST.get(family_key, set()):
            continue
        info = FAMILY_INFO[family_key]
        records.append(
            WordRecord(
                word=word,
                family_key=family_key,
                suffix_form=suffix_form,
                suffix_meaning=info["meaning"],
                part_of_speech=info["part_of_speech"],
                frequency=frequency,
            )
        )
    return records


def _select_records(records: list[WordRecord]) -> list[WordRecord]:
    by_family: dict[str, list[WordRecord]] = defaultdict(list)
    for record in records:
        by_family[record.family_key].append(record)

    selected: list[WordRecord] = []
    for family_key, quota in FAMILY_QUOTAS.items():
        family_records = by_family.get(family_key, [])
        if len(family_records) < quota:
            raise RuntimeError(
                f"not enough {family_key} candidates: need {quota}, got {len(family_records)}"
            )
        family_records = sorted(
            family_records, key=lambda item: (-item.frequency, len(item.word), item.word)
        )
        selected.extend(family_records[:quota])

    if len(selected) != TARGET_WORDS:
        raise RuntimeError(f"expected {TARGET_WORDS} selected words, got {len(selected)}")

    selected = sorted(selected, key=lambda item: (-item.frequency, len(item.word), item.word))
    words = [record.word for record in selected]
    if len(words) != len(set(words)):
        raise RuntimeError("selected words are not unique")
    return selected


def _build_suffix_pool(records: list[WordRecord]) -> list[str]:
    return _dedupe([record.suffix_form for record in records])


def _build_meaning_pool(records: list[WordRecord]) -> list[str]:
    return _dedupe([record.suffix_meaning for record in records])


def _build_pos_pool(records: list[WordRecord]) -> list[str]:
    base_pool = ["noun", "adjective", "verb", "adverb"]
    selected_pos = {record.part_of_speech for record in records}
    pool = [item for item in base_pool if item in selected_pos or item == "adverb"]
    return _dedupe(pool)


def _build_word_pool(records: list[WordRecord]) -> list[str]:
    return _dedupe([record.word for record in records])


def _choice_seed(record: WordRecord, difficulty: str) -> str:
    return f"{record.word}:{record.family_key}:{difficulty}"


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


def _build_family_match_answer(
    record: WordRecord,
    family_groups: dict[str, list[str]],
    rng: random.Random,
) -> str:
    peers = [word for word in family_groups[record.family_key] if word != record.word]
    if not peers:
        raise RuntimeError(f"no family peers available for {record.word}")
    return rng.choice(peers)


def _build_family_match_choices(
    record: WordRecord,
    family_groups: dict[str, list[str]],
    word_pool: list[str],
    rng: random.Random,
) -> tuple[str, list[str]]:
    answer = _build_family_match_answer(record, family_groups, rng)
    distractors = [word for word in word_pool if word != answer and word not in family_groups[record.family_key]]
    rng.shuffle(distractors)
    choices = [answer, *distractors[:3]]
    if len(choices) < 4:
        raise RuntimeError(f"not enough family-match distractors for {record.word!r}")
    rng.shuffle(choices)
    if len(set(choices)) != 4:
        raise RuntimeError(f"duplicate family-match choices for {record.word!r}")
    return answer, choices


def _build_question(
    record: WordRecord,
    *,
    difficulty: str,
    family_groups: dict[str, list[str]],
    suffix_pool: list[str],
    meaning_pool: list[str],
    pos_pool: list[str],
    word_pool: list[str],
) -> dict[str, object]:
    rng = random.Random(_choice_seed(record, difficulty))

    if difficulty == "Easy":
        templates = [
            f'Which suffix appears at the end of "{record.word}"?',
            f'What suffix is used in "{record.word}"?',
            f'Identify the suffix in "{record.word}".',
        ]
        question = rng.choice(templates)
        answer = record.suffix_form
        choices = _build_choices(answer, suffix_pool, rng)
        explanation = (
            f'The word ends with {record.suffix_form}, which usually means '
            f'{record.suffix_meaning}.'
        )
        tags = ["suffix", record.family_key, "suffix_id", "word-meaning", "cse", "suffix-form"]
    elif difficulty == "Medium":
        templates = [
            f'What does the suffix in "{record.word}" usually mean?',
            f'Which meaning best fits the suffix in "{record.word}"?',
            f'Pick the meaning of the suffix in "{record.word}".',
        ]
        question = rng.choice(templates)
        answer = record.suffix_meaning
        choices = _build_choices(answer, meaning_pool, rng)
        explanation = f'The suffix {record.suffix_form} usually means {record.suffix_meaning}.'
        tags = ["suffix", record.family_key, "suffix_meaning", "word-meaning", "cse"]
    elif difficulty == "Hard":
        templates = [
            f'What kind of word does the suffix in "{record.word}" usually help create?',
            f'Which part of speech is usually formed by the suffix in "{record.word}"?',
            f'The suffix in "{record.word}" most often helps make what kind of word?',
        ]
        question = rng.choice(templates)
        answer = record.part_of_speech
        choices = _build_choices(answer, pos_pool, rng)
        explanation = f'The suffix {record.suffix_form} usually helps form a {record.part_of_speech}.'
        tags = ["suffix", record.family_key, "part-of-speech", "word-meaning", "cse"]
    else:
        templates = [
            f'Which word below uses the same suffix family as "{record.word}"?',
            f'Which option is another example of the suffix family in "{record.word}"?',
            f'Which word below matches the same suffix pattern as "{record.word}"?',
        ]
        question = rng.choice(templates)
        answer, choices = _build_family_match_choices(
            record,
            family_groups,
            word_pool,
            rng,
        )
        explanation = (
            f'"{record.word}" and "{answer}" both use the {record.suffix_form} family, '
            f'which usually means {record.suffix_meaning}.'
        )
        tags = ["suffix", record.family_key, "suffix_match", "word-meaning", "cse"]

    if len(choices) != 4:
        raise RuntimeError(f"question {record.word!r} does not have 4 choices")
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
    family_groups: dict[str, list[str]] = defaultdict(list)
    for record in records:
        family_groups[record.family_key].append(record.word)

    suffix_pool = _build_suffix_pool(records)
    meaning_pool = _build_meaning_pool(records)
    pos_pool = _build_pos_pool(records)
    word_pool = _build_word_pool(records)

    questions: list[dict[str, object]] = []
    question_id = 1
    for difficulty in DIFFICULTY_ORDER:
        for record in records:
            question = _build_question(
                record,
                difficulty=difficulty,
                family_groups=family_groups,
                suffix_pool=suffix_pool,
                meaning_pool=meaning_pool,
                pos_pool=pos_pool,
                word_pool=word_pool,
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

    selected_words = [record.word for record in records]
    if len(selected_words) != len(set(selected_words)):
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
    candidates = _collect_candidates(frequency_map)
    records = _select_records(candidates)

    family_summary = Counter(record.family_key for record in records)
    print("Selected suffix words:")
    for family_key in FAMILY_QUOTAS:
        words = [record.word for record in records if record.family_key == family_key]
        preview = ", ".join(words[:8])
        print(f"  {family_key:>5} ({len(words):>2}): {preview}")

    questions = _build_bank(records)
    _validate_bank(questions, records)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    print(f"Selected {len(records)} words across {len(family_summary)} suffix families")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
