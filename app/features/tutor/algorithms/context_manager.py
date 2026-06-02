"""Context Manager for the Smart Chat Engine.

Responsible for constructing, updating, serializing, and deserializing
ConversationContext. Handles topic thread management, exchange window
eviction, and topic shift detection.
"""

from __future__ import annotations

import re
from typing import Any

from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ComplexityOverride,
    ConversationContext,
    DiscourseState,
    Exchange,
    SocraticState,
    TopicThread,
)


# ---------------------------------------------------------------------------
# Anaphoric reference patterns (used by topic shift detection)
# ---------------------------------------------------------------------------

_ANAPHORIC_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bit\b", re.IGNORECASE),
    re.compile(r"\bthat\b", re.IGNORECASE),
    re.compile(r"\bthis\b", re.IGNORECASE),
    re.compile(r"\bthese\b", re.IGNORECASE),
    re.compile(r"\bthose\b", re.IGNORECASE),
    re.compile(r"\bthe concept\b", re.IGNORECASE),
    re.compile(r"\bthe topic\b", re.IGNORECASE),
    re.compile(r"\bthe same\b", re.IGNORECASE),
    re.compile(r"\bthem\b", re.IGNORECASE),
    re.compile(r"\bits\b", re.IGNORECASE),
]

# Maximum exchanges in a context window
_MAX_EXCHANGES = 10

# Maximum topic threads (1 active + 3 preserved)
_MAX_TOPIC_THREADS = 4

# Current schema version
_CURRENT_SCHEMA_VERSION = 1

# Public alias for tests and external consumers
CURRENT_SCHEMA_VERSION = _CURRENT_SCHEMA_VERSION


