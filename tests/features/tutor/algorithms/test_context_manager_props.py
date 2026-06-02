"""Property-based tests for the Context Manager.

Uses Hypothesis to validate universal correctness properties of the
ContextManager module.
"""

from __future__ import annotations

import re

from hypothesis import assume, given, settings
from hypothesis.strategies import (
    booleans,
    composite,
    dictionaries,
    floats,
    integers,
    just,
    lists,
    none,
    one_of,
    sampled_from,
    text,
)

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
    _ANAPHORIC_PATTERNS,
    _MAX_EXCHANGES,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Anaphoric words to exclude from generated messages for Property 3
_ANAPHORIC_WORDS = frozenset([
    "it", "that", "this", "these", "those", "them", "its",
])


@composite
def disjoint_term_sets(draw):
    """Generate two sets of words that share zero terms.

    Returns (thread_terms, message_words) where:
    - thread_terms: list of 1-5 words for a TopicThread's key_terms
    - message_words: list of 1-5 words guaranteed disjoint from thread_terms
      and containing no anaphoric references
    """
    # Use prefix 'aaa' for thread terms and prefix 'zzz' for message terms
    # to guarantee disjointness via non-overlapping character spaces
    num_thread_terms = draw(integers(min_value=1, max_value=5))
    thread_terms = []
    for _ in range(num_thread_terms):
        suffix = draw(text(alphabet="bcdefgh", min_size=2, max_size=6))
        term = f"aaa{suffix}"
        thread_terms.append(term)

    num_message_words = draw(integers(min_value=1, max_value=5))
    message_words = []
    for _ in range(num_message_words):
        suffix = draw(text(alphabet="vwxyz", min_size=2, max_size=6))
        word = f"zzz{suffix}"
        assume(word not in _ANAPHORIC_WORDS)
        message_words.append(word)

    return thread_terms, message_words


# ---------------------------------------------------------------------------
# Strategy for Property 1: Context exchange window invariant
# ---------------------------------------------------------------------------

_INTENTS = [
    "explain_section",
    "give_example",
    "summarize",
    "quiz_me",
    "conceptual_question",
    "greeting",
    "thanks",
]


@composite
def exchange_sequence(draw):
    """Generate a list of 1–20 exchanges with varied topic subjects.

    Returns a list of (user_message, response, intent, topic_subject) tuples.
    Uses 1–4 distinct topic subjects to simulate real conversations where
    some exchanges share a topic and some shift topics.
    """
    num_subjects = draw(integers(min_value=1, max_value=4))
    subjects = [
        draw(text(alphabet="abcdefghijklmnop", min_size=3, max_size=10))
        for _ in range(num_subjects)
    ]
    # Ensure subjects are unique and non-empty
    subjects = list({s for s in subjects if len(s) >= 3})
    assume(len(subjects) >= 1)

    num_exchanges = draw(integers(min_value=1, max_value=20))
    exchanges = []
    for _ in range(num_exchanges):
        subject = draw(sampled_from(subjects))
        intent = draw(sampled_from(_INTENTS))
        user_msg = f"tell me about {subject}"
        response = f"Here is info about {subject}."
        exchanges.append((user_msg, response, intent, subject))

    return exchanges


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 1: Context exchange window invariant
# ---------------------------------------------------------------------------


