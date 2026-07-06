"""Data-driven registries for semantic sections and blocks."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


def normalize_heading(text: str) -> str:
    """Normalize a heading for semantic matching."""

    stripped = " ".join(text.replace("\u2014", "-").replace("\u2013", "-").split())
    stripped = stripped.strip(" \t\r\n-:·•")
    stripped = re.sub(r"^[#>*\-\s]+", "", stripped)
    stripped = re.sub(
        r"^(?:\d+(?:\.\d+)*|[ivxlcdm]+|[A-Z])[\).:-]?\s+",
        "",
        stripped,
        flags=re.IGNORECASE,
    )
    return stripped.strip()


def _slugify_heading(text: str) -> str:
    cleaned = normalize_heading(text)
    cleaned = cleaned.lower()
    cleaned = re.sub(r"[^a-z0-9]+", "-", cleaned)
    return cleaned.strip("-")


@dataclass(frozen=True, slots=True)
class SectionDefinition:
    """A registered section shape."""

    kind: str
    canonical_title: str
    aliases: tuple[str, ...] = ()
    parent_kind: str | None = None
    level: int | None = None
    role: str = "section"
    description: str = ""

    @property
    def lookup_keys(self) -> tuple[str, ...]:
        keys = [self.canonical_title, *self.aliases]
        return tuple(_slugify_heading(key) for key in keys if key.strip())


@dataclass(frozen=True, slots=True)
class BlockDefinition:
    """A registered block shape."""

    kind: str
    output_type: str
    aliases: tuple[str, ...] = ()
    description: str = ""
    language_aliases: tuple[str, ...] = ()


@dataclass(slots=True)
class SectionMatch:
    """The result of resolving a heading against the section registry."""

    kind: str
    title: str
    display_title: str
    role: str = "section"
    registered: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BlockMatch:
    """The result of resolving a markdown block."""

    kind: str
    output_type: str
    content: Any
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    children: list[Any] = field(default_factory=list)


class SectionRegistry:
    """Registry of semantic section names and aliases."""

    def __init__(self) -> None:
        self._definitions: dict[str, SectionDefinition] = {}
        self._lookup: dict[str, SectionDefinition] = {}

    def register(self, definition: SectionDefinition) -> None:
        self._definitions[definition.kind] = definition
        for key in definition.lookup_keys:
            self._lookup[key] = definition

    def resolve_major(self, title: str) -> SectionDefinition | None:
        key = _slugify_heading(title)
        definition = self._lookup.get(key)
        if definition is None:
            return None
        if definition.parent_kind is not None:
            return None
        return definition

    def resolve_child(
        self,
        title: str,
        *,
        parent_kind: str,
        level: int,
    ) -> SectionDefinition | None:
        key = _slugify_heading(title)
        definition = self._lookup.get(key)
        if definition is None:
            return None
        if definition.parent_kind is not None and definition.parent_kind != parent_kind:
            return None
        if definition.level is not None and definition.level != level:
            return None
        return definition

    def classify_top_level(
        self,
        title: str,
        *,
        phase: str,
    ) -> SectionMatch:
        """Classify a top-level H2 heading."""

        canonical = normalize_heading(title)
        definition = self.resolve_major(canonical)
        if definition is not None:
            return SectionMatch(
                kind=definition.kind,
                title=canonical,
                display_title=canonical,
                role=definition.role,
                registered=True,
                metadata={"canonical_title": definition.canonical_title},
            )

        if phase in {"after_explanations", "microconcepts"}:
            return SectionMatch(
                kind="micro_concept",
                title=canonical,
                display_title=canonical,
                role="microconcept",
                registered=False,
                metadata={"inferred": True, "phase": phase},
            )

        return SectionMatch(
            kind="generic_section",
            title=canonical,
            display_title=canonical,
            role="generic",
            registered=False,
            metadata={"inferred": True, "phase": phase},
        )

    def classify_child(
        self,
        title: str,
        *,
        parent_kind: str,
        level: int,
    ) -> SectionMatch:
        canonical = normalize_heading(title)
        definition = self.resolve_child(canonical, parent_kind=parent_kind, level=level)
        if definition is not None:
            return SectionMatch(
                kind=definition.kind,
                title=canonical,
                display_title=canonical,
                role=definition.role,
                registered=True,
                metadata={"canonical_title": definition.canonical_title, "parent_kind": parent_kind},
            )

        role = "subsection"
        kind = "generic_subsection"
        if parent_kind == "explanations":
            kind = "generic_explanation"
            role = "explanation"
        elif parent_kind == "micro_concept":
            kind = "generic_microconcept_subsection"
            role = "microconcept_subsection"
        elif parent_kind == "worked_examples":
            kind = "generic_worked_example"
            role = "worked_example"
        elif parent_kind == "final_challenge":
            kind = "generic_final_challenge"
            role = "final_challenge"

        return SectionMatch(
            kind=kind,
            title=canonical,
            display_title=canonical,
            role=role,
            registered=False,
            metadata={"inferred": True, "parent_kind": parent_kind, "level": level},
        )

    @property
    def ordered_major_kinds(self) -> list[str]:
        kinds = [
            "explanations",
            "worked_examples",
            "key_takeaways",
            "summary",
            "final_challenge",
        ]
        return [kind for kind in kinds if kind in self._definitions]


class BlockRegistry:
    """Registry and heuristics for markdown block classification."""

    def __init__(self) -> None:
        self._definitions: dict[str, BlockDefinition] = {}

    def register(self, definition: BlockDefinition) -> None:
        self._definitions[definition.kind] = definition

    def definition_for_kind(self, kind: str) -> BlockDefinition | None:
        return self._definitions.get(kind)

    def parse_body(
        self,
        text: str,
        *,
        section_kind: str = "",
        section_title: str = "",
    ) -> list[BlockMatch]:
        blocks: list[BlockMatch] = []
        for chunk in _split_text_chunks(text):
            match = self._classify_chunk(chunk, section_kind=section_kind, section_title=section_title)
            if match is not None:
                blocks.append(match)
        return blocks

    def parse_fence(
        self,
        *,
        language: str | None,
        text: str,
        section_kind: str = "",
        section_title: str = "",
    ) -> BlockMatch:
        language_key = (language or "").strip().lower()
        if language_key in {"mermaid"}:
            return BlockMatch(
                kind="mermaid",
                output_type="code",
                content=text.strip("\n"),
                language="mermaid",
                metadata={
                    "semantic_kind": "mermaid",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"svg"}:
            return BlockMatch(
                kind="svg",
                output_type="svg",
                content=text.strip("\n"),
                language=None,
                metadata={
                    "semantic_kind": "svg",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"math", "formula", "latex", "tex"}:
            return BlockMatch(
                kind="formula",
                output_type="formula",
                content=text.strip("\n"),
                language=language_key or "formula",
                metadata={
                    "semantic_kind": "formula",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"quiz", "embedded-quiz", "embedded_quiz"}:
            return BlockMatch(
                kind="embedded_quiz",
                output_type="check_understanding",
                content=self._parse_inline_checks(text),
                language=None,
                metadata={
                    "semantic_kind": "embedded_quiz",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"exercise", "interactive", "interactive-exercise"}:
            return BlockMatch(
                kind="interactive_exercise",
                output_type="check_understanding",
                content=self._parse_inline_checks(text),
                language=None,
                metadata={
                    "semantic_kind": "interactive_exercise",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"question"}:
            return BlockMatch(
                kind="question",
                output_type="prose",
                content=text.strip("\n"),
                language=None,
                metadata={
                    "semantic_kind": "question",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"answer"}:
            return BlockMatch(
                kind="answer",
                output_type="prose",
                content=text.strip("\n"),
                language=None,
                metadata={
                    "semantic_kind": "answer",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"diagram"}:
            return BlockMatch(
                kind="diagram",
                output_type="svg",
                content=text.strip("\n"),
                language=None,
                metadata={
                    "semantic_kind": "diagram",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        if language_key in {"video"}:
            return BlockMatch(
                kind="video",
                output_type="prose",
                content=text.strip("\n"),
                language=None,
                metadata={
                    "semantic_kind": "video",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )
        return BlockMatch(
            kind="code",
            output_type="code",
            content=text.strip("\n"),
            language=language_key or None,
            metadata={
                "semantic_kind": "code",
                "section_kind": section_kind,
                "section_title": section_title,
            },
        )

    def _classify_chunk(
        self,
        chunk: str,
        *,
        section_kind: str,
        section_title: str,
    ) -> BlockMatch | None:
        stripped = chunk.strip()
        if not stripped:
            return None

        if self._looks_like_table(stripped):
            headers, rows = self._parse_table(stripped)
            return BlockMatch(
                kind="table",
                output_type="table",
                content={"headers": headers, "rows": rows},
                metadata={
                    "semantic_kind": "table",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_divider(stripped):
            return BlockMatch(
                kind="divider",
                output_type="prose",
                content="---",
                metadata={
                    "semantic_kind": "divider",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_image(stripped):
            return BlockMatch(
                kind="image",
                output_type="prose",
                content=stripped,
                metadata={
                    "semantic_kind": "image",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_quote(stripped):
            variant = self._quote_variant(stripped)
            output_type = "warning" if variant == "warning" else "tip" if variant in {"tip", "note", "callout"} else "prose"
            content = self._strip_quote_markers(stripped)
            if variant == "quote":
                content = stripped
            return BlockMatch(
                kind=variant,
                output_type=output_type,
                content=content,
                metadata={
                    "semantic_kind": variant,
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_list(stripped):
            list_kind, items = self._parse_list(stripped)
            if section_kind == "quick_check" and list_kind == "ordered_list":
                checks: list[dict[str, Any]] = []
                for item in items:
                    question = item.strip()
                    answer = self._infer_quick_check_answer(question, section_title=section_title)
                    if answer:
                        checks.append({"question": question, "answer": answer})
                if checks:
                    return BlockMatch(
                        kind="check_understanding",
                        output_type="check_understanding",
                        content=checks,
                        metadata={
                            "semantic_kind": "check_understanding",
                            "section_kind": section_kind,
                            "section_title": section_title,
                        },
                    )
            output_type = "step_by_step" if list_kind == "ordered_list" else "list"
            return BlockMatch(
                kind=list_kind,
                output_type=output_type,
                content="\n".join(items),
                metadata={
                    "semantic_kind": list_kind,
                    "items": items,
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_definition(stripped):
            term, body = self._parse_definition(stripped)
            return BlockMatch(
                kind="definition",
                output_type="prose",
                content=body,
                metadata={
                    "semantic_kind": "definition",
                    "term": term,
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_question(stripped):
            payload = self._parse_inline_check_payload(stripped)
            if payload and (payload.get("choices") or payload.get("answer")):
                return BlockMatch(
                    kind="check_understanding",
                    output_type="check_understanding",
                    content=[payload],
                    metadata={
                        "semantic_kind": "check_understanding",
                        "question": payload.get("question", ""),
                        "answer": payload.get("answer", ""),
                        "choices": payload.get("choices", []),
                        "correct_choice_index": payload.get("correct_choice_index"),
                        "section_kind": section_kind,
                        "section_title": section_title,
                    },
                )

            question, answer = self._parse_question_answer(stripped)
            if answer:
                return BlockMatch(
                    kind="check_understanding",
                    output_type="check_understanding",
                    content=[{"question": question, "answer": answer}],
                    metadata={
                        "semantic_kind": "check_understanding",
                        "question": question,
                        "answer": answer,
                        "section_kind": section_kind,
                        "section_title": section_title,
                    },
                )
            return BlockMatch(
                kind="question",
                output_type="prose",
                content=question,
                metadata={
                    "semantic_kind": "question",
                    "answer": answer,
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        if self._looks_like_formula(stripped):
            return BlockMatch(
                kind="formula",
                output_type="formula",
                content=self._strip_formula_markers(stripped),
                metadata={
                    "semantic_kind": "formula",
                    "section_kind": section_kind,
                    "section_title": section_title,
                },
            )

        return BlockMatch(
            kind="prose",
            output_type="prose",
            content=self._normalize_paragraph(stripped),
            metadata={
                "semantic_kind": "prose",
                "inline_code": self._extract_inline_code(stripped),
                "section_kind": section_kind,
                "section_title": section_title,
            },
        )

    @staticmethod
    def _normalize_paragraph(text: str) -> str:
        return "\n\n".join(part.strip() for part in text.split("\n\n") if part.strip())

    @staticmethod
    def _extract_inline_code(text: str) -> list[str]:
        return re.findall(r"`([^`]+)`", text)

    @staticmethod
    def _looks_like_divider(text: str) -> bool:
        return bool(re.fullmatch(r"[-*_]{3,}", text.replace(" ", "")))

    @staticmethod
    def _looks_like_image(text: str) -> bool:
        return bool(re.search(r"!\[[^\]]*\]\([^)]+\)", text)) or text.lstrip().startswith("<img")

    @staticmethod
    def _looks_like_quote(text: str) -> bool:
        return text.lstrip().startswith(">")

    @staticmethod
    def _quote_variant(text: str) -> str:
        first_line = text.splitlines()[0].lstrip()
        label = re.match(r"^>\s*\[!(?P<label>[A-Z]+)\]", first_line)
        if not label:
            return "quote"
        return label.group("label").strip().lower()

    @staticmethod
    def _strip_quote_markers(text: str) -> str:
        lines = []
        for line in text.splitlines():
            stripped = line.lstrip()
            if stripped.startswith(">"):
                stripped = stripped[1:]
                if stripped.startswith(" "):
                    stripped = stripped[1:]
            if stripped.startswith("[!") and "]" in stripped:
                stripped = stripped.split("]", 1)[-1].lstrip()
            lines.append(stripped)
        return "\n".join(lines).strip()

    @staticmethod
    def _looks_like_table(text: str) -> bool:
        lines = [line.rstrip() for line in text.splitlines() if line.strip()]
        if len(lines) < 2:
            return False
        if "|" not in lines[0]:
            return False
        return bool(re.search(r"^\s*\|?[\s:-]+\|[\s:-|]+\s*$", lines[1]))

    @staticmethod
    def _parse_table(text: str) -> tuple[list[str], list[list[str]]]:
        lines = [line.rstrip() for line in text.splitlines() if line.strip()]
        headers = [cell.strip() for cell in _split_table_row(lines[0])]
        rows: list[list[str]] = []
        for line in lines[2:]:
            rows.append([cell.strip() for cell in _split_table_row(line)])
        return headers, rows

    @staticmethod
    def _looks_like_list(text: str) -> bool:
        lines = [line for line in text.splitlines() if line.strip()]
        if not lines:
            return False
        return all(
            re.match(r"^(?:[-*+]\s+|\d+[).]\s+|\[(?: |x|X)\]\s+)", line.lstrip()) is not None
            for line in lines
        )

    @staticmethod
    def _parse_list(text: str) -> tuple[str, list[str]]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return "bullet_list", []
        if all(re.match(r"^\d+[).]\s+", line) for line in lines):
            return "ordered_list", [
                re.sub(r"^\d+[).]\s+", "", line).strip() for line in lines
            ]
        if any(re.match(r"^\[(?: |x|X)\]\s+", line) for line in lines):
            return "checklist", [
                re.sub(r"^\[(?: |x|X)\]\s+", "", re.sub(r"^[-*+]\s+", "", line)).strip()
                for line in lines
            ]
        return "bullet_list", [
            re.sub(r"^[-*+]\s+", "", re.sub(r"^\d+[).]\s+", "", line)).strip()
            for line in lines
        ]

    @staticmethod
    def _normalize_quick_check_question(question: str) -> str:
        cleaned = re.sub(r"^\d+[).]\s*", "", question.strip())
        cleaned = cleaned.replace("`", "").replace("*", "")
        cleaned = re.sub(r"""[\"\.,:;!?()\[\]]""", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned.strip().lower()

    @staticmethod
    def _infer_quick_check_answer(question: str, *, section_title: str = "") -> str:
        normalized = BlockRegistry._normalize_quick_check_question(question)

        if "prefix" in normalized or any(term in normalized for term in {"re-", "sub-", "inter-", "multi-", "auto-", "pre-", "post-"}):
            return BlockRegistry._infer_prefix_answer(normalized)
        if "root" in normalized or any(term in normalized for term in {"aud", "port", "script", "scrib", "graph", "spect", "bio", "chron", "struct", "hydr", "mini"}):
            return BlockRegistry._infer_root_answer(normalized)
        if "suffix" in normalized or any(term in normalized for term in {"-ful", "-ness", "-less", "-er", "-ly", "-ed", "-al", "-ic", "-tion", "-ment", "-able"}):
            return BlockRegistry._infer_suffix_answer(normalized)
        if "family" in normalized or any(term in normalized for term in {"base word", "helpful", "national", "powerful", "teacher", "happiness", "inflection", "derivation"}):
            return BlockRegistry._infer_word_family_answer(normalized)
        if section_title:
            lower_title = section_title.lower()
            if any(term in lower_title for term in {"subject", "agreement", "coordination", "attractor", "pronoun", "collective", "there construction", "there constructions", "quantities"}):
                return BlockRegistry._infer_subject_verb_answer(normalized)
            if any(term in lower_title for term in {"prefix", "decode", "signal"}):
                return BlockRegistry._infer_prefix_answer(normalized)
            if "root" in lower_title:
                return BlockRegistry._infer_root_answer(normalized)
            if any(term in lower_title for term in {"suffix", "spelling", "shift"}):
                return BlockRegistry._infer_suffix_answer(normalized)
            if "family" in lower_title:
                return BlockRegistry._infer_word_family_answer(normalized)

        specific_answers: list[tuple[str, str]] = [
            # Word meaning
            ("which word is more formal in office writing", "inquire"),
            ("every synonym can replace the original word in every sentence", "False"),
            ("what should you check besides the dictionary meaning", "tone and usage"),
            ("what clue in a sentence often helps you spot the right meaning", "context clues"),
            ("the most common meaning of a word is always the correct meaning in context", "False"),
            ("in the sentence the answer was not vague but precise", "contrast"),
            ("which sounds more formal", "inquire"),
            ("why is strong rain a weaker choice than heavy rain", "It does not sound natural with rain"),
            ("two synonyms always have the same connotation", "False"),
            ("what should you check first the word's popularity or its part of speech", "its part of speech"),
            ("if two answers both look close what should you do next", "Test both choices in the sentence"),
            ("which options are easiest to eliminate immediately", "random words"),
            ("which word best matches the meaning of concise", "brief"),
            ("what does ambiguous mean", "unclear"),
            ("which word best matches commence", "begin"),
            ("which word best replaces inquire in this sentence", "asked"),
            ("which word best fits the report was and easy to understand", "concise"),
            ("which word is closest in meaning to inquire in a formal office context", "ask"),
            ("which clue in the sentence helps you decide the meaning of an unfamiliar word", "The surrounding context clues"),
            ("which is a better fit in a memo help or assist", "assist"),
            ("which word best matches ambiguous when a message is hard to understand", "unclear"),
            ("which pair is the closest synonym pair", "slim / skinny"),
            ("what does meticulous mean", "careful"),

            ("what kind of clue word often signals a contrast or opposite idea", "a contrast clue"),
            ("every antonym pair is exact in every sentence", "False"),
            ("why do you need to check part of speech first", "Because the opposite must match the same word class"),
            ("which clue word usually introduces a contrast", "although"),
            ("what should you do after seeing although in a sentence", "look for the opposite idea"),
            ("a contrast clue can help you eliminate several choices quickly", "True"),
            ("why should you check part of speech before using a prefix clue", "Because the opposite must match the same word class"),
            ("does a negative prefix always guarantee the correct antonym", "False"),
            ("what does dis- often suggest", "not, opposite, or undoing"),
            ("which word is the opposite of invalid in the sentence below", "valid"),
            ("choose the best antonym for abundant in the sentence below", "scarce"),
            ("what is the best opposite of transparent here", "opaque"),
            ("which word is the antonym of reluctant in this sentence", "eager"),
            ("choose the opposite of approve in formal writing", "reject"),
            ("which word best opposes permanent", "temporary"),
            ("which word is the antonym of hostile", "friendly"),
            ("which clue word often signals contrast in a sentence", "however"),
            ("which word is the opposite of expand", "shrink"),
            ("which word best opposes accept in a formal context", "reject"),
            ("which pair is the closest antonym pair", "hot / cold"),

            ("which word best describes a careful spender in a positive way", "thrifty"),
            ("what is denotation", "dictionary meaning"),
            ("what is connotation", "the feeling or association a word carries"),
            ("can two words have the same denotation but different connotation", "True"),
            ("which word would be safest in a neutral news report", "small"),
            ("which connotation is usually best for a formal report", "neutral"),
            ("which connotation sounds harsh or insulting", "negative"),
            ("which connotation sounds approving or respectful", "positive"),
            ("what should you check first in a connotation item", "the sentence purpose and tone"),
            ("if a word is correct in meaning but too harsh should you keep it", "No"),
            ("what kind of word usually fits a neutral news story", "neutral"),

            ("what is a context clue", "A hint in the surrounding words or sentence"),
            ("context clues can appear in a nearby sentence, not only the same sentence", "True"),
            ("context clues can appear in a nearby sentence not only the same sentence", "True"),
            ("which is more useful the target word alone or the target word plus the surrounding sentence", "the target word plus the surrounding sentence"),
            ("what should you check after you find the clue", "the blank's meaning"),
            ("the blank should be solved by meaning alone", "False"),
            ("which signal word often introduces a definition clue", "means"),
            ("if the sentence says x or y what is y usually doing", "restating or defining the word"),
            ("punctuation can help reveal meaning", "True"),
            ("punctuation can help reveal the meaning of the blank", "True"),
            ("which phrase often signals a restatement clue", "in other words"),
            ("is a restatement clue usually close to the word it explains", "True"),
            ("a restatement clue can use easier words than the target word", "True"),
            ("which word usually signals contrast", "however"),
            ("what kind of clue is unlike", "contrast clue"),
            ("contrast clues can help you eliminate wrong choices fast", "True"),
            ("contrast clues can help you eliminate wrong answers fast", "True"),
            ("which phrase often introduces examples", "for example"),
            ("what should you look for after the examples", "the shared idea"),
            ("example clues always give the exact definition word for word", "False"),
            ("which punctuation mark can signal a restatement clue", "comma"),
            ("what is an appositive", "a noun phrase that renames another noun"),
            ("punctuation can help reveal meaning even without a clue word", "True"),
            ("the sentence can still give a clue even without means or however", "True"),
            ("what should you do when there is no obvious clue word", "use the surrounding sentence and part of speech"),
            ("why does part of speech matter", "It tells you what kind of word fits"),
            ("the sentence can still give a clue even without words like means or however", "True"),
            ("what does glacier mean", "slow-moving mass of ice"),
            ("what does vapid mean", "dull and lifeless"),
            ("what does rigid mean", "stiff or inflexible"),
            ("what does utensils mean", "tools for cooking or eating"),
            ("what does envoy mean", "representative"),
            ("what does timid mean", "shy or afraid"),
            ("what does reticent mean", "reserved or quiet"),
            ("what does conflagration mean", "a large fire"),
            ("what does fervent mean", "passionate or intense"),
            ("what does somnolent mean", "sleepy"),
            ("what does parsimonious mean", "very stingy with money"),

            ("does an idiom usually mean exactly what the words say", "False"),
            ("what should you focus on first the literal words or the intended meaning", "the intended meaning"),
            ("why are idioms tricky on exams", "Because the literal words can mislead you"),
            ("what helps you most in an idiom question besides the phrase itself", "context"),
            ("the most literal answer is always correct", "False"),
            ("which words often signal a contrast", "but or however"),
            ("what is the figurative meaning of hit the nail on the head", "say or do something exactly right"),
            ("is the literal picture the final answer in an idiom question", "False"),
            ("what should you trust more than the literal image", "the intended meaning"),

            ("what is the first thing you should do when you meet a multiple meaning word", "the part of speech and sentence context"),
            ("if a word can be a noun or a verb what should you check", "the part of speech"),
            ("should you always choose the most common dictionary meaning", "False"),

            # Sentence completion and grammar fit
            ("which time clue usually signals simple past", "yesterday"),
            ("what does by the time often suggest", "an earlier completed action"),
            ("tense should stay consistent unless the time changes", "True"),
            ("what should a parallel list have", "matching forms"),
            ("which pair needs balance on both sides", "parallel structure"),
            ("nouns and verbs can freely mix in the same list", "False"),
            ("what matters more for a or an spelling or sound", "sound"),
            ("which is correct interested in or interested on", "interested in"),
            ("which word is used for a comparison between two things", "between"),
            ("which is correct fewer errors or less errors", "fewer errors"),
            ("between is usually used for more than two items", "False"),

            ("what should you look for first in a tense item", "the time clue"),
            ("which clue usually points to simple present", "every day"),
            ("which clue usually points to simple past", "last week"),
            ("which tense usually fits a habit", "simple present"),
            ("which tense usually fits a finished event", "simple past"),
            ("every day usually invites past tense", "False"),
            ("which word often signals a later time", "tomorrow"),
            ("in a future time clause should will usually appear inside the clause", "No"),
            ("when the meeting starts is a future clause that can still use present tense", "True"),
            ("which tense links a past action to the present", "present perfect"),
            ("which tense shows an earlier past action", "past perfect"),
            ("already often signals perfect tense", "True"),
            ("which tense shows action in progress now", "present progressive"),
            ("which tense shows action in progress in the past", "past progressive"),
            ("progressive tense focuses on the middle of the action", "True"),
            ("what is backshifting", "Moving the verb one step back in reported speech"),
            ("which future form often becomes would in reported speech", "will"),
            ("said that often triggers tense shift", "True"),

            ("what should you identify first", "The frame"),
            ("a difficult-looking word is always the best choice", "False"),
            ("what does the frame help you detect", "What can stay in the race"),
            ("what should you remove first if the meaning clashes", "Meaning"),
            ("a near-synonym is always safe", "False"),
            ("what clue word tells you the answer must be exact", "Exact"),
            ("what should match the subject", "Grammar"),
            ("what should match the antecedent", "Pronoun"),
            ("grammar can eliminate a choice even if the meaning looks fine", "True"),
            ("what does register tell you", "Tone"),
            ("a word can be correct in meaning but wrong in tone", "True"),
            ("what kind of language usually fits a memo", "Formal"),
            ("what does a result connector show", "A result"),
            ("what does a contrast connector show", "A contrast"),
            ("punctuation can help eliminate the wrong connector", "True"),
            ("what should you do when two choices remain", "Test both in the sentence"),
            ("what can still separate the final pair", "Tone"),
            ("the last two choices should be guessed without checking", "False"),

            ("what does register depend on", "The situation"),
            ("register is only about using long words", "False"),
            ("which kind of language usually appears in a manual", "Technical"),
            ("which register usually allows contractions more freely", "Casual"),
            ("which register is better for a public advisory", "Formal"),
            ("casual register is always wrong", "False"),
            ("which register is most likely in a policy notice", "Official"),
            ("which register is most likely in a quick informational message", "Neutral"),
            ("consultative register is used only in writing", "False"),
            ("which register is most likely in a laboratory manual", "Technical"),
            ("which register is most likely in a research abstract", "Academic"),
            ("technical language is always more formal than academic language", "False"),
            ("what clue often tells you that the register is official", "Official words"),
            ("what clue often tells you that the register is casual", "Contractions"),
            ("tone clues matter as much as meaning clues", "True"),

            # Connector and logical fit
            ("what is a connector's main job", "To show the relationship between ideas"),
            ("every connector can be used anywhere if the sentence sounds natural", "False"),
            ("which relationship does however usually show", "Contrast"),
            ("which coordinator usually shows contrast", "but"),
            ("which coordinator usually shows result", "so"),
            ("which connector often begins a dependent reason clause", "because"),
            ("which connector often means except if", "unless"),
            ("which connector often introduces a condition", "if"),
            ("which connector usually adds one more point", "moreover"),
            ("which connector sounds more formal moreover or but", "moreover"),
            ("which connector keeps the same direction of thought", "and"),
            ("which connector usually shows an opposite idea", "but"),
            ("which connector often admits one fact before the main point continues", "although"),
            ("which connector often admits a fact before the main point continues", "although"),
            ("which connector is closer to concession than simple contrast", "although"),
            ("contrast means the same thing as addition", "False"),
            ("which connector usually introduces a reason", "because"),
            ("which connector usually introduces a result", "so"),
            ("what should you ask first in a cause-result item", "Whether the blank shows a reason or an effect"),
            ("which connector usually introduces an example", "for example"),
            ("which connector usually rephrases the same idea", "in other words"),
            ("which connector usually shows the next step", "then"),
            ("what is a contrast signal's main job", "To show how two ideas differ"),
            ("contrast always means the same thing as addition", "False"),
            ("which signal usually introduces a direct turn between equal ideas", "but"),
            ("which connector often shows a side-by-side difference", "whereas"),
            ("which connector often corrects the first idea", "instead"),
            ("instead is mainly for direct comparison", "False"),
            ("what punctuation often appears before a conjunctive adverb", "semicolon"),
            ("what punctuation often appears before but or yet when joining two independent clauses", "comma"),
            ("despite usually begins a full clause with its own subject and verb", "False"),
            ("what is the cause", "The reason"),
            ("what is the effect", "The result"),
            ("cause and effect always appear in that order in the sentence", "False"),
            ("therefore is usually followed by a comma in formal writing", "True"),
            ("which phrase shows purpose not result", "so that"),
            ("which word usually shows a reason", "because"),
            ("which word usually shows a result", "so"),
            ("however shows cause and effect", "False"),
            ("which word usually introduces an opposite idea", "however"),
            ("which word adds another point", "moreover"),
            ("which word is closest to furthermore", "moreover"),
            ("addition connectors always show a new idea that is unrelated", "False"),
            ("which word often signals the last step", "finally"),
            ("which word often signals the step after the first one", "next"),
            ("sequence words always show cause", "False"),
            ("which phrase often introduces a specific case", "for example"),
            ("which phrase often repeats the same idea in clearer words", "in other words"),
            ("example and restatement mean exactly the same thing", "False"),
            ("which word means except if", "unless"),
            ("which phrase prepares for a possible problem", "otherwise"),
            ("provided that shows a condition", "True"),

            # Pronoun reference
            ("what is an antecedent", "The noun a pronoun refers to"),
            ("what should a pronoun point to", "Its antecedent"),
            ("the nearest noun is always the antecedent", "False"),
            ("what is ambiguity", "More than one possible antecedent"),
            ("what should you do if a pronoun is unclear", "Repeat the noun or rewrite the sentence"),
            ("a pronoun can be grammatically correct and still be unclear", "True"),
            ("what does each applicant suggest", "One person at a time"),
            ("which pronoun shows possession for a plural antecedent", "their"),
            ("can singular they be used in modern standard english", "True"),
            ("when do you use a reflexive pronoun", "when the subject and object are the same"),
            ("which form goes before a noun their or theirs", "their"),
            ("herself can usually replace her", "False"),
            ("which relative pronoun usually refers to a person as subject", "who"),
            ("which relative pronoun shows possession", "whose"),
            ("which relative pronoun usually refers to a thing", "which"),
        ]

        for needle, answer in specific_answers:
            if needle in normalized:
                return answer

        connector_answer = BlockRegistry._infer_connector_answer(normalized)
        if connector_answer:
            return connector_answer
        elimination_answer = BlockRegistry._infer_elimination_answer(normalized)
        if elimination_answer:
            return elimination_answer
        register_answer = BlockRegistry._infer_register_answer(normalized)
        if register_answer:
            return register_answer

        return ""

    @staticmethod
    def _infer_prefix_answer(question: str) -> str:
        if "what is a prefix" in question:
            return "An affix added before a base word."
        if "what does re- usually signal" in question or "what prefix often means again" in question:
            return "Again or back."
        if "why should you check the base word too" in question:
            return "It gives the core meaning of the word."
        if "why is context still important" in question:
            return "The sentence decides the exact sense."
        if "what does sub- usually mean" in question or "what prefix often means under" in question:
            return "Under or below."
        if "what does inter- usually mean" in question:
            return "Between."
        if "what does multi- usually mean" in question:
            return "Many or multiple."
        if "which prefix suggests self" in question or "what does auto- usually mean" in question:
            return "auto-"
        if "what prefix often means before" in question or "what does pre- usually mean" in question:
            return "pre-"
        if "what prefix often means after" in question:
            return "post-"
        if "what should you do first when decoding a word" in question:
            return "Find the prefix."
        if "why is the base word important" in question:
            return "It gives the core meaning of the word."
        if "why should you check the sentence" in question:
            return "The sentence confirms the exact sense."
        if "what should you do if two answers look close" in question:
            return "Test both choices in the sentence."
        if "why should you not stop at the signal" in question:
            return "The full word and sentence decide the meaning."
        if "not stop at the signal" in question or "signal" in question:
            return "The full word and sentence decide the meaning."
        if "what does auto- suggest" in question:
            return "Self."
        if "what does sub- mean" in question:
            return "Under or below."
        if "what does inter- mean" in question:
            return "Between."
        if "what does pre- mean" in question:
            return "Before."
        if "what does post- mean" in question:
            return "After."
        if "what does re- mean" in question:
            return "Again or back."
        return "A prefix changes the meaning before the base word."

    @staticmethod
    def _infer_root_answer(question: str) -> str:
        if "what is a root word" in question:
            return "The core of a word that carries the main meaning."
        if "what does the root do in a word family" in question:
            return "It gives the shared meaning to related words."
        if "why should you check affixes too" in question:
            return "Affixes can change meaning or part of speech."
        if "why is context still important" in question:
            return "The sentence confirms the exact sense."
        if "what is a free root" in question:
            return "A root that can stand alone as a word."
        if "what is a bound root" in question:
            return "A root that cannot stand alone."
        if "why are root families helpful" in question:
            return "They help you decode unfamiliar words."
        if "which is easier to spot in microscope" in question:
            return "The root."
        if "what does aud mean" in question:
            return "Hear or listen."
        if "what does port mean" in question:
            return "Carry."
        if "which root means to write" in question:
            return "script / scrib"
        if "which root means water" in question:
            return "hydr"
        if "what does graph carry" in question:
            return "Write."
        if "what does spect carry" in question:
            return "Look or see."
        if "what does bio carry" in question:
            return "Life."
        if "what does chron carry" in question:
            return "Time."
        if "what is the first thing you should do in a root-word question" in question:
            return "Find the root."
        if "why do you check the root family" in question:
            return "It helps you group related words and meanings."
        if "why do you still read the sentence" in question:
            return "The sentence decides the exact sense."
        if "why should you not stop at the first familiar part" in question:
            return "The rest of the word can change the meaning."
        if "what idea does graph carry" in question:
            return "Write."
        if "what idea does spect carry" in question:
            return "Look or see."
        if "what idea does bio carry" in question:
            return "Life."
        if "what idea does chron carry" in question:
            return "Time."
        if "what idea does hydr carry" in question:
            return "Water."
        if "what idea does struct carry" in question:
            return "Build."
        if "what idea does mini carry" in question:
            return "Small."
        return "The root carries the core meaning."

    @staticmethod
    def _infer_suffix_answer(question: str) -> str:
        if "what is a suffix" in question:
            return "An affix added to the end of a word."
        if "what does -ful usually suggest" in question:
            return "Full of; having."
        if "every word ending in -ly is an adverb" in question:
            return "False."
        if "what should you check after spotting a suffix" in question:
            return "The base word and the sentence context."
        if "what does -ness usually create" in question:
            return "A noun meaning a state or quality."
        if "which suffix often makes a word mean without" in question:
            return "-less"
        if "which suffix can mean person who" in question:
            return "-er"
        if "which family often helps form adjectives" in question:
            return "The -al / -ic family."
        if "what suffix often shows past tense" in question:
            return "-ed"
        if "what suffix often turns an adjective into an adverb" in question:
            return "-ly"
        if "what suffix often means state or quality" in question:
            return "-ness"
        if "what often happens to y before -ness" in question:
            return "The y usually changes to i."
        if "what often happens to a silent e before -ly" in question:
            return "The silent e usually drops."
        if "why does running have two n" in question:
            return "The spelling rule doubles the consonant after a short vowel."
        if "what should you do if the spelling looks strange" in question:
            return "Check the base word and the suffix rule."
        if "what is the first thing you should do in a suffix question" in question:
            return "Identify the base word."
        if "why is the base word important" in question:
            return "It gives the core meaning."
        if "what does context confirm" in question:
            return "The exact meaning and grammar."
        if "what should you do if two answers look close" in question:
            return "Test both in the sentence."
        if "why does running have two n" in question:
            return "The spelling rule doubles the consonant after a short vowel."
        return "The suffix changes meaning or grammar at the end of the word."

    @staticmethod
    def _infer_word_family_answer(question: str) -> str:
        if "what is the base word in a word family" in question:
            return "The root or main word that related forms grow from."
        if "why is helpful part of the help family" in question:
            return "It comes from the same base word and keeps the related meaning."
        if "why is meaning more important than letter shape alone" in question:
            return "Related words can change spelling while keeping the meaning."
        if "what changes when a suffix is added" in question:
            return "The word class or meaning can change."
        if "what is a base word" in question:
            return "The simplest word that a family grows from."
        if "what does national show about nation" in question:
            return "National is a related adjective form of nation."
        if "why is powerful part of power family" in question:
            return "It is a derived form from the same base word."
        if "does every family member need to look identical" in question:
            return "No."
        if "what is the difference between inflection and derivation" in question:
            return "Inflection changes grammar; derivation can change meaning or part of speech."
        if "why is teacher related to teach" in question:
            return "Teacher is a derived family member meaning one who teaches."
        if "why is happiness related to happy" in question:
            return "Happiness is a derived noun for the state of being happy."
        if "what should you check after spotting a family member" in question:
            return "The base word, affixes, and the sentence context."
        if "what is the first thing you should find in a word family item" in question:
            return "The base word."
        if "why should you check the sentence too" in question:
            return "The sentence confirms which family form fits."
        if "what is the danger of guessing from the first few letters" in question:
            return "Words can look similar but be unrelated."
        if "why is family meaning more useful than letter shape alone" in question:
            return "Meaning stays consistent across family forms."
        return "Words in the same family share a common base meaning."

    @staticmethod
    def _infer_connector_answer(question: str) -> str:
        if "connector's main job" in question or "connectors main job" in question:
            return "To show the relationship between ideas."
        if "every connector can be used anywhere" in question:
            return "False."
        if "however" in question and "usually show" in question:
            return "Contrast."
        if "because" in question and "usually show" in question:
            return "Cause or reason."
        if "connector usually joins two equal clauses in contrast" in question:
            return "but"
        if "stronger contrast signal" in question and "equal clauses" in question:
            return "however"
        if "although usually introduces a dependent clause" in question:
            return "True."
        if "connector usually takes a full clause" in question and "contrast" in question:
            return "although"
        if "connector usually takes a noun phrase" in question and "contrast" in question:
            return "despite"
        if "while can be contrastive" in question:
            return "True."
        if "side-by-side difference" in question:
            return "whereas"
        if "corrects the first idea" in question:
            return "instead"
        if "instead is mainly for direct comparison" in question:
            return "False."
        if "punctuation often appears before a conjunctive adverb" in question:
            return "semicolon"
        if "punctuation often appears before but or yet" in question:
            return "comma"
        if "despite usually begins a full clause" in question:
            return "False."
        if "safest direct reason word" in question:
            return "because"
        if "may also mean time" in question:
            return "since"
        if "formal and often joins two independent clauses" in question:
            return "for"
        if "usually shows a direct result" in question:
            return "so"
        if "often appears after a semicolon" in question:
            return "therefore"
        if "therefore' is usually followed by a comma" in question:
            return "True."
        if "usually takes a noun phrase" in question and "cause" in question:
            return "because of"
        if "usually takes a full clause" in question and "cause" in question:
            return "because"
        if "because of the rain" in question:
            return "True."
        if "word can mean either reason or time" in question:
            return "since"
        if "phrase shows purpose, not result" in question:
            return "so that"
        if "so that and so mean the same thing" in question:
            return "False."
        if "what is the cause" in question:
            return "The reason."
        if "what is the effect" in question:
            return "The result."
        if "cause and effect always appear" in question:
            return "False."
        if "connector usually takes a noun phrase" in question:
            return "because of"
        if "connector usually takes a full clause" in question:
            return "because"
        if "what connector usually introduces a reason" in question:
            return "because or since"
        if "what connector usually introduces a result" in question:
            return "therefore or as a result"
        if "what should you ask first in a cause-result item" in question:
            return "Whether the blank shows a reason or an effect."
        return ""

    @staticmethod
    def _infer_elimination_answer(question: str) -> str:
        if "what should you identify first" in question:
            return "The frame."
        if "difficult-looking word is always the best choice" in question:
            return "False."
        if "what does the frame help you detect" in question:
            return "What can stay in the race."
        if "what should you remove first if the meaning clashes" in question:
            return "Meaning."
        if "near-synonym is always safe" in question:
            return "False."
        if "what clue word tells you the answer must be exact" in question:
            return "Exact."
        if "what should match the subject" in question:
            return "Grammar."
        if "what should match the antecedent" in question:
            return "Pronoun."
        if "grammar can eliminate a choice even if the meaning looks fine" in question:
            return "True."
        if "what does register tell you" in question:
            return "Tone."
        if "word can be correct in meaning but wrong in tone" in question:
            return "True."
        if "what kind of language usually fits a memo" in question:
            return "Formal."
        if "what does a result connector show" in question:
            return "A result."
        if "what does a contrast connector show" in question:
            return "A contrast."
        if "punctuation can help eliminate the wrong connector" in question:
            return "True."
        if "what should you do when two choices remain" in question:
            return "Test both in the sentence."
        if "what can still separate the final pair" in question:
            return "Tone."
        if "last two choices should be guessed" in question:
            return "False."
        if "what should you remove first" in question and "meaning clashes" in question:
            return "Meaning."
        if "what clue word tells you the answer must be exact" in question:
            return "Exact."
        return ""

    @staticmethod
    def _infer_register_answer(question: str) -> str:
        if "what does register depend on" in question:
            return "The situation."
        if "register is only about using long words" in question:
            return "False."
        if "usually appears in a manual" in question:
            return "Formal."
        if "register usually allows contractions more freely" in question:
            return "Casual."
        if "better for a public advisory" in question:
            return "Formal."
        if "casual register is always wrong" in question:
            return "False."
        if "most likely in a policy notice" in question:
            return "Official."
        if "most likely in a quick informational message" in question:
            return "Neutral."
        if "consultative register is used only in writing" in question:
            return "False."
        if "most likely in a laboratory manual" in question:
            return "Formal."
        if "most likely in a research abstract" in question:
            return "Formal."
        if "technical language is always more formal than academic language" in question:
            return "False."
        if "what clue often tells you that the register is official" in question:
            return "Official words."
        if "what clue often tells you that the register is casual" in question:
            return "Contractions."
        if "tone clues matter as much as meaning clues" in question:
            return "True."
        return ""

    @staticmethod
    def _infer_subject_verb_answer(question: str) -> str:
        if "if the head noun is singular" in question:
            return "A singular verb."
        if "head noun" in question:
            if "the pile of documents" in question:
                return "pile"
            if "the team with the new uniforms" in question:
                return "team"
            return "The head noun."
        if "noun closest to the verb always controls agreement" in question:
            return "False."
        if "as well as" in question and "plural" in question:
            return "No."
        if "together with the crew" in question or "the captain" in question:
            return "False."
        if "notes and the draft" in question:
            return "are"
        if "noun in a phrase after of" in question and "control agreement" in question:
            return "No."
        if "list of names are long" in question:
            return "False."
        if "everyone in the room are ready" in question:
            return "False."
        if "the scissors is" in question and "the scissors are" in question:
            return "are"
        if "news" in question and "singular verb" in question:
            return "Yes."
        if "neither of the routes" in question:
            return "was"
        if "committee are meeting" in question:
            return "No."
        if "a number of employees" in question:
            return "are"
        if "the number of employees" in question:
            return "is"
        if "there" in question and "folder on the shelf" in question:
            return "is"
        if "what kind of verb should follow" in question:
            return "A singular verb."
        if "which is correct" in question and "the notes and the draft" in question:
            return "are"
        if "which is correct" in question and "the scissors" in question:
            return "are"
        if "which is correct" in question and "neither of the routes" in question:
            return "was"
        if "which is correct" in question and "a number of employees" in question:
            return "are"
        if "which is correct" in question and "the number of employees" in question:
            return "is"
        if "what is the subject" in question and "team with the new uniforms" in question:
            return "team"
        return "The subject controls agreement."

    @staticmethod
    def _looks_like_definition(text: str) -> bool:
        return bool(re.match(r"^(?:Definition|Term)\s*[:\-]\s+", text, flags=re.IGNORECASE))

    @staticmethod
    def _parse_definition(text: str) -> tuple[str, str]:
        match = re.match(r"^(?P<term>Definition|Term)\s*[:\-]\s*(?P<body>.+)$", text, flags=re.IGNORECASE | re.DOTALL)
        if match is None:
            return "Definition", text
        return match.group("term").strip(), match.group("body").strip()

    @staticmethod
    def _looks_like_question(text: str) -> bool:
        return bool(re.match(r"^(?:Question|Q)\s*[:\-]\s+", text, flags=re.IGNORECASE))

    @staticmethod
    def _parse_question_answer(text: str) -> tuple[str, str]:
        match = re.match(
            r"^(?P<question>(?:Question|Q)\s*[:\-]\s+.+?)(?:\n+|$)(?P<answer>(?:Answer|A)\s*[:\-]\s+.+)?$",
            text,
            flags=re.IGNORECASE | re.DOTALL,
        )
        if match is None:
            return text.strip(), ""
        question = re.sub(r"^(?:Question|Q)\s*[:\-]\s+", "", match.group("question"), flags=re.IGNORECASE).strip()
        answer = match.group("answer") or ""
        answer = re.sub(r"^(?:Answer|A)\s*[:\-]\s+", "", answer, flags=re.IGNORECASE).strip()
        return question, answer

    @staticmethod
    def _parse_inline_check_payload(text: str) -> dict[str, Any] | None:
        lines = [line.rstrip() for line in text.splitlines()]
        if not lines:
            return None

        question_parts: list[str] = []
        choices: list[str] = []
        answer_parts: list[str] = []
        rationale_parts: list[str] = []
        mode = "question"

        for raw_line in lines:
            stripped = raw_line.strip()
            if not stripped:
                continue

            question_match = re.match(r"^(?:Question|Q)\s*[:\-]\s*(.+)$", stripped, flags=re.IGNORECASE)
            if question_match:
                question_parts.append(question_match.group(1).strip())
                mode = "question"
                continue

            choices_match = re.match(r"^(?:Choices?|Options?)\s*[:\-]\s*$", stripped, flags=re.IGNORECASE)
            if choices_match:
                mode = "choices"
                continue

            answer_match = re.match(r"^(?:Answer|A|Correct)\s*[:\-]\s*(.+)$", stripped, flags=re.IGNORECASE)
            if answer_match:
                answer_parts.append(answer_match.group(1).strip())
                mode = "answer"
                continue

            rationale_match = re.match(r"^(?:Rationale|Explanation|Why)\s*[:\-]\s*(.+)$", stripped, flags=re.IGNORECASE)
            if rationale_match:
                rationale_parts.append(rationale_match.group(1).strip())
                mode = "rationale"
                continue

            if mode == "choices":
                choice_match = re.match(r"^(?:[-*]|\d+[).])\s+(.+)$", stripped)
                if choice_match:
                    choices.append(choice_match.group(1).strip())
                    continue

            if mode == "answer":
                answer_parts.append(stripped)
            elif mode == "rationale":
                rationale_parts.append(stripped)
            else:
                question_parts.append(stripped)

        question = " ".join(question_parts).strip()
        answer = " ".join(answer_parts).strip()
        rationale = " ".join(rationale_parts).strip()

        if not question:
            return None

        payload: dict[str, Any] = {
            "question": question,
            "answer": answer,
            "rationale": rationale,
        }
        if choices:
            normalized_answer = BlockRegistry._normalize_choice_text(answer)
            correct_choice_index = next(
                (i for i, choice in enumerate(choices) if BlockRegistry._normalize_choice_text(choice) == normalized_answer),
                None,
            )
            if correct_choice_index is None:
                correct_choice_index = BlockRegistry._parse_choice_letter(answer, len(choices))
            payload["choices"] = choices
            if correct_choice_index is not None:
                payload["correct_choice_index"] = correct_choice_index
                payload["answer"] = choices[correct_choice_index]
        return payload

    @staticmethod
    def _looks_like_formula(text: str) -> bool:
        stripped = text.strip()
        return (
            (stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4)
            or (stripped.startswith("$") and stripped.endswith("$") and len(stripped) > 2)
            or stripped.startswith("\\[")
            and stripped.endswith("\\]")
        )

    @staticmethod
    def _strip_formula_markers(text: str) -> str:
        stripped = text.strip()
        if stripped.startswith("$$") and stripped.endswith("$$"):
            return stripped[2:-2].strip()
        if stripped.startswith("$") and stripped.endswith("$"):
            return stripped[1:-1].strip()
        if stripped.startswith("\\[") and stripped.endswith("\\]"):
            return stripped[2:-2].strip()
        return stripped

    @staticmethod
    def _parse_inline_checks(text: str) -> list[dict[str, Any]]:
        checks: list[dict[str, Any]] = []
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        for chunk in chunks:
            payload = BlockRegistry._parse_inline_check_payload(chunk)
            if payload and (payload.get("question") or payload.get("answer")):
                checks.append(payload)
        return checks

    @staticmethod
    def _normalize_choice_text(text: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[`*_]", "", text)).strip().lower().rstrip(".?!")

    @staticmethod
    def _parse_choice_letter(answer: str, choice_count: int) -> int | None:
        if not answer:
            return None
        match = re.match(r"^(?:choice\s*)?([abc])(?:[\).:\-\s].*)?$", answer.strip(), flags=re.IGNORECASE)
        if not match:
            return None
        index = ord(match.group(1).upper()) - ord("A")
        return index if 0 <= index < choice_count else None


def create_default_section_registry() -> SectionRegistry:
    registry = SectionRegistry()
    registrations = [
        SectionDefinition(
            kind="explanations",
            canonical_title="Explanations",
            aliases=("Explanation", "Introduction", "Why This Topic Matters"),
            role="major",
        ),
        SectionDefinition(
            kind="worked_examples",
            canonical_title="Worked Examples",
            aliases=("Worked Example", "Examples", "Example Section"),
            role="major",
        ),
        SectionDefinition(
            kind="key_takeaways",
            canonical_title="Key Takeaways",
            aliases=("Takeaways", "Key Points", "Key Ideas"),
            role="major",
        ),
        SectionDefinition(
            kind="summary",
            canonical_title="Summary",
            aliases=("Recap", "Wrap Up", "Wrap-up"),
            role="major",
        ),
        SectionDefinition(
            kind="final_challenge",
            canonical_title="Final Challenge",
            aliases=("Challenge", "Final Practice", "Exit Ticket"),
            role="major",
        ),
        SectionDefinition(
            kind="introduction",
            canonical_title="Introduction",
            aliases=("Intro", "Overview", "Getting Started"),
            parent_kind="explanations",
            level=3,
            role="explanation_subsection",
        ),
        SectionDefinition(
            kind="why_topic_is_tested",
            canonical_title="Why Topic Is Tested",
            aliases=("Why This Topic Is Tested", "Why This Appears On Exams", "Why It Matters"),
            parent_kind="explanations",
            level=3,
            role="explanation_subsection",
        ),
        SectionDefinition(
            kind="common_mistakes",
            canonical_title="Common Mistakes",
            aliases=("Mistakes", "Common Errors", "Pitfalls"),
            parent_kind="explanations",
            level=3,
            role="explanation_subsection",
        ),
        SectionDefinition(
            kind="learning_objectives",
            canonical_title="Learning Objectives",
            aliases=("Learning Goals", "Objectives", "What You Will Learn"),
            parent_kind="explanations",
            level=3,
            role="explanation_subsection",
        ),
        SectionDefinition(
            kind="overview",
            canonical_title="Overview",
            aliases=("Concept Overview", "Summary of the Concept"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="core_principle",
            canonical_title="Core Principle",
            aliases=("Principle", "Rule", "Main Idea"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="visualization",
            canonical_title="Visualization",
            aliases=("Visual", "Diagram", "Picture", "Mental Image"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="micro_common_mistakes",
            canonical_title="Common Mistakes",
            aliases=("Misconceptions", "Pitfalls", "Errors"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="worked_mini_example",
            canonical_title="Worked Mini Example",
            aliases=("Mini Example", "Worked Example", "Example", "Example Walkthrough"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="quick_check",
            canonical_title="Quick Check",
            aliases=("Check Your Understanding", "Checkpoint", "Self Check"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="key_insight",
            canonical_title="Key Insight",
            aliases=("Insight", "Big Idea", "Takeaway"),
            parent_kind="micro_concept",
            level=3,
            role="microconcept_subsection",
        ),
        SectionDefinition(
            kind="mixed_practice_set",
            canonical_title="Mixed Practice Set",
            aliases=("Mixed Practice", "Mixed Set"),
            parent_kind="final_challenge",
            level=3,
            role="final_challenge_subsection",
        ),
        SectionDefinition(
            kind="self_assessment",
            canonical_title="Self Assessment",
            aliases=("Self-Assessment", "Assessment"),
            parent_kind="final_challenge",
            level=3,
            role="final_challenge_subsection",
        ),
        SectionDefinition(
            kind="whats_next",
            canonical_title="What's Next?",
            aliases=("Whats Next", "Next Steps"),
            parent_kind="final_challenge",
            level=3,
            role="final_challenge_subsection",
        ),
    ]
    for definition in registrations:
        registry.register(definition)
    return registry


def create_default_block_registry() -> BlockRegistry:
    registry = BlockRegistry()
    for definition in [
        BlockDefinition(kind="prose", output_type="prose"),
        BlockDefinition(kind="bullet_list", output_type="list"),
        BlockDefinition(kind="ordered_list", output_type="step_by_step"),
        BlockDefinition(kind="checklist", output_type="list"),
        BlockDefinition(kind="table", output_type="table"),
        BlockDefinition(kind="quote", output_type="prose"),
        BlockDefinition(kind="tip", output_type="tip"),
        BlockDefinition(kind="warning", output_type="warning"),
        BlockDefinition(kind="note", output_type="tip"),
        BlockDefinition(kind="callout", output_type="tip"),
        BlockDefinition(kind="code", output_type="code"),
        BlockDefinition(kind="formula", output_type="formula"),
        BlockDefinition(kind="svg", output_type="svg"),
        BlockDefinition(kind="mermaid", output_type="code"),
        BlockDefinition(kind="image", output_type="prose"),
        BlockDefinition(kind="video", output_type="prose"),
        BlockDefinition(kind="divider", output_type="prose"),
        BlockDefinition(kind="definition", output_type="prose"),
        BlockDefinition(kind="question", output_type="prose"),
        BlockDefinition(kind="answer", output_type="prose"),
        BlockDefinition(kind="diagram", output_type="svg"),
        BlockDefinition(kind="interactive_exercise", output_type="check_understanding"),
        BlockDefinition(kind="embedded_quiz", output_type="check_understanding"),
        BlockDefinition(kind="example", output_type="example"),
    ]:
        registry.register(definition)
    return registry


def _split_text_chunks(text: str) -> list[str]:
    chunks: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            if current:
                chunks.append("\n".join(current).strip())
                current = []
            continue
        current.append(line.rstrip())
    if current:
        chunks.append("\n".join(current).strip())
    return chunks


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]
