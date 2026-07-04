"""Generate the Verbal Ability / Word Meanings / Antonyms question bank.

This generator uses two web sources:

- Open English Wordnet for antonym relations and glosses.
- Hermit Dave's FrequencyWords list for a simple frequency ladder.

The output is a 600-item JSON bank with unique target words, four answer
choices per item, and a balanced 150 / 150 / 150 / 150 difficulty split.
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
    / "antonyms"
    / "questions.json"
)

WORDNET_URL = "https://en-word.net/static/english-wordnet-2025.zip"
FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Antonyms"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

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

PREFIXES = ("un", "in", "im", "ir", "il", "dis", "non", "anti", "de", "mis")

QUESTION_TEMPLATES = {
    "direct": [
        lambda q: f'Which word is the antonym of "{q["word"]}" in this sense: "{q["definition"]}"?',
        lambda q: f'What is the opposite of "{q["word"]}" when it means "{q["definition"]}"?',
        lambda q: f'Choose the best antonym for "{q["word"]}" in the sense "{q["definition"]}".',
        lambda q: f'Which option means the reverse of "{q["word"]}" in this sense: "{q["definition"]}"?',
    ],
    "context": [
        lambda q: f'In the sentence "{q["sentence"]}" and in the sense "{q["definition"]}", which word is the best antonym for "{q["word"]}"?',
        lambda q: f'What is the opposite of "{q["word"]}" in the sentence "{q["sentence"]}", when it means "{q["definition"]}"?',
        lambda q: f'Which choice best replaces "{q["word"]}" with its opposite meaning in "{q["sentence"]}" and this sense: "{q["definition"]}"?',
    ],
    "definition": [
        lambda q: f'Which word is the antonym of "{q["word"]}", which means "{q["definition"]}"?',
        lambda q: f'What is the opposite of "{q["word"]}" in the sense "{q["definition"]}"?',
        lambda q: f'Choose the word that best opposes "{q["word"]}" when it means "{q["definition"]}".',
        lambda q: f'Which option is the antonym of "{q["word"]}" in this sense: "{q["definition"]}"?',
    ],
    "contrast": [
        lambda q: f'The sentence below shows a contrast. In the sense "{q["definition"]}", which word best opposes "{q["word"]}"? "{q["sentence"]}"',
        lambda q: f'The sentence turns in the opposite direction. Which option is the antonym of "{q["word"]}" when it means "{q["definition"]}"? "{q["sentence"]}"',
        lambda q: f'Which choice is the best opposite of "{q["word"]}" in this contrast sentence and sense "{q["definition"]}"? "{q["sentence"]}"',
    ],
    "prefix": [
        lambda q: f'The word "{q["word"]}" contains a prefix that suggests reversal. Which choice is the best antonym?',
        lambda q: f'Which word is the best opposite of "{q["word"]}" after the negative prefix is noticed?',
        lambda q: f'The prefix in "{q["word"]}" hints at a reversed meaning. Which option is the antonym?',
    ],
}

QUESTION_WEIGHTS = {
    "Easy": ("direct", "context", "definition", "direct"),
    "Medium": ("context", "definition", "contrast", "direct"),
    "Hard": ("definition", "contrast", "context", "prefix"),
    "Ultra": ("definition", "contrast", "prefix", "direct"),
}

SENTENCE_TEMPLATES = {
    "adj": {
        "context": [
            "The report was {word} after the first review.",
            "The room felt {word} once everyone left.",
            "Her tone sounded {word} during the meeting.",
        ],
        "contrast": [
            "Although the first version was {word}, the revised version was easier to read.",
            "The rule was {word}, but the new version was more flexible.",
            "The explanation seemed {word}, yet the final draft was clearer.",
        ],
    },
    "v": {
        "context": [
            "The committee decided to {word} the proposal.",
            "The manager asked them to {word} the draft.",
            "The court may {word} the rule next year.",
        ],
        "contrast": [
            "Although the first panel wanted to {word} the plan, the second panel wanted to change it.",
            "The board might {word} the policy, but the staff prefers a new one.",
            "The group chose to {word} the idea, yet the committee wanted a different approach.",
        ],
    },
    "n": {
        "context": [
            "The article discussed the {word} of the issue.",
            "The speech focused on the {word} of the plan.",
            "The memo explained the {word} in detail.",
        ],
        "contrast": [
            "Although the first report stressed the {word}, the final report focused on something different.",
            "The discussion highlighted the {word}, but the revision shifted the focus.",
            "The committee mentioned the {word}, yet the new plan moved away from it.",
        ],
    },
    "adv": {
        "context": [
            "She answered {word} during the interview.",
            "He spoke {word} before the panel.",
            "The instructions were given {word} in the briefing.",
        ],
        "contrast": [
            "Although the first speaker explained things {word}, the second speaker was much clearer.",
            "The manager spoke {word}, but the assistant spoke with a different style.",
            "The message was delivered {word}, yet the follow-up was more direct.",
        ],
    },
}


@dataclass(frozen=True, slots=True)
class PairRecord:
    word: str
    answer: str
    pos: str
    gloss: str
    word_frequency: int
    answer_frequency: int


@dataclass(slots=True)
class WordSummary:
    word: str
    pos: str
    frequency: int
    records: list[PairRecord]


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


def _parse_wordnet_entry(line: str) -> tuple[str, str, list[str], list[tuple[str, str, str, str]], str] | None:
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


def _build_pair_records(
    archive: zipfile.ZipFile,
    frequency_map: dict[str, int],
) -> tuple[dict[str, list[PairRecord]], dict[str, set[str]]]:
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

    records_by_word: dict[str, list[PairRecord]] = defaultdict(list)
    all_words_by_pos: dict[str, set[str]] = defaultdict(set)

    for offset, pos, words, pointers, gloss in parsed_entries:
        norm_pos = _normalize_pos(pos)
        if norm_pos not in CONTENT_POS:
            continue
        for sym, target_offset, target_pos, source_target in pointers:
            if sym != "!":
                continue
            if len(source_target) != 4:
                continue
            try:
                source_index = int(source_target[:2], 16)
                target_index = int(source_target[2:], 16)
            except ValueError:
                continue

            source_word = words[source_index - 1] if 1 <= source_index <= len(words) else (words[0] if words else "")
            target_words = synset_words.get((target_pos, target_offset), [])
            target_word = (
                target_words[target_index - 1]
                if 1 <= target_index <= len(target_words)
                else (target_words[0] if target_words else "")
            )

            source = _sanitize_lemma(source_word)
            answer = _sanitize_lemma(target_word)
            if source is None or answer is None or source == answer:
                continue

            if len(source) < 3 or len(answer) < 3:
                continue

            pair = PairRecord(
                word=source,
                answer=answer,
                pos=norm_pos,
                gloss=gloss,
                word_frequency=frequency_map.get(source, 0),
                answer_frequency=frequency_map.get(answer, 0),
            )
            records_by_word[source].append(pair)
            all_words_by_pos[norm_pos].add(source)
            all_words_by_pos[norm_pos].add(answer)

    return records_by_word, all_words_by_pos


def _choose_best_record(records: list[PairRecord], answer_usage: Counter[str]) -> PairRecord:
    def sort_key(record: PairRecord) -> tuple[int, int, int, int, str]:
        prefix_bonus = 1 if _prefix_hint(record.word, record.answer) else 0
        return (
            answer_usage[record.answer],
            -prefix_bonus,
            -record.answer_frequency,
            len(record.gloss),
            record.answer,
        )

    return sorted(records, key=sort_key)[0]


def _prefix_hint(word: str, answer: str) -> str:
    for prefix in PREFIXES:
        if not word.startswith(prefix):
            continue
        stem = word[len(prefix) :]
        if len(stem) >= 3 and stem == answer:
            return prefix
    return ""


def _choose_variant(
    word: str,
    answer: str,
    difficulty: str,
    rng: random.Random,
) -> str:
    options = list(QUESTION_WEIGHTS[difficulty])
    if _prefix_hint(word, answer):
        if "prefix" not in options:
            options.append("prefix")
    else:
        options = [option for option in options if option != "prefix"]
    if "definition" not in options:
        options.append("definition")
    return rng.choice(options)


def _build_sentence(word: str, pos: str, variant: str, rng: random.Random) -> str:
    key = pos if pos in SENTENCE_TEMPLATES else "n"
    pool = SENTENCE_TEMPLATES[key]["contrast" if variant == "contrast" else "context"]
    sentence = rng.choice(pool).format(word=word)
    sentence = _sanitize_text(sentence)
    return sentence if sentence.endswith(".") else f"{sentence}."


def _build_question_text(record: PairRecord, difficulty: str, variant: str, rng: random.Random) -> str:
    context = {
        "word": record.word,
        "sentence": _build_sentence(record.word, record.pos, variant, rng)
        if variant in {"context", "contrast"}
        else "",
        "definition": record.gloss or f"the opposite meaning of {record.word}",
    }
    template = rng.choice(QUESTION_TEMPLATES[variant])
    return _sanitize_text(template(context))


def _build_choice_pool(
    records: Iterable[PairRecord],
) -> dict[str, list[str]]:
    pools: dict[str, list[str]] = defaultdict(list)
    for record in records:
        pools[record.pos].append(record.word)
        pools[record.pos].append(record.answer)
    for pos, words in list(pools.items()):
        unique: list[str] = []
        seen: set[str] = set()
        for word in words:
            if word in seen or not WORD_RE.fullmatch(word):
                continue
            seen.add(word)
            unique.append(word)
        pools[pos] = unique
    return pools


def _build_distractors(
    record: PairRecord,
    band_pool: list[str],
    global_pool: list[str],
    rng: random.Random,
) -> list[str]:
    banned = {record.word, record.answer}
    banned.update(token.lower() for token in re.findall(r"[A-Za-z]+", record.gloss))
    banned.update(
        answer
        for answer in [record.word, record.answer, *_antonyms_from_gloss(record.gloss)]
        if WORD_RE.fullmatch(answer)
    )

    def _pick(pool: list[str]) -> list[str]:
        choices: list[str] = []
        for word in pool:
            if word in banned or word == record.word or word == record.answer:
                continue
            if word in choices:
                continue
            choices.append(word)
            if len(choices) == 3:
                break
        return choices

    # Prefer same-band distractors for a smoother difficulty ladder.
    shuffled_band = band_pool[:]
    rng.shuffle(shuffled_band)
    distractors = _pick(shuffled_band)
    if len(distractors) < 3:
        shuffled_global = global_pool[:]
        rng.shuffle(shuffled_global)
        for word in _pick(shuffled_global):
            if word not in distractors:
                distractors.append(word)
            if len(distractors) == 3:
                break

    if len(distractors) < 3:
        raise ValueError(f"not enough distractors for {record.word}")
    return distractors[:3]


def _antonyms_from_gloss(gloss: str) -> list[str]:
    tokens = [token.lower() for token in re.findall(r"[A-Za-z]+", gloss)]
    return [token for token in tokens if token not in STOP_WORDS and len(token) > 2]


def _build_record(
    selected: WordSummary,
    record: PairRecord,
    difficulty: str,
    band_pool: list[str],
    global_pool: list[str],
    index: int,
) -> dict[str, object]:
    rng = random.Random(f"{selected.word}:{difficulty}:{index}")
    variant = _choose_variant(record.word, record.answer, difficulty, rng)
    question = _build_question_text(record, difficulty, variant, rng)
    distractors = _build_distractors(record, band_pool, global_pool, rng)
    choices = [record.answer, *distractors]
    rng.shuffle(choices)
    if record.answer not in choices:
        raise ValueError(f"answer missing from choices for {record.word}")
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError(f"bad choices for {record.word}")

    if variant == "definition":
        explanation = f'The gloss "{record.gloss or record.word}" points to "{record.answer}" as the opposite.'
    elif variant == "context":
        explanation = f'In the sentence, "{record.answer}" is the opposite of "{record.word}".'
    elif variant == "contrast":
        explanation = f'The contrast in the sentence points away from "{record.word}" and toward "{record.answer}".'
    elif variant == "prefix":
        prefix = _prefix_hint(record.word, record.answer)
        explanation = (
            f'The prefix "{prefix}" in "{record.word}" suggests reversal, and the base form is "{record.answer}".'
            if prefix
            else f'"{record.word}" means the opposite of "{record.answer}".'
        )
    else:
        explanation = f'"{record.word}" means the opposite of "{record.answer}".'

    tags = [
        record.pos,
        "antonym",
        "wordnet",
        difficulty.lower(),
        variant,
    ]
    if _prefix_hint(record.word, record.answer):
        tags.append("prefix-clue")
    if variant in {"context", "contrast"}:
        tags.append("sentence")
    if variant == "definition":
        tags.append("definition")

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": difficulty,
        "question": question,
        "choices": choices,
        "answer": record.answer,
        "explanation": explanation,
        "tags": _dedupe_preserve_order(tags),
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _dedupe_preserve_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        result.append(item)
    return result


def _select_words(
    summaries: list[WordSummary],
) -> list[tuple[str, WordSummary]]:
    summaries = sorted(summaries, key=lambda item: (-item.frequency, len(item.word), item.word))
    if len(summaries) < 600:
        raise ValueError(f"expected at least 600 antonym candidates, got {len(summaries)}")

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
        selected.extend((difficulty, summary) for summary in chosen)
    return selected


def _validate_bank(questions: list[dict[str, object]], selected_words: list[str]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    if len(selected_words) != len(set(selected_words)):
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
        question_key = (str(question["question"]), tuple(sorted(str(choice) for choice in choices)))
        if question_key in seen_questions:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_questions.add(question_key)


def main() -> int:
    frequency_map = _download_frequency_map()
    archive_bytes = _load_wordnet_source()
    archive = zipfile.ZipFile(io.BytesIO(archive_bytes))
    records_by_word, all_words_by_pos = _build_pair_records(archive, frequency_map)

    summaries: list[WordSummary] = []
    for word, records in records_by_word.items():
        if word in STOP_WORDS:
            continue
        primary_pos = Counter(record.pos for record in records).most_common(1)[0][0]
        summaries.append(
            WordSummary(
                word=word,
                pos=primary_pos,
                frequency=frequency_map.get(word, 0),
                records=sorted(
                    records,
                    key=lambda record: (
                        -record.answer_frequency,
                        len(record.gloss),
                        record.answer,
                    ),
                ),
            )
        )

    selected = _select_words(summaries)

    selected_by_band_pos: dict[str, dict[str, list[str]]] = defaultdict(lambda: defaultdict(list))
    for difficulty, summary in selected:
        selected_by_band_pos[difficulty][summary.pos].append(summary.word)

    questions: list[dict[str, object]] = []
    selected_words: list[str] = []
    answer_usage: Counter[str] = Counter()

    for index, (difficulty, summary) in enumerate(selected, start=1):
        band_pool = selected_by_band_pos[difficulty][summary.pos]
        global_pool = sorted(
            all_words_by_pos.get(summary.pos, set()),
            key=lambda word: (-frequency_map.get(word, 0), len(word), word),
        )
        record = _choose_best_record(summary.records, answer_usage)
        answer_usage[record.answer] += 1
        selected_words.append(summary.word)
        questions.append(
            _build_record(
                summary,
                record,
                difficulty,
                band_pool,
                global_pool,
                index,
            )
        )

    _validate_bank(questions, selected_words)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
