"""Property-based tests for the Anaphora Resolver.

Uses Hypothesis to validate that anaphoric references always resolve to
the most recent active TopicThread subject in the conversation context.

# Feature: smart-chat-engine, Property 2: Anaphora resolution targets most recent thread subject
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis.strategies import (
    booleans,
    composite,
    integers,
    lists,
    sampled_from,
    text,
)

from app.features.tutor.algorithms.anaphora_resolver import AnaphoraResolver
from app.features.tutor.algorithms.chat_models import (
    ConversationContext,
    DiscourseState,
    TopicThread,
)


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

# Realistic topic subjects — normalized concept phrases of 1-5 words
SAMPLE_SUBJECTS = [
    "subject-verb agreement",
    "order of operations",
    "photosynthesis",
    "civil service exam",
    "noun forms",
    "parallel structure",
    "fraction addition",
    "reading comprehension",
    "active voice",
    "percentage problems",
    "algebraic expressions",
    "sentence structure",
    "vocabulary in context",
    "data interpretation",
    "logical reasoning",
]

# Anaphoric references that should trigger resolution
ANAPHORIC_PHRASES = [
    "explain it more",
    "what about that",
    "tell me more about this",
    "I don't understand it",
    "can you explain this concept",
    "how does that work",
    "give me an example of it",
    "why is that important",
    "break this topic down",
    "is that on the exam",
    "simplify it for me",
    "this is confusing",
    "elaborate on that concept",
    "how do I remember them",
    "what are those",
]

valid_subject = sampled_from(SAMPLE_SUBJECTS)
valid_anaphoric_message = sampled_from(ANAPHORIC_PHRASES)
valid_discourse_state = sampled_from(list(DiscourseState))


@composite
def topic_thread(draw, force_active: bool | None = None):
    """Generate a TopicThread with a realistic subject."""
    subject = draw(valid_subject)
    start_index = draw(integers(min_value=0, max_value=9))
    key_terms = subject.split("-") if "-" in subject else subject.split()
    is_active = draw(booleans()) if force_active is None else force_active
    return TopicThread(
        subject=subject,
        start_exchange_index=start_index,
        key_terms=key_terms,
        is_active=is_active,
    )


@composite
def context_with_active_thread(draw):
    """Generate a ConversationContext guaranteed to have at least one active TopicThread.

    The most recent active thread is the last active thread in the list.
    """
    # Generate 1–3 inactive threads (preserved)
    inactive_threads = draw(
        lists(topic_thread(force_active=False), min_size=0, max_size=3)
    )
    # Generate exactly 1 active thread (the most recent)
    active = draw(topic_thread(force_active=True))
    discourse_state = draw(valid_discourse_state)

    # Build the thread list: inactive threads first, then the active one last
    all_threads = inactive_threads + [active]

    ctx = ConversationContext(
        topic_threads=all_threads,
        discourse_state=discourse_state,
    )
    return ctx, active.subject


# ---------------------------------------------------------------------------
# Property 2: Anaphora resolution targets most recent thread subject
# Validates: Requirements 1.2
# ---------------------------------------------------------------------------


class TestAnaphoraResolutionTargetsMostRecentThreadSubject:
    """For any message containing an anaphoric reference (pronoun or
    demonstrative) and a ConversationContext with an active TopicThread,
    the AnaphoraResolver SHALL resolve the reference to the subject of
    the most recent active TopicThread.

    **Validates: Requirements 1.2**
    """

    @settings(max_examples=30)
    @given(
        message=valid_anaphoric_message,
        ctx_and_subject=context_with_active_thread(),
    )
    def test_resolves_to_most_recent_active_thread_subject(
        self,
        message: str,
        ctx_and_subject: tuple[ConversationContext, str],
    ) -> None:
        """Anaphoric references resolve to the most recent active thread subject."""
        ctx, expected_subject = ctx_and_subject
        resolver = AnaphoraResolver()

        result = resolver.resolve(message, ctx)

        # The referent must be the most recent active thread's subject
        assert result.referent == expected_subject, (
            f"Expected referent '{expected_subject}' but got '{result.referent}'. "
            f"Message: '{message}', threads: {[t.subject for t in ctx.topic_threads]}"
        )

    @settings(max_examples=30)
    @given(
        message=valid_anaphoric_message,
        ctx_and_subject=context_with_active_thread(),
    )
    def test_confidence_above_threshold_when_active_thread_exists(
        self,
        message: str,
        ctx_and_subject: tuple[ConversationContext, str],
    ) -> None:
        """When an active thread exists, confidence should be above the threshold."""
        ctx, _ = ctx_and_subject
        resolver = AnaphoraResolver()

        result = resolver.resolve(message, ctx)

        assert result.confidence >= 0.4, (
            f"Confidence {result.confidence} below threshold 0.4 "
            f"despite active thread existing"
        )

    @settings(max_examples=30)
    @given(
        message=valid_anaphoric_message,
        ctx_and_subject=context_with_active_thread(),
    )
    def test_resolved_message_contains_referent(
        self,
        message: str,
        ctx_and_subject: tuple[ConversationContext, str],
    ) -> None:
        """The resolved message should contain the referent replacing the pronoun."""
        ctx, expected_subject = ctx_and_subject
        resolver = AnaphoraResolver()

        result = resolver.resolve(message, ctx)

        assert expected_subject in result.resolved, (
            f"Expected '{expected_subject}' in resolved message "
            f"'{result.resolved}' but it's not there"
        )

    @settings(max_examples=30)
    @given(
        message=valid_anaphoric_message,
        ctx_and_subject=context_with_active_thread(),
    )
    def test_candidates_include_all_thread_subjects(
        self,
        message: str,
        ctx_and_subject: tuple[ConversationContext, str],
    ) -> None:
        """The candidates list should include subjects from available threads."""
        ctx, expected_subject = ctx_and_subject
        resolver = AnaphoraResolver()

        result = resolver.resolve(message, ctx)

        # The expected subject should always be in the candidates
        assert expected_subject in result.candidates, (
            f"Expected subject '{expected_subject}' not in candidates: "
            f"{result.candidates}"
        )
