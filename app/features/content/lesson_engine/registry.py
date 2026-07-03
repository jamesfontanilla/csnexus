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
        elif parent_kind == "exam_strategies":
            kind = "generic_strategy"
            role = "strategy"
        elif parent_kind == "memory_aids":
            kind = "generic_memory_aid"
            role = "memory_aid"
        elif parent_kind == "practice_review":
            kind = "generic_practice_review"
            role = "practice_review"
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
            "exam_strategies",
            "memory_aids",
            "practice_review",
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
    def _parse_inline_checks(text: str) -> list[dict[str, str]]:
        checks: list[dict[str, str]] = []
        chunks = [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]
        for chunk in chunks:
            question, answer = BlockRegistry._parse_question_answer(chunk)
            if question and answer:
                checks.append({"question": question, "answer": answer})
        return checks


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
            kind="exam_strategies",
            canonical_title="Exam Strategies",
            aliases=("Exam Strategy", "Strategies", "Test Strategies"),
            role="major",
        ),
        SectionDefinition(
            kind="memory_aids",
            canonical_title="Memory Aids",
            aliases=("Mnemonic", "Mnemonics", "Memory Aid"),
            role="major",
        ),
        SectionDefinition(
            kind="practice_review",
            canonical_title="Practice & Review",
            aliases=("Practice and Review", "Practice Review", "Practice", "Review"),
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
            kind="universal_solving_framework",
            canonical_title="Universal Solving Framework",
            aliases=("Solving Framework", "Framework"),
            parent_kind="exam_strategies",
            level=3,
            role="strategy_subsection",
        ),
        SectionDefinition(
            kind="time_management",
            canonical_title="Time Management",
            aliases=("Timing", "Pacing"),
            parent_kind="exam_strategies",
            level=3,
            role="strategy_subsection",
        ),
        SectionDefinition(
            kind="shortcut_elimination_techniques",
            canonical_title="Shortcut & Elimination Techniques",
            aliases=("Shortcut Techniques", "Elimination Techniques", "Shortcuts"),
            parent_kind="exam_strategies",
            level=3,
            role="strategy_subsection",
        ),
        SectionDefinition(
            kind="exam_day_tips",
            canonical_title="Exam-Day Tips",
            aliases=("Exam Day Tips", "Test Day Tips"),
            parent_kind="exam_strategies",
            level=3,
            role="strategy_subsection",
        ),
        SectionDefinition(
            kind="mnemonics",
            canonical_title="Mnemonics",
            aliases=("Mnemonic Devices",),
            parent_kind="memory_aids",
            level=3,
            role="memory_aid_subsection",
        ),
        SectionDefinition(
            kind="mental_models",
            canonical_title="Mental Models",
            aliases=("Models", "Mental Pictures"),
            parent_kind="memory_aids",
            level=3,
            role="memory_aid_subsection",
        ),
        SectionDefinition(
            kind="shortcuts_and_tricks",
            canonical_title="Shortcuts & Tricks",
            aliases=("Shortcuts", "Tricks"),
            parent_kind="memory_aids",
            level=3,
            role="memory_aid_subsection",
        ),
        SectionDefinition(
            kind="what_to_memorize",
            canonical_title="What To Memorize",
            aliases=("What to Memorize", "Must Memorize"),
            parent_kind="memory_aids",
            level=3,
            role="memory_aid_subsection",
        ),
        SectionDefinition(
            kind="before_you_practice",
            canonical_title="Before You Practice",
            aliases=("Before Practice", "Practice Setup"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
        ),
        SectionDefinition(
            kind="which_method",
            canonical_title="Which Method?",
            aliases=("Method Selection", "Choose the Method"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
        ),
        SectionDefinition(
            kind="guided_practice",
            canonical_title="Guided Practice",
            aliases=("Guided Exercises", "Practice Walkthrough"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
        ),
        SectionDefinition(
            kind="independent_practice",
            canonical_title="Independent Practice",
            aliases=("Practice Alone", "Solo Practice"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
        ),
        SectionDefinition(
            kind="challenge_questions",
            canonical_title="Challenge Questions",
            aliases=("Challenge Set", "Hard Questions"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
        ),
        SectionDefinition(
            kind="connections",
            canonical_title="Connections",
            aliases=("Connection", "Links"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
        ),
        SectionDefinition(
            kind="mastery_checklist",
            canonical_title="Mastery Checklist",
            aliases=("Checklist", "Mastery Check"),
            parent_kind="practice_review",
            level=3,
            role="practice_subsection",
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
