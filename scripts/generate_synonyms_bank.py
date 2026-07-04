"""Generate the Verbal Ability / Word Meanings / Synonyms question bank.

This version rebuilds the bank from a curated Barron word list, verifies
synonym pairs with Datamuse, and uses dictionaryapi.dev for definition-based
prompts. The goal is 600 unique target words with varied question wording.

Usage:
    python scripts/generate_synonyms_bank.py
"""

from __future__ import annotations

import concurrent.futures as cf
import json
import random
import re
import time
from dataclasses import dataclass, replace
from functools import lru_cache
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
    / "synonyms"
    / "questions.json"
)

SOURCE_URL = (
    "https://raw.githubusercontent.com/KokeCacao/Barron3500/master/"
    "Basic%20Word%20List.txt"
)
DATAMUSE_URL = "https://api.datamuse.com/words"
DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
SESSION = requests.Session()
SESSION.mount("https://", HTTPAdapter(pool_connections=48, pool_maxsize=48, max_retries=2))
SESSION.mount("http://", HTTPAdapter(pool_connections=48, pool_maxsize=48, max_retries=2))

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Synonyms"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")
DIFFICULTY_THRESHOLDS = (
    ("Easy", 8.0),
    ("Medium", 1.0),
    ("Hard", 0.15),
    ("Ultra", 0.0),
)

WORD_RE = re.compile(r"^[a-z]+$")
POS_PREFIX_RE = re.compile(r"^(?:v|n|adj|adv|prep|pron|conj|interj)\b", re.I)
GLOSS_RE = re.compile(r"([A-Za-z][A-Za-z ;,\-()]*?)\.\s+(?=[A-Z])")
SPLIT_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")

CONTENT_POS = {"adj", "v", "n", "adv"}
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
}

MODIFIER_WORDS = {
    "almost",
    "barely",
    "chiefly",
    "commonly",
    "essentially",
    "especially",
    "extremely",
    "fairly",
    "frequently",
    "generally",
    "highly",
    "largely",
    "literally",
    "mostly",
    "nearly",
    "normally",
    "occasionally",
    "often",
    "primarily",
    "quickly",
    "rather",
    "really",
    "roughly",
    "rarely",
    "simply",
    "slightly",
    "somewhat",
    "slowly",
    "seldom",
    "too",
    "truly",
    "typically",
    "usually",
    "well",
    "just",
    "only",
}

QUESTION_TEMPLATES = {
    "direct": [
        lambda q: f'Which word is closest in meaning to "{q["word"]}"?',
        lambda q: f'What is a synonym for "{q["word"]}"?',
        lambda q: f'Choose the word nearest in meaning to "{q["word"]}".',
        lambda q: f'Which word best matches "{q["word"]}"?',
    ],
    "context": [
        lambda q: (
            f'Which word best replaces "{q["word"]}" in the sentence '
            f'"{q["sentence"]}"?'
        ),
        lambda q: f'In the sentence "{q["sentence"]}", what does "{q["word"]}" mean?',
        lambda q: f'Which word would keep the sentence meaning if it replaced "{q["word"]}"?',
        lambda q: f'Which choice fits the sentence best when it replaces "{q["word"]}"?',
    ],
    "definition": [
        lambda q: f'Which word means "{q["definition"]}"?',
        lambda q: f'Pick the word that matches this meaning: "{q["definition"]}".',
        lambda q: f'Which option best matches the meaning "{q["definition"]}"?',
    ],
}

QUESTION_WEIGHTS = {
    "Easy": ("direct", "context", "direct"),
    "Medium": ("direct", "context", "definition"),
    "Hard": ("context", "definition", "direct", "definition"),
    "Ultra": ("definition", "context", "definition", "direct"),
}