class ContextManager:
    """Manages the lifecycle of ConversationContext objects."""

    def build_context(self, serialized: dict[str, Any] | None) -> ConversationContext:
        """Deserialize a context dict or create a fresh ConversationContext.

        If the serialized dict is None, malformed, or has an unrecognized
        schema version, returns a fresh default context.
        """
        if serialized is None:
            return ConversationContext()

        try:
            return self._deserialize(serialized)
        except (KeyError, TypeError, ValueError, AttributeError, IndexError):
            # Malformed context — start fresh (Requirement 7.4)
            return ConversationContext()

    def serialize(self, ctx: ConversationContext) -> dict[str, Any]:
        """Serialize a ConversationContext to a JSON-compatible dict.

        The output always includes a `schema_version` field for forward
        compatibility (Requirement 7.1).
        """
        return {
            "schema_version": _CURRENT_SCHEMA_VERSION,
            "exchanges": [
                {
                    "user_message": ex.user_message,
                    "assistant_response": ex.assistant_response,
                    "intent": ex.intent,
                    "topic_thread_subject": ex.topic_thread_subject,
                }
                for ex in ctx.exchanges
            ],
            "topic_threads": [
                {
                    "subject": tt.subject,
                    "start_exchange_index": tt.start_exchange_index,
                    "key_terms": list(tt.key_terms),
                    "is_active": tt.is_active,
                }
                for tt in ctx.topic_threads
            ],
            "discourse_state": ctx.discourse_state.value,
            "socratic_state": {
                "active": ctx.socratic_state.active,
                "target_concept": ctx.socratic_state.target_concept,
                "key_terms": list(ctx.socratic_state.key_terms),
                "attempts": ctx.socratic_state.attempts,
                "reasoning_type": ctx.socratic_state.reasoning_type,
            },
            "complexity_override": (
                {
                    "level": ctx.complexity_override.level.value,
                    "remaining_responses": ctx.complexity_override.remaining_responses,
                }
                if ctx.complexity_override is not None
                else None
            ),
            "template_usage": dict(ctx.template_usage),
        }

    def update_context(
        self,
        ctx: ConversationContext,
        user_msg: str,
        response: str,
        intent: str,
    ) -> ConversationContext:
        """Append an exchange and update discourse state and topic threads.

        Handles topic shift detection: if a shift is detected, deactivates
        the current thread and starts a new one. Enforces the max 4 topic
        threads limit (1 active + 3 preserved).

        Returns the updated context (mutated in place for efficiency).
        """
        # Detect topic shift before creating the exchange
        topic_shifted = self.detect_topic_shift(ctx, user_msg)

        if topic_shifted:
            # Deactivate the current active thread
            active_thread = self._get_active_thread(ctx)
            if active_thread is not None:
                active_thread.is_active = False

            # Create a new topic thread for the shifted topic
            new_subject = self._extract_subject(user_msg)
            new_thread = TopicThread(
                subject=new_subject,
                start_exchange_index=len(ctx.exchanges),
                key_terms=self._extract_key_terms(user_msg),
                is_active=True,
            )
            ctx.topic_threads.append(new_thread)

            # Enforce max topic threads (1 active + 3 preserved)
            self._enforce_max_topic_threads(ctx)

            topic_subject = new_subject
        else:
            active_thread = self._get_active_thread(ctx)
            if active_thread is not None:
                topic_subject = active_thread.subject
            else:
                # No active thread exists — start a new one
                new_subject = self._extract_subject(user_msg)
                new_thread = TopicThread(
                    subject=new_subject,
                    start_exchange_index=len(ctx.exchanges),
                    key_terms=self._extract_key_terms(user_msg),
                    is_active=True,
                )
                ctx.topic_threads.append(new_thread)
                self._enforce_max_topic_threads(ctx)
                topic_subject = new_subject

        # Create exchange
        exchange = Exchange(
            user_message=user_msg,
            assistant_response=response,
            intent=intent,
            topic_thread_subject=topic_subject,
        )
        ctx.exchanges.append(exchange)

        # Evict if over limit
        if len(ctx.exchanges) > _MAX_EXCHANGES:
            ctx = self.evict_oldest(ctx)

        # Update discourse state based on intent
        ctx.discourse_state = self._compute_discourse_state(intent, ctx)

        return ctx

    def evict_oldest(self, ctx: ConversationContext) -> ConversationContext:
        """Remove the oldest exchange(s), preserving topic thread subjects.

        Maintains the 10-exchange window (Requirement 1.6). Topic thread
        subjects from evicted exchanges are preserved if the thread is still
        referenced by remaining exchanges (Requirement 1.7). Threads whose
        subjects are no longer referenced are marked inactive but kept in
        the topic_threads list for back-reference support.
        """
        while len(ctx.exchanges) > _MAX_EXCHANGES:
            evicted = ctx.exchanges.pop(0)

            # Check if the evicted exchange's topic thread is still referenced
            evicted_subject = evicted.topic_thread_subject
            still_referenced = any(
                ex.topic_thread_subject == evicted_subject for ex in ctx.exchanges
            )

            if not still_referenced:
                # Mark the thread inactive — keep in list for back-references
                for tt in ctx.topic_threads:
                    if tt.subject == evicted_subject and tt.is_active:
                        tt.is_active = False

        return ctx

    def detect_topic_shift(self, ctx: ConversationContext, message: str) -> bool:
        """Detect whether the message represents a topic shift.

        A topic shift occurs when (Requirement 1.4):
        1. The message shares zero key terms with the active TopicThread's
           subject and key_terms
        2. The message contains no anaphoric references

        If there is no active topic thread, no shift is detected (it's a
        new conversation).
        """
        active_thread = self._get_active_thread(ctx)
        if active_thread is None:
            return False

        # Check for anaphoric references
        if self._contains_anaphoric_reference(message):
            return False

        # Check for term overlap with active thread
        if self._shares_terms_with_thread(message, active_thread):
            return False

        # No shared terms and no anaphoric references → topic shift
        return True

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _contains_anaphoric_reference(self, message: str) -> bool:
        """Check if the message contains any anaphoric reference patterns."""
        for pattern in _ANAPHORIC_PATTERNS:
            if pattern.search(message):
                return True
        return False

    def _shares_terms_with_thread(self, message: str, thread: TopicThread) -> bool:
        """Check if the message shares any key terms with the thread."""
        message_lower = message.lower()
        message_words = set(re.findall(r"\b[a-z]+\b", message_lower))

        # Check against thread subject
        subject_words = set(re.findall(r"\b[a-z]+\b", thread.subject.lower()))
        if message_words & subject_words:
            return True

        # Check against thread key terms
        for term in thread.key_terms:
            term_lower = term.lower()
            # Check if the full term appears in the message
            if term_lower in message_lower:
                return True
            # Check if any word of the term appears in the message words
            term_words = set(re.findall(r"\b[a-z]+\b", term_lower))
            if term_words & message_words:
                return True

        return False

    def _get_active_thread(self, ctx: ConversationContext) -> TopicThread | None:
        """Get the currently active topic thread, if any."""
        for thread in ctx.topic_threads:
            if thread.is_active:
                return thread
        return None

    def _extract_subject(self, message: str) -> str:
        """Extract a topic subject from a message (simplified heuristic)."""
        # Remove common question starters and extract the noun phrase
        cleaned = re.sub(
            r"^(?:what is|what are|how do|how does|why do|why does|explain|tell me about)\s+",
            "",
            message.strip(),
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"[?.!]+$", "", cleaned).strip()
        return cleaned if cleaned else message.strip()

    def _extract_key_terms(self, message: str) -> list[str]:
        """Extract key terms from a message for topic thread tracking.

        Filters out common stop words and returns meaningful terms.
        """
        stop_words = frozenset([
            "a", "an", "the", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "can", "shall",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "about", "as", "into", "through", "during", "before", "after",
            "and", "but", "or", "nor", "not", "so", "yet", "both",
            "what", "how", "why", "when", "where", "who", "which",
            "me", "my", "i", "you", "your", "we", "our", "they", "their",
            "it", "its", "that", "this", "these", "those", "them",
            "more", "most", "some", "any", "all", "each", "every",
            "just", "also", "very", "too", "much", "many",
            "explain", "tell", "give", "show", "please",
        ])
        words = re.findall(r"\b[a-z]+\b", message.lower())
        terms = [w for w in words if w not in stop_words and len(w) > 2]
        # Return unique terms, preserving order, max 5
        seen: set[str] = set()
        unique_terms: list[str] = []
        for term in terms:
            if term not in seen:
                seen.add(term)
                unique_terms.append(term)
            if len(unique_terms) >= 5:
                break
        return unique_terms

    def _enforce_max_topic_threads(self, ctx: ConversationContext) -> None:
        """Ensure at most _MAX_TOPIC_THREADS topic threads exist.

        Removes the oldest inactive threads first.
        """
        while len(ctx.topic_threads) > _MAX_TOPIC_THREADS:
            # Find the oldest inactive thread to remove
            for i, tt in enumerate(ctx.topic_threads):
                if not tt.is_active:
                    ctx.topic_threads.pop(i)
                    break
            else:
                # All threads are active (shouldn't happen), remove oldest
                ctx.topic_threads.pop(0)

    def _compute_discourse_state(
        self, intent: str, ctx: ConversationContext
    ) -> DiscourseState:
        """Determine the next discourse state based on the current intent."""
        if intent == "quiz_me":
            return DiscourseState.QUIZ_PENDING
        if intent in ("explain_section", "give_example", "summarize"):
            return DiscourseState.FOLLOW_UP
        if intent == "conceptual_question" and ctx.socratic_state.active:
            return DiscourseState.SOCRATIC_EXCHANGE
        return DiscourseState.FOLLOW_UP

    def _deserialize(self, data: dict[str, Any]) -> ConversationContext:
        """Deserialize a dict into a ConversationContext.

        Handles schema migration for older versions (Requirement 7.5).
        Raises KeyError/TypeError/ValueError on invalid data.
        """
        schema_version = data.get("schema_version")

        # Reject unknown future versions — cannot forward-migrate
        if schema_version is None or not isinstance(schema_version, int):
            raise ValueError(f"Missing or invalid schema_version: {schema_version}")
        if schema_version > _CURRENT_SCHEMA_VERSION:
            raise ValueError(f"Unrecognized schema version: {schema_version}")

        # Migrate older versions to current (Requirement 7.5)
        if schema_version < _CURRENT_SCHEMA_VERSION:
            data = self._migrate(data, schema_version)

        # Parse exchanges
        raw_exchanges = data.get("exchanges")
        if not isinstance(raw_exchanges, list):
            raw_exchanges = []
        exchanges = [
            Exchange(
                user_message=ex["user_message"],
                assistant_response=ex["assistant_response"],
                intent=ex["intent"],
                topic_thread_subject=ex["topic_thread_subject"],
            )
            for ex in raw_exchanges
        ]

        # Parse topic threads
        raw_threads = data.get("topic_threads")
        if not isinstance(raw_threads, list):
            raw_threads = []
        topic_threads = [
            TopicThread(
                subject=tt["subject"],
                start_exchange_index=tt["start_exchange_index"],
                key_terms=list(tt.get("key_terms", [])),
                is_active=tt.get("is_active", True),
            )
            for tt in raw_threads
        ]

        # Parse discourse state
        raw_discourse = data.get("discourse_state", "initial")
        discourse_state = DiscourseState(raw_discourse)

        # Parse socratic state
        ss_data = data.get("socratic_state")
        if not isinstance(ss_data, dict):
            ss_data = {}
        socratic_state = SocraticState(
            active=bool(ss_data.get("active", False)),
            target_concept=ss_data.get("target_concept"),
            key_terms=list(ss_data.get("key_terms", [])),
            attempts=int(ss_data.get("attempts", 0)),
            reasoning_type=ss_data.get("reasoning_type"),
        )

        # Parse complexity override
        co_data = data.get("complexity_override")
        complexity_override = None
        if co_data is not None and isinstance(co_data, dict):
            complexity_override = ComplexityOverride(
                level=ComplexityLevel(co_data["level"]),
                remaining_responses=int(co_data["remaining_responses"]),
            )

        # Parse template usage
        raw_usage = data.get("template_usage")
        template_usage: dict[str, list[int]] = {}
        if isinstance(raw_usage, dict):
            for key, val in raw_usage.items():
                if isinstance(key, str) and isinstance(val, list):
                    template_usage[key] = [int(v) for v in val]

        return ConversationContext(
            schema_version=_CURRENT_SCHEMA_VERSION,
            exchanges=exchanges,
            topic_threads=topic_threads,
            discourse_state=discourse_state,
            socratic_state=socratic_state,
            complexity_override=complexity_override,
            template_usage=template_usage,
        )

    def _migrate(self, data: dict[str, Any], from_version: int) -> dict[str, Any]:
        """Migrate a serialized context from an older schema version.

        Applies sequential migrations from from_version up to
        _CURRENT_SCHEMA_VERSION, preserving all compatible state
        (Requirement 7.5).
        """
        migrated = dict(data)

        # Migration from version 0 → 1:
        # Version 0 didn't have socratic_state, complexity_override, or
        # template_usage. Fill with defaults.
        if from_version < 1:
            if "socratic_state" not in migrated:
                migrated["socratic_state"] = {
                    "active": False,
                    "target_concept": None,
                    "key_terms": [],
                    "attempts": 0,
                    "reasoning_type": None,
                }
            if "complexity_override" not in migrated:
                migrated["complexity_override"] = None
            if "template_usage" not in migrated:
                migrated["template_usage"] = {}
            if "discourse_state" not in migrated:
                migrated["discourse_state"] = "initial"
            # Ensure topic threads have key_terms and is_active
            for tt in migrated.get("topic_threads", []):
                if "key_terms" not in tt:
                    tt["key_terms"] = []
                if "is_active" not in tt:
                    tt["is_active"] = True

        migrated["schema_version"] = _CURRENT_SCHEMA_VERSION
        return migrated