class TestContextExchangeWindowInvariant:
    """For any sequence of N user-assistant exchanges (N >= 1) added to a
    ConversationContext, the context SHALL contain at most 10 exchanges,
    the oldest SHALL be evicted first, and any TopicThread subject from an
    evicted exchange SHALL remain in the topic_threads list if that thread
    is still referenced by exchanges within the window.

    **Validates: Requirements 1.6, 1.7**
    """

    @settings(max_examples=30)
    @given(data=exchange_sequence())
    def test_context_never_exceeds_max_exchanges(
        self,
        data: list[tuple[str, str, str, str]],
    ) -> None:
        """After any number of exchanges are added via update_context,
        the context never holds more than 10 exchanges."""
        cm = ContextManager()
        ctx = ConversationContext()

        for user_msg, response, intent, _ in data:
            ctx = cm.update_context(ctx, user_msg, response, intent)
            assert len(ctx.exchanges) <= _MAX_EXCHANGES, (
                f"Context has {len(ctx.exchanges)} exchanges, exceeds max "
                f"of {_MAX_EXCHANGES}."
            )

    @settings(max_examples=30)
    @given(data=exchange_sequence())
    def test_evicted_topic_subjects_preserved_when_still_referenced(
        self,
        data: list[tuple[str, str, str, str]],
    ) -> None:
        """When eviction occurs via evict_oldest(), topic thread subjects
        from evicted exchanges are preserved in topic_threads if still
        referenced by remaining exchanges within the window.

        This tests evict_oldest() in isolation to verify Requirement 1.7
        without interference from the _MAX_TOPIC_THREADS limit."""
        cm = ContextManager()
        ctx = ConversationContext()

        # Build exchanges and topic threads directly to test eviction logic
        for user_msg, response, intent, subject in data:
            exchange = Exchange(
                user_message=user_msg,
                assistant_response=response,
                intent=intent,
                topic_thread_subject=subject,
            )
            ctx.exchanges.append(exchange)

            # Ensure each subject has a topic thread entry
            existing_subjects = {tt.subject for tt in ctx.topic_threads}
            if subject not in existing_subjects:
                ctx.topic_threads.append(
                    TopicThread(
                        subject=subject,
                        start_exchange_index=len(ctx.exchanges) - 1,
                        key_terms=[subject],
                        is_active=True,
                    )
                )

        # Only test eviction behavior when we exceed the window
        if len(ctx.exchanges) > _MAX_EXCHANGES:
            ctx = cm.evict_oldest(ctx)

            # After eviction, every subject still referenced in the exchange
            # window must have a topic thread entry
            subjects_in_window = {ex.topic_thread_subject for ex in ctx.exchanges}
            subjects_in_threads = {tt.subject for tt in ctx.topic_threads}

            for subject in subjects_in_window:
                assert subject in subjects_in_threads, (
                    f"Topic subject {subject!r} is referenced by an exchange "
                    f"in the window but has no corresponding TopicThread "
                    f"entry after eviction.\n"
                    f"Subjects in window: {subjects_in_window}\n"
                    f"Subjects in threads: {subjects_in_threads}"
                )

    @settings(max_examples=30)
    @given(data=exchange_sequence())
    def test_evict_oldest_maintains_window_size(
        self,
        data: list[tuple[str, str, str, str]],
    ) -> None:
        """The evict_oldest() method removes the oldest exchanges first,
        keeping at most 10 in the window."""
        cm = ContextManager()
        ctx = ConversationContext()

        # Add all exchanges directly to ctx.exchanges (bypassing update_context)
        # to test evict_oldest in isolation
        for user_msg, response, intent, subject in data:
            exchange = Exchange(
                user_message=user_msg,
                assistant_response=response,
                intent=intent,
                topic_thread_subject=subject,
            )
            ctx.exchanges.append(exchange)

            # Add a topic thread for this subject if not already present
            existing_subjects = {tt.subject for tt in ctx.topic_threads}
            if subject not in existing_subjects:
                ctx.topic_threads.append(
                    TopicThread(
                        subject=subject,
                        start_exchange_index=len(ctx.exchanges) - 1,
                        key_terms=[subject],
                        is_active=True,
                    )
                )

        # Run evict_oldest if over limit
        if len(ctx.exchanges) > _MAX_EXCHANGES:
            ctx = cm.evict_oldest(ctx)

        assert len(ctx.exchanges) <= _MAX_EXCHANGES, (
            f"evict_oldest left {len(ctx.exchanges)} exchanges, expected "
            f"<= {_MAX_EXCHANGES}."
        )

    @settings(max_examples=30)
    @given(data=exchange_sequence())
    def test_eviction_removes_oldest_first(
        self,
        data: list[tuple[str, str, str, str]],
    ) -> None:
        """Eviction removes the oldest exchanges first — the remaining
        exchanges are the most recent ones in order."""
        cm = ContextManager()
        ctx = ConversationContext()

        all_exchanges: list[Exchange] = []
        for user_msg, response, intent, subject in data:
            exchange = Exchange(
                user_message=user_msg,
                assistant_response=response,
                intent=intent,
                topic_thread_subject=subject,
            )
            all_exchanges.append(exchange)
            ctx.exchanges.append(exchange)

            existing_subjects = {tt.subject for tt in ctx.topic_threads}
            if subject not in existing_subjects:
                ctx.topic_threads.append(
                    TopicThread(
                        subject=subject,
                        start_exchange_index=len(ctx.exchanges) - 1,
                        key_terms=[subject],
                        is_active=True,
                    )
                )

        if len(ctx.exchanges) > _MAX_EXCHANGES:
            ctx = cm.evict_oldest(ctx)

        # The remaining exchanges should be the last N (where N <= 10)
        expected_remaining = all_exchanges[-_MAX_EXCHANGES:]
        assert ctx.exchanges == expected_remaining, (
            "After eviction, remaining exchanges are not the most recent ones."
        )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 3: Topic shift detection on term disjointness