SENTENCE_TEMPLATES = {
    "Easy": {
        "adj": [
            "The new policy seemed {word} after the first review.",
            "It was a {word} decision that needed more work.",
            "The response felt {word} during the interview.",
        ],
        "v": [
            "The editor asked the team to {word} the report before noon.",
            "We will {word} the issue before the meeting.",
            "Please {word} the draft and send it back.",
        ],
        "n": [
            "The committee reviewed the {word} during the meeting.",
            "The report included a clear {word} from the manager.",
            "The team discussed the {word} before the vote.",
        ],
        "adv": [
            "She spoke {word} during the briefing.",
            "He worked {word} to finish the draft.",
            "The answer was given {word} in the meeting.",
        ],
    },
    "Medium": {
        "adj": [
            "The proposal seemed {word} once the committee reviewed it again.",
            "The explanation was {word}, so the team asked for more detail.",
            "The result felt {word} after the second reading.",
        ],
        "v": [
            "The board will {word} the proposal before the final vote.",
            "We must {word} the issue before the deadline.",
            "The manager asked the staff to {word} the draft carefully.",
        ],
        "n": [
            "The report presented the {word} in a clear format.",
            "The committee examined the {word} before making a choice.",
            "They discussed the {word} at length during the meeting.",
        ],
        "adv": [
            "She answered {word} during the interview.",
            "He moved {word} to avoid drawing attention.",
            "The message was delivered {word} in the briefing.",
        ],
    },
    "Hard": {
        "adj": [
            "The policy looked {word}, which is why the board requested revisions.",
            "The explanation was {word}, so the team sought a clearer version.",
            "The situation felt {word} after the second analysis.",
        ],
        "v": [
            "The commission will {word} the proposal before the final vote.",
            "We need to {word} the issue with care before the deadline.",
            "The editor asked the writer to {word} the draft for clarity.",
        ],
        "n": [
            "The report framed the {word} as a major concern.",
            "The committee examined the {word} before deciding on action.",
            "They treated the {word} as a key point in the discussion.",
        ],
        "adv": [
            "She answered {word}, keeping her response brief and measured.",
            "He spoke {word} so the room would not lose focus.",
            "The message was delivered {word} during the meeting.",
        ],
    },
    "Ultra": {
        "adj": [
            "The report described the issue as {word}, so the board wanted more detail.",
            "The wording was {word}, and the staff asked for a clearer version.",
            "The explanation sounded {word} even after a second reading.",
        ],
        "v": [
            "The panel will {word} the proposal before the final review.",
            "We must {word} the issue carefully before the deadline.",
            "The editor asked the writer to {word} the statement with precision.",
        ],
        "n": [
            "The report treated the {word} as a serious concern.",
            "The committee examined the {word} before making a final decision.",
            "They discussed the {word} in detail during the review.",
        ],
        "adv": [
            "She answered {word}, avoiding unnecessary detail.",
            "He spoke {word} so the room would stay focused.",
            "The instructions were delivered {word} in the briefing.",
        ],
    },
}


@dataclass
class SourceEntry:
    word: str
    gloss: str
    source_index: int


@dataclass
class SynonymHit:
    word: str
    score: float
    pos: tuple[str, ...]


