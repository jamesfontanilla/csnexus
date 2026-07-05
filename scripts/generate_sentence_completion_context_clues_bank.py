"""Generate the Verbal Ability / Sentence Completion / Context Clues bank.

This generator reuses the same WordNet-backed record selection as the existing
context-clues bank, but it flips the output into actual sentence-completion
items. The bank keeps the same 600-item / 150-per-difficulty split and uses a
small clue-type slice so the questions stay varied.

Usage:
    python scripts/generate_sentence_completion_context_clues_bank.py
"""

from __future__ import annotations

import json
import random
import re
import sys
from collections import Counter
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts import generate_context_clues_bank as base

OUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "seed"
    / "questions"
    / "verbal-ability"
    / "sentence-completion"
    / "context-clues"
    / "questions.json"
)

SUBTEST = "Verbal Ability"
MODULE = "Sentence Completion"
SUBTOPIC = "Context Clues"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"

TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = base.DIFFICULTY_ORDER
CLUE_TYPE_TARGETS = {"Easy": 25, "Medium": 25, "Hard": 25, "Ultra": 25}

COMPLETION_STEMS = [
    lambda q: f'Which word best completes this {q["hint"]} sentence "{q["sentence"]}"?',
    lambda q: f'Choose the word that best fills the blank in this {q["hint"]} sentence "{q["sentence"]}".',
    lambda q: f'What is the best word for the blank in this {q["hint"]} sentence "{q["sentence"]}"?',
    lambda q: f'Which choice best fits the blank in this {q["hint"]} sentence "{q["sentence"]}"?',
    lambda q: f'Which word most precisely completes this {q["hint"]} sentence "{q["sentence"]}"?',
]

CLUE_TYPE_STEMS = [
    lambda q: f'What type of context clue is used in this {q["hint"]} sentence "{q["sentence"]}"?',
    lambda q: f'This {q["hint"]} sentence "{q["sentence"]}" uses which context clue to help you choose the blank?',
    lambda q: f'Which context clue best explains the blank in this {q["hint"]} sentence "{q["sentence"]}"?',
]

CONTEXT_HINT_PREFIXES = [
    "office",
    "work",
    "formal",
    "team",
    "public",
    "news",
    "policy",
    "meeting",
    "classroom",
    "exam",
    "email",
    "briefing",
]

CONTEXT_HINT_SUFFIXES = [
    "memo",
    "report",
    "notice",
    "update",
    "announcement",
    "statement",
    "proposal",
    "review",
    "summary",
    "message",
]

QUESTION_CONTEXT_HINTS = [
    f"{prefix} {suffix}"
    for prefix in CONTEXT_HINT_PREFIXES
    for suffix in CONTEXT_HINT_SUFFIXES
]

COMPLETION_SENTENCE_TEMPLATES = {
    "adj": {
        "definition": [
            "The ____ report was {meaning}.",
            "The ____ proposal was {meaning}.",
            "The ____ response was {meaning}.",
        ],
        "restatement": [
            "The ____ report, or {meaning}, needed little revision.",
            "The ____ proposal, in other words, was {meaning}.",
            "The ____ response, that is, {meaning}, was clear.",
        ],
        "contrast": [
            "Although the first draft was {antonym}, the final draft was ____.",
            "The rule was {antonym}, but the new version was ____.",
            "The initial plan was {antonym}; the revised plan was ____.",
        ],
        "punctuation": [
            "The ____ report - {meaning} - needed little revision.",
            "The ____ proposal ({meaning}) needed revision.",
            "The ____ response: {meaning}.",
        ],
        "comparison": [
            "Like a {meaning} report, the ____ memo needed little editing.",
            "As a {meaning} plan, the ____ one was easy to follow.",
            "Like a {meaning} response, the ____ note was clear.",
        ],
    },
    "v": {
        "definition": [
            "To ____ means to {meaning}.",
            "The team decided to ____, or to {meaning}, before noon.",
            "The committee asked the group to ____, that is, to {meaning}, after the review.",
        ],
        "restatement": [
            "The team will ____, or to {meaning}, before noon.",
            "The committee decided to ____, that is, to {meaning}, after the review.",
            "They plan to ____, in other words, to {meaning}, after the review.",
        ],
        "contrast": [
            "Although they once {antonym}, they now ____.",
            "They used to {antonym}, but today they ____.",
            "The old board would {antonym}, whereas the new board will ____.",
        ],
        "punctuation": [
            "The team will ____ - to {meaning} - before noon.",
            "The committee decided to ____ ({meaning}) after the review.",
            "They plan to ____: {meaning}.",
        ],
    },
    "n": {
        "definition": [
            "The ____ was {meaning}.",
            "The committee discussed the ____ at the meeting.",
            "The report included a clear ____ from the manager.",
        ],
        "restatement": [
            "The ____, or {meaning}, was placed on the desk.",
            "The ____, in other words, was {meaning}.",
            "The ____, also known as {meaning}, was brought to the meeting.",
        ],
        "contrast": [
            "The old plan was weak, but the new ____ was strong.",
            "The first draft failed; the revised ____ worked well.",
            "The old policy was rigid, but the new ____ was flexible.",
        ],
        "punctuation": [
            "The ____ ({meaning}) was placed on the desk.",
            "The ____: {meaning}.",
            "The ____ - {meaning} - was brought to the meeting.",
        ],
    },
    "adv": {
        "definition": [
            "She spoke ____, meaning {meaning}.",
            "He moved ____, which means {meaning}.",
            "The answer was given ____ during the briefing.",
        ],
        "restatement": [
            "She spoke ____, or {meaning}, during the briefing.",
            "He moved ____, or {meaning}, across the room.",
            "The answer was given ____, in other words, {meaning}.",
        ],
        "contrast": [
            "Although others spoke {antonym}, she spoke ____.",
            "The first team moved {antonym}, but the second moved ____.",
            "They answered {antonym}, yet she answered ____.",
        ],
        "punctuation": [
            "She spoke ____ ({meaning}) during the briefing.",
            "He moved ____ - {meaning} - across the room.",
            "The answer was given ____: {meaning}.",
        ],
    },
}


