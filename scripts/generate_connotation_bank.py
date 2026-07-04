"""Generate the Verbal Ability / Word Meanings / Connotation question bank.

This generator uses the AFINN English sentiment lexicon as a connotation
signal, then builds a 600-item bank with unique answer words across four
difficulty bands:

- Easy: strong positive/negative connotation
- Medium: clear but less extreme connotation
- Hard: moderate connotation
- Ultra: subtle / lightly loaded connotation

The prompts are scenario-based and designed to feel like CSE word-meaning
items rather than raw sentiment-label questions.

Usage:
    python scripts/generate_connotation_bank.py
"""

from __future__ import annotations

import json
import random
import re
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
    / "connotation"
    / "questions.json"
)

SOURCE_URL = "https://raw.githubusercontent.com/fnielsen/afinn/master/afinn/data/AFINN-en-165.txt"
SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Connotation"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(pool_connections=16, pool_maxsize=16, max_retries=2))
SESSION.mount("http://", HTTPAdapter(pool_connections=16, pool_maxsize=16, max_retries=2))

WORD_RE = re.compile(r"^[a-z][a-z'\-]*$")
MIN_WORD_LENGTH = 4

BLACKLIST = {
    "apeshit",
    "ass",
    "assfucking",
    "asshole",
    "badass",
    "bastard",
    "bastards",
    "bitch",
    "bitches",
    "bullshit",
    "cunt",
    "damn",
    "damned",
    "damnit",
    "dipshit",
    "dumbass",
    "fuck",
    "fucked",
    "fucker",
    "fuckers",
    "fuckface",
    "fuckhead",
    "fuckin",
    "fucking",
    "fucktard",
    "goddamn",
    "hell",
    "haha",
    "hahaha",
    "hahahah",
    "jackass",
    "jackasses",
    "lawl",
    "lmao",
    "lmfao",
    "lol",
    "lolol",
    "lololol",
    "lolololol",
    "lool",
    "motherfucker",
    "motherfucking",
    "roflmao",
    "rotfl",
    "rotflmfao",
    "rotflol",
    "shit",
    "shithead",
    "shitty",
    "slut",
    "son-of-a-bitch",
    "eery",
    "whore",
}


@dataclass(frozen=True)
class TermEntry:
    word: str
    score: int
    source_index: int

    @property
    def polarity(self) -> str:
        return "positive" if self.score > 0 else "negative"


def _get(url: str, **kwargs: object) -> requests.Response:
    response = SESSION.get(url, timeout=30, **kwargs)
    response.raise_for_status()
    return response


def _normalize_word(word: str) -> str:
    return re.sub(r"\s+", " ", word.strip().lower())


