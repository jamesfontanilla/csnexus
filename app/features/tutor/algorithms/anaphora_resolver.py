"""Anaphora Resolver for the Smart Chat Engine.

Resolves pronouns and demonstrative references (e.g., "it", "that",
"this concept") back to the most recent active TopicThread subject
in the conversation context.

No external APIs — resolution is purely rule-based using pattern matching
against known anaphoric references and scoring against available referents.
"""

from __future__ import annotations

import re

from app.features.tutor.algorithms.chat_models import (
    ConversationContext,
    ResolvedMessage,
)

# ---------------------------------------------------------------------------
# Anaphoric patterns
# ---------------------------------------------------------------------------

# Patterns that indicate an anaphoric reference (pronoun or demonstrative)
ANAPHORIC_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\b(it)\b", re.IGNORECASE),
    re.compile(r"\b(that)\b", re.IGNORECASE),
    re.compile(r"\b(this)\b", re.IGNORECASE),
    re.compile(r"\b(this concept)\b", re.IGNORECASE),
    re.compile(r"\b(that concept)\b", re.IGNORECASE),
    re.compile(r"\b(the concept)\b", re.IGNORECASE),
    re.compile(r"\b(this topic)\b", re.IGNORECASE),
    re.compile(r"\b(that topic)\b", re.IGNORECASE),
    re.compile(r"\b(the topic)\b", re.IGNORECASE),
    re.compile(r"\b(this one)\b", re.IGNORECASE),
    re.compile(r"\b(that one)\b", re.IGNORECASE),
    re.compile(r"\b(these)\b", re.IGNORECASE),
    re.compile(r"\b(those)\b", re.IGNORECASE),
    re.compile(r"\b(them)\b", re.IGNORECASE),
]

# Confidence threshold below which resolution is considered ambiguous
CONFIDENCE_THRESHOLD: float = 0.4


class AnaphoraResolver:
    """Resolves anaphoric references in user messages to topic thread subjects.

    The resolver scans the message for pronoun/demonstrative patterns and
    attempts to resolve them to the subject of the most recent active
    TopicThread in the conversation context.
    """

    def resolve(self, message: str, ctx: ConversationContext) -> ResolvedMessage:
        """Resolve anaphoric references in a message.

        Args:
            message: The user's raw message text.
            ctx: The current conversation context with topic threads.

        Returns:
            A ResolvedMessage with the resolved text, confidence,
            candidate list, and chosen referent.
        """
        # Find anaphoric references in the message
        matched_references = self._find_anaphoric_references(message)

        if not matched_references:
            # No anaphoric references found — return message as-is
            return ResolvedMessage(
                original=message,
                resolved=message,
                confidence=1.0,
                candidates=[],
                referent=None,
            )

        # Gather candidate referents from topic threads
        candidates = self._gather_candidates(ctx)

        if not candidates:
            # Anaphoric reference found but no candidates available
            return ResolvedMessage(
                original=message,
                resolved=message,
                confidence=0.0,
                candidates=[],
                referent=None,
            )

        # Resolve to the most recent active topic thread subject
        referent, confidence = self._select_referent(candidates, ctx)

        # Build resolved message by replacing anaphoric references
        resolved = self._replace_references(message, matched_references, referent)

        # If confidence is below threshold, mark as ambiguous
        if confidence < CONFIDENCE_THRESHOLD:
            return ResolvedMessage(
                original=message,
                resolved=resolved,
                confidence=confidence,
                candidates=candidates,
                referent=None,
            )

        return ResolvedMessage(
            original=message,
            resolved=resolved,
            confidence=confidence,
            candidates=candidates,
            referent=referent,
        )

    def _find_anaphoric_references(self, message: str) -> list[tuple[str, int, int]]:
        """Find all anaphoric references in the message.

        Returns list of (matched_text, start, end) tuples.
        """
        references: list[tuple[str, int, int]] = []
        for pattern in ANAPHORIC_PATTERNS:
            for match in pattern.finditer(message):
                references.append((match.group(1), match.start(1), match.end(1)))

        # Sort by position and deduplicate overlapping matches
        references.sort(key=lambda x: x[1])
        deduped: list[tuple[str, int, int]] = []
        last_end = -1
        for ref in references:
            if ref[1] >= last_end:
                deduped.append(ref)
                last_end = ref[2]

        return deduped

    def _gather_candidates(self, ctx: ConversationContext) -> list[str]:
        """Gather candidate referents from topic threads.

        Returns subjects of all topic threads, ordered most-recent first.
        """
        candidates: list[str] = []
        for thread in reversed(ctx.topic_threads):
            if thread.subject and thread.subject not in candidates:
                candidates.append(thread.subject)
        return candidates

    def _select_referent(
        self, candidates: list[str], ctx: ConversationContext
    ) -> tuple[str, float]:
        """Select the best referent from candidates.

        The most recent active topic thread subject is preferred.
        Returns (referent, confidence).
        """
        # Find the most recent active thread
        for thread in reversed(ctx.topic_threads):
            if thread.is_active and thread.subject:
                # High confidence for active thread with subject
                return thread.subject, 0.9

        # No active thread — fall back to most recent thread subject
        if candidates:
            # Lower confidence when no active thread
            return candidates[0], 0.5

        return "", 0.0

    def _replace_references(
        self,
        message: str,
        references: list[tuple[str, int, int]],
        referent: str,
    ) -> str:
        """Replace anaphoric references in the message with the referent.

        Processes replacements from end to start to preserve positions.
        """
        if not referent:
            return message

        result = message
        # Process from end to start so positions stay valid
        for ref_text, start, end in reversed(references):
            result = result[:start] + referent + result[end:]

        return result

    def contains_anaphoric_reference(self, message: str) -> bool:
        """Check if a message contains any anaphoric reference.

        Useful for topic shift detection — a message with an anaphoric
        reference should not be treated as a topic shift.
        """
        for pattern in ANAPHORIC_PATTERNS:
            if pattern.search(message):
                return True
        return False
