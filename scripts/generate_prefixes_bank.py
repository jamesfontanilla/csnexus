"""Generate the Verbal Ability / Word Meanings / Prefixes question bank.

The bank is built from a transparent prefix-word core plus a frequency-backed
fallback pass. The questions stay focused on prefix meaning, prefix
identification, base-word recognition, and simple meaning matching so the
final set stays aligned with CSE-style vocabulary work.

Usage:
    python scripts/generate_prefixes_bank.py
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
    / "prefixes"
    / "questions.json"
)

FREQUENCY_URL = (
    "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/"
    "content/2018/en/en_50k.txt"
)
DICTIONARY_URL = "https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

SUBTEST = "Verbal Ability"
MODULE = "Word Meanings"
SUBTOPIC = "Prefixes"
CATEGORY = ["Professional", "Sub-Professional"]
LANGUAGE = "English"
TARGET_COUNTS = {"Easy": 150, "Medium": 150, "Hard": 150, "Ultra": 150}
DIFFICULTY_ORDER = ("Easy", "Medium", "Hard", "Ultra")

WORD_RE = re.compile(r"^[a-z]+$")

PREFIX_INFO = {
    "un": {"forms": ("un",), "meaning": "not; opposite of"},
    "re": {"forms": ("re",), "meaning": "again; back"},
    "pre": {"forms": ("pre",), "meaning": "before; earlier than"},
    "dis": {"forms": ("dis",), "meaning": "not; opposite of"},
    "mis": {"forms": ("mis",), "meaning": "wrongly; badly"},
    "non": {"forms": ("non",), "meaning": "not; without"},
    "over": {"forms": ("over",), "meaning": "too much; above"},
    "under": {"forms": ("under",), "meaning": "below; too little"},
    "sub": {"forms": ("sub",), "meaning": "under; below"},
    "anti": {"forms": ("anti",), "meaning": "against; opposed to"},
    "inter": {"forms": ("inter",), "meaning": "between; among"},
    "trans": {"forms": ("trans",), "meaning": "across; through"},
    "fore": {"forms": ("fore",), "meaning": "before; front"},
    "mid": {"forms": ("mid",), "meaning": "middle"},
    "semi": {"forms": ("semi",), "meaning": "half; partly"},
    "out": {"forms": ("out",), "meaning": "beyond; greater; outside"},
    "post": {"forms": ("post",), "meaning": "after; later"},
    "auto": {"forms": ("auto",), "meaning": "self"},
    "multi": {"forms": ("multi",), "meaning": "many; multiple"},
    "micro": {"forms": ("micro",), "meaning": "very small"},
    "hyper": {"forms": ("hyper",), "meaning": "above; beyond; excessive"},
    "counter": {"forms": ("counter",), "meaning": "against; in response to"},
    "tele": {"forms": ("tele",), "meaning": "far; at a distance"},
    "intra": {"forms": ("intra",), "meaning": "within"},
    "pseudo": {"forms": ("pseudo",), "meaning": "false; fake"},
    "ultra": {"forms": ("ultra",), "meaning": "beyond; extreme"},
    "de": {"forms": ("de",), "meaning": "remove; reverse; away"},
    "co": {"forms": ("co",), "meaning": "with; together"},
    "com": {"forms": ("com",), "meaning": "with; together"},
    "con": {"forms": ("con",), "meaning": "with; together"},
    "in": {"forms": ("in",), "meaning": "not; without"},
    "im": {"forms": ("im",), "meaning": "not; without"},
    "il": {"forms": ("il",), "meaning": "not; without"},
    "ir": {"forms": ("ir",), "meaning": "not; without"},
    "bi": {"forms": ("bi",), "meaning": "two; twice"},
    "tri": {"forms": ("tri",), "meaning": "three; triple"},
    "uni": {"forms": ("uni",), "meaning": "one; single"},
    "mono": {"forms": ("mono",), "meaning": "one; single"},
    "poly": {"forms": ("poly",), "meaning": "many; multiple"},
    "pro": {"forms": ("pro",), "meaning": "forward; in favor of"},
    "en": {"forms": ("en",), "meaning": "cause to; put into"},
    "em": {"forms": ("em",), "meaning": "cause to; put into"},
}

FALLBACK_ALLOWED_PREFIXES = {
    "un",
    "pre",
    "dis",
    "mis",
    "non",
    "over",
    "under",
    "sub",
    "anti",
    "inter",
    "trans",
    "fore",
    "mid",
    "semi",
    "out",
    "post",
    "auto",
    "multi",
    "micro",
    "hyper",
    "counter",
    "tele",
    "intra",
    "pseudo",
    "ultra",
}

CORE_WORDS_BY_PREFIX = {
    "un": [
        "unhappy",
        "unsafe",
        "unfair",
        "unable",
        "unkind",
        "unknown",
        "unusual",
        "untrue",
        "unlocked",
        "unfairly",
        "unafraid",
        "unpack",
        "unload",
        "unread",
        "unwise",
        "unfriendly",
        "unwanted",
        "unneeded",
        "unlike",
        "uncover",
        "unopened",
    ],
    "re": [
        "reopen",
        "replay",
        "reuse",
        "remake",
        "recheck",
        "reprint",
        "remind",
        "return",
        "rebuild",
        "rearrange",
        "restart",
        "reenter",
        "reapply",
        "redirect",
        "rejoin",
        "reselect",
        "reintroduce",
        "rewrite",
        "reopen",
        "reconsider",
        "reapply",
    ],
    "pre": [
        "preview",
        "preheat",
        "prepay",
        "pretest",
        "preschool",
        "prearrange",
        "preorder",
        "prewar",
        "preselect",
        "preapprove",
        "predate",
        "prepack",
        "preload",
        "prepaid",
        "preexisting",
        "prelude",
        "premature",
        "precheck",
    ],
    "dis": [
        "disagree",
        "disappear",
        "disapprove",
        "disconnect",
        "dishonest",
        "disobey",
        "dislike",
        "disable",
        "disarm",
        "disband",
        "discredit",
        "disqualify",
        "displease",
        "disfigure",
        "disorder",
        "discontinue",
        "disown",
        "dismantle",
        "distribute",
        "discharge",
    ],
    "mis": [
        "misread",
        "misplace",
        "misjudge",
        "misuse",
        "mislead",
        "misspell",
        "misprint",
        "misbehave",
        "misheard",
        "miscall",
        "misstate",
        "misapply",
        "miscount",
        "misdirect",
        "mistrust",
        "misinform",
        "miscalculate",
        "mismanage",
        "misquote",
    ],
    "non": [
        "nonstop",
        "nonfiction",
        "nonprofit",
        "nonfat",
        "nonstick",
        "nonviolent",
        "nonresident",
        "nonverbal",
        "nonpayment",
        "nonessential",
        "nonmember",
        "nonstandard",
        "nonseason",
        "nonissue",
        "nonrenewable",
        "nonconformist",
        "nonpolitical",
        "nonworking",
        "nonpartisan",
    ],
    "over": [
        "overeat",
        "overcook",
        "overwork",
        "overreact",
        "overpay",
        "overcharge",
        "oversleep",
        "overestimate",
        "overload",
        "overuse",
        "overrule",
        "overstate",
        "overbuild",
        "overhaul",
        "overfill",
        "overcrowd",
        "overheat",
        "overthink",
        "overlook",
    ],
    "under": [
        "underpay",
        "undercook",
        "underestimate",
        "underperform",
        "understate",
        "underuse",
        "undervalue",
        "undercut",
        "underground",
        "undersea",
        "underline",
        "underwrite",
        "underlay",
        "undercount",
        "underwater",
        "undercover",
        "underfed",
        "underdeveloped",
        "underage",
    ],
    "sub": [
        "submarine",
        "submerge",
        "subzero",
        "substandard",
        "subtitle",
        "subdivision",
        "subtopic",
        "subsoil",
        "subway",
        "subscript",
        "subsection",
        "subheading",
        "subsurface",
        "subcontract",
        "subculture",
        "substitute",
        "subsidiary",
        "subatomic",
        "submerge",
    ],
    "anti": [
        "antibiotic",
        "antidote",
        "antisocial",
        "antifreeze",
        "antiseptic",
        "antiwar",
        "antihero",
        "antigravity",
        "antiviral",
        "antitax",
        "antispam",
        "antifraud",
        "antiaging",
        "antibacterial",
        "antirust",
        "antitheft",
        "antipollution",
        "antismoking",
        "antimatter",
    ],
    "inter": [
        "interact",
        "interconnect",
        "international",
        "intercity",
        "interstate",
        "interschool",
        "interpersonal",
        "interrelated",
        "interchange",
        "interoffice",
        "interfaith",
        "interbreed",
        "interlink",
        "interwoven",
        "intercourse",
        "interject",
        "intervene",
        "interview",
        "intersection",
    ],
    "trans": [
        "transport",
        "transfer",
        "translate",
        "transform",
        "transplant",
        "transcribe",
        "transmit",
        "transatlantic",
        "transoceanic",
        "transcontinental",
        "transnational",
        "transmute",
        "transcode",
        "transfigure",
        "transfusion",
        "transcript",
        "transaction",
        "transmission",
        "transgender",
    ],
    "fore": [
        "forecast",
        "foretell",
        "forewarn",
        "foresee",
        "forehead",
        "foreground",
        "forearm",
        "foreword",
        "forewarned",
        "foregone",
        "foretaste",
        "foreman",
        "forelock",
        "foreclose",
        "forefront",
        "foresight",
        "forever",
        "foreseen",
        "foreclosure",
    ],
    "mid": [
        "midday",
        "midnight",
        "midway",
        "midterm",
        "midweek",
        "midsummer",
        "midline",
        "midpoint",
    ],
    "semi": [
        "semicircle",
        "semicolon",
        "semifinal",
        "semiannual",
        "semisweet",
        "semiautomatic",
        "semitransparent",
        "semiconscious",
    ],
    "out": [
        "outgrow",
        "outshine",
        "outnumber",
        "outlast",
        "outpace",
        "outdo",
        "outplay",
        "outsmart",
        "outburst",
    ],
    "post": [
        "postpone",
        "postscript",
        "postgraduate",
        "postwar",
        "postmodern",
        "postdate",
        "postnatal",
        "postseason",
        "posttest",
    ],
    "auto": [
        "autobiography",
        "autograph",
        "automatic",
        "autonomous",
        "autopilot",
        "autoimmune",
        "autocorrect",
        "autofill",
    ],
    "multi": [
        "multiple",
        "multilingual",
        "multimedia",
        "multipurpose",
        "multinational",
        "multistory",
        "multitask",
        "multicolor",
    ],
    "micro": [
        "microscope",
        "microwave",
        "microbe",
        "microchip",
        "microfilm",
        "microsecond",
        "microprocessor",
        "microclimate",
    ],
    "hyper": [
        "hyperactive",
        "hypertension",
        "hypertext",
        "hyperlink",
        "hyperbole",
        "hypercritical",
        "hypersensitive",
        "hypermarket",
    ],
    "counter": [
        "counterattack",
        "counterclockwise",
        "counterfeit",
        "counterbalance",
        "countermeasure",
        "counterclaim",
        "counterexample",
        "counterproductive",
    ],
    "tele": [
        "telephone",
        "television",
        "telescope",
        "telegraph",
        "telecast",
        "telepathy",
        "telephoto",
        "telecommute",
        "telework",
    ],
    "intra": [
        "intramural",
        "intravenous",
        "intranet",
        "intracellular",
        "intrastate",
        "intraocular",
        "intrapersonal",
        "intraoffice",
    ],
    "pseudo": [
        "pseudoscience",
        "pseudonym",
        "pseudopod",
        "pseudocode",
        "pseudointellectual",
        "pseudohistory",
        "pseudomorphic",
        "pseudoreal",
    ],
    "ultra": [
        "ultraviolet",
        "ultrasonic",
        "ultrafast",
        "ultralight",
        "ultramodern",
        "ultraquiet",
        "ultraconservative",
        "ultrafine",
    ],
}

FALLBACK_BLACKLIST = {
    "ability",
    "about",
    "above",
    "accept",
    "access",
    "account",
    "across",
    "actress",
    "address",
    "again",
    "against",
    "ahead",
    "air",
    "allow",
    "alone",
    "along",
    "already",
    "always",
    "among",
    "answer",
    "anyone",
    "appear",
    "apple",
    "around",
    "artist",
    "attack",
    "because",
    "before",
    "behind",
    "belong",
    "better",
    "between",
    "beyond",
    "black",
    "board",
    "body",
    "book",
    "building",
    "business",
    "call",
    "careful",
    "certain",
    "change",
    "child",
    "city",
    "clear",
    "close",
    "college",
    "come",
    "common",
    "company",
    "complete",
    "conduct",
    "connect",
    "consider",
    "contain",
    "continue",
    "control",
    "country",
    "course",
    "cover",
    "create",
    "current",
    "danger",
    "data",
    "day",
    "decide",
    "describe",
    "design",
    "detail",
    "develop",
    "difference",
    "discuss",
    "discover",
    "distance",
    "doctor",
    "education",
    "effect",
    "effort",
    "email",
    "enemy",
    "enjoy",
    "enter",
    "environment",
    "example",
    "experience",
    "family",
    "far",
    "friend",
    "general",
    "good",
    "government",
    "great",
    "group",
    "happen",
    "help",
    "important",
    "information",
    "inside",
    "interest",
    "international",
    "introduce",
    "involve",
    "kind",
    "knowledge",
    "large",
    "learn",
    "less",
    "line",
    "little",
    "long",
    "make",
    "market",
    "middle",
    "money",
    "move",
    "need",
    "night",
    "nothing",
    "number",
    "open",
    "people",
    "place",
    "point",
    "power",
    "press",
    "pretty",
    "problem",
    "produce",
    "project",
    "proper",
    "protect",
    "public",
    "question",
    "real",
    "reason",
    "record",
    "report",
    "return",
    "right",
    "school",
    "second",
    "service",
    "special",
    "state",
    "story",
    "system",
    "thing",
    "time",
    "today",
    "together",
    "understand",
    "use",
    "value",
    "water",
    "work",
}

FALLBACK_KEYWORDS = {
    "un": ("not", "without", "opposite", "lack", "lacking"),
    "pre": ("before", "earlier", "advance", "ahead"),
    "dis": ("not", "away", "apart", "opposite", "reverse", "against"),
    "mis": ("wrong", "wrongly", "badly", "incorrect", "error"),
    "non": ("not", "without", "absence", "lack"),
    "over": ("too", "excessive", "above", "more than", "surpass"),
    "under": ("below", "too little", "less than", "lower", "beneath"),
    "sub": ("under", "below", "beneath", "lesser"),
    "anti": ("against", "opposed", "counter", "prevent", "stop"),
    "inter": ("between", "among", "joint", "mutual"),
    "trans": ("across", "through", "beyond", "change", "transfer"),
    "fore": ("before", "front", "ahead"),
    "mid": ("middle",),
    "semi": ("half", "partly"),
    "out": ("beyond", "outside", "more", "surpass"),
    "post": ("after", "later"),
    "auto": ("self",),
    "multi": ("many", "multiple"),
    "micro": ("small", "tiny"),
    "hyper": ("excessive", "beyond", "above", "too much"),
    "counter": ("against", "opposite", "response", "return"),
    "tele": ("far", "distance"),
    "intra": ("within",),
    "pseudo": ("false", "fake"),
    "ultra": ("extreme", "beyond"),
    "de": ("remove", "reverse", "away", "off", "down"),
}


@dataclass
class WordRecord:
    word: str
    prefix_key: str
    prefix_form: str
    prefix_meaning: str
    difficulty_rank: float
    definition: str = ""

    @property
    def base(self) -> str:
        return self.word[len(self.prefix_form) :]


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _truncate(text: str, limit: int) -> str:
    words = text.split()
    if len(words) <= limit:
        return text
    return " ".join(words[:limit]).rstrip(",;:.!?") + "..."


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
        word = parts[0].lower().strip()
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
        response = requests.get(DICTIONARY_URL.format(word=word), timeout=20)
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


def _extract_prefix_form(word: str) -> tuple[str, str] | None:
    matches: list[tuple[int, str, str]] = []
    for key, info in PREFIX_INFO.items():
        for form in info["forms"]:
            if word.startswith(form) and len(word) > len(form) + 2:
                matches.append((len(form), key, form))
    if not matches:
        return None
    _, key, form = sorted(matches, key=lambda item: (-item[0], item[1], item[2]))[0]
    return key, form


def _collect_core_words(frequency_map: dict[str, int]) -> list[WordRecord]:
    core_words: list[WordRecord] = []
    seen: set[str] = set()
    for prefix_key, words in CORE_WORDS_BY_PREFIX.items():
        info = PREFIX_INFO[prefix_key]
        for word in words:
            if word in seen:
                continue
            extracted = _extract_prefix_form(word)
            if extracted is None:
                continue
            extracted_key, prefix_form = extracted
            if extracted_key != prefix_key:
                continue
            seen.add(word)
            core_words.append(
                WordRecord(
                    word=word,
                    prefix_key=prefix_key,
                    prefix_form=prefix_form,
                    prefix_meaning=info["meaning"],
                    difficulty_rank=float(frequency_map.get(word, 0)),
                )
            )
    return core_words


def _collect_fallback_words(
    frequency_map: dict[str, int],
    existing_words: set[str],
) -> list[WordRecord]:
    words = sorted(
        frequency_map.items(),
        key=lambda item: (-item[1], len(item[0]), item[0]),
    )
    records: list[WordRecord] = []
    for word, frequency in words:
        if word in existing_words or word in FALLBACK_BLACKLIST:
            continue
        extracted = _extract_prefix_form(word)
        if extracted is None:
            continue
        prefix_key, prefix_form = extracted
        if prefix_key not in FALLBACK_ALLOWED_PREFIXES:
            continue
        definition = _fetch_definition(word)
        keywords = FALLBACK_KEYWORDS.get(prefix_key, ())
        if keywords and not any(keyword in definition.lower() for keyword in keywords):
            continue
        records.append(
            WordRecord(
                word=word,
                prefix_key=prefix_key,
                prefix_form=prefix_form,
                prefix_meaning=PREFIX_INFO[prefix_key]["meaning"],
                difficulty_rank=float(frequency),
                definition=definition,
            )
        )
    return records


def _choose_question_kind(record: WordRecord, index: int) -> str:
    if record.prefix_key in {"un", "re", "pre", "dis", "mis", "non", "over", "under", "sub", "anti"}:
        order = ("prefix_meaning", "prefix_id", "base_word", "meaning")
    elif record.prefix_key in {"inter", "trans", "fore", "mid", "semi", "out", "post", "auto", "multi", "micro"}:
        order = ("prefix_id", "prefix_meaning", "meaning", "base_word")
    else:
        order = ("prefix_meaning", "meaning", "prefix_id", "base_word")
    return order[index % len(order)]


def _build_sentence(record: WordRecord, rng: random.Random) -> str:
    base = record.base or record.word
    if record.prefix_key in {"re", "pre", "post", "trans", "out", "over", "under", "dis", "mis"}:
        templates = [
            f'The office asked staff to {record.word} the file before the deadline.',
            f'The team had to {record.word} the plan after the review.',
            f'The supervisor asked them to {record.word} the report carefully.',
        ]
    elif record.prefix_key in {"sub", "inter", "counter", "tele", "intra"}:
        templates = [
            f'The lesson used the word "{record.word}" in a technical context.',
            f'The report included the word "{record.word}" in a science example.',
            f'The article used "{record.word}" to describe a process or relation.',
        ]
    else:
        templates = [
            f'The word "{record.word}" appeared in a vocabulary exercise.',
            f'The teacher used "{record.word}" in a sentence.',
            f'The memo included the word "{record.word}" for practice.',
        ]
    sentence = rng.choice(templates)
    return sentence if sentence.endswith(".") else f"{sentence}."


def _build_distractors(
    record: WordRecord,
    pools: dict[str, list[str]],
    rng: random.Random,
    *,
    question_kind: str,
) -> list[str]:
    if question_kind == "prefix_id":
        answer = record.prefix_form + "-"
        pool = pools["prefixes"]
        banned = {answer}
    elif question_kind == "prefix_meaning":
        answer = record.prefix_meaning
        pool = pools["meanings"]
        banned = {answer}
    elif question_kind == "base_word":
        answer = record.base
        pool = pools["bases"]
        banned = {answer, record.word}
    else:
        answer = record.word
        pool = pools["words"]
        banned = {answer}

    options = [item for item in pool if item not in banned]
    rng.shuffle(options)
    distractors = options[:3]
    if len(distractors) < 3:
        fallback = [item for item in pools["words"] if item not in banned and item not in distractors]
        rng.shuffle(fallback)
        for item in fallback:
            distractors.append(item)
            if len(distractors) == 3:
                break
    return distractors[:3]


def _build_question_text(
    record: WordRecord,
    question_kind: str,
    rng: random.Random,
    definition: str,
) -> str:
    prefix_label = f"{record.prefix_form}-"
    if question_kind == "prefix_meaning":
        templates = [
            f'In "{record.word}", what does the prefix {prefix_label} mean?',
            f'What is the meaning of the prefix in "{record.word}"?',
            f'Which meaning best matches the prefix in "{record.word}"?',
        ]
    elif question_kind == "prefix_id":
        templates = [
            f'Which prefix appears in "{record.word}"?',
            f'What prefix is used at the start of "{record.word}"?',
            f'Which prefix forms the beginning of "{record.word}"?',
        ]
    elif question_kind == "base_word":
        templates = [
            f'What is the base word in "{record.word}"?',
            f'Which root word best matches "{record.word}"?',
            f'What word is left after removing the prefix from "{record.word}"?',
        ]
    else:
        if definition:
            templates = [
                f'Which word matches this meaning: "{definition}"?',
                f'Pick the word that best fits this short definition: "{definition}".',
                f'Which choice is closest to the meaning "{definition}"?',
            ]
        else:
            sentence = _build_sentence(record, rng)
            templates = [
                f'Which word best fits the sentence "{sentence}"?',
                f'In the sentence "{sentence}", which word is the best match?',
                f'Which choice would complete the sentence "{sentence}"?',
            ]
    return rng.choice(templates)


def _build_record(
    record: WordRecord,
    pools: dict[str, list[str]],
    index: int,
) -> dict[str, object]:
    rng = random.Random(f"{record.word}:{index}")
    definition = record.definition or _fetch_definition(record.word)
    question_kind = _choose_question_kind(record, index)
    question = _build_question_text(record, question_kind, rng, definition)
    distractors = _build_distractors(record, pools, rng, question_kind=question_kind)

    if question_kind == "prefix_id":
        answer = f"{record.prefix_form}-"
    elif question_kind == "prefix_meaning":
        answer = record.prefix_meaning
    elif question_kind == "base_word":
        answer = record.base
    else:
        answer = record.word

    choices = [answer, *distractors]
    rng.shuffle(choices)
    if len(choices) != 4 or len(set(choices)) != 4:
        raise ValueError(f"bad choices for {record.word}")
    if answer not in choices:
        raise ValueError(f"answer missing for {record.word}")

    if question_kind == "prefix_id":
        explanation = f'The word begins with {record.prefix_form}-, which signals {record.prefix_meaning}.'
    elif question_kind == "prefix_meaning":
        explanation = f'The prefix {record.prefix_form}- usually means {record.prefix_meaning}.'
    elif question_kind == "base_word":
        explanation = f'Removing the prefix leaves the base word "{record.base}".'
    else:
        if definition:
            explanation = f'The dictionary clue points to "{record.word}".'
        else:
            explanation = f'"{record.word}" is the word formed with the prefix {record.prefix_form}-.'

    tags = [
        "prefix",
        record.prefix_key,
        question_kind,
        "word-meaning",
        "cse",
    ]
    if question_kind == "prefix_id":
        tags.append("prefix-form")
    if question_kind == "base_word":
        tags.append("root-word")
    if question_kind == "meaning":
        tags.append("definition")

    return {
        "id": index,
        "subtest": SUBTEST,
        "module": MODULE,
        "subtopic": SUBTOPIC,
        "difficulty": "",
        "question": question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": _dedupe(tags),
        "category": CATEGORY,
        "language": LANGUAGE,
    }


def _select_records(records: list[WordRecord]) -> list[WordRecord]:
    if len(records) < 600:
        raise RuntimeError(f"expected at least 600 prefix candidates, got {len(records)}")

    # Higher frequency first, then shorter words, then alphabetical.
    ordered = sorted(records, key=lambda item: (-item.difficulty_rank, len(item.word), item.word))

    bands = [
        ordered[: len(ordered) // 4],
        ordered[len(ordered) // 4 : len(ordered) // 2],
        ordered[len(ordered) // 2 : (len(ordered) * 3) // 4],
        ordered[(len(ordered) * 3) // 4 :],
    ]

    selected: list[WordRecord] = []
    for difficulty, band in zip(DIFFICULTY_ORDER, bands):
        if len(band) < TARGET_COUNTS[difficulty]:
            raise RuntimeError(
                f"not enough {difficulty.lower()} candidates: needed {TARGET_COUNTS[difficulty]}, got {len(band)}"
            )
        selected.extend(band[: TARGET_COUNTS[difficulty]])
    return selected


def _build_pools(records: list[WordRecord]) -> dict[str, list[str]]:
    prefixes = []
    meanings = []
    bases = []
    words = []
    for record in records:
        prefixes.append(f"{record.prefix_form}-")
        meanings.append(record.prefix_meaning)
        bases.append(record.base)
        words.append(record.word)
    pools = {
        "prefixes": _dedupe(prefixes),
        "meanings": _dedupe(meanings),
        "bases": _dedupe(bases),
        "words": _dedupe(words),
    }
    return pools


def _validate_bank(questions: list[dict[str, object]], records: list[WordRecord]) -> None:
    if len(questions) != 600:
        raise RuntimeError(f"expected 600 questions, got {len(questions)}")
    ids = [question["id"] for question in questions]
    if ids != list(range(1, 601)):
        raise RuntimeError("question ids are not sequential from 1 to 600")
    words = [record.word for record in records]
    if len(words) != len(set(words)):
        raise RuntimeError("target words are not unique")
    seen_questions: set[tuple[str, tuple[str, ...]]] = set()
    counts = Counter(str(question["difficulty"]) for question in questions)
    if counts != TARGET_COUNTS:
        raise RuntimeError(f"unexpected difficulty distribution: {dict(counts)}")
    for question in questions:
        choices = list(question["choices"])  # type: ignore[assignment]
        if len(choices) != 4:
            raise RuntimeError(f"question {question['id']} does not have 4 choices")
        if len(set(choices)) != 4:
            raise RuntimeError(f"question {question['id']} has duplicate choices")
        answer = str(question["answer"])
        if answer not in choices:
            raise RuntimeError(f"answer missing from choices for question {question['id']}")
        key = (str(question["question"]), tuple(sorted(str(choice) for choice in choices)))
        if key in seen_questions:
            raise RuntimeError(f"duplicate question and choice set at id {question['id']}")
        seen_questions.add(key)


def main() -> int:
    frequency_map = _download_frequency_map()
    core_records = _collect_core_words(frequency_map)
    fallback_records = _collect_fallback_words(frequency_map, {record.word for record in core_records})
    records = _select_records([*core_records, *fallback_records])

    for record in records:
        record.definition = record.definition or _fetch_definition(record.word)

    pools = _build_pools(records)
    questions = [_build_record(record, pools, index) for index, record in enumerate(records, start=1)]

    # fill in difficulty after the bank is built, based on the selected band.
    for index, question in enumerate(questions, start=1):
        if index <= 150:
            question["difficulty"] = "Easy"
        elif index <= 300:
            question["difficulty"] = "Medium"
        elif index <= 450:
            question["difficulty"] = "Hard"
        else:
            question["difficulty"] = "Ultra"

    _validate_bank(questions, records)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(questions, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(questions)} questions to {OUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
