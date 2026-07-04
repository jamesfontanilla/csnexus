"""Generate the Verbal Ability / Word Meanings / Context Clues question bank.

The generator uses:

- Open English Wordnet for words, glosses, synonyms, and antonyms.
- Hermit Dave's FrequencyWords list for the difficulty ladder.

The final bank contains 600 unique target words with a 150 / 150 / 150 / 150
difficulty split. Most items ask for the meaning of the target word in context.
A smaller slice asks which clue type is being used so the bank covers the
lesson material more fully.
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

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "word-meaning"
    / "context-clues"
    / "questions.json"
)

WORDNET_URL = "https://en-word.net/static/english-wordnet-2025.zip"
FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Context Clues"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
CLUE_TYPE_TARGETS = {"Easy": 25, "Medium": 25, "Hard": 25, "Ultra": 25}

CONTENT_POS = {"adj", "n", "v", "adv"}
WORD_RE = re.compile(r"^[a-z]+$")

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

CLUE_TYPES = ("definition", "restatement", "contrast", "punctuation", "comparison")

MEANING_STEMS = {
    "definition": [
        lambda q: f'What does "{q["word"]}" mean in the sentence "{q["sentence"]}"?',
        lambda q: f'Which word best matches "{q["word"]}" in context?',
        lambda q: f'In the sentence "{q["sentence"]}", what does "{q["word"]}" mean?',
    ],
    "restatement": [
        lambda q: f'Which word best matches "{q["word"]}" after the restatement clue in "{q["sentence"]}"?',
        lambda q: f'What does "{q["word"]}" mean when the sentence restates it as "{q["answer_hint"]}"?',
        lambda q: f'Choose the best meaning of "{q["word"]}" from the restated clue in "{q["sentence"]}".',
    ],
    "contrast": [
        lambda q: f'What does "{q["word"]}" mean in the contrast shown by "{q["sentence"]}"?',
        lambda q: f'Which word best matches "{q["word"]}" in the contrast sentence?',
        lambda q: f'In the sentence "{q["sentence"]}", what does "{q["word"]}" most nearly mean?',
    ],
    "punctuation": [
        lambda q: f'What does "{q["word"]}" mean in the sentence that uses punctuation to explain it?',
        lambda q: f'Which word best matches "{q["word"]}" when the clue is set off by punctuation?',
        lambda q: f'What is the meaning of "{q["word"]}" in "{q["sentence"]}"?',
    ],
    "comparison": [
        lambda q: f'What does "{q["word"]}" mean in the comparison sentence "{q["sentence"]}"?',
        lambda q: f'Which word best matches "{q["word"]}" in the comparison clue?',
        lambda q: f'In the sentence "{q["sentence"]}", what does "{q["word"]}" mean?',
    ],
}

CLUE_TYPE_STEMS = [
    lambda q: f'What type of context clue is used in the sentence "{q["sentence"]}"?',
    lambda q: f'The sentence "{q["sentence"]}" uses which context clue to explain "{q["word"]}"?',
    lambda q: f'Which context clue best explains "{q["word"]}" in the sentence "{q["sentence"]}"?',
]

SENTENCE_TEMPLATES = {
    "adj": {
        "definition": [
            "The {word} report was {answer} and easy to follow.",
            "The {word} proposal was {answer} and needed revision.",
            "The {word} response was {answer} and clear.",
        ],
        "restatement": [
            "The {word} report, or {answer} report, was easy to follow.",
            "The {word} proposal, or {answer} proposal, needed revision.",
            "The {word} response, or {answer} response, was clear.",
        ],
        "contrast": [
            "Although the first draft was {antonym}, the final draft was {word}.",
            "The rule was {antonym}, but the new version was {word}.",
            "The initial plan was {antonym}; the revised plan was {word}.",
        ],
        "punctuation": [
            "The {word} report - {answer} and easy to follow - needed little revision.",
            "The {word} proposal ({answer}) needed revision.",
            "The {word} response: {answer} and clear.",
        ],
        "comparison": [
            "Like a {answer} report, the {word} memo needed little editing.",
            "As a {answer} worker, the {word} clerk checked every detail.",
            "Like a {answer} plan, the {word} one was easy to follow.",
        ],
    },
    "n": {
        "definition": [
            "The {word}, a {answer}, was placed on the desk.",
            "The {word} is a {answer} used in the meeting.",
            "The {word} was a {answer} brought to the council.",
        ],
        "restatement": [
            "The {word}, or {answer}, was placed on the desk.",
            "The {word}, also a {answer}, was brought to the meeting.",
            "The {word}, in other words, a {answer}, was very useful.",
        ],
        "punctuation": [
            "The {word} ({answer}) was placed on the desk.",
            "The {word} - {answer} - was brought to the meeting.",
            "The {word}: {answer}.",
        ],
    },
    "v": {
        "definition": [
            "To {word} means to {answer}.",
            "The editor asked the team to {word} the report before noon.",
            "The committee decided to {word} the proposal.",
        ],
        "restatement": [
            "The team will {word}, or {answer}, before noon.",
            "The committee decided to {word}, or {answer}, the proposal.",
            "They plan to {word}, that is, to {answer}, after the review.",
        ],
        "contrast": [
            "Although they once {antonym}, they now {word}.",
            "They used to {antonym}, but today they {word}.",
            "The old board would {antonym}, whereas the new board will {word}.",
        ],
        "punctuation": [
            "The team will {word} - {answer} - before noon.",
            "The committee decided to {word} ({answer}) after the review.",
            "They plan to {word}: {answer}.",
        ],
    },
    "adv": {
        "definition": [
            "She spoke {word}, meaning {answer}.",
            "He moved {word}, which means {answer}.",
            "The answer was given {word} during the briefing.",
        ],
        "restatement": [
            "She spoke {word}, or {answer}, during the briefing.",
            "He moved {word}, or {answer}, across the room.",
            "The answer was given {word}, or {answer}, in the meeting.",
        ],
        "contrast": [
            "Although others spoke {antonym}, she spoke {word}.",
            "The first team moved {antonym}, but the second moved {word}.",
            "They answered {antonym}, yet she answered {word}.",
        ],
        "punctuation": [
            "She spoke {word} ({answer}) during the briefing.",
            "He moved {word} - {answer} - across the room.",
            "The answer was given {word}: {answer}.",
        ],
    },
}


@dataclass(slots=True)
class SenseRecord:
    word: str
    pos: str
    gloss: str
    synonyms: tuple[str, ...]
    antonyms: tuple[str, ...]
    answer: str
    target_frequency: int
    answer_frequency: int

    @property
    def quality_score(self) -> tuple[int, int, int, int, str]:
        return (
            1 if self.answer_frequency > 0 else 0,
            self.answer_frequency,
            len(self.synonyms),
            len(self.antonyms),
            self.answer,
        )


@dataclass(slots=True)
class WordSummary:
    word: str
    frequency: int
    record: SenseRecord

    @property
    def pos(self) -> str:
        return self.record.pos


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


def _normalize_pos(pos: str) -> str:
    return {"a": "adj", "s": "adj", "n": "n", "v": "v", "r": "adv"}.get(pos, pos)


def _sanitize_lemma(raw: str) -> str | None:
    lemma = raw.lower().strip()
    if not lemma or "_" in lemma or "-" in lemma or "'" in lemma:
        return None
    if not WORD_RE.fullmatch(lemma):
        return None
    if lemma in STOP_WORDS:
        return None
    return lemma


def _sanitize_gloss(gloss: str) -> str:
    text = _normalize_whitespace(gloss)
    text = re.sub(r"^\([^)]*\)\s*", "", text)
    text = text.split(";", 1)[0]
    text = re.sub(r"\s*\([^)]*\)\s*$", "", text)
    text = text.split('"', 1)[0]
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    text = _truncate_words(text, 14)
    return text.strip(" ,;:.")


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
    response = requests.get(url, timeout=60, **kwargs)
    response.raise_for_status()
    return response


def _download_frequency_map() -> dict[str, int]:
    response = _get(FREQUENCY_URL)
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
            pointers.append((tokens[index], tokens[index + 1], tokens[index + 2], tokens[index + 3]))
            index += 4
    except (IndexError, ValueError):
        return None

    return offset, pos, words, pointers, _sanitize_gloss(gloss)


def _load_wordnet_source() -> bytes:
    response = _get(WORDNET_URL)
    return response.content


def _build_records(
    archive: zipfile.ZipFile,
    frequency_map: dict[str, int],
) -> tuple[dict[str, list[SenseRecord]], dict[str, set[str]]]:
    files = [
        "oewn2025/data.adj",
        "oewn2025/data.verb",
        "oewn2025/data.noun",
        "oewn2025/data.adv",
    ]

    synset_words: dict[tuple[str, str], list[str]] = {}
    parsed_entries: list[tuple[str, str, list[str], list[tuple[str, str, str, str]], str]] = []

    for filename in files:
        with archive.open(filename) as handle:
            for raw_line in handle:
                line = raw_line.decode("utf-8", errors="replace").strip()
                parsed = _parse_wordnet_entry(line)
                if parsed is None:
                    continue
                offset, pos, words, pointers, gloss = parsed
                synset_words[(pos, offset)] = words
                parsed_entries.append(parsed)

    lemma_antonyms: dict[str, set[str]] = defaultdict(set)
    for offset, pos, words, pointers, _gloss in parsed_entries:
        for sym, target_offset, target_pos, _source_target in pointers:
            if sym != "!":
                continue
            target_words = synset_words.get((target_pos, target_offset), [])
            if not target_words:
                continue
            clean_targets = [
                target
                for target in (_sanitize_lemma(word) for word in target_words)
                if target is not None
            ]
            if not clean_targets:
                continue
            for source_word in words:
                source = _sanitize_lemma(source_word)
                if source is None:
                    continue
                for target in clean_targets:
                    if target != source:
                        lemma_antonyms[source].add(target)
                        lemma_antonyms[target].add(source)

    records_by_word: dict[str, list[SenseRecord]] = defaultdict(list)
    all_words_by_pos: dict[str, set[str]] = defaultdict(set)

    for _offset, pos, words, _pointers, gloss in parsed_entries:
        norm_pos = _normalize_pos(pos)
        if norm_pos not in CONTENT_POS:
            continue
        clean_words = []
        for raw_word in words:
            cleaned = _sanitize_lemma(raw_word)
            if cleaned is not None:
                clean_words.append(cleaned)
        if len(clean_words) < 2:
            continue
        for word in clean_words:
            synonyms = tuple(other for other in clean_words if other != word)
            if not synonyms:
                continue
            answer = max(
                synonyms,
                key=lambda other: (
                    frequency_map.get(other, 0),
                    -len(other),
                    other,
                ),
            )
            answer_frequency = frequency_map.get(answer, 0)
            record = SenseRecord(
                word=word,
                pos=norm_pos,
                gloss=gloss,
                synonyms=synonyms,
                antonyms=tuple(sorted(lemma_antonyms.get(word, set()))),
                answer=answer,
                target_frequency=frequency_map.get(word, 0),
                answer_frequency=answer_frequency,
            )
            if record.target_frequency <= 0:
                continue
            if record.answer_frequency <= 0:
                continue
            records_by_word[word].append(record)
            all_words_by_pos[norm_pos].add(word)
            all_words_by_pos[norm_pos].add(answer)

    if not records_by_word:
        raise RuntimeError("no usable WordNet records were built")

    return records_by_word, all_words_by_pos


def _choose_best_record(records: list[SenseRecord]) -> SenseRecord:
    preferred = [record for record in records if record.answer_frequency > 0]
    if preferred:
        records = preferred

    def sort_key(record: SenseRecord) -> tuple[int, int, int, int, str]:
        return (
            1 if record.answer_frequency > 0 else 0,
            record.answer_frequency,
            len(record.synonyms),
            len(record.antonyms),
            record.answer,
        )

    return sorted(records, key=sort_key, reverse=True)[0]


def _variant_pool(record: SenseRecord, difficulty: str, kind: str) -> list[str]:
    base: list[str]
    if record.pos == "adj":
        base = ["definition", "restatement", "punctuation", "comparison"]
        if record.antonyms:
            base.insert(2, "contrast")
    elif record.pos == "v":
        base = ["definition", "restatement", "punctuation"]
        if record.antonyms:
            base.insert(2, "contrast")
    elif record.pos == "adv":
        base = ["definition", "restatement", "punctuation"]
        if record.antonyms:
            base.insert(2, "contrast")
    else:
        base = ["definition", "restatement", "punctuation"]

    if kind == "clue_type":
        return base

    if difficulty == "Easy":
        weighted = ["definition", "definition", "restatement", "punctuation"]
    elif difficulty == "Medium":
        weighted = ["definition", "restatement", "punctuation", "contrast"]
    elif difficulty == "Hard":
        weighted = ["restatement", "contrast", "punctuation", "contrast"]
    else:
        weighted = ["contrast", "punctuation", "restatement", "contrast"]

    if "comparison" in base:
        weighted.append("comparison")
    return [variant for variant in weighted if variant in base]


def _pick_variant(record: SenseRecord, difficulty: str, kind: str, rng: random.Random) -> str:
    options = _variant_pool(record, difficulty, kind)
    if not options:
        options = ["definition"]
    return rng.choice(options)


def _pick_antonym(record: SenseRecord, rng: random.Random) -> str:
    if not record.antonyms:
        return record.answer
    choices = [word for word in record.antonyms if word != record.word and word != record.answer]
    if not choices:
        choices = list(record.antonyms)
    choices.sort(key=lambda word: (-len(word), word))
    return rng.choice(choices)


def _build_sentence(record: SenseRecord, variant: str, rng: random.Random) -> str:
    pos_templates = SENTENCE_TEMPLATES.get(record.pos, SENTENCE_TEMPLATES["n"])
    templates = pos_templates.get(variant) or pos_templates.get("definition") or ["{word} {answer}."]
    template = rng.choice(templates)
    context = {
        "word": record.word,
        "answer": record.answer,
        "antonym": _pick_antonym(record, rng),
    }
    sentence = _sanitize_text(template.format(**context))
    return sentence if sentence.endswith(".") else f"{sentence}."


def _meaning_question_text(record: SenseRecord, variant: str, sentence: str, rng: random.Random) -> str:
    template = rng.choice(MEANING_STEMS[variant])
    payload = {
        "word": record.word,
        "answer": record.answer,
        "answer_hint": record.answer,
        "sentence": sentence,
    }
    return _sanitize_text(template(payload))


def _clue_type_question_text(record: SenseRecord, sentence: str, rng: random.Random) -> str:
    template = rng.choice(CLUE_TYPE_STEMS)
    payload = {
        "word": record.word,
        "sentence": sentence,
    }
    return _sanitize_text(template(payload))


def _build_meaning_distractors(
    record: SenseRecord,
    pools: dict[str, list[str]],
    rng: random.Random,
) -> list[str]:
    banned = {record.word, record.answer}
    banned.update(
        token.lower()
        for token in re.findall(r"[A-Za-z]+", record.gloss)
        if len(token) > 1
    )
    banned.update(record.synonyms)
    banned.update(record.antonyms)
    candidate_pool: list[str] = []
    for key in (record.pos, "any"):
        candidate_pool.extend(pools.get(key, []))
    unique_pool: list[str] = []
    seen: set[str] = set()
    for word in candidate_pool:
        if word in seen or word in banned or not WORD_RE.fullmatch(word):
            continue
        seen.add(word)
        unique_pool.append(word)
    rng.shuffle(unique_pool)
    distractors = unique_pool[:3]
    if len(distractors) < 3:
        fallback = [word for word in pools.get("any", []) if word not in banned and word not in distractors]
        rng.shuffle(fallback)
        for word in fallback:
            distractors.append(word)
            if len(distractors) == 3:
                break
    if len(distractors) < 3:
        raise ValueError(f"not enough distractors for {record.word}")
    return distractors[:3]


def _build_clue_type_distractors(answer: str, rng: random.Random) -> list[str]:
    distractors = [clue for clue in CLUE_TYPES if clue != answer]
    rng.shuffle(distractors)
    return distractors[:3]


def _build_explanation(
    record: SenseRecord,
    variant: str,
    kind: str,
    sentence: str,
) -> str:
    if kind == "clue_type":
        return f'The sentence uses a {variant} clue to explain "{record.word}".'
    if variant == "contrast":
        ant = _pick_antonym(record, random.Random(record.word))
        return f'The contrast clue points away from "{ant}" and toward "{record.answer}".'
    if variant == "comparison":
        return f'The comparison clue helps show that "{record.word}" means "{record.answer}".'
    if variant == "punctuation":
        return f'The punctuation clue points to "{record.answer}" as the meaning of "{record.word}".'
    if variant == "restatement":
        return f'The restatement clue points to "{record.answer}" as the meaning of "{record.word}".'
    return f'The definition clue points to "{record.answer}" as the meaning of "{record.word}".'


def _build_record(
    summary: WordSummary,
    difficulty: str,
    kind: str,
    variant: str,
    pools: dict[str, list[str]],
    index: int,
) -> dict[str, object]:
    record = summary.record
    rng = random.Random(f"{summary.word}:{difficulty}:{kind}:{variant}:{index}")
    sentence = _build_sentence(record, variant, rng)

    if kind == "clue_type":
        answer = variant
        choices = [answer, *_build_clue_type_distractors(answer, rng)]
        rng.shuffle(choices)
        question = _clue_type_question_text(record, sentence, rng)
    else:
        answer = record.answer
        distractors = _build_meaning_distractors(record, pools, rng)
        choices = [answer, *distractors]
        rng.shuffle(choices)
        question = _meaning_question_text(record, variant, sentence, rng)

    if answer not in choices:
        raise ValueError(f"answer missing from choices for {record.word}")
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError(f"bad choices for {record.word}")

    explanation = _build_explanation(record, variant, kind, sentence)
    tags = [
        record.pos,
        "context-clue",
        "word-meaning",
        kind,
        difficulty.lower(),
        variant,
    ]
    if record.antonyms:
        tags.append("antonym-capable")

    return {
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


def _clue_type_score(summary: WordSummary) -> tuple[int, int, int, int, str]:
    record = summary.record
    return (
        1 if record.antonyms else 0,
        1 if record.pos == "adj" else 0,
        1 if record.pos in {"adj", "v", "adv"} else 0,
        record.answer_frequency,
        record.word,
    )


def _select_candidates(summaries: list[WordSummary]) -> list[tuple[str, WordSummary]]:
    summaries = sorted(summaries, key=lambda item: (-item.frequency, len(item.word), item.word))
    if len(summaries) < 600:
        raise ValueError(f"expected at least 600 context-clue candidates, got {len(summaries)}")

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
        ranked = sorted(band, key=lambda summary: (-summary.record.quality_score[1], -summary.record.quality_score[2], summary.word))
        chosen = ranked[: TARGET_COUNTS[difficulty]]
        if len(chosen) != TARGET_COUNTS[difficulty]:
            raise ValueError(
                f"expected {TARGET_COUNTS[difficulty]} {difficulty} items, got {len(chosen)}"
            )
        clue_candidates = sorted(chosen, key=_clue_type_score, reverse=True)
        clue_count = CLUE_TYPE_TARGETS[difficulty]
        clue_selected = clue_candidates[:clue_count]
        meaning_selected = [summary for summary in chosen if summary not in clue_selected]
        selected.extend(("clue_type", summary) for summary in clue_selected)
        selected.extend(("meaning", summary) for summary in meaning_selected)
    return selected


def _group_pools(selected: list[tuple[str, WordSummary]]) -> dict[str, list[str]]:
    pools: dict[str, list[str]] = {"any": []}
    for _kind, summary in selected:
        record = summary.record
        pools["any"].append(record.word)
        pools["any"].append(record.answer)
        pools.setdefault(record.pos, []).append(record.word)
        pools[record.pos].append(record.answer)
    for key, values in list(pools.items()):
        seen: set[str] = set()
        unique: list[str] = []
        for value in values:
            if value in seen or not WORD_RE.fullmatch(value):
                continue
            seen.add(value)
            unique.append(value)
        pools[key] = unique
    return pools


def _validate_bank(
    questions: list[dict[str, object]],
    selected: list[tuple[str, WordSummary]],
) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    target_words = [summary.word for _kind, summary in selected]
    if len(target_words) != len(set(target_words)):
        raise ValueError("target words are not unique")

    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise ValueError(f"unexpected difficulty distribution: {dict(counts)}")

    kind_counts = Counter("clue_type" if "clue_type" in question["tags"] else "meaning" for question in questions)
    expected_kinds = {"meaning": 500, "clue_type": 100}
    if kind_counts != expected_kinds:
        raise ValueError(f"unexpected kind distribution: {dict(kind_counts)}")

    clue_counts = Counter(str(question["difficulty"]) for question in questions if "clue_type" in question["tags"])
    if clue_counts != CLUE_TYPE_TARGETS:
        raise ValueError(f"unexpected clue-type distribution: {dict(clue_counts)}")

    seen_pairs: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        choices = list(question["choices"])  # type: ignore[assignment]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")
        question_key = (str(question["question"]), tuple(sorted(str(choice) for choice in choices)))
        if question_key in seen_pairs:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_pairs.add(question_key)


def main() -> int:
    frequency_map = _download_frequency_map()
    archive_bytes = _load_wordnet_source()
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    records_by_word, all_words_by_pos = _build_records(archive, frequency_map)

    summaries: list[WordSummary] = []
    for word, records in records_by_word.items():
        best_record = _choose_best_record(records)
        if best_record.target_frequency <= 0:
            continue
        summaries.append(
            WordSummary(
                word=word,
                frequency=best_record.target_frequency,
                record=best_record,
            )
        )

    if len(summaries) < 600:
        raise RuntimeError(f"not enough usable context-clue candidates: {len(summaries)}")

    selected = _select_candidates(summaries)
    pools = _group_pools(selected)

    questions: list[dict[str, object]] = []
    banded_selection = [
        ("Easy", selected[:150]),
        ("Medium", selected[150:300]),
        ("Hard", selected[300:450]),
        ("Ultra", selected[450:600]),
    ]
    index = 1
    for difficulty, band in banded_selection:
        for kind, summary in band:
            variant_rng = random.Random(f"{summary.word}:{difficulty}:{kind}:{index}:variant")
            variant = _pick_variant(summary.record, difficulty, kind, variant_rng)
            questions.append(
                _build_record(
                    summary=summary,
                    difficulty=difficulty,
                    kind=kind,
                    variant=variant,
                    pools=pools,
                    index=index,
                )
            )
            index += 1

    _validate_bank(questions, selected)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
