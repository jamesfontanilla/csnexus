"""A lightweight Markdown lexer for lesson content."""

from __future__ import annotations

from dataclasses import dataclass, field
import re
from typing import Any


@dataclass(slots=True)
class MarkdownToken:
    """A coarse token emitted by the Markdown lexer."""

    kind: str
    text: str
    level: int = 0
    language: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class MarkdownLexer:
    """Split Markdown into headings, fenced blocks, and raw body chunks."""

    _heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    _fence_pattern = re.compile(r"^(```|~~~)\s*([\w+-]*)\s*$")

    def lex(self, markdown: str) -> list[MarkdownToken]:
        text = markdown.replace("\r\n", "\n").replace("\r", "\n")
        tokens: list[MarkdownToken] = []
        body_lines: list[str] = []
        in_fence = False
        fence_delimiter = ""
        fence_language: str | None = None
        fence_lines: list[str] = []

        def flush_body() -> None:
            if not body_lines:
                return
            body = "\n".join(body_lines).rstrip()
            if body.strip():
                tokens.append(MarkdownToken(kind="body", text=body))
            body_lines.clear()

        for line in text.split("\n"):
            if in_fence:
                if line.strip() == fence_delimiter:
                    tokens.append(
                        MarkdownToken(
                            kind="fence",
                            text="\n".join(fence_lines).rstrip(),
                            language=fence_language,
                        )
                    )
                    in_fence = False
                    fence_delimiter = ""
                    fence_language = None
                    fence_lines = []
                else:
                    fence_lines.append(line)
                continue

            fence_match = self._fence_pattern.match(line.strip())
            if fence_match is not None:
                flush_body()
                in_fence = True
                fence_delimiter = fence_match.group(1)
                fence_language = fence_match.group(2) or None
                fence_lines = []
                continue

            heading_match = self._heading_pattern.match(line)
            if heading_match is not None:
                flush_body()
                tokens.append(
                    MarkdownToken(
                        kind="heading",
                        text=heading_match.group(2).strip(),
                        level=len(heading_match.group(1)),
                    )
                )
                continue

            body_lines.append(line)

        flush_body()
        if in_fence and fence_lines:
            tokens.append(
                MarkdownToken(
                    kind="fence",
                    text="\n".join(fence_lines).rstrip(),
                    language=fence_language,
                    metadata={"unterminated": True},
                )
            )
        return tokens
