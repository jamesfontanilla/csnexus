"""Markdown-to-AST lesson parser."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import re
from typing import Any, Iterable

from .ast import LessonBlockNode, LessonDocumentAst, LessonSectionNode
from .lexer import MarkdownLexer, MarkdownToken
from .registry import (
    BlockMatch,
    BlockRegistry,
    SectionMatch,
    SectionRegistry,
    create_default_block_registry,
    create_default_section_registry,
    normalize_heading,
)
from .validation import validate_lesson_document

_WORDS_PER_MINUTE = 200
_CACHE_LIMIT = 64


@dataclass(slots=True)
class _HeadingNode:
    level: int
    raw_title: str
    title: str
    numbering: str | None = None
    body_tokens: list[MarkdownToken] = field(default_factory=list)
    children: list["_HeadingNode"] = field(default_factory=list)


class MarkdownLessonParser:
    """Parse Markdown lessons into a semantic document AST."""

    def __init__(
        self,
        *,
        section_registry: SectionRegistry | None = None,
        block_registry: BlockRegistry | None = None,
        lexer: MarkdownLexer | None = None,
    ) -> None:
        self.section_registry = section_registry or create_default_section_registry()
        self.block_registry = block_registry or create_default_block_registry()
        self.lexer = lexer or MarkdownLexer()

    def parse(self, markdown: str, *, category: str = "") -> LessonDocumentAst:
        tokens = self.lexer.lex(markdown)
        heading_root = self._build_heading_tree(tokens)
        title_node, content_root = self._extract_title_node(heading_root)
        title = (
            title_node.title
            if title_node is not None
            else (content_root.children[0].title if content_root.children else "Untitled Lesson")
        )

        top_level_nodes = list(content_root.children)
        phase = "pre_explanations"
        semantic_sections: list[LessonSectionNode] = []
        lead_source = title_node.body_tokens if title_node is not None else content_root.body_tokens
        lead_in_blocks = self._parse_tokens_to_blocks(
            lead_source,
            section_kind="lead_in",
            section_title=title,
        )

        for node in top_level_nodes:
            classification, next_phase = self._classify_top_level_node(node, phase=phase)
            section = self._convert_heading_node(
                node,
                classification=classification,
                parent_kind=None,
            )
            semantic_sections.append(section)
            phase = next_phase

        document = LessonDocumentAst(
            title=title,
            summary="",
            lead_in_blocks=lead_in_blocks,
            sections=semantic_sections,
        )
        self._populate_convenience_lists(document)
        self._normalize_document(document)
        document.warnings = [issue.message for issue in validate_lesson_document(document)]
        self._decorate_metadata(document, category=category)
        return document

    def _build_heading_tree(self, tokens: list[MarkdownToken]) -> _HeadingNode:
        root = _HeadingNode(level=0, raw_title="", title="")
        stack = [root]
        for token in tokens:
            if token.kind == "heading":
                title = normalize_heading(token.text)
                numbering = self._extract_numbering(token.text)
                node = _HeadingNode(level=token.level, raw_title=token.text, title=title, numbering=numbering)
                while stack and stack[-1].level >= token.level:
                    stack.pop()
                if not stack:
                    stack = [root]
                stack[-1].children.append(node)
                stack.append(node)
            else:
                stack[-1].body_tokens.append(token)
        return root

    def _extract_title_node(self, root: _HeadingNode) -> tuple[_HeadingNode | None, _HeadingNode]:
        for child in root.children:
            if child.level == 1:
                return child, child
        return None, root

    def _classify_top_level_node(
        self,
        node: _HeadingNode,
        *,
        phase: str,
    ) -> tuple[SectionMatch, str]:
        if node.level != 2:
            if node.level == 1:
                classification = SectionMatch(
                    kind="generic_section",
                    title=node.title,
                    display_title=node.title,
                    role="generic",
                    registered=False,
                    metadata={"inferred": True, "non_h2": True},
                )
                return classification, phase
            classification = SectionMatch(
                kind="generic_subsection",
                title=node.title,
                display_title=node.title,
                role="subsection",
                registered=False,
                metadata={"inferred": True, "non_h2": True},
            )
            return classification, phase

        classification = self.section_registry.classify_top_level(node.title, phase=phase)
        next_phase = phase
        if classification.kind == "explanations":
            next_phase = "after_explanations"
        elif classification.kind == "worked_examples":
            next_phase = "after_worked_examples"
        elif classification.kind in {"exam_strategies", "memory_aids", "practice_review", "key_takeaways", "summary", "final_challenge"}:
            next_phase = classification.kind
        elif classification.kind == "micro_concept" and phase in {"after_explanations", "microconcepts"}:
            next_phase = "microconcepts"
        return classification, next_phase

    def _convert_heading_node(
        self,
        node: _HeadingNode,
        *,
        classification: SectionMatch,
        parent_kind: str | None,
    ) -> LessonSectionNode:
        blocks = self._parse_tokens_to_blocks(
            node.body_tokens,
            section_kind=classification.kind,
            section_title=classification.display_title,
        )
        children: list[LessonSectionNode] = []
        child_kind = classification.kind
        for child in node.children:
            child_classification = self.section_registry.classify_child(
                child.title,
                parent_kind=child_kind,
                level=child.level,
            )
            if classification.kind not in {"explanations", "micro_concept", "worked_examples", "exam_strategies", "memory_aids", "practice_review", "final_challenge"} and child_classification.kind.startswith("generic_"):
                child_classification = SectionMatch(
                    kind=child_classification.kind,
                    title=child.title,
                    display_title=child.title,
                    role="generic",
                    registered=False,
                    metadata={**child_classification.metadata, "parent_kind": child_kind},
                )
            children.append(
                self._convert_heading_node(
                    child,
                    classification=child_classification,
                    parent_kind=child_kind,
                )
            )

        word_count = self._count_words(node)
        estimated_seconds = max(15, int(round(word_count / _WORDS_PER_MINUTE * 60))) if word_count else 15
        metadata = {
            "role": classification.role,
            "registered": classification.registered,
            "source_title": node.raw_title,
            "numbering": node.numbering,
            **classification.metadata,
        }
        section = LessonSectionNode(
            kind=classification.kind,
            title=classification.display_title,
            blocks=blocks,
            subsections=children,
            metadata=metadata,
            level=node.level,
            word_count=word_count,
            estimated_reading_seconds=estimated_seconds,
        )
        return section

    def _parse_tokens_to_blocks(
        self,
        tokens: list[MarkdownToken],
        *,
        section_kind: str,
        section_title: str,
    ) -> list[LessonBlockNode]:
        blocks: list[LessonBlockNode] = []
        for token in tokens:
            if token.kind == "body":
                matches = self.block_registry.parse_body(
                    token.text,
                    section_kind=section_kind,
                    section_title=section_title,
                )
                blocks.extend(self._convert_block_matches(matches))
            elif token.kind == "fence":
                match = self.block_registry.parse_fence(
                    language=token.language,
                    text=token.text,
                    section_kind=section_kind,
                    section_title=section_title,
                )
                blocks.append(self._convert_block_match(match))
        return blocks

    def _convert_block_matches(self, matches: list[BlockMatch]) -> list[LessonBlockNode]:
        blocks: list[LessonBlockNode] = []
        pending_question: LessonBlockNode | None = None
        for match in matches:
            if match.kind == "question":
                pending_question = self._convert_block_match(match)
                continue
            if match.kind == "answer" and pending_question is not None:
                pending_question.metadata["answer"] = match.content
                pending_question.metadata["paired_answer"] = True
                blocks.append(
                    LessonBlockNode(
                        kind="check_understanding",
                        content=[
                            {
                                "question": str(pending_question.content or ""),
                                "answer": str(match.content or ""),
                                "rationale": str(match.metadata.get("rationale") or ""),
                            }
                        ],
                        metadata={
                            "semantic_kind": "check_understanding",
                            "paired": True,
                            "source_question": pending_question.content,
                        },
                    )
                )
                pending_question = None
                continue

            if pending_question is not None:
                blocks.append(pending_question)
                pending_question = None
            blocks.append(self._convert_block_match(match))

        if pending_question is not None:
            blocks.append(pending_question)
        return blocks

    def _convert_block_match(self, match: BlockMatch) -> LessonBlockNode:
        metadata = dict(match.metadata)
        metadata.setdefault("semantic_kind", match.kind)
        metadata.setdefault("renderer_type", match.output_type)
        return LessonBlockNode(
            kind=match.kind,
            content=match.content,
            children=[self._coerce_child(child) for child in match.children],
            metadata=metadata,
            language=match.language,
        )

    def _coerce_child(self, child: Any) -> LessonBlockNode:
        if isinstance(child, LessonBlockNode):
            return child
        if isinstance(child, dict):
            return LessonBlockNode(
                kind=str(child.get("kind", "prose")),
                content=child.get("content"),
                children=[
                    self._coerce_child(grandchild)
                    for grandchild in child.get("children") or []
                    if isinstance(grandchild, (LessonBlockNode, dict))
                ],
                metadata=dict(child.get("metadata") or {}),
                language=child.get("language"),
            )
        return LessonBlockNode(kind="prose", content=str(child))

    def _populate_convenience_lists(self, document: LessonDocumentAst) -> None:
        document.explanations = [section for section in document.sections if section.kind == "explanations"]
        document.microconcepts = [section for section in document.sections if section.kind == "micro_concept"]
        document.worked_examples = [section for section in document.sections if section.kind == "worked_examples"]
        document.exam_strategies = [section for section in document.sections if section.kind == "exam_strategies"]
        document.memory_aids = [section for section in document.sections if section.kind == "memory_aids"]
        document.practice_review = [section for section in document.sections if section.kind == "practice_review"]
        document.final_challenge = [section for section in document.sections if section.kind == "final_challenge"]
        document.generic_sections = [
            section
            for section in document.sections
            if section.kind.startswith("generic_")
        ]

    def _normalize_document(self, document: LessonDocumentAst) -> None:
        if document.lead_in_blocks and not document.summary.strip():
            first = self._first_meaningful_text(document.lead_in_blocks)
            if first:
                document.summary = first

        if not document.summary.strip():
            document.summary = self._build_summary(document)

        document.learning_objectives = self._extract_learning_objectives(document)
        document.key_takeaways = self._extract_key_takeaways(document)

        if not document.explanations:
            fallback_blocks = document.lead_in_blocks or self._collect_section_blocks(document.sections[:1])
            explanation = LessonSectionNode(
                kind="explanations",
                title="Explanations",
                blocks=fallback_blocks,
                metadata={"synthetic": True},
                level=2,
                word_count=sum(section.word_count for section in document.sections[:1]),
                estimated_reading_seconds=30,
            )
            document.explanations = [explanation]
            document.sections.insert(0, explanation)

        if not document.worked_examples:
            placeholder = LessonSectionNode(
                kind="worked_examples",
                title="Worked Examples",
                blocks=[
                    LessonBlockNode(
                        kind="prose",
                        content="Worked examples are embedded within lesson sections.",
                        metadata={"synthetic": True},
                    )
                ],
                metadata={"synthetic": True},
                level=2,
                word_count=7,
                estimated_reading_seconds=20,
            )
            document.worked_examples = [placeholder]
            document.sections.append(placeholder)

        if not document.key_takeaways:
            document.key_takeaways = self._derive_key_takeaways(document)

        if not document.summary.strip():
            document.summary = f"Lesson covering {document.title}."

    def _decorate_metadata(self, document: LessonDocumentAst, *, category: str) -> None:
        section_count = len(document.sections)
        total_word_count = sum(section.word_count for section in document.sections)
        practice_problem_count = self._count_practice_checks(document.sections)
        difficulty_distribution = {
            "easy": 0,
            "medium": max(1, len(document.microconcepts)),
            "hard": 0,
        }
        metadata = {
            "title": document.title,
            "estimated_reading_minutes": max(1, int(round(total_word_count / _WORDS_PER_MINUTE))) or 1,
            "section_count": section_count,
            "learning_objective_count": len(document.learning_objectives),
            "has_practice_problems": practice_problem_count > 0,
            "practice_problem_count": practice_problem_count,
            "difficulty_distribution": difficulty_distribution,
            "total_word_count": total_word_count,
        }
        if category:
            metadata["category"] = category
        document.metadata = metadata

    def _extract_learning_objectives(self, document: LessonDocumentAst) -> list[str]:
        items: list[str] = []
        for section in document.sections:
            if section.kind == "explanations":
                for child in section.subsections:
                    if child.kind == "learning_objectives":
                        items.extend(self._block_text_lines(child.blocks))
        return self._dedupe_text(items)

    def _extract_key_takeaways(self, document: LessonDocumentAst) -> list[str]:
        items: list[str] = []
        for section in document.sections:
            if section.kind == "key_takeaways":
                items.extend(self._block_text_lines(section.blocks))
            if section.kind == "summary":
                items.extend(self._block_text_lines(section.blocks))
        return self._dedupe_text(items)

    def _derive_key_takeaways(self, document: LessonDocumentAst) -> list[str]:
        candidates = [
            section.title
            for section in document.sections
            if section.kind in {"micro_concept", "worked_examples", "exam_strategies"}
        ]
        if not candidates:
            candidates = [document.summary or document.title]
        return self._dedupe_text(candidates)[:5]

    def _collect_sections_by_kind(
        self,
        sections: list[LessonSectionNode],
        kinds: set[str],
    ) -> list[LessonSectionNode]:
        return [section for section in sections if section.kind in kinds]

    def _collect_section_blocks(self, sections: list[LessonSectionNode]) -> list[LessonBlockNode]:
        blocks: list[LessonBlockNode] = []
        for section in sections:
            blocks.extend(section.blocks)
        return blocks

    def _build_summary(self, document: LessonDocumentAst) -> str:
        for section in document.sections:
            for block in section.blocks:
                text = self._block_as_text(block)
                if text:
                    return text
            for child in section.subsections:
                for block in child.blocks:
                    text = self._block_as_text(block)
                    if text:
                        return text
        if document.lead_in_blocks:
            text = self._first_meaningful_text(document.lead_in_blocks)
            if text:
                return text
        if document.title:
            return f"Learn {document.title}."
        return ""

    def _first_meaningful_text(self, blocks: list[LessonBlockNode]) -> str:
        for block in blocks:
            text = self._block_as_text(block)
            if text:
                return text
        return ""

    def _block_as_text(self, block: LessonBlockNode) -> str:
        if isinstance(block.content, str):
            return " ".join(block.content.split()).strip()
        if isinstance(block.content, list):
            parts = []
            for item in block.content:
                if isinstance(item, dict):
                    parts.append(" ".join(str(v) for v in item.values() if isinstance(v, str)))
                else:
                    parts.append(str(item))
            return " ".join(part for part in parts if part.strip()).strip()
        if isinstance(block.content, dict):
            for key in ("content", "text", "body", "summary", "title"):
                value = block.content.get(key)
                if isinstance(value, str) and value.strip():
                    return " ".join(value.split()).strip()
        return ""

    def _block_text_lines(self, blocks: list[LessonBlockNode]) -> list[str]:
        lines: list[str] = []
        for block in blocks:
            text = self._block_as_text(block)
            if not text:
                continue
            for line in re.split(r"\n+", text):
                candidate = line.strip(" -*\t")
                if candidate:
                    lines.append(candidate)
        return lines

    def _extract_inline_checks(self, sections: list[LessonSectionNode]) -> list[dict[str, str]]:
        checks: list[dict[str, str]] = []
        for section in sections:
            for block in section.blocks:
                if block.kind == "check_understanding" and isinstance(block.content, list):
                    for item in block.content:
                        if isinstance(item, dict):
                            question = str(item.get("question") or "").strip()
                            answer = str(item.get("answer") or "").strip()
                            if question or answer:
                                checks.append({"question": question, "answer": answer})
        return checks

    def _count_practice_checks(self, sections: list[LessonSectionNode]) -> int:
        count = 0
        for section in sections:
            count += len(self._extract_inline_checks([section]))
            if section.subsections:
                count += self._count_practice_checks(section.subsections)
        return count

    @staticmethod
    def _dedupe_text(items: Iterable[str]) -> list[str]:
        seen: set[str] = set()
        result: list[str] = []
        for item in items:
            value = " ".join(str(item).split()).strip()
            if not value:
                continue
            key = value.lower()
            if key in seen:
                continue
            seen.add(key)
            result.append(value)
        return result

    @staticmethod
    def _count_words(node: _HeadingNode) -> int:
        text = " ".join(
            token.text
            for token in node.body_tokens
            if token.kind in {"body", "fence"}
        )
        return len(re.findall(r"\S+", text))

    @staticmethod
    def _extract_numbering(title: str) -> str | None:
        match = re.match(r"^(?P<number>\d+(?:\.\d+)*)(?:[\).:-]|\s)\s*(?P<rest>.+)$", title.strip())
        if match is None:
            return None
        return match.group("number")


class LessonParseCache:
    """Small in-memory cache keyed by lesson content hash."""

    def __init__(self, limit: int = _CACHE_LIMIT) -> None:
        self.limit = limit
        self._items: dict[str, dict[str, Any]] = {}
        self._order: list[str] = []

    def get(self, key: str) -> dict[str, Any] | None:
        value = self._items.get(key)
        if value is None:
            return None
        if key in self._order:
            self._order.remove(key)
        self._order.append(key)
        return value

    def set(self, key: str, value: dict[str, Any]) -> None:
        if key in self._items:
            self._order.remove(key)
        self._items[key] = value
        self._order.append(key)
        while len(self._order) > self.limit:
            oldest = self._order.pop(0)
            self._items.pop(oldest, None)


_DEFAULT_PARSER = MarkdownLessonParser()
_PARSE_CACHE = LessonParseCache()


def parse_lesson_markdown(markdown: str, category: str = "") -> dict[str, Any]:
    """Parse lesson Markdown into the compiled lesson-content JSON contract."""

    cache_key = hashlib.sha256(f"{category}\0{markdown}".encode("utf-8")).hexdigest()
    cached = _PARSE_CACHE.get(cache_key)
    if cached is not None:
        return cached

    document = _DEFAULT_PARSER.parse(markdown, category=category)
    from .compiler import compile_lesson_model

    model = compile_lesson_model(document)
    result = model
    _PARSE_CACHE.set(cache_key, result)
    return result