def _sanitize_text(text: str) -> str:
    return base._sanitize_text(text)


def _meaning_phrase(record: base.SenseRecord) -> str:
    phrase = (record.gloss or record.answer or "").strip()
    phrase = re.sub(r"\s+", " ", phrase)
    phrase = re.sub(r"^(?:to|a|an|the)\s+", "", phrase, flags=re.IGNORECASE)
    return phrase or record.answer


def _blank_word(sentence: str, word: str) -> str:
    pattern = re.compile(rf"\b{re.escape(word)}\b")
    return pattern.sub("____", sentence, count=1)


def _completion_question_text(sentence: str, rng: random.Random, context_hint: str) -> str:
    template = rng.choice(COMPLETION_STEMS)
    payload = {"sentence": sentence, "hint": context_hint}
    return _sanitize_text(template(payload))


def _clue_type_question_text(sentence: str, rng: random.Random, context_hint: str) -> str:
    template = rng.choice(CLUE_TYPE_STEMS)
    payload = {"sentence": sentence, "hint": context_hint}
    return _sanitize_text(template(payload))


def _build_explanation(
    record: base.SenseRecord,
    variant: str,
    kind: str,
) -> str:
    meaning = _meaning_phrase(record)
    if kind == "clue_type":
        return f"The sentence uses a {variant} clue to help you choose the blank."
    if variant == "contrast":
        ant = base._pick_antonym(record, random.Random(record.word))
        if ant and ant != record.word:
            return (
                f'The contrast clue points away from "{ant}" and toward '
                f'"{record.word}", which means "{meaning}".'
            )
        return f'"{record.word}" means "{meaning}", and the contrast clue supports it.'
    if variant == "comparison":
        return (
            f'The comparison clue shows that "{record.word}" fits the same idea as '
            f'"{meaning}".'
        )
    if variant == "punctuation":
        return f'The punctuation clue explains that "{record.word}" means "{meaning}".'
    if variant == "restatement":
        return f'The restatement clue repeats the meaning of "{record.word}" as "{meaning}".'
    return f'The definition clue points to "{record.word}", which means "{meaning}".'


def _build_completion_distractors(
    record: base.SenseRecord,
    pools: dict[str, list[str]],
    rng: random.Random,
) -> list[str]:
    return base._build_meaning_distractors(record, pools, rng)


def _build_clue_type_distractors(answer: str, rng: random.Random) -> list[str]:
    distractors = [clue for clue in base.CLUE_TYPES if clue != answer]
    rng.shuffle(distractors)
    return distractors[:3]