@dataclass
class Candidate:
    word: str
    gloss: str
    gloss_tokens: tuple[str, ...]
    source_index: int
    difficulty: str
    frequency: float
    pos: tuple[str, ...]
    synonyms: tuple[SynonymHit, ...]
    answer: str
    answer_pos: str
    answer_source: str
    answer_score: float
    definition: str = ""

    @property
    def primary_pos(self) -> str:
        return _primary_pos(self.pos)


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _truncate_words(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(",;:.!?") + "..."


def _sanitize_text(text: str) -> str:
    return _normalize_whitespace(text.replace('"', "'"))


def _dedupe_preserve_order(items: list[str]) -> list[str]:
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
            time.sleep(backoff * (2**attempt))
            continue
        response.raise_for_status()
        return response
    response.raise_for_status()
    return response


def _primary_pos(pos_tags: tuple[str, ...]) -> str:
    for pos in POS_PRIORITY:
        if pos in pos_tags:
            return pos
    return pos_tags[0] if pos_tags else ""


def _parse_source_entries(text: str) -> list[SourceEntry]:
    entries: list[SourceEntry] = []
    seen: set[str] = set()
    for source_index, raw_line in enumerate(text.splitlines()):
        line = raw_line.strip()
        if not line:
            continue
        if line[0] in "•■":
            line = line[1:].strip()
        if " " not in line:
            continue
        word, rest = line.split(" ", 1)
        word = word.strip().lower().strip(".,;:!?")
        if not WORD_RE.fullmatch(word):
            continue
        if word in seen or word in STOP_WORDS:
            continue
        if not POS_PREFIX_RE.match(rest.lstrip()):
            continue
        match = GLOSS_RE.search(rest)
        if not match:
            continue
        gloss = _normalize_whitespace(match.group(1))
        entries.append(SourceEntry(word=word, gloss=gloss, source_index=source_index))
        seen.add(word)
    return entries


@lru_cache(maxsize=None)
def _fetch_word_info(word: str) -> tuple[float, tuple[str, ...]]:
    response = _get(
        DATAMUSE_URL,
        params={"sp": word, "md": "fp", "max": 1},
        timeout=20,
    )
    payload = response.json()
    if not payload:
        raise ValueError(f"Datamuse returned no data for {word}")
    tags = payload[0].get("tags", [])
    frequency = 0.0
    pos_tags: list[str] = []
    for tag in tags:
        if tag.startswith("f:"):
            try:
                frequency = float(tag[2:])
            except ValueError:
                frequency = 0.0
        elif tag in CONTENT_POS:
            pos_tags.append(tag)
    if not pos_tags:
        raise ValueError(f"No content POS tags for {word}")
    return frequency, tuple(dict.fromkeys(pos_tags))


@lru_cache(maxsize=None)
def _fetch_synonyms(word: str) -> tuple[SynonymHit, ...]:
    response = _get(
        DATAMUSE_URL,
        params={"rel_syn": word, "md": "p", "max": 40},
        timeout=20,
    )
    payload = response.json()
    hits: list[SynonymHit] = []
    for item in payload:
        synonym = item.get("word", "").lower().strip()
        if not WORD_RE.fullmatch(synonym) or synonym == word:
            continue
        tags = tuple(tag for tag in item.get("tags", []) if tag in CONTENT_POS)
        hits.append(SynonymHit(word=synonym, score=float(item.get("score", 0)), pos=tags))
    hits.sort(key=lambda hit: (-hit.score, hit.word))
    return tuple(hits)


def _choose_answer(word: str, gloss: str, synonyms: tuple[SynonymHit, ...]) -> tuple[str, str, float] | None:
    gloss_tokens = [
        token.lower()
        for token in re.findall(r"[A-Za-z]+", gloss)
        if len(token) > 1 and token.lower() not in STOP_WORDS and token.lower() not in MODIFIER_WORDS
    ]
    synonym_map = {hit.word: hit for hit in synonyms}
    gloss_hits: list[tuple[str, float, str]] = []
    for token in gloss_tokens:
        hit = synonym_map.get(token)
        if not hit:
            continue
        score = hit.score + 100000.0
        gloss_hits.append((token, score, "gloss"))
    if gloss_hits:
        token, score, source = max(gloss_hits, key=lambda item: (item[1], -len(item[0]), item[0]))
        return token, source, score
    synonym_hits: list[tuple[str, float, str]] = []
    for hit in synonyms:
        if hit.word in STOP_WORDS or len(hit.word) <= 1:
            continue
        synonym_hits.append((hit.word, hit.score, "synonym"))
    if synonym_hits:
        token, score, source = max(synonym_hits, key=lambda item: (item[1], -len(item[0]), item[0]))
        return token, source, score
    return None


def _assign_difficulty(frequency: float) -> str:
    for difficulty, threshold in DIFFICULTY_THRESHOLDS:
        if frequency >= threshold:
            return difficulty
    return "Ultra"


def _pick_sentence(word: str, difficulty: str, pos_tags: tuple[str, ...]) -> str:
    pos = _primary_pos(pos_tags)
    if pos not in SENTENCE_TEMPLATES[difficulty]:
        pos = "n"
    template = random.Random(f"{difficulty}:{word}:sentence").choice(SENTENCE_TEMPLATES[difficulty][pos])
    sentence = _sanitize_text(template.format(word=word))
    return sentence if sentence.endswith(".") else f"{sentence}."


def _build_definition(word: str, pos_tags: tuple[str, ...]) -> str:
    try:
        response = _get(DICTIONARY_URL.format(word=word), timeout=20)
    except requests.HTTPError as exc:
        status_code = getattr(exc.response, "status_code", None)
        if status_code in {404, 429}:
            return ""
        raise
    if not response.ok:
        return ""
    payload = response.json()
    if not isinstance(payload, list) or not payload:
        return ""
    preferred = list(pos_tags) + [pos for pos in POS_PRIORITY if pos not in pos_tags]
    meanings = payload[0].get("meanings", [])
    for wanted_pos in preferred:
        for meaning in meanings:
            if meaning.get("partOfSpeech") != wanted_pos:
                continue
            for definition in meaning.get("definitions", []):
                text = _normalize_whitespace(str(definition.get("definition", "")))
                if not text:
                    continue
                text = re.split(r"[;]", text)[0].strip()
                text = text.replace('"', "'")
                text = _truncate_words(text, 14)
                return text.rstrip(".")
    for meaning in meanings:
        for definition in meaning.get("definitions", []):
            text = _normalize_whitespace(str(definition.get("definition", "")))
            if not text:
                continue
            text = re.split(r"[;]", text)[0].strip()
            text = text.replace('"', "'")
            text = _truncate_words(text, 14)
            return text.rstrip(".")
    return ""


def _enrich_entry(entry: SourceEntry) -> Candidate | None:
    try:
        frequency, pos_tags = _fetch_word_info(entry.word)
        synonyms = _fetch_synonyms(entry.word)
    except Exception:
        return None
    if not synonyms:
        return None
    answer_data = _choose_answer(entry.word, entry.gloss, synonyms)
    if answer_data is None:
        return None
    answer, answer_source, answer_score = answer_data
    return Candidate(
        word=entry.word,
        gloss=entry.gloss,
        gloss_tokens=tuple(
            token.lower()
            for token in re.findall(r"[A-Za-z]+", entry.gloss)
            if len(token) > 1
        ),
        source_index=entry.source_index,
        difficulty=_assign_difficulty(frequency),
        frequency=frequency,
        pos=pos_tags,
        synonyms=synonyms,
        answer=answer,
        answer_pos=_primary_pos(next((hit.pos for hit in synonyms if hit.word == answer), pos_tags)),
        answer_source=answer_source,
        answer_score=answer_score,
    )


def _select_candidates(candidates: list[Candidate]) -> list[Candidate]:
    buckets: dict[str, list[Candidate]] = {difficulty: [] for difficulty in DIFFICULTY_ORDER}
    for candidate in candidates:
        if candidate.difficulty in buckets:
            buckets[candidate.difficulty].append(candidate)

    def sort_key(
        candidate: Candidate, difficulty: str
    ) -> tuple[float, float, float, int, int, str]:
        confidence = 1.0 if candidate.answer_source == "gloss" else 0.0
        if difficulty in {"Easy", "Medium"}:
            return (
                -confidence,
                -candidate.answer_score,
                -candidate.frequency,
                len(candidate.word),
                candidate.source_index,
                candidate.word,
            )
        return (
            -confidence,
            -candidate.answer_score,
            candidate.frequency,
            -len(candidate.word),
            candidate.source_index,
            candidate.word,
        )

    selected: list[Candidate] = []
    for difficulty in DIFFICULTY_ORDER:
        ranked = sorted(buckets[difficulty], key=lambda candidate: sort_key(candidate, difficulty))
        chosen = ranked[: TARGET_COUNTS[difficulty]]
        if len(chosen) != TARGET_COUNTS[difficulty]:
            raise ValueError(
                f"expected {TARGET_COUNTS[difficulty]} {difficulty} items, got {len(chosen)}"
            )
        selected.extend(chosen)
    return selected


def _build_choice_pools(candidates: list[Candidate]) -> dict[str, list[str]]:
    pools: dict[str, list[str]] = {"any": []}
    for candidate in candidates:
        pools["any"].append(candidate.word)
        pools["any"].append(candidate.answer)
        if candidate.primary_pos:
            pools.setdefault(candidate.primary_pos, []).append(candidate.word)
            pools[candidate.primary_pos].append(candidate.answer)
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


def _candidate_primary_pos(candidate: Candidate) -> str:
    return _primary_pos(candidate.pos)


def _build_distractors(candidate: Candidate, pools: dict[str, list[str]], rng: random.Random) -> list[str]:
    banned = {candidate.word, candidate.answer}
    banned.update(candidate.gloss_tokens)
    banned.update(hit.word for hit in candidate.synonyms)
    candidate_pool: list[str] = []
    for key in (candidate.answer_pos, _candidate_primary_pos(candidate), "any"):
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
    return distractors[:3]


def _pick_variant(candidate: Candidate, rng: random.Random) -> str:
    options = list(QUESTION_WEIGHTS[candidate.difficulty])
    if candidate.definition:
        available = {"direct", "context", "definition"}
    else:
        available = {"direct", "context"}
    filtered = [variant for variant in options if variant in available]
    if not filtered:
        filtered = ["direct"]
    return rng.choice(filtered)


def _build_question_text(candidate: Candidate, variant: str, rng: random.Random) -> str:
    template = rng.choice(QUESTION_TEMPLATES[variant])
    context = {
        "word": candidate.word,
        "sentence": _pick_sentence(candidate.word, candidate.difficulty, candidate.pos),
        "definition": candidate.definition or candidate.gloss,
    }
    return _sanitize_text(template(context))


def _build_record(
    candidate: Candidate,
    pools: dict[str, list[str]],
    index: int,
) -> dict[str, object]:
    rng = random.Random(f"{candidate.word}:{candidate.difficulty}:{index}")
    variant = _pick_variant(candidate, rng)
    question = _build_question_text(candidate, variant, rng)
    distractors = _build_distractors(candidate, pools, rng)
    choices = [candidate.answer, *distractors]
    rng.shuffle(choices)
    if candidate.answer not in choices:
        raise ValueError(f"answer missing from choices for {candidate.word}")
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError(f"bad choices for {candidate.word}")

    explanation: str
    if variant == "definition":
        explanation = f'The definition clue points to "{candidate.answer}".'
    elif variant == "context":
        explanation = f'In the sentence, "{candidate.word}" means "{candidate.answer}".'
    else:
        explanation = f'"{candidate.word}" means "{candidate.answer}".'

    tags = [
        _candidate_primary_pos(candidate),
        "synonym",
        "barron",
        candidate.difficulty.lower(),
        variant,
    ]
    if candidate.answer_source == "gloss":
        tags.append("gloss-answer")
    else:
        tags.append("synonym-answer")
    tags.append("definition" if variant == "definition" else "sentence")

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": candidate.difficulty,
        "question": question,
        "choices": choices,
        "answer": candidate.answer,
        "explanation": explanation,
        "tags": _dedupe_preserve_order(tags),
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _validate_bank(questions: list[dict[str, object]], selected: list[Candidate]) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")
    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")
    selected_words = [candidate.word for candidate in selected]
    if len(selected_words) != len(set(selected_words)):
        raise ValueError("target words are not unique")
    counts = {difficulty: 0 for difficulty in DIFFICULTY_ORDER}
    seen_pairs: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        difficulty = str(question["difficulty"])
        if difficulty not in counts:
            raise ValueError(f"unexpected difficulty {difficulty}")
        counts[difficulty] += 1
        choices = list(question["choices"])  # type: ignore[assignment]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")
        key = (str(question["question"]), tuple(sorted(str(choice) for choice in choices)))
        if key in seen_pairs:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_pairs.add(key)
    expected = TARGET_COUNTS
    if counts != expected:
        raise ValueError(f"unexpected difficulty distribution: {counts}")


def main() -> int:
    source_response = _get(SOURCE_URL, timeout=30)
    source_entries = _parse_source_entries(source_response.text)
    if not source_entries:
        raise RuntimeError("no source entries parsed from Barron list")

    with cf.ThreadPoolExecutor(max_workers=24) as executor:
        candidates = [candidate for candidate in executor.map(_enrich_entry, source_entries) if candidate]

    selected = _select_candidates(candidates)

    with cf.ThreadPoolExecutor(max_workers=8) as executor:
        definitions = list(executor.map(lambda c: _build_definition(c.word, c.pos), selected))

    selected = [replace(candidate, definition=definition) for candidate, definition in zip(selected, definitions)]

    pools = _build_choice_pools(selected)
    questions = [_build_record(candidate, pools, index) for index, candidate in enumerate(selected, start=1)]
    _validate_bank(questions, selected)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(
        json.dumps(questions, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
