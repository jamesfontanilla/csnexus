"""Pseudo-AI flashcard generator — deterministic heuristics only.

Extracts terms from lesson markdown content and generates flashcards
using regex patterns, word frequency classification, and template-based
card generation. No paid LLM APIs.

Requirements: 11.1-11.10
"""

from __future__ import annotations

import random
import re
from dataclasses import dataclass, field
from enum import Enum


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GeneratedCardType(str, Enum):
    BASIC = "basic"
    CLOZE = "cloze"
    MCQ = "mcq"


@dataclass
class GeneratedCard:
    """A single card produced by the generator, pending user approval."""

    front: str
    back: str
    card_type: GeneratedCardType
    difficulty: Difficulty
    mnemonic: str | None = None
    source_term: str = ""


@dataclass
class GenerationResult:
    """Complete output of a generation run."""

    cards: list[GeneratedCard] = field(default_factory=list)
    terms_extracted: int = 0
    lesson_id: int = 0
    error: str | None = None


# ---------------------------------------------------------------------------
# Common English words (simplified frequency list for difficulty classification)
# Words in this set are considered "easy" (high frequency).
# ---------------------------------------------------------------------------

_COMMON_WORDS: frozenset[str] = frozenset({
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "i",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her",
    "she", "or", "an", "will", "my", "one", "all", "would", "there",
    "their", "what", "so", "up", "out", "if", "about", "who", "get",
    "which", "go", "me", "when", "make", "can", "like", "time", "no",
    "just", "him", "know", "take", "people", "into", "year", "your",
    "good", "some", "could", "them", "see", "other", "than", "then",
    "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first",
    "well", "way", "even", "new", "want", "because", "any", "these",
    "give", "day", "most", "us", "is", "are", "was", "were", "been",
    "has", "had", "did", "does", "may", "might", "must", "shall",
    "should", "need", "used", "word", "each", "many", "number",
    "part", "find", "long", "down", "side", "water", "more", "write",
    "call", "very", "still", "between", "never", "last", "let",
    "thought", "city", "tree", "cross", "farm", "hard", "start",
    "story", "saw", "far", "sea", "draw", "left", "late", "run",
    "while", "press", "close", "night", "real", "life", "few",
    "north", "open", "seem", "together", "next", "white", "children",
    "begin", "got", "walk", "example", "ease", "paper", "group",
    "always", "music", "those", "both", "mark", "often", "letter",
    "until", "mile", "river", "car", "feet", "care", "second",
    "book", "carry", "took", "science", "eat", "room", "friend",
    "began", "idea", "fish", "mountain", "stop", "once", "base",
    "hear", "horse", "cut", "sure", "watch", "color", "face", "wood",
    "main", "enough", "plain", "girl", "usual", "young", "ready",
    "above", "ever", "red", "list", "though", "feel", "talk", "bird",
    "soon", "body", "dog", "family", "direct", "pose", "leave",
    "song", "measure", "door", "product", "black", "short", "class",
    "wind", "question", "happen", "complete", "ship", "area", "half",
    "rock", "order", "fire", "south", "problem", "piece", "told",
    "knew", "pass", "since", "top", "whole", "king", "space", "heard",
    "best", "hour", "better", "true", "during", "hundred", "five",
    "remember", "step", "early", "hold", "west", "ground", "interest",
    "reach", "fast", "verb", "sing", "listen", "six", "table",
    "travel", "less", "morning", "ten", "simple", "several", "vowel",
    "toward", "war", "lay", "against", "pattern", "slow", "center",
    "love", "person", "money", "serve", "appear", "road", "map",
    "rain", "rule", "govern", "pull", "cold", "notice", "voice",
    "unit", "power", "town", "fine", "certain", "fly", "fall", "lead",
    "cry", "dark", "machine", "note", "wait", "plan", "figure",
    "star", "box", "noun", "field", "rest", "correct", "able",
    "pound", "done", "beauty", "drive", "stood", "contain", "front",
    "teach", "week", "final", "gave", "green", "oh", "quick",
    "develop", "ocean", "warm", "free", "minute", "strong", "special",
    "mind", "behind", "clear", "tail", "produce", "fact", "street",
    "inch", "multiply", "nothing", "course", "stay", "wheel", "full",
    "force", "blue", "object", "decide", "surface", "deep", "moon",
    "island", "foot", "system", "busy", "test", "record", "boat",
    "common", "gold", "possible", "plane", "stead", "dry", "wonder",
    "laugh", "thousand", "ago", "ran", "check", "game", "shape",
    "equate", "hot", "miss", "brought", "heat", "snow", "tire",
    "bring", "yes", "distant", "fill", "east", "paint", "language",
    "among", "grand", "ball", "yet", "wave", "drop", "heart", "am",
    "present", "heavy", "dance", "engine", "position", "arm",
    "wide", "sail", "material", "size", "vary", "settle", "speak",
    "weight", "general", "ice", "matter", "circle", "pair", "include",
    "divide", "syllable", "felt", "perhaps", "pick", "sudden",
    "count", "square", "reason", "length", "represent", "art",
    "subject", "region", "energy", "probable", "bed", "dream",
    "sentence", "supply", "wish", "definition",
})