def _parse_source() -> list[TermEntry]:
    response = _get(SOURCE_URL)
    entries: list[TermEntry] = []
    seen: set[str] = set()
    for source_index, raw_line in enumerate(response.text.splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        try:
            word, raw_score = line.rsplit("\t", 1)
        except ValueError:
            continue
        word = _normalize_word(word)
        if not WORD_RE.fullmatch(word):
            continue
        if len(word) < MIN_WORD_LENGTH:
            continue
        if word in seen or word in BLACKLIST:
            continue
        try:
            score = int(raw_score)
        except ValueError:
            continue
        if score == 0:
            continue
        seen.add(word)
        entries.append(TermEntry(word=word, score=score, source_index=source_index))
    return entries


def _sort_candidates(entries: Iterable[TermEntry]) -> list[TermEntry]:
    return sorted(
        entries,
        key=lambda entry: (
            _inflection_penalty(entry.word),
            len(entry.word),
            entry.word,
            entry.source_index,
        ),
    )


def _inflection_penalty(word: str) -> int:
    if word.endswith("ing") or word.endswith("ed"):
        return 3
    if word.endswith("es") and len(word) > 4:
        return 2
    if word.endswith("s") and len(word) > 4:
        return 1
    return 0


def _take_first(
    entries: list[TermEntry],
    count: int,
    *,
    used_words: set[str],
) -> list[TermEntry]:
    chosen: list[TermEntry] = []
    for entry in entries:
        if entry.word in used_words:
            continue
        used_words.add(entry.word)
        chosen.append(entry)
        if len(chosen) >= count:
            break
    if len(chosen) != count:
        raise RuntimeError(f"unable to select {count} unique terms from source")
    return chosen


def _ordered_group(entries: list[TermEntry], score: int) -> list[TermEntry]:
    return _sort_candidates(entry for entry in entries if entry.score == score)


def _select_buckets(entries: list[TermEntry]) -> list[tuple[str, TermEntry]]:
    used: set[str] = set()

    score_groups = {score: _ordered_group(entries, score) for score in range(-5, 6) if score != 0}

    easy_positive = _take_first(
        _sort_candidates(
            [
                *score_groups[5],
                *score_groups[4],
                *score_groups[3],
            ]
        ),
        75,
        used_words=used,
    )
    easy_negative = _take_first(
        _sort_candidates(
            [
                *score_groups[-5],
                *score_groups[-4],
                *score_groups[-3],
            ]
        ),
        75,
        used_words=used,
    )

    medium_positive = _take_first(score_groups[3], 75, used_words=used)
    medium_negative = _take_first(score_groups[-3], 75, used_words=used)

    hard_positive = _take_first(score_groups[2], 75, used_words=used)
    hard_negative = _take_first(score_groups[-2], 75, used_words=used)

    ultra_positive = _take_first(score_groups[1], 75, used_words=used)
    ultra_negative = _take_first(score_groups[-1], 75, used_words=used)

    ordered: list[tuple[str, TermEntry]] = []
    for pair in zip(easy_positive, easy_negative):
        ordered.append(("Easy", pair[0]))
        ordered.append(("Easy", pair[1]))
    for pair in zip(medium_positive, medium_negative):
        ordered.append(("Medium", pair[0]))
        ordered.append(("Medium", pair[1]))
    for pair in zip(hard_positive, hard_negative):
        ordered.append(("Hard", pair[0]))
        ordered.append(("Hard", pair[1]))
    for pair in zip(ultra_positive, ultra_negative):
        ordered.append(("Ultra", pair[0]))
        ordered.append(("Ultra", pair[1]))

    if len(ordered) != 600:
        raise RuntimeError(f"unexpected selected-item count: {len(ordered)}")
    return ordered


def _scenario_phrase(bucket: str, polarity: str, index: int) -> str:
    if bucket == "Ultra":
        speakers = [
            "A reporter",
            "An editor",
            "A clerk",
            "An officer",
            "A principal",
            "A supervisor",
            "A writer",
            "A coordinator",
        ]
        documents = [
            "news report",
            "memo",
            "notice",
            "briefing",
            "summary",
            "update",
            "statement",
            "report",
        ]
        topics = [
            "a policy change",
            "a meeting update",
            "a school notice",
            "a project status report",
            "a public announcement",
            "a service reminder",
            "a work summary",
            "a factual briefing",
        ]
    elif bucket == "Easy" and polarity == "positive":
        speakers = [
            "A teacher",
            "A coach",
            "A parent",
            "A friend",
            "A mentor",
            "A nurse",
            "A manager",
            "A volunteer",
        ]
        documents = [
            "compliment",
            "thank-you note",
            "praise letter",
            "encouragement message",
            "appreciation note",
            "friendly reply",
            "kind review",
            "celebration message",
        ]
        topics = [
            "a student's effort",
            "a helpful act",
            "a team victory",
            "a kind gesture",
            "a thoughtful reply",
            "a successful project",
            "a generous donation",
            "good news",
        ]
    elif bucket == "Easy" and polarity == "negative":
        speakers = [
            "A critic",
            "A supervisor",
            "A buyer",
            "A customer",
            "An inspector",
            "A reviewer",
            "A neighbor",
            "A driver",
        ]
        documents = [
            "complaint",
            "warning",
            "critical review",
            "incident report",
            "correction note",
            "feedback memo",
            "caution message",
            "concern letter",
        ]
        topics = [
            "a poor result",
            "a bad habit",
            "a safety issue",
            "a weak performance",
            "a messy room",
            "a delayed task",
            "a disappointing answer",
            "a costly mistake",
        ]
    elif polarity == "positive":
        speakers = [
            "A manager",
            "An editor",
            "A counselor",
            "A teacher",
            "A coach",
            "A supervisor",
            "A project lead",
            "A team captain",
        ]
        documents = [
            "memo",
            "report",
            "reply",
            "review",
            "note",
            "update",
            "message",
            "briefing",
        ]
        topics = [
            "a thoughtful act",
            "a helpful plan",
            "a kind gesture",
            "a good result",
            "a successful effort",
            "a respectful comment",
            "a smart choice",
            "a positive outcome",
        ]
    else:
        speakers = [
            "A manager",
            "An editor",
            "An inspector",
            "A reviewer",
            "A supervisor",
            "A reporter",
            "A policy writer",
            "A team lead",
        ]
        documents = [
            "memo",
            "report",
            "reply",
            "review",
            "note",
            "update",
            "message",
            "briefing",
        ]
        topics = [
            "a weak result",
            "a risky choice",
            "a careless mistake",
            "a poor habit",
            "a serious problem",
            "a disappointing outcome",
            "a rough draft",
            "a tense situation",
        ]

    speaker = speakers[index % len(speakers)]
    document = documents[(index // len(speakers)) % len(documents)]
    topic = topics[(index // (len(speakers) * len(documents))) % len(topics)]
    return f"{speaker} writing a {document} about {topic}"


def _pick_from_pool(
    pool: list[TermEntry],
    rng: random.Random,
    *,
    exclude: set[str],
    limit: int = 12,
) -> str:
    candidates = [entry.word for entry in pool if entry.word not in exclude]
    if not candidates:
        raise RuntimeError("no distractor candidates available")
    window = candidates[: max(4, min(limit, len(candidates)))]
    return rng.choice(window)


def _build_choices(
    entry: TermEntry,
    *,
    bucket: str,
    rng: random.Random,
    pools: dict[int, list[TermEntry]],
) -> list[str]:
    exclude = {entry.word}
    if bucket == "Easy":
        if entry.score > 0:
            score_plan = [2, 1, -1]
        else:
            score_plan = [-2, -1, 1]
    elif bucket == "Medium":
        if entry.score > 0:
            score_plan = [2, 1, -1]
        else:
            score_plan = [-2, -1, 1]
    elif bucket == "Hard":
        if entry.score > 0:
            score_plan = [1, -1, -2]
        else:
            score_plan = [-1, 1, 2]
    else:
        # Ultra items are the mildest connotation words, so the distractors
        # should be noticeably more loaded in either direction.
        score_plan = [3, 2, -2]

    choices = [entry.word]
    for score in score_plan:
        candidate = _pick_from_pool(pools[score], rng, exclude=exclude)
        choices.append(candidate)
        exclude.add(candidate)

    rng.shuffle(choices)
    if len(set(choices)) != 4:
        raise RuntimeError(f"duplicate choices generated for {entry.word}")
    return choices


def _template_for(bucket: str, polarity: str, index: int) -> str:
    if bucket == "Ultra":
        templates = [
            "Which word keeps the tone most neutral?",
            "Which word is the least emotionally loaded?",
            "Which word would a careful writer prefer for a balanced note?",
            "Which word best avoids an unintended emotional shade?",
        ]
    elif bucket == "Easy" and polarity == "positive":
        templates = [
            "Which word has the most positive connotation?",
            "Which word sounds the warmest?",
            "Which word feels the most approving?",
            "Which word would you choose for praise?",
        ]
    elif bucket == "Easy" and polarity == "negative":
        templates = [
            "Which word has the most negative connotation?",
            "Which word sounds the harshest?",
            "Which word feels the most disapproving?",
            "Which word would you avoid in a polite comment?",
        ]
    elif bucket == "Hard" and polarity == "positive":
        templates = [
            "Which word would a careful editor choose to keep the tone fair?",
            "Which word is the gentler choice?",
            "Which word keeps the sentence calm and respectful?",
            "Which word best avoids sounding too critical?",
        ]
    elif bucket == "Hard" and polarity == "negative":
        templates = [
            "Which word carries the sharper negative shade?",
            "Which word feels more judgmental?",
            "Which word would sound more pointed in a warning?",
            "Which word is the less polite choice?",
        ]
    elif polarity == "positive":
        templates = [
            "Which word would sound most respectful in a formal report?",
            "Which word feels the least loaded?",
            "Which word sounds friendlier in a note?",
            "Which word best fits a balanced compliment?",
        ]
    else:
        templates = [
            "Which word would sound most disapproving in a critique?",
            "Which word carries the clearer negative shade?",
            "Which word sounds sharper in a warning?",
            "Which word would a careful writer avoid?",
        ]
    return templates[index % len(templates)]


def generate_bank() -> list[dict[str, object]]:
    entries = _parse_source()
    selected = _select_buckets(entries)

    pools: dict[int, list[TermEntry]] = {
        score: _sort_candidates(entry for entry in entries if entry.score == score)
        for score in (-5, -4, -3, -2, -1, 1, 2, 3, 4, 5)
    }

    rng = random.Random(20260704)
    questions: list[dict[str, object]] = []
    seen_questions: set[str] = set()

    bucket_counters = {difficulty: 0 for difficulty in DIFFICULTY_ORDER}
    for overall_index, (difficulty, entry) in enumerate(selected, start=1):
        bucket_index = bucket_counters[difficulty]
        bucket_counters[difficulty] += 1

        question = _template_for(difficulty, entry.polarity, bucket_index)
        scenario = _scenario_phrase(difficulty, entry.polarity, bucket_index)
        stem = f"{scenario}: {question}"
        choices = _build_choices(entry, bucket=difficulty, rng=rng, pools=pools)
        answer = entry.word
        if answer not in choices:
            raise RuntimeError(f"answer missing from choices for {entry.word}")

        explanation = (
            f'"{entry.word}" carries a {entry.polarity} connotation '
            f"(score {entry.score:+d}), so it best matches the tone asked for."
        )

        payload = {
            "id": overall_index,
            "subtest": SUBTEST,
            "module": MODULE,
            "subtopic": SUBTOPIC,
            "difficulty": difficulty,
            "question": stem,
            "choices": choices,
            "answer": answer,
            "explanation": explanation,
            "tags": [
                "connotation",
                entry.polarity,
                difficulty.lower(),
                f"score-{abs(entry.score)}",
            ],
            "category": CATEGORY,
            "language": LANGUAGE,
        }

        if stem in seen_questions:
            raise RuntimeError(f"duplicate question stem generated: {stem}")
        seen_questions.add(stem)
        questions.append(payload)

    return questions


def main() -> int:
    questions = generate_bank()
    counts = {difficulty: 0 for difficulty in DIFFICULTY_ORDER}
    answers: set[str] = set()
    stems: set[str] = set()
    for item in questions:
        counts[str(item["difficulty"])] += 1
        answers.add(str(item["answer"]))
        stems.add(str(item["question"]))

    if counts != TARGET_COUNTS:
        raise RuntimeError(f"unexpected difficulty counts: {counts}")
    if len(answers) != 600:
        raise RuntimeError(f"expected 600 unique answers, found {len(answers)}")
    if len(stems) != 600:
        raise RuntimeError(f"expected 600 unique questions, found {len(stems)}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    print(f"Difficulty counts: {counts}")
    print(f"Unique answers: {len(answers)}")
    print(f"Unique question stems: {len(stems)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
