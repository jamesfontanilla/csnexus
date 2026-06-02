"""Property-based tests for the Socratic Module.

Uses Hypothesis to validate universal correctness properties of the
SocraticModule.
"""

from __future__ import annotations

from hypothesis import given, settings
from hypothesis.strategies import (
    booleans,
    builds,
    integers,
    just,
    lists,
    none,
    one_of,
    sampled_from,
    text,
)

from app.features.tutor.algorithms.chat_models import (
    ConversationContext,
    DiscourseState,
    Exchange,
    MasteryLevel,
    SocraticState,
    TopicThread,
)
from app.features.tutor.algorithms.socratic_module import (
    REASONING_TYPES,
    SocraticModule,
)

# Mastery levels eligible for Socratic activation (FAMILIAR and above).
_FAMILIAR_PLUS_LEVELS = [
    MasteryLevel.FAMILIAR,
    MasteryLevel.PROFICIENT,
    MasteryLevel.ADVANCED,
    MasteryLevel.MASTERED,
]


# ---------------------------------------------------------------------------
# Shared strategies
# ---------------------------------------------------------------------------


def _topic_thread_strategy():
    """Generate arbitrary TopicThread instances."""
    return builds(
        TopicThread,
        subject=text(min_size=1, max_size=30),
        start_exchange_index=integers(min_value=0, max_value=9),
        key_terms=lists(text(min_size=1, max_size=15), min_size=0, max_size=5),
        is_active=booleans(),
    )


def _exchange_strategy():
    """Generate arbitrary Exchange instances."""
    return builds(
        Exchange,
        user_message=text(min_size=1, max_size=50),
        assistant_response=text(min_size=1, max_size=100),
        intent=text(min_size=1, max_size=20),
        topic_thread_subject=text(min_size=1, max_size=30),
    )


def _socratic_state_strategy():
    """Generate arbitrary SocraticState instances."""
    return builds(
        SocraticState,
        active=booleans(),
        target_concept=one_of(none(), text(min_size=1, max_size=30)),
        key_terms=lists(text(min_size=1, max_size=15), min_size=0, max_size=3),
        attempts=integers(min_value=0, max_value=5),
        reasoning_type=one_of(none(), sampled_from(REASONING_TYPES)),
    )


def _conversation_context_strategy():
    """Generate arbitrary ConversationContext instances."""
    return builds(
        ConversationContext,
        exchanges=lists(_exchange_strategy(), min_size=0, max_size=10),
        topic_threads=lists(_topic_thread_strategy(), min_size=0, max_size=4),
        discourse_state=sampled_from(DiscourseState),
        socratic_state=_socratic_state_strategy(),
    )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 9: Socratic evaluation partitions on key term match count
# ---------------------------------------------------------------------------