# ---------------------------------------------------------------------------
# Term Extraction
# ---------------------------------------------------------------------------


@dataclass
class ExtractedTerm:
    """A term-definition pair extracted from lesson content."""

    term: str
    definition: str


def _extract_terms(content: str) -> list[ExtractedTerm]:
    """Extract term-definition pairs from markdown content.

    Patterns recognized:
    1. "Term: Definition" (colon separator)
    2. "Term — Definition" (em-dash separator)
    3. **bold term** followed by definition sentence
    4. *italic term* followed by definition sentence
    5. Markdown table rows (first column = term, second = definition)
    """
    terms: list[ExtractedTerm] = []
    seen_terms: set[str] = set()

    lines = content.split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        extracted = _try_extract_from_line(line)
        if extracted:
            for term in extracted:
                normalized = term.term.lower().strip()
                if normalized and normalized not in seen_terms and len(normalized) > 1:
                    seen_terms.add(normalized)
                    terms.append(term)

    return terms


def _try_extract_from_line(line: str) -> list[ExtractedTerm]:
    """Try all extraction patterns on a single line."""
    results: list[ExtractedTerm] = []

    # Pattern 1: "Term: Definition" (but not markdown headers or URLs)
    if not line.startswith("#") and not line.startswith("http"):
        match = re.match(r"^([A-Z][^:]{1,80}):\s+(.{10,})", line)
        if match:
            results.append(ExtractedTerm(
                term=match.group(1).strip(),
                definition=match.group(2).strip(),
            ))
            return results

    # Pattern 2: "Term — Definition" (em-dash)
    match = re.match(r"^(.{2,80})\s*[—–]\s*(.{10,})", line)
    if match and not line.startswith("#"):
        results.append(ExtractedTerm(
            term=match.group(1).strip(),
            definition=match.group(2).strip(),
        ))
        return results

    # Pattern 3: **bold term** followed by definition
    match = re.match(r"^\*\*([^*]{2,80})\*\*\s*[-–—:]?\s*(.{10,})", line)
    if match:
        results.append(ExtractedTerm(
            term=match.group(1).strip(),
            definition=match.group(2).strip(),
        ))
        return results

    # Pattern 4: *italic term* followed by definition
    match = re.match(r"^\*([^*]{2,80})\*\s*[-–—:]?\s*(.{10,})", line)
    if match:
        results.append(ExtractedTerm(
            term=match.group(1).strip(),
            definition=match.group(2).strip(),
        ))
        return results

    # Pattern 5: Markdown table row (| term | definition |)
    match = re.match(r"^\|\s*([^|]{2,80})\s*\|\s*([^|]{10,})\s*\|", line)
    if match:
        term = match.group(1).strip()
        defn = match.group(2).strip()
        # Skip table headers (dashes)
        if not re.match(r"^[-:]+$", term) and not re.match(r"^[-:]+$", defn):
            results.append(ExtractedTerm(term=term, definition=defn))
            return results

    return results


# ---------------------------------------------------------------------------
# Difficulty Classification
# ---------------------------------------------------------------------------


def classify_difficulty(
    term: str, word_frequency_list: set[str] | None = None
) -> Difficulty:
    """Classify term difficulty using word frequency (Req 11.4).

    - Easy: all words in the term are common (high frequency)
    - Medium: some words are common, some are not
    - Hard: most words are uncommon (low frequency)
    """
    freq_list = word_frequency_list or _COMMON_WORDS
    words = re.findall(r"[a-zA-Z]+", term.lower())

    if not words:
        return Difficulty.MEDIUM

    common_count = sum(1 for w in words if w in freq_list)
    ratio = common_count / len(words)

    if ratio >= 0.8:
        return Difficulty.EASY
    elif ratio >= 0.4:
        return Difficulty.MEDIUM
    else:
        return Difficulty.HARD


# ---------------------------------------------------------------------------
# Card Generation
# ---------------------------------------------------------------------------


def _generate_basic_card(term: ExtractedTerm, difficulty: Difficulty) -> GeneratedCard:
    """Generate a basic front/back flashcard."""
    front = f"What is {term.term}?"
    back = term.definition
    mnemonic = _generate_mnemonic(term.term, difficulty)
    return GeneratedCard(
        front=front,
        back=back,
        card_type=GeneratedCardType.BASIC,
        difficulty=difficulty,
        mnemonic=mnemonic,
        source_term=term.term,
    )