# ---------------------------------------------------------------------------


class TestTopicShiftDetectionOnTermDisjointness:
    """For any user message and active TopicThread, if the message shares
    zero key terms with the thread's subject AND contains no anaphoric
    references, the ContextManager SHALL detect a topic shift and start
    a new TopicThread.

    **Validates: Requirements 1.4**
    """

    @settings(max_examples=30)
    @given(data=disjoint_term_sets())
    def test_disjoint_message_triggers_topic_shift(
        self,
        data: tuple[list[str], list[str]],
    ) -> None:
        """When a message shares zero key terms with the active thread and
        contains no anaphoric references, detect_topic_shift returns True."""
        thread_terms, message_words = data

        # Build the message from the disjoint words
        message = " ".join(message_words)

        # Verify our message doesn't accidentally contain anaphoric patterns
        for pattern in _ANAPHORIC_PATTERNS:
            assume(not pattern.search(message))

        # Build a context with an active topic thread
        subject = thread_terms[0] if thread_terms else "aaatopic"
        thread = TopicThread(
            subject=subject,
            start_exchange_index=0,
            key_terms=thread_terms,
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        # Verify disjointness: no word in message appears in thread terms or subject
        message_word_set = set(re.findall(r"\b[a-z]+\b", message.lower()))
        subject_word_set = set(re.findall(r"\b[a-z]+\b", subject.lower()))
        all_thread_words = set()
        for term in thread_terms:
            all_thread_words.update(re.findall(r"\b[a-z]+\b", term.lower()))
        all_thread_words.update(subject_word_set)

        assume(len(message_word_set & all_thread_words) == 0)

        # Act
        cm = ContextManager()
        result = cm.detect_topic_shift(ctx, message)

        # Assert: topic shift SHALL be detected
        assert result is True, (
            f"Expected topic shift but got False.\n"
            f"Message: {message!r}\n"
            f"Thread subject: {subject!r}\n"
            f"Thread key_terms: {thread_terms}\n"
        )

    @settings(max_examples=30)
    @given(data=disjoint_term_sets())
    def test_no_shift_when_no_active_thread(
        self,
        data: tuple[list[str], list[str]],
    ) -> None:
        """When there is no active topic thread, no topic shift is detected
        (it's a new conversation, not a shift)."""
        _, message_words = data
        message = " ".join(message_words)

        # Context with no active thread
        ctx = ConversationContext(topic_threads=[])

        cm = ContextManager()
        result = cm.detect_topic_shift(ctx, message)

        assert result is False

    @settings(max_examples=30)
    @given(data=disjoint_term_sets())
    def test_no_shift_when_message_contains_anaphoric_reference(
        self,
        data: tuple[list[str], list[str]],
    ) -> None:
        """When a message contains an anaphoric reference, no topic shift
        is detected even if terms are disjoint."""
        thread_terms, message_words = data

        # Add an anaphoric word to the message
        message = " ".join(message_words) + " explain it more"

        subject = thread_terms[0] if thread_terms else "aaatopic"
        thread = TopicThread(
            subject=subject,
            start_exchange_index=0,
            key_terms=thread_terms,
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        cm = ContextManager()
        result = cm.detect_topic_shift(ctx, message)

        assert result is False, (
            f"Expected no topic shift (anaphoric reference present) but got True.\n"
            f"Message: {message!r}\n"
        )

    @settings(max_examples=30)
    @given(data=disjoint_term_sets())
    def test_no_shift_when_message_shares_terms(
        self,
        data: tuple[list[str], list[str]],
    ) -> None:
        """When a message shares key terms with the active thread, no topic
        shift is detected."""
        thread_terms, _ = data
        assume(len(thread_terms) > 0)

        # Build message that includes one of the thread terms
        shared_term = thread_terms[0]
        message = f"tell me more about {shared_term} please"

        # Ensure message doesn't accidentally have anaphoric patterns
        for pattern in _ANAPHORIC_PATTERNS:
            assume(not pattern.search(message))

        subject = thread_terms[0]
        thread = TopicThread(
            subject=subject,
            start_exchange_index=0,
            key_terms=thread_terms,
            is_active=True,
        )
        ctx = ConversationContext(topic_threads=[thread])

        cm = ContextManager()
        result = cm.detect_topic_shift(ctx, message)

        assert result is False, (
            f"Expected no topic shift (shared terms) but got True.\n"
            f"Message: {message!r}\n"
            f"Shared term: {shared_term!r}\n"
        )


# ---------------------------------------------------------------------------
# Strategies for Property 17: Context serialization round-trip
# ---------------------------------------------------------------------------

# Safe text that doesn't cause issues with serialization
_safe_text = text(
    alphabet="abcdefghijklmnopqrstuvwxyz ",
    min_size=1,
    max_size=30,
)

_intent_names = sampled_from([
    "explain_section",
    "give_example",
    "summarize",
    "quiz_me",
    "greeting",
    "thanks",
    "conceptual_question",
    "direct_answer_request",
    "quiz_answer_attempt",
    "complexity_adjustment",
    "cross_reference_request",
])

_reasoning_types = sampled_from([
    "definition_recall",
    "comparison",
    "application",
    "cause_effect",
])


@composite
def exchanges_strategy(draw):
    """Generate a valid Exchange."""
    return Exchange(
        user_message=draw(_safe_text),
        assistant_response=draw(_safe_text),
        intent=draw(_intent_names),
        topic_thread_subject=draw(_safe_text),
    )


@composite
def topic_threads_strategy(draw):
    """Generate a valid TopicThread."""
    return TopicThread(
        subject=draw(_safe_text),
        start_exchange_index=draw(integers(min_value=0, max_value=9)),
        key_terms=draw(lists(_safe_text, min_size=0, max_size=5)),
        is_active=draw(booleans()),
    )


@composite
def socratic_state_strategy(draw):
    """Generate a valid SocraticState."""
    active = draw(booleans())
    return SocraticState(
        active=active,
        target_concept=draw(one_of(none(), _safe_text)),
        key_terms=draw(lists(_safe_text, min_size=0, max_size=3)),
        attempts=draw(integers(min_value=0, max_value=3)),
        reasoning_type=draw(one_of(none(), _reasoning_types)),
    )


@composite
def complexity_override_strategy(draw):
    """Generate a valid ComplexityOverride or None."""
    if draw(booleans()):
        return None
    return ComplexityOverride(
        level=draw(sampled_from(ComplexityLevel)),
        remaining_responses=draw(integers(min_value=0, max_value=3)),
    )


@composite
def template_usage_strategy(draw):
    """Generate a valid template_usage dict."""
    num_entries = draw(integers(min_value=0, max_value=4))
    usage: dict[str, list[int]] = {}
    for _ in range(num_entries):
        intent = draw(_intent_names)
        indices = draw(lists(integers(min_value=0, max_value=5), min_size=0, max_size=4))
        usage[intent] = indices
    return usage


@composite
def conversation_context_strategy(draw):
    """Generate a valid ConversationContext with all fields populated."""
    return ConversationContext(
        schema_version=CURRENT_SCHEMA_VERSION,
        exchanges=draw(lists(exchanges_strategy(), min_size=0, max_size=10)),
        topic_threads=draw(lists(topic_threads_strategy(), min_size=0, max_size=4)),
        discourse_state=draw(sampled_from(DiscourseState)),
        socratic_state=draw(socratic_state_strategy()),
        complexity_override=draw(complexity_override_strategy()),
        template_usage=draw(template_usage_strategy()),
    )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 17: Context serialization round-trip
# ---------------------------------------------------------------------------


class TestContextSerializationRoundTrip:
    """For any valid ConversationContext, serializing to JSON and
    deserializing back SHALL produce a structurally equal
    ConversationContext where all fields contain the same values.

    serialize(deserialize(serialize(ctx))) == serialize(ctx)

    **Validates: Requirements 7.2, 7.3**
    """

    @settings(max_examples=30)
    @given(ctx=conversation_context_strategy())
    def test_serialize_deserialize_round_trip(self, ctx: ConversationContext) -> None:
        """Serializing and deserializing produces an equivalent context."""
        cm = ContextManager()

        # Serialize the original context
        serialized = cm.serialize(ctx)

        # Deserialize back to a ConversationContext
        reconstructed = cm.build_context(serialized)

        # Serialize the reconstructed context
        re_serialized = cm.serialize(reconstructed)

        # The two serialized forms must be identical
        assert serialized == re_serialized, (
            f"Round-trip failed.\n"
            f"Original serialized: {serialized}\n"
            f"Re-serialized: {re_serialized}\n"
        )

    @settings(max_examples=30)
    @given(ctx=conversation_context_strategy())
    def test_schema_version_included_in_serialized_output(
        self, ctx: ConversationContext
    ) -> None:
        """Schema version is always included in serialized output."""
        cm = ContextManager()
        serialized = cm.serialize(ctx)

        assert "schema_version" in serialized
        assert serialized["schema_version"] == CURRENT_SCHEMA_VERSION

    @settings(max_examples=30)
    @given(ctx=conversation_context_strategy())
    def test_all_fields_survive_round_trip(self, ctx: ConversationContext) -> None:
        """All fields survive the round-trip: exchanges, topic_threads,
        discourse_state, socratic_state."""
        cm = ContextManager()

        serialized = cm.serialize(ctx)
        reconstructed = cm.build_context(serialized)

        # exchanges count matches
        assert len(reconstructed.exchanges) == len(ctx.exchanges)
        for orig, recon in zip(ctx.exchanges, reconstructed.exchanges):
            assert orig.user_message == recon.user_message
            assert orig.assistant_response == recon.assistant_response
            assert orig.intent == recon.intent
            assert orig.topic_thread_subject == recon.topic_thread_subject

        # topic_threads count matches
        assert len(reconstructed.topic_threads) == len(ctx.topic_threads)
        for orig, recon in zip(ctx.topic_threads, reconstructed.topic_threads):
            assert orig.subject == recon.subject
            assert orig.start_exchange_index == recon.start_exchange_index
            assert orig.key_terms == recon.key_terms
            assert orig.is_active == recon.is_active

        # discourse_state matches
        assert reconstructed.discourse_state == ctx.discourse_state

        # socratic_state matches
        assert reconstructed.socratic_state.active == ctx.socratic_state.active
        assert reconstructed.socratic_state.target_concept == ctx.socratic_state.target_concept
        assert reconstructed.socratic_state.key_terms == ctx.socratic_state.key_terms
        assert reconstructed.socratic_state.attempts == ctx.socratic_state.attempts
        assert reconstructed.socratic_state.reasoning_type == ctx.socratic_state.reasoning_type

        # complexity_override matches
        if ctx.complexity_override is None:
            assert reconstructed.complexity_override is None
        else:
            assert reconstructed.complexity_override is not None
            assert reconstructed.complexity_override.level == ctx.complexity_override.level
            assert (
                reconstructed.complexity_override.remaining_responses
                == ctx.complexity_override.remaining_responses
            )

        # template_usage matches
        assert reconstructed.template_usage == ctx.template_usage


# ---------------------------------------------------------------------------
# Strategies for Property 18: Malformed context graceful recovery
# ---------------------------------------------------------------------------

# Primitive JSON-like values for building malformed dicts
_json_primitives = one_of(
    text(min_size=0, max_size=20),
    integers(min_value=-1000, max_value=1000),
    floats(allow_nan=False, allow_infinity=False),
    booleans(),
    none(),
)

# Build nested JSON-like structures (dicts and lists of primitives)
_json_values = one_of(
    _json_primitives,
    lists(_json_primitives, min_size=0, max_size=3),
    dictionaries(text(min_size=1, max_size=10), _json_primitives, min_size=0, max_size=3),
)


@composite
def malformed_context_missing_fields(draw):
    """Generate a dict that looks like a context but is missing required fields."""
    # Start with schema_version but omit key fields randomly
    d: dict = {"schema_version": CURRENT_SCHEMA_VERSION}
    # Randomly include/exclude fields with wrong or missing content
    if draw(booleans()):
        d["exchanges"] = draw(_json_values)  # wrong type (not a list of dicts)
    if draw(booleans()):
        d["topic_threads"] = draw(_json_values)
    if draw(booleans()):
        d["discourse_state"] = draw(one_of(
            integers(),  # wrong type
            text(alphabet="xyz", min_size=1, max_size=5),  # invalid enum value
            none(),
        ))
    return d


@composite
def malformed_context_wrong_types(draw):
    """Generate a dict with correct keys but wrong value types."""
    return {
        "schema_version": CURRENT_SCHEMA_VERSION,
        "exchanges": draw(one_of(
            just("not a list"),
            just(123),
            # List of dicts missing required fields
            lists(
                dictionaries(text(min_size=1, max_size=8), _json_primitives, min_size=0, max_size=2),
                min_size=1,
                max_size=3,
            ),
        )),
        "topic_threads": draw(one_of(
            just(None),
            just("wrong"),
            just(42),
        )),
        "discourse_state": draw(one_of(
            just(999),
            just("invalid_state"),
            none(),
        )),
        "socratic_state": draw(one_of(
            just("not a dict"),
            just(None),
            just([1, 2, 3]),
        )),
        "complexity_override": draw(_json_values),
        "template_usage": draw(one_of(
            just("not a dict"),
            just(123),
            none(),
        )),
    }


@composite
def malformed_context_bad_schema_version(draw):
    """Generate a dict with an unrecognized or invalid schema_version."""
    bad_version = draw(one_of(
        integers(min_value=CURRENT_SCHEMA_VERSION + 1, max_value=999),  # future version
        just(None),
        just("one"),  # wrong type
        just(-1),  # negative
        just(3.14),  # float
    ))
    return {
        "schema_version": bad_version,
        "exchanges": [],
        "topic_threads": [],
        "discourse_state": "initial",
    }


@composite
def malformed_context_random_garbage(draw):
    """Generate a completely random dict with no relation to expected schema."""
    return draw(dictionaries(
        text(min_size=1, max_size=15),
        _json_values,
        min_size=0,
        max_size=8,
    ))


@composite
def malformed_context_any(draw):
    """Draw from any of the malformed context strategies."""
    strategy = draw(sampled_from([
        malformed_context_missing_fields(),
        malformed_context_wrong_types(),
        malformed_context_bad_schema_version(),
        malformed_context_random_garbage(),
    ]))
    return draw(strategy)


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 18: Malformed context graceful recovery
# ---------------------------------------------------------------------------


class TestMalformedContextGracefulRecovery:
    """For any dict that fails ConversationContext validation (missing
    required fields, wrong types, or unrecognized schema_version), the
    ContextManager SHALL return a fresh default ConversationContext
    without raising an exception.

    **Validates: Requirements 7.4**
    """

    @settings(max_examples=30)
    @given(malformed=malformed_context_any())
    def test_malformed_context_returns_fresh_context(
        self, malformed: dict
    ) -> None:
        """build_context() never raises on malformed input and returns
        a fresh ConversationContext with default values."""
        cm = ContextManager()

        # This must NOT raise any exception
        result = cm.build_context(malformed)

        # Result is a valid ConversationContext
        assert isinstance(result, ConversationContext)

        # Fresh context has empty exchanges
        assert result.exchanges == []

        # Fresh context has no topic threads
        assert result.topic_threads == []

        # Fresh context has INITIAL discourse state
        assert result.discourse_state == DiscourseState.INITIAL

        # Fresh context has inactive socratic state
        assert result.socratic_state.active is False
        assert result.socratic_state.attempts == 0

        # Fresh context has no complexity override
        assert result.complexity_override is None

    @settings(max_examples=30)
    @given(malformed=malformed_context_missing_fields())
    def test_missing_fields_returns_fresh_context(self, malformed: dict) -> None:
        """Dicts with correct schema_version but missing/corrupt required
        fields still produce a fresh context without exception."""
        cm = ContextManager()

        result = cm.build_context(malformed)

        assert isinstance(result, ConversationContext)
        assert result.discourse_state == DiscourseState.INITIAL

    @settings(max_examples=30)
    @given(malformed=malformed_context_wrong_types())
    def test_wrong_types_returns_fresh_context(self, malformed: dict) -> None:
        """Dicts with correct keys but wrong value types produce a fresh
        context without exception."""
        cm = ContextManager()

        result = cm.build_context(malformed)

        assert isinstance(result, ConversationContext)
        assert result.exchanges == []
        assert result.discourse_state == DiscourseState.INITIAL

    @settings(max_examples=30)
    @given(malformed=malformed_context_bad_schema_version())
    def test_bad_schema_version_returns_fresh_context(self, malformed: dict) -> None:
        """Dicts with unrecognized or invalid schema_version produce a
        fresh context without exception."""
        cm = ContextManager()

        result = cm.build_context(malformed)

        assert isinstance(result, ConversationContext)
        assert result.exchanges == []
        assert result.discourse_state == DiscourseState.INITIAL

    @settings(max_examples=30)
    @given(malformed=malformed_context_random_garbage())
    def test_random_garbage_returns_fresh_context(self, malformed: dict) -> None:
        """Completely random dicts produce a fresh context without exception."""
        cm = ContextManager()

        result = cm.build_context(malformed)

        assert isinstance(result, ConversationContext)
        assert result.exchanges == []
        assert result.topic_threads == []
        assert result.discourse_state == DiscourseState.INITIAL
