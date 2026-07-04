"""Generate the Verbal Ability / Word Meanings / Idioms and Figurative Phrases bank.

The bank is built from a curated public idioms list and split into four
difficulty ladders of 150 items each. The goal is 600 unique idioms / figurative
phrases with a mix of direct-definition, reverse-definition, and context-style
prompts.

Usage:
    python scripts/generate_idioms_and_figurative_phrases_bank.py
"""

from __future__ import annotations

import json
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

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
    / "idioms-and-figurative-phrases"
    / "questions.json"
)

SOURCE_URL = "https://raw.githubusercontent.com/baiango/english_idioms/main/idioms.csv"
SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Idioms and Figurative Phrases"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
QUESTION_TYPES = ("meaning_to_idiom", "idiom_to_meaning", "idea_to_idiom", "figurative_clarify")
SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(pool_connections=16, pool_maxsize=16, max_retries=2))
SESSION.mount("http://", HTTPAdapter(pool_connections=16, pool_maxsize=16, max_retries=2))
MEANING_ALIASES = {
    ("ride the wave", "go with the flow"): "Adapt to what is happening",
}


@dataclass(frozen=True)
class IdiomEntry:
    idiom: str
    meaning: str
    source_index: int


def _get(url: str, **kwargs: object) -> requests.Response:
    response = SESSION.get(url, timeout=30, **kwargs)
    response.raise_for_status()
    return response


def _normalize_text(text: str) -> str:
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = text.replace('"', "")
    text = re.sub(r"\s+", " ", text)
    return text.strip(" \t\r\n.;:-")