def _generate_cloze_card(term: ExtractedTerm, difficulty: Difficulty) -> GeneratedCard:
    """Generate a cloze deletion card with {{c1::term::hint}} format."""
    # Replace the term in the definition with a cloze deletion
    hint = term.term[:3] + "..." if len(term.term) > 3 else ""
    cloze_marker = f"{{{{c1::{term.term}::{hint}}}}}" if hint else f"{{{{c1::{term.term}}}}}"

    # Try to embed the term in the definition
    if term.term.lower() in term.definition.lower():
        # Replace the first occurrence (case-insensitive)
        pattern = re.compile(re.escape(term.term), re.IGNORECASE)
        front = pattern.sub(cloze_marker, term.definition, count=1)
    else:
        front = f"{cloze_marker} is defined as: {term.definition}"

    mnemonic = _generate_mnemonic(term.term, difficulty)
    return GeneratedCard(
        front=front,
        back=term.term,
        card_type=GeneratedCardType.CLOZE,
        difficulty=difficulty,
        mnemonic=mnemonic,
        source_term=term.term,
    )


def _generate_mcq_card(
    term: ExtractedTerm,
    difficulty: Difficulty,
    all_terms: list[ExtractedTerm],
) -> GeneratedCard:
    """Generate an MCQ card with distractors from other terms."""
    front = f"Which of the following best defines '{term.term}'?"

    # Correct answer
    correct = term.definition

    # Select distractors from other terms' definitions
    distractors: list[str] = []
    other_terms = [t for t in all_terms if t.term != term.term]
    # Shuffle deterministically based on term content
    rng = random.Random(hash(term.term))
    rng.shuffle(other_terms)

    for other in other_terms[:3]:
        if other.definition != correct:
            distractors.append(other.definition)

    # Pad with generic distractors if needed
    generic = [
        "None of the above",
        "All of the above",
        "This term has no standard definition",
    ]
    while len(distractors) < 3:
        distractors.append(generic[len(distractors)])

    # Build options list with correct answer at a deterministic position
    options = [correct] + distractors[:3]
    rng.shuffle(options)

    import json
    back = json.dumps(options)

    mnemonic = _generate_mnemonic(term.term, difficulty)
    return GeneratedCard(
        front=front,
        back=back,
        card_type=GeneratedCardType.MCQ,
        difficulty=difficulty,
        mnemonic=mnemonic,
        source_term=term.term,
    )


# ---------------------------------------------------------------------------
# Mnemonic Generation
# ---------------------------------------------------------------------------


def _generate_mnemonic(term: str, difficulty: Difficulty) -> str | None:
    """Generate a mnemonic for medium/hard terms (Req 11.6).

    Strategies: acronym, association, or rhyming hint.
    Returns None for easy terms.
    """
    if difficulty == Difficulty.EASY:
        return None

    words = term.split()

    # Acronym strategy: first letters of multi-word terms
    if len(words) >= 2:
        acronym = "".join(w[0].upper() for w in words if w)
        return f"Remember: {acronym} ({term})"

    # Association strategy for single words
    if len(term) > 4:
        return f"Think of '{term[:3]}...' to recall {term}"

    return f"Key term: {term}"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def generate_flashcards(
    lesson_content: str,
    lesson_id: int,
    requested_card_count: int = 25,
    word_frequency_list: set[str] | None = None,
) -> GenerationResult:
    """Extract terms and generate cards from lesson markdown content.

    Card distribution target: 40% basic, 35% cloze, 25% MCQ.
    Returns error if fewer than 10 terms extracted (Req 11.9).
    Enforces 10-50 cards per lesson.

    Args:
        lesson_content: Raw markdown text of the lesson.
        lesson_id: ID of the source lesson.
        requested_card_count: Target number of cards (10-50).
        word_frequency_list: Optional custom frequency list for difficulty.

    Returns:
        GenerationResult with cards or error message.
    """
    # Clamp requested count
    card_count = max(10, min(50, requested_card_count))

    # Extract terms
    terms = _extract_terms(lesson_content)

    if len(terms) < 10:
        return GenerationResult(
            terms_extracted=len(terms),
            lesson_id=lesson_id,
            error=f"Insufficient terms extracted ({len(terms)}). Minimum 10 required.",
        )

    # Limit to requested count
    terms_to_use = terms[:card_count]

    # Classify difficulty for each term
    difficulties = {
        t.term: classify_difficulty(t.term, word_frequency_list)
        for t in terms_to_use
    }

    # Distribute cards: 40% basic, 35% cloze, 25% MCQ
    total = len(terms_to_use)
    num_basic = max(1, round(total * 0.40))
    num_cloze = max(1, round(total * 0.35))
    # Remaining cards are MCQ

    cards: list[GeneratedCard] = []

    # Generate basic cards
    for term in terms_to_use[:num_basic]:
        cards.append(_generate_basic_card(term, difficulties[term.term]))

    # Generate cloze cards
    for term in terms_to_use[num_basic:num_basic + num_cloze]:
        cards.append(_generate_cloze_card(term, difficulties[term.term]))

    # Generate MCQ cards
    for term in terms_to_use[num_basic + num_cloze:]:
        cards.append(_generate_mcq_card(term, difficulties[term.term], terms_to_use))

    return GenerationResult(
        cards=cards,
        terms_extracted=len(terms),
        lesson_id=lesson_id,
    )
