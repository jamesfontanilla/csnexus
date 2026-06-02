"""Unit tests for the Context Manager.

Tests context construction, exchange eviction, topic shift detection,
serialization/deserialization round-trip, and schema version migration.

Requirements: 1.1, 1.4, 1.6, 1.7, 7.1, 7.2, 7.3, 7.4, 7.5
"""

from __future__ import annotations

import pytest

from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ComplexityOverride,
    ConversationContext,
    DiscourseState,
    Exchange,
    SocraticState,
    TopicThread,
)
from app.features.tutor.algorithms.context_manager import (
    CURRENT_SCHEMA_VERSION,
    ContextManager,
    _MAX_EXCHANGES,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_exchange(
    user_message: str = "hello",
    assistant_response: str = "hi there",
    intent: str = "greeting",
    topic_thread_subject: str = "greetings",
) -> Exchange:
    """Build an Exchange with sensible defaults."""
    return Exchange(
        user_message=user_message,
        assistant_response=assistant_response,
        intent=intent,
        topic_thread_subject=topic_thread_subject,
    )


def _make_context_with_exchanges(n: int, subject: str = "algebra") -> ConversationContext:
    """Build a ConversationContext pre-loaded with n exchanges."""
    exchanges = [
        _make_exchange(
            user_message=f"msg {i}",
            assistant_response=f"resp {i}",
            intent="explain_section",
            topic_thread_subject=subject,
        )
        for i in range(n)
    ]
    thread = TopicThread(
        subject=subject,
        start_exchange_index=0,
        key_terms=[subject],
        is_active=True,
    )
    return ConversationContext(
        exchanges=exchanges,
        topic_threads=[thread],
    )


# ---------------------------------------------------------------------------
# Tests: build_context (Req 1.1, 7.1, 7.4)
# ---------------------------------------------------------------------------


class TestBuildContextFromNone:
    """Test context construction from None (fresh context)."""

    def test_none_returns_fresh_context(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context(None)

        assert isinstance(ctx, ConversationContext)
        assert ctx.exchanges == []
        assert ctx.topic_threads == []
        assert ctx.discourse_state == DiscourseState.INITIAL
        assert ctx.socratic_state.active is False
        assert ctx.complexity_override is None
        assert ctx.template_usage == {}

    def test_fresh_context_has_current_schema_version(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context(None)
        assert ctx.schema_version == CURRENT_SCHEMA_VERSION


class TestBuildContextFromValidDict:
    """Test context construction from a valid serialized dict."""

    def test_valid_dict_reconstructs_exchanges(self) -> None:
        cm = ContextManager()
        serialized = {
            "schema_version": CURRENT_SCHEMA_VERSION,
            "exchanges": [
                {
                    "user_message": "What is algebra?",
                    "assistant_response": "Algebra is...",
                    "intent": "explain_section",
                    "topic_thread_subject": "algebra",
                }
            ],
            "topic_threads": [
                {
                    "subject": "algebra",
                    "start_exchange_index": 0,
                    "key_terms": ["algebra", "variables"],
                    "is_active": True,
                }
            ],
            "discourse_state": "follow_up",
            "socratic_state": {
                "active": False,
                "target_concept": None,
                "key_terms": [],
                "attempts": 0,
                "reasoning_type": None,
            },
            "complexity_override": None,
            "template_usage": {"explain_section": [0, 1]},
        }

        ctx = cm.build_context(serialized)

        assert len(ctx.exchanges) == 1
        assert ctx.exchanges[0].user_message == "What is algebra?"
        assert ctx.exchanges[0].intent == "explain_section"
        assert ctx.topic_threads[0].subject == "algebra"
        assert ctx.topic_threads[0].key_terms == ["algebra", "variables"]
        assert ctx.discourse_state == DiscourseState.FOLLOW_UP
        assert ctx.template_usage == {"explain_section": [0, 1]}

    def test_valid_dict_with_complexity_override(self) -> None:
        cm = ContextManager()
        serialized = {
            "schema_version": CURRENT_SCHEMA_VERSION,
            "exchanges": [],
            "topic_threads": [],
            "discourse_state": "initial",
            "socratic_state": {
                "active": False,
                "target_concept": None,
                "key_terms": [],
                "attempts": 0,
                "reasoning_type": None,
            },
            "complexity_override": {
                "level": "SIMPLIFIED",
                "remaining_responses": 2,
            },
            "template_usage": {},
        }

        ctx = cm.build_context(serialized)

        assert ctx.complexity_override is not None
        assert ctx.complexity_override.level == ComplexityLevel.SIMPLIFIED
        assert ctx.complexity_override.remaining_responses == 2

    def test_valid_dict_with_active_socratic_state(self) -> None:
        cm = ContextManager()
        serialized = {
            "schema_version": CURRENT_SCHEMA_VERSION,
            "exchanges": [],
            "topic_threads": [],
            "discourse_state": "socratic_exchange",
            "socratic_state": {
                "active": True,
                "target_concept": "variable isolation",
                "key_terms": ["isolate", "variable", "equation"],
                "attempts": 2,
                "reasoning_type": "application",
            },
            "complexity_override": None,
            "template_usage": {},
        }

        ctx = cm.build_context(serialized)

        assert ctx.socratic_state.active is True
        assert ctx.socratic_state.target_concept == "variable isolation"
        assert ctx.socratic_state.key_terms == ["isolate", "variable", "equation"]
        assert ctx.socratic_state.attempts == 2
        assert ctx.socratic_state.reasoning_type == "application"


class TestBuildContextFromMalformedDict:
    """Test context construction from malformed dicts (Req 7.4)."""

    def test_empty_dict_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({})
        assert isinstance(ctx, ConversationContext)
        assert ctx.exchanges == []

    def test_missing_schema_version_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({"exchanges": [], "topic_threads": []})
        assert ctx.exchanges == []
        assert ctx.discourse_state == DiscourseState.INITIAL

    def test_future_schema_version_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({"schema_version": 999, "exchanges": []})
        assert ctx.exchanges == []
        assert ctx.discourse_state == DiscourseState.INITIAL

    def test_non_integer_schema_version_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({"schema_version": "one"})
        assert isinstance(ctx, ConversationContext)
        assert ctx.exchanges == []

    def test_exchanges_wrong_type_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({
            "schema_version": CURRENT_SCHEMA_VERSION,
            "exchanges": "not a list",
            "discourse_state": "initial",
        })
        # Should still produce a valid context (exchanges treated as empty)
        assert isinstance(ctx, ConversationContext)

    def test_invalid_discourse_state_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({
            "schema_version": CURRENT_SCHEMA_VERSION,
            "exchanges": [],
            "topic_threads": [],
            "discourse_state": "nonexistent_state",
        })
        assert isinstance(ctx, ConversationContext)
        assert ctx.exchanges == []

    def test_none_value_for_required_exchange_field_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({
            "schema_version": CURRENT_SCHEMA_VERSION,
            "exchanges": [{"user_message": None}],
            "topic_threads": [],
            "discourse_state": "initial",
        })
        assert isinstance(ctx, ConversationContext)

    def test_random_garbage_returns_fresh(self) -> None:
        cm = ContextManager()
        ctx = cm.build_context({"foo": "bar", "baz": [1, 2, 3]})
        assert isinstance(ctx, ConversationContext)
        assert ctx.exchanges == []


# ---------------------------------------------------------------------------
# Tests: evict_oldest (Req 1.6, 1.7)
# ---------------------------------------------------------------------------


class TestExchangeEviction:
    """Test exchange eviction at 10 exchanges with topic thread preservation."""

    def test_no_eviction_when_at_limit(self) -> None:
        cm = ContextManager()
        ctx = _make_context_with_exchanges(10)
        ctx = cm.evict_oldest(ctx)
        assert len(ctx.exchanges) == 10

    def test_eviction_when_over_limit(self) -> None:
        cm = ContextManager()
        ctx = _make_context_with_exchanges(12)
        ctx = cm.evict_oldest(ctx)
        assert len(ctx.exchanges) == _MAX_EXCHANGES

    def test_oldest_exchanges_removed_first(self) -> None:
        cm = ContextManager()
        ctx = _make_context_with_exchanges(12)
        # The remaining exchanges should be the last 10
        ctx = cm.evict_oldest(ctx)
        assert ctx.exchanges[0].user_message == "msg 2"
        assert ctx.exchanges[-1].user_message == "msg 11"

    def test_topic_thread_preserved_when_still_referenced(self) -> None:
        """When evicted exchange's topic is still referenced by remaining
        exchanges, the topic thread must remain in the list."""
        cm = ContextManager()
        # 11 exchanges all referencing "algebra"
        ctx = _make_context_with_exchanges(11, subject="algebra")
        ctx = cm.evict_oldest(ctx)

        # "algebra" is still referenced by remaining exchanges
        subjects_in_threads = {tt.subject for tt in ctx.topic_threads}
        assert "algebra" in subjects_in_threads

    def test_topic_thread_deactivated_when_no_longer_referenced(self) -> None:
        """When no remaining exchange references the evicted thread,
        the thread is marked inactive but kept for back-references."""
        cm = ContextManager()
        ctx = ConversationContext()

        # First exchange with subject "geometry"
        ctx.exchanges.append(_make_exchange(
            user_message="what is geometry",
            topic_thread_subject="geometry",
        ))
        ctx.topic_threads.append(TopicThread(
            subject="geometry",
            start_exchange_index=0,
            key_terms=["geometry"],
            is_active=True,
        ))

        # 10 more exchanges with subject "algebra"
        for i in range(10):
            ctx.exchanges.append(_make_exchange(
                user_message=f"algebra msg {i}",
                topic_thread_subject="algebra",
            ))
        ctx.topic_threads.append(TopicThread(
            subject="algebra",
            start_exchange_index=1,
            key_terms=["algebra"],
            is_active=True,
        ))

        # Now we have 11 exchanges — evict oldest
        ctx = cm.evict_oldest(ctx)

        # "geometry" is no longer referenced by any remaining exchange
        geometry_thread = next(
            (tt for tt in ctx.topic_threads if tt.subject == "geometry"), None
        )
        if geometry_thread is not None:
            assert geometry_thread.is_active is False

    def test_update_context_enforces_max_exchanges(self) -> None:
        """update_context triggers eviction when adding beyond the limit."""
        cm = ContextManager()
        ctx = _make_context_with_exchanges(10)

        ctx = cm.update_context(ctx, "new message about algebra", "response", "explain_section")
        assert len(ctx.exchanges) <= _MAX_EXCHANGES


# ---------------------------------------------------------------------------
# Tests: detect_topic_shift (Req 1.4)
# ---------------------------------------------------------------------------


class TestTopicShiftDetection:
    """Test topic shift detection for disjoint terms."""

    def test_shift_detected_for_completely_disjoint_terms(self) -> None:
        cm = ContextManager()
        thread = TopicThread(
            subject="photosynthesis",
            start_exchange_index=0,
            key_terms=["photosynthesis", "chlorophyll", "sunlight"],
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        # Message about a completely different topic with no anaphoric refs
        result = cm.detect_topic_shift(ctx, "explain quantum mechanics")
        assert result is True

    def test_no_shift_when_sharing_key_terms(self) -> None:
        cm = ContextManager()
        thread = TopicThread(
            subject="photosynthesis",
            start_exchange_index=0,
            key_terms=["photosynthesis", "chlorophyll", "sunlight"],
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        result = cm.detect_topic_shift(ctx, "how does chlorophyll work")
        assert result is False

    def test_no_shift_when_message_contains_anaphoric_reference(self) -> None:
        cm = ContextManager()
        thread = TopicThread(
            subject="photosynthesis",
            start_exchange_index=0,
            key_terms=["photosynthesis", "chlorophyll"],
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        # "it" is anaphoric — refers back to current topic
        result = cm.detect_topic_shift(ctx, "explain it in simpler words")
        assert result is False

    def test_no_shift_when_no_active_thread(self) -> None:
        cm = ContextManager()
        ctx = ConversationContext(topic_threads=[])

        result = cm.detect_topic_shift(ctx, "random message about anything")
        assert result is False

    def test_no_shift_when_message_shares_subject_words(self) -> None:
        cm = ContextManager()
        thread = TopicThread(
            subject="subject verb agreement",
            start_exchange_index=0,
            key_terms=["subject", "verb", "agreement"],
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        result = cm.detect_topic_shift(ctx, "give me examples of verb agreement")
        assert result is False

    def test_shift_with_inactive_thread_only(self) -> None:
        """If all threads are inactive, no shift detected (treated as new)."""
        cm = ContextManager()
        thread = TopicThread(
            subject="old topic",
            start_exchange_index=0,
            key_terms=["old", "topic"],
            is_active=False,
        )
        ctx = ConversationContext(topic_threads=[thread])

        result = cm.detect_topic_shift(ctx, "brand new unrelated question")
        assert result is False


# ---------------------------------------------------------------------------
# Tests: serialization/deserialization round-trip (Req 7.2, 7.3)
# ---------------------------------------------------------------------------


class TestSerializationRoundTrip:
    """Test that serialize → deserialize produces structurally equal context."""

    def test_empty_context_round_trip(self) -> None:
        cm = ContextManager()
        ctx = ConversationContext()

        serialized = cm.serialize(ctx)
        reconstructed = cm.build_context(serialized)

        assert reconstructed.exchanges == []
        assert reconstructed.topic_threads == []
        assert reconstructed.discourse_state == DiscourseState.INITIAL
        assert reconstructed.complexity_override is None

    def test_full_context_round_trip(self) -> None:
        cm = ContextManager()
        ctx = ConversationContext(
            schema_version=CURRENT_SCHEMA_VERSION,
            exchanges=[
                Exchange(
                    user_message="what is algebra",
                    assistant_response="Algebra deals with...",
                    intent="explain_section",
                    topic_thread_subject="algebra",
                ),
                Exchange(
                    user_message="give me an example",
                    assistant_response="For instance, 2x + 3 = 7...",
                    intent="give_example",
                    topic_thread_subject="algebra",
                ),
            ],
            topic_threads=[
                TopicThread(
                    subject="algebra",
                    start_exchange_index=0,
                    key_terms=["algebra", "variables", "equations"],
                    is_active=True,
                )
            ],
            discourse_state=DiscourseState.FOLLOW_UP,
            socratic_state=SocraticState(
                active=True,
                target_concept="variable isolation",
                key_terms=["isolate", "variable"],
                attempts=1,
                reasoning_type="application",
            ),
            complexity_override=ComplexityOverride(
                level=ComplexityLevel.DETAILED,
                remaining_responses=2,
            ),
            template_usage={"explain_section": [0, 2], "give_example": [1]},
        )

        serialized = cm.serialize(ctx)
        reconstructed = cm.build_context(serialized)
        re_serialized = cm.serialize(reconstructed)

        assert serialized == re_serialized

    def test_schema_version_present_in_serialized(self) -> None:
        cm = ContextManager()
        ctx = ConversationContext()
        serialized = cm.serialize(ctx)

        assert "schema_version" in serialized
        assert serialized["schema_version"] == CURRENT_SCHEMA_VERSION

    def test_serialized_output_is_json_compatible(self) -> None:
        """All values in serialized output are JSON-compatible types."""
        import json

        cm = ContextManager()
        ctx = _make_context_with_exchanges(3)
        serialized = cm.serialize(ctx)

        # Should not raise
        json_str = json.dumps(serialized)
        assert isinstance(json_str, str)

    def test_exchanges_preserve_all_fields(self) -> None:
        cm = ContextManager()
        exchange = Exchange(
            user_message="test msg",
            assistant_response="test resp",
            intent="quiz_me",
            topic_thread_subject="math",
        )
        ctx = ConversationContext(exchanges=[exchange])

        serialized = cm.serialize(ctx)
        reconstructed = cm.build_context(serialized)

        assert reconstructed.exchanges[0].user_message == "test msg"
        assert reconstructed.exchanges[0].assistant_response == "test resp"
        assert reconstructed.exchanges[0].intent == "quiz_me"
        assert reconstructed.exchanges[0].topic_thread_subject == "math"


# ---------------------------------------------------------------------------
# Tests: schema version migration (Req 7.5)
# ---------------------------------------------------------------------------


class TestSchemaVersionMigration:
    """Test migration from older schema versions to current."""

    def test_version_0_migrates_to_current(self) -> None:
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [
                {
                    "user_message": "hi",
                    "assistant_response": "hello",
                    "intent": "greeting",
                    "topic_thread_subject": "greeting",
                }
            ],
            "topic_threads": [
                {
                    "subject": "greeting",
                    "start_exchange_index": 0,
                }
            ],
        }

        ctx = cm.build_context(old_context)

        assert isinstance(ctx, ConversationContext)
        assert ctx.schema_version == CURRENT_SCHEMA_VERSION
        assert len(ctx.exchanges) == 1
        assert ctx.exchanges[0].user_message == "hi"

    def test_version_0_fills_missing_socratic_state(self) -> None:
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [],
            "topic_threads": [],
        }

        ctx = cm.build_context(old_context)

        assert ctx.socratic_state.active is False
        assert ctx.socratic_state.attempts == 0
        assert ctx.socratic_state.key_terms == []

    def test_version_0_fills_missing_complexity_override(self) -> None:
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [],
            "topic_threads": [],
        }

        ctx = cm.build_context(old_context)
        assert ctx.complexity_override is None

    def test_version_0_fills_missing_template_usage(self) -> None:
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [],
            "topic_threads": [],
        }

        ctx = cm.build_context(old_context)
        assert ctx.template_usage == {}

    def test_version_0_fills_missing_discourse_state(self) -> None:
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [],
            "topic_threads": [],
        }

        ctx = cm.build_context(old_context)
        assert ctx.discourse_state == DiscourseState.INITIAL

    def test_version_0_topic_threads_get_key_terms_and_is_active(self) -> None:
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [],
            "topic_threads": [
                {
                    "subject": "fractions",
                    "start_exchange_index": 0,
                    # Missing key_terms and is_active
                }
            ],
        }

        ctx = cm.build_context(old_context)

        assert ctx.topic_threads[0].key_terms == []
        assert ctx.topic_threads[0].is_active is True

    def test_preserves_existing_fields_during_migration(self) -> None:
        """Migration preserves all compatible state from the old version."""
        cm = ContextManager()
        old_context = {
            "schema_version": 0,
            "exchanges": [
                {
                    "user_message": "explain fractions",
                    "assistant_response": "Fractions represent parts...",
                    "intent": "explain_section",
                    "topic_thread_subject": "fractions",
                }
            ],
            "topic_threads": [
                {
                    "subject": "fractions",
                    "start_exchange_index": 0,
                }
            ],
        }

        ctx = cm.build_context(old_context)

        assert ctx.exchanges[0].user_message == "explain fractions"
        assert ctx.exchanges[0].assistant_response == "Fractions represent parts..."
        assert ctx.topic_threads[0].subject == "fractions"