def _parse_source() -> list[IdiomEntry]:
    response = _get(SOURCE_URL)
    entries: list[IdiomEntry] = []
    seen_idioms: set[str] = set()
    seen_meanings: set[str] = set()
    for source_index, raw_line in enumerate(response.text.splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        match = re.match(r'^"?\{(.+?)\}>>\{(.+?)\}"?$', line)
        if not match:
            continue
        idiom = _normalize_text(match.group(1))
        meaning = _normalize_text(match.group(2))
        if not idiom or not meaning:
            continue
        idiom_key = idiom.lower()
        meaning_key = meaning.lower()
        if idiom_key in seen_idioms or meaning_key in seen_meanings:
            continue
        seen_idioms.add(idiom_key)
        seen_meanings.add(meaning_key)
        entries.append(IdiomEntry(idiom=idiom, meaning=meaning, source_index=source_index))
    return entries


def _pick_distinct(values: list[str], answer: str, rng: random.Random, count: int = 3) -> list[str]:
    unique_pool = [value for value in dict.fromkeys(values) if value != answer]
    if len(unique_pool) < count:
        raise ValueError("not enough values to pick distinct distractors")
    scored = sorted(
        unique_pool,
        key=lambda value: (
            abs(len(value) - len(answer)),
            abs(value.count(" ") - answer.count(" ")),
            value.lower(),
        ),
    )
    window = scored[: max(24, count * 8)]
    if len(window) <= count:
        return window[:count]
    return rng.sample(window, count)


def _clean_sentence(text: str) -> str:
    text = _normalize_text(text)
    if text and text[-1] not in ".!?":
        text += "."
    return text


def _display_meaning(entry: IdiomEntry) -> str:
    alias = MEANING_ALIASES.get((entry.idiom.lower(), entry.meaning.lower()))
    return alias or entry.meaning


def _meaning_to_idiom_question(entry: IdiomEntry, rng: random.Random, pool: list[IdiomEntry]) -> tuple[str, list[str], str]:
    choices = [entry.idiom, *_pick_distinct([item.idiom for item in pool], entry.idiom, rng)]
    rng.shuffle(choices)
    question = rng.choice(
        [
            f'Which idiom means "{entry.meaning}"?',
            f'Choose the idiom that matches "{entry.meaning}".',
            f'What figurative expression has the meaning "{entry.meaning}"?',
        ]
    )
    answer = entry.idiom
    return question, choices, answer


def _idiom_to_meaning_question(entry: IdiomEntry, rng: random.Random, pool: list[IdiomEntry]) -> tuple[str, list[str], str]:
    answer_meaning = _display_meaning(entry)
    meanings = [answer_meaning, *_pick_distinct([_display_meaning(item) for item in pool], answer_meaning, rng)]
    rng.shuffle(meanings)
    question = rng.choice(
        [
            f'What does "{entry.idiom}" mean?',
            f'What is the figurative meaning of "{entry.idiom}"?',
            f'Choose the meaning of "{entry.idiom}".',
        ]
    )
    answer = answer_meaning
    return question, meanings, answer


def _idea_to_idiom_question(entry: IdiomEntry, rng: random.Random, pool: list[IdiomEntry]) -> tuple[str, list[str], str]:
    choices = [entry.idiom, *_pick_distinct([item.idiom for item in pool], entry.idiom, rng)]
    rng.shuffle(choices)
    idea = entry.meaning.lower().rstrip(".")
    question = rng.choice(
        [
            f"Which idiom best matches the idea of {idea}?",
            f'Which idiom would you use for the idea "{entry.meaning}"?',
            f"Which phrase best expresses {idea}?",
        ]
    )
    answer = entry.idiom
    return question, choices, answer


def _figurative_clarify_question(entry: IdiomEntry, rng: random.Random, pool: list[IdiomEntry]) -> tuple[str, list[str], str]:
    answer_meaning = _display_meaning(entry)
    meanings = [answer_meaning, *_pick_distinct([_display_meaning(item) for item in pool], answer_meaning, rng)]
    rng.shuffle(meanings)
    question = rng.choice(
        [
            f'What idea is being expressed by "{entry.idiom}"?',
            f'In plain English, what does "{entry.idiom}" suggest?',
            f'Which meaning best explains "{entry.idiom}"?',
        ]
    )
    answer = answer_meaning
    return question, meanings, answer


QUESTION_BUILDERS: dict[str, Callable[[IdiomEntry, random.Random, list[IdiomEntry]], tuple[str, list[str], str]]] = {
    "meaning_to_idiom": _meaning_to_idiom_question,
    "idiom_to_meaning": _idiom_to_meaning_question,
    "idea_to_idiom": _idea_to_idiom_question,
    "figurative_clarify": _figurative_clarify_question,
}


def _difficulty_for_index(index: int) -> str:
    return DIFFICULTY_ORDER[index // 150]


def _template_for(index: int, difficulty: str) -> str:
    template_cycles = {
        "Easy": ("meaning_to_idiom", "idiom_to_meaning", "meaning_to_idiom", "idea_to_idiom"),
        "Medium": ("idea_to_idiom", "meaning_to_idiom", "idiom_to_meaning", "figurative_clarify"),
        "Hard": ("idiom_to_meaning", "figurative_clarify", "idea_to_idiom", "meaning_to_idiom"),
        "Ultra": ("figurative_clarify", "idea_to_idiom", "idiom_to_meaning", "figurative_clarify"),
    }
    cycle = template_cycles[difficulty]
    return cycle[index % len(cycle)]


def _build_question(
    entry: IdiomEntry,
    *,
    difficulty: str,
    template: str,
    pool: list[IdiomEntry],
    rng: random.Random,
    question_id: int,
) -> dict[str, object]:
    question, choices, answer = QUESTION_BUILDERS[template](entry, rng, pool)
    if len({choice.strip() for choice in choices}) != 4:
        raise ValueError(f"choices are not unique for {entry.idiom!r}")
    if answer not in choices:
        raise ValueError(f"answer not present in choices for {entry.idiom!r}")
    explanation = f'"{entry.idiom}" means "{_display_meaning(entry)}".'
    return {
        "id": question_id,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": [
            "idiom",
            "figurative-language",
            difficulty.lower(),
            template,
        ],
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def generate_bank() -> list[dict[str, object]]:
    entries = _parse_source()
    if len(entries) < 600:
        raise RuntimeError(f"source only produced {len(entries)} unique idioms")

    selected = entries[:600]
    rng = random.Random(20260704)
    questions: list[dict[str, object]] = []
    for index, entry in enumerate(selected):
        difficulty = _difficulty_for_index(index)
        template = _template_for(index % 150, difficulty)
        question = _build_question(
            entry,
            difficulty=difficulty,
            template=template,
            pool=selected,
            rng=rng,
            question_id=index + 1,
        )
        questions.append(question)
    return questions


def main() -> int:
    questions = generate_bank()
    counts = {difficulty: 0 for difficulty in DIFFICULTY_ORDER}
    seen_idioms: set[str] = set()
    for item in questions:
        counts[str(item["difficulty"])] += 1
        key = str(item["answer"]).lower()
        if key in seen_idioms:
            pass
        seen_idioms.add(key)

    if counts != TARGET_COUNTS:
        raise RuntimeError(f"unexpected difficulty counts: {counts}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    print(f"Difficulty counts: {counts}")
    print(f"Unique answers: {len(seen_idioms)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