class TestSocraticEvaluationPartitionsOnKeyTermMatch:
    """For any learner response to a Socratic question with stored key_terms
    of length K (1 <= K <= 3), if the response contains >= 2 of those terms
    the evaluation SHALL return `understood=True`, and if it contains < 2
    the evaluation SHALL return `understood=False`.

    **Validates: Requirements 3.3, 3.4**
    """

    @settings(max_examples=30)
    @given(
        key_terms=lists(
            text(
                alphabet="abcdefghijklmnopqrstuvwxyz",
                min_size=4,
                max_size=10,
            ),
            min_size=2,
            max_size=3,
            unique=True,
        ),
        attempts=integers(min_value=0, max_value=2),
    )
    def test_response_with_at_least_two_key_terms_returns_understood_true(
        self, key_terms: list[str], attempts: int
    ) -> None:
        """When >= 2 key terms appear in the response, understood is True."""
        module = SocraticModule()

        # Build a response that includes at least 2 key terms.
        response = f"I think {key_terms[0]} is related to {key_terms[1]} somehow"

        socratic_state = SocraticState(
            active=True,
            target_concept="test concept",
            key_terms=key_terms,
            attempts=attempts,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(response, socratic_state)

        assert result.understood is True, (
            f"Expected understood=True when >= 2 key terms matched.\n"
            f"Key terms: {key_terms}\n"
            f"Response: {response!r}\n"
            f"Matched terms: {result.matched_terms}\n"
        )
        assert len(result.matched_terms) >= 2

    @settings(max_examples=30)
    @given(
        key_terms=lists(
            text(
                alphabet="abcdefghijklmnopqrstuvwxyz",
                min_size=4,
                max_size=10,
            ),
            min_size=2,
            max_size=3,
            unique=True,
        ),
        filler=text(
            alphabet="abcdefghijklmnopqrstuvwxyz ",
            min_size=1,
            max_size=30,
        ),
        attempts=integers(min_value=0, max_value=2),
    )
    def test_response_with_fewer_than_two_key_terms_returns_understood_false(
        self, key_terms: list[str], filler: str, attempts: int
    ) -> None:
        """When < 2 key terms appear in the response, understood is False."""
        module = SocraticModule()

        # Build a response that contains zero key terms by using filler
        # that avoids any of the generated key terms.
        # Filter out filler that accidentally contains a key term.
        response = filler
        matched_count = sum(
            1 for term in key_terms if term.lower() in response.lower()
        )
        # If the filler accidentally matched >= 2 terms, make it empty-safe
        if matched_count >= 2:
            response = "no idea"

        socratic_state = SocraticState(
            active=True,
            target_concept="test concept",
            key_terms=key_terms,
            attempts=attempts,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(response, socratic_state)

        assert result.understood is False, (
            f"Expected understood=False when < 2 key terms matched.\n"
            f"Key terms: {key_terms}\n"
            f"Response: {response!r}\n"
            f"Matched terms: {result.matched_terms}\n"
        )
        assert len(result.matched_terms) < 2

    @settings(max_examples=30)
    @given(
        key_terms=lists(
            text(
                alphabet="abcdefghijklmnopqrstuvwxyz",
                min_size=4,
                max_size=10,
            ),
            min_size=1,
            max_size=1,
            unique=True,
        ),
        attempts=integers(min_value=0, max_value=2),
    )
    def test_single_key_term_match_returns_understood_false(
        self, key_terms: list[str], attempts: int
    ) -> None:
        """When only 1 key term exists and is matched, understood is still
        False because the threshold is >= 2."""
        module = SocraticModule()

        # Response contains the single key term.
        response = f"I believe it is about {key_terms[0]} in some way"

        socratic_state = SocraticState(
            active=True,
            target_concept="test concept",
            key_terms=key_terms,
            attempts=attempts,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(response, socratic_state)

        # With only 1 key term available, max match is 1 which is < 2.
        assert result.understood is False, (
            f"Expected understood=False when only 1 key term can be matched.\n"
            f"Key terms: {key_terms}\n"
            f"Response: {response!r}\n"
            f"Matched terms: {result.matched_terms}\n"
        )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 8: Socratic activation for conceptual
# questions at FAMILIAR+
# ---------------------------------------------------------------------------


class TestSocraticActivationAtFamiliarPlus:
    """For any message classified as `conceptual_question` and any
    mastery_level in {FAMILIAR, PROFICIENT, ADVANCED, MASTERED}, the
    SocraticModule SHALL activate and produce a guiding question rather
    than a direct answer, and the SocraticState SHALL contain a non-null
    target_concept with 1–3 key_terms.

    **Validates: Requirements 3.1, 3.2**
    """

    @settings(max_examples=30)
    @given(
        mastery_level=sampled_from(_FAMILIAR_PLUS_LEVELS),
        exchanges=lists(_exchange_strategy(), min_size=0, max_size=10),
        topic_threads=lists(_topic_thread_strategy(), min_size=0, max_size=4),
        discourse_state=sampled_from(DiscourseState),
        reasoning_type=sampled_from(REASONING_TYPES),
    )
    def test_should_activate_returns_true_for_familiar_plus(
        self,
        mastery_level: MasteryLevel,
        exchanges: list[Exchange],
        topic_threads: list[TopicThread],
        discourse_state: DiscourseState,
        reasoning_type: str,
    ) -> None:
        """Socratic module activates for conceptual_question intent when
        mastery is FAMILIAR or above and attempts are below the max."""
        # Build a context where Socratic state is NOT at max attempts.
        ctx = ConversationContext(
            exchanges=exchanges,
            topic_threads=topic_threads,
            discourse_state=discourse_state,
            socratic_state=SocraticState(
                active=False,
                target_concept=None,
                key_terms=[],
                attempts=0,
                reasoning_type=None,
            ),
        )

        module = SocraticModule()

        result = module.should_activate(
            intent="conceptual_question",
            mastery_level=mastery_level,
            ctx=ctx,
        )

        assert result is True, (
            f"SocraticModule.should_activate() returned False for "
            f"mastery_level={mastery_level.value} with intent=conceptual_question.\n"
            f"Context discourse_state: {ctx.discourse_state}\n"
            f"Socratic state: active={ctx.socratic_state.active}, "
            f"attempts={ctx.socratic_state.attempts}\n"
        )

    @settings(max_examples=30)
    @given(
        mastery_level=sampled_from(_FAMILIAR_PLUS_LEVELS),
        concept=text(min_size=3, max_size=30),
        section_content=text(min_size=10, max_size=200),
        reasoning_type=sampled_from(REASONING_TYPES),
    )
    def test_guiding_question_has_valid_socratic_state(
        self,
        mastery_level: MasteryLevel,
        concept: str,
        section_content: str,
        reasoning_type: str,
    ) -> None:
        """When Socratic mode activates, generate_guiding_question produces
        a SocraticPrompt with non-null target_concept and 1-3 key_terms."""
        module = SocraticModule()

        prompt = module.generate_guiding_question(
            concept=concept,
            section_content=section_content,
            reasoning_type=reasoning_type,
        )

        # target_concept must be non-null and match the input concept.
        assert prompt.target_concept is not None, (
            "SocraticPrompt.target_concept is None after generation."
        )
        assert prompt.target_concept == concept, (
            f"SocraticPrompt.target_concept '{prompt.target_concept}' "
            f"does not match input concept '{concept}'."
        )

        # key_terms must contain 1-3 entries.
        assert 1 <= len(prompt.key_terms) <= 3, (
            f"SocraticPrompt.key_terms has {len(prompt.key_terms)} entries, "
            f"expected 1-3. key_terms={prompt.key_terms}"
        )

        # The question should be a non-empty string.
        assert len(prompt.question) > 0, (
            "SocraticPrompt.question is empty."
        )

        # The reasoning_type should be set.
        assert prompt.reasoning_type == reasoning_type, (
            f"SocraticPrompt.reasoning_type '{prompt.reasoning_type}' "
            f"does not match input '{reasoning_type}'."
        )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 10: Socratic inactive for BEGINNER mastery
# ---------------------------------------------------------------------------


class TestSocraticInactiveForBeginnerMastery:
    """For any message classified as `conceptual_question` and
    mastery_level = BEGINNER, the SocraticModule SHALL NOT activate and
    the Chat_Engine SHALL produce a direct explanation.

    **Validates: Requirements 3.7**
    """

    @settings(max_examples=30)
    @given(ctx=_conversation_context_strategy())
    def test_should_activate_returns_false_for_beginner(
        self, ctx: ConversationContext
    ) -> None:
        """Socratic module never activates for BEGINNER mastery regardless
        of conversation context state."""
        module = SocraticModule()

        result = module.should_activate(
            intent="conceptual_question",
            mastery_level=MasteryLevel.BEGINNER,
            ctx=ctx,
        )

        assert result is False, (
            f"SocraticModule.should_activate() returned True for BEGINNER mastery.\n"
            f"Context discourse_state: {ctx.discourse_state}\n"
            f"Socratic state: active={ctx.socratic_state.active}, "
            f"attempts={ctx.socratic_state.attempts}\n"
            f"Exchanges count: {len(ctx.exchanges)}\n"
        )