def _build_record(
    summary: base.WordSummary,
    difficulty: str,
    kind: str,
    variant: str,
    pools: dict[str, list[str]],
    index: int,
    attempt: int = 0,
) -> dict[str, object]:
    record = summary.record
    rng = random.Random(f"{summary.word}:{difficulty}:{kind}:{variant}:{index}")
    meaning = _meaning_phrase(record)
    templates = COMPLETION_SENTENCE_TEMPLATES.get(record.pos, COMPLETION_SENTENCE_TEMPLATES["n"])
    template_choices = templates.get(variant) or templates.get("definition") or ["The ____ was {meaning}."]
    template = rng.choice(template_choices)
    full_sentence = template.format(
        meaning=meaning,
        antonym=base._pick_antonym(record, rng),
    )
    sentence = _blank_word(full_sentence, record.word)
    hint_seed = sum((index + 1) * ord(char) for index, char in enumerate(summary.word)) + (attempt * 13)
    context_hint = QUESTION_CONTEXT_HINTS[hint_seed % len(QUESTION_CONTEXT_HINTS)]

    if kind == "clue_type":
        answer = variant
        choices = [answer, *_build_clue_type_distractors(answer, rng)]
        rng.shuffle(choices)
        question = _clue_type_question_text(sentence, rng, context_hint)
    else:
        answer = record.word
        distractors = _build_completion_distractors(record, pools, rng)
        choices = [answer, *distractors]
        rng.shuffle(choices)
        question = _completion_question_text(sentence, rng, context_hint)

    if answer not in choices:
        raise ValueError(f"answer missing from choices for {record.word}")
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError(f"bad choices for {record.word}")

    explanation = _build_explanation(record, variant, kind)
    item_kind = "clue_type" if kind == "clue_type" else "completion"
    tags = [
        record.pos,
        "sentence-completion",
        "context-clue",
        item_kind,
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
        "tags": base._dedupe_preserve_order(tags),
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _validate_bank(
    questions: list[dict[str, object]],
    selected: list[tuple[str, base.WordSummary]],
) -> None:
    if len(questions) != 600:
        raise ValueError(f"expected 600 questions, got {len(questions)}")

    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise ValueError("question ids are not sequential from 1 to 600")

    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise ValueError(f"unexpected difficulty distribution: {dict(counts)}")

    kind_counts = Counter(
        "clue_type" if "clue_type" in question["tags"] else "completion"
        for question in questions
    )
    expected_kinds = {"completion": 500, "clue_type": 100}
    if kind_counts != expected_kinds:
        raise ValueError(f"unexpected kind distribution: {dict(kind_counts)}")

    clue_counts = Counter(
        str(question["difficulty"]) for question in questions if "clue_type" in question["tags"]
    )
    if clue_counts != CLUE_TYPE_TARGETS:
        raise ValueError(f"unexpected clue-type distribution: {dict(clue_counts)}")

    question_texts = [str(question["question"]) for question in questions]
    if len(question_texts) != len(set(question_texts)):
        raise ValueError("question texts are not unique")

    target_words = [summary.word for _kind, summary in selected]
    if len(target_words) != len(set(target_words)):
        raise ValueError("target words are not unique")

    seen_pairs: set[tuple[str, tuple[str, ...]]] = set()
    for question in questions:
        choices = [str(choice) for choice in question["choices"]]  # type: ignore[index]
        if len(choices) != 4:
            raise ValueError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise ValueError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise ValueError(f"answer missing from choices for question {question['id']}")
        question_key = (str(question["question"]), tuple(sorted(choices)))
        if question_key in seen_pairs:
            raise ValueError(f"duplicate question and choice set at id {question['id']}")
        seen_pairs.add(question_key)


def main() -> int:
    frequency_map = base._download_frequency_map()
    archive_bytes = base._load_wordnet_source()
    archive = base.zipfile.ZipFile(base.io.BytesIO(archive_bytes))
    records_by_word, _all_words_by_pos = base._build_records(archive, frequency_map)

    summaries: list[base.WordSummary] = []
    for word, records in records_by_word.items():
        best_record = base._choose_best_record(records)
        if best_record.target_frequency <= 0:
            continue
        summaries.append(
            base.WordSummary(
                word=word,
                frequency=best_record.target_frequency,
                record=best_record,
            )
        )

    if len(summaries) < 600:
        raise RuntimeError(f"not enough usable context-clue candidates: {len(summaries)}")

    selected = base._select_candidates(summaries)
    pools = base._group_pools(selected)

    questions: list[dict[str, object]] = []
    seen_questions: set[str] = set()
    seen_keys: set[tuple[str, tuple[str, ...]]] = set()
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
            variant = base._pick_variant(summary.record, difficulty, kind, variant_rng)
            built = None
            for attempt in range(len(QUESTION_CONTEXT_HINTS)):
                candidate = _build_record(
                    summary=summary,
                    difficulty=difficulty,
                    kind=kind,
                    variant=variant,
                    pools=pools,
                    index=index,
                    attempt=attempt,
                )
                question_text = str(candidate["question"])
                if question_text in seen_questions:
                    continue
                key = (str(candidate["question"]), tuple(sorted(str(choice) for choice in candidate["choices"])))
                if key in seen_keys:
                    continue
                seen_questions.add(question_text)
                seen_keys.add(key)
                built = candidate
                break
            if built is None:
                raise RuntimeError(f"could not produce a unique question for {summary.word}")
            questions.append(built)
            index += 1

    _validate_bank(questions, selected)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
