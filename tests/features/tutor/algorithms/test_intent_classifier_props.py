"""Property-based tests for the Intent Classifier.

Uses Hypothesis to validate universal correctness properties of the
IntentClassifier module.
"""

from __future__ import annotations

from hypothesis import given, settings, assume
from hypothesis.strategies import text, sampled_from, lists, composite

from app.features.tutor.algorithms.chat_models import (
    ClassificationResult,
    ConversationContext,
    DiscourseState,
    IntentScore,
    ResolvedMessage,
    TopicThread,
)
from app.features.tutor.algorithms.intent_classifier import IntentClassifier


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 4: Short message classified as quiz answer in quiz-pending state
# ---------------------------------------------------------------------------


class TestShortMessageQuizAnswerInQuizPendingState:
    """For any message of 30 characters or fewer, when the DiscourseState is
    `quiz_pending`, the IntentClassifier SHALL classify the message as
    `quiz_answer_attempt` regardless of message content.

    **Validates: Requirements 2.2**
    """

    @settings(max_examples=30)
    @given(message=text(min_size=1, max_size=30))
    def test_short_message_classified_as_quiz_answer(self, message: str) -> None:
        """Any message ≤ 30 chars in quiz_pending state is classified as
        quiz_answer_attempt with full confidence."""
        # Build a context with quiz_pending discourse state
        ctx = ConversationContext(
            discourse_state=DiscourseState.QUIZ_PENDING,
            topic_threads=[
                TopicThread(
                    subject="quiz topic",
                    start_exchange_index=0,
                    key_terms=["quiz", "topic"],
                    is_active=True,
                )
            ],
        )

        # Build a resolved message (no anaphora resolution needed)
        resolved = ResolvedMessage(
            original=message,
            resolved=message,
            confidence=1.0,
            candidates=[],
            referent=None,
        )

        classifier = IntentClassifier()
        result: ClassificationResult = classifier.classify(
            message=message,
            resolved_message=resolved,
            ctx=ctx,
        )

        assert result.intent == "quiz_answer_attempt", (
            f"Expected 'quiz_answer_attempt' but got '{result.intent}'.\n"
            f"Message: {message!r} (len={len(message)})\n"
            f"Discourse state: {ctx.discourse_state}\n"
        )
        assert result.confidence == 1.0, (
            f"Expected confidence 1.0 but got {result.confidence}.\n"
            f"Message: {message!r}\n"
        )
        assert result.needs_disambiguation is False


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 6: Thread-continuing intent wins ties
# ---------------------------------------------------------------------------

# Intents that continue an active thread (from IntentClassifier._continues_thread)
_CONTINUING_INTENTS = [
    "explain_section",
    "give_example",
    "summarize",
    "conceptual_question",
    "complexity_adjustment",
    "cross_reference_request",
    "direct_answer_request",
]

# Intents that do NOT continue a thread
_NON_CONTINUING_INTENTS = [
    "greeting",
    "next_step",
    "quiz_me",
    "relate_to_exam",
    "memory_aid",
    "thanks",
    "quiz_answer_attempt",
]


@composite
def tied_intent_pair(draw):
    """Generate a pair of (continuing_intent, non_continuing_intent) with equal scores."""
    continuing = draw(sampled_from(_CONTINUING_INTENTS))
    non_continuing = draw(sampled_from(_NON_CONTINUING_INTENTS))
    return continuing, non_continuing


class TestThreadContinuingIntentWinsTies:
    """For any message that produces two or more intents with equal scores,
    the IntentClassifier SHALL select the intent that continues the current
    active TopicThread over one that would start a new thread.

    The IntentClassifier gives a +0.1 thread continuity bonus to intents
    that align with the active thread, and uses _break_tie to prefer
    thread-continuing intents when final scores are equal.

    **Validates: Requirements 2.4**
    """

    @settings(max_examples=30)
    @given(pair=tied_intent_pair())
    def test_thread_continuing_intent_wins_tie(
        self, pair: tuple[str, str]
    ) -> None:
        """When two intents have equal scores, the thread-continuing intent
        wins over the non-thread-continuing intent."""
        continuing_intent, non_continuing_intent = pair

        # Build a context with an active topic thread
        ctx = ConversationContext(
            discourse_state=DiscourseState.FOLLOW_UP,
            topic_threads=[
                TopicThread(
                    subject="grammar concepts",
                    start_exchange_index=0,
                    key_terms=["grammar", "concepts", "rules"],
                    is_active=True,
                )
            ],
        )

        classifier = IntentClassifier()

        # Directly test the tie-breaking logic by constructing equal-scored
        # IntentScore objects where one continues the thread and one does not.
        tied_score = 0.7
        tied_scores = [
            IntentScore(
                intent=non_continuing_intent,
                score=tied_score,
                source="pattern",
            ),
            IntentScore(
                intent=continuing_intent,
                score=tied_score,
                source="pattern",
            ),
        ]

        # _break_tie should select the continuing intent regardless of order
        winner = classifier._break_tie(tied_scores, ctx)

        assert winner.intent == continuing_intent, (
            f"Expected thread-continuing intent '{continuing_intent}' to win tie "
            f"but got '{winner.intent}'.\n"
            f"Tied intents: {[s.intent for s in tied_scores]}\n"
            f"Active thread: {ctx.topic_threads[0].subject}\n"
        )

    @settings(max_examples=30)
    @given(pair=tied_intent_pair())
    def test_thread_continuing_wins_regardless_of_position(
        self, pair: tuple[str, str]
    ) -> None:
        """The thread-continuing intent wins even when it appears first in
        the tied list (verifying the logic doesn't just pick the last one)."""
        continuing_intent, non_continuing_intent = pair

        ctx = ConversationContext(
            discourse_state=DiscourseState.FOLLOW_UP,
            topic_threads=[
                TopicThread(
                    subject="math operations",
                    start_exchange_index=0,
                    key_terms=["math", "operations", "addition"],
                    is_active=True,
                )
            ],
        )

        classifier = IntentClassifier()
        tied_score = 0.5

        # Place continuing intent FIRST in the list
        tied_scores_first = [
            IntentScore(
                intent=continuing_intent,
                score=tied_score,
                source="pattern",
            ),
            IntentScore(
                intent=non_continuing_intent,
                score=tied_score,
                source="pattern",
            ),
        ]

        winner_first = classifier._break_tie(tied_scores_first, ctx)
        assert winner_first.intent == continuing_intent, (
            f"Expected '{continuing_intent}' when placed first, "
            f"got '{winner_first.intent}'"
        )

        # Place continuing intent LAST in the list
        tied_scores_last = [
            IntentScore(
                intent=non_continuing_intent,
                score=tied_score,
                source="pattern",
            ),
            IntentScore(
                intent=continuing_intent,
                score=tied_score,
                source="pattern",
            ),
        ]

        winner_last = classifier._break_tie(tied_scores_last, ctx)
        assert winner_last.intent == continuing_intent, (
            f"Expected '{continuing_intent}' when placed last, "
            f"got '{winner_last.intent}'"
        )

    @settings(max_examples=30)
    @given(
        continuing_intents=lists(
            sampled_from(_CONTINUING_INTENTS), min_size=1, max_size=3, unique=True
        ),
        non_continuing_intent=sampled_from(_NON_CONTINUING_INTENTS),
    )
    def test_any_continuing_intent_preferred_over_non_continuing(
        self,
        continuing_intents: list[str],
        non_continuing_intent: str,
    ) -> None:
        """When multiple intents tie and at least one continues the thread,
        the result is always a thread-continuing intent (never a non-continuing one)."""
        ctx = ConversationContext(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[
                TopicThread(
                    subject="vocabulary",
                    start_exchange_index=0,
                    key_terms=["vocabulary", "words", "meaning"],
                    is_active=True,
                )
            ],
        )

        classifier = IntentClassifier()
        tied_score = 0.6

        # Build tied list: non-continuing first, then continuing ones
        tied_scores = [
            IntentScore(
                intent=non_continuing_intent,
                score=tied_score,
                source="pattern",
            ),
        ] + [
            IntentScore(intent=ci, score=tied_score, source="pattern")
            for ci in continuing_intents
        ]

        winner = classifier._break_tie(tied_scores, ctx)

        assert winner.intent in continuing_intents, (
            f"Expected one of {continuing_intents} to win tie "
            f"but got '{winner.intent}'.\n"
            f"Non-continuing intent '{non_continuing_intent}' should never win "
            f"when a thread-continuing alternative exists."
        )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 7: Low-confidence triggers disambiguation
# ---------------------------------------------------------------------------


class TestLowConfidenceTriggersDisambiguation:
    """For any message where all intent candidate scores are below 0.4:
    - If ≥ 2 candidate intents exist, the classifier returns
      needs_disambiguation=True with the top 2 options.
    - If < 2 candidates exist, the classifier returns needs_disambiguation=True
      with disambiguation_options=None (clarifying prompt).

    **Validates: Requirements 2.5**
    """

    @settings(max_examples=100)
    @given(
        scores=lists(
            sampled_from([
                "explain_section",
                "give_example",
                "summarize",
                "quiz_me",
                "relate_to_exam",
                "memory_aid",
                "next_step",
                "greeting",
                "thanks",
                "conceptual_question",
                "direct_answer_request",
                "quiz_answer_attempt",
                "complexity_adjustment",
                "cross_reference_request",
            ]),
            min_size=2,
            max_size=6,
            unique=True,
        ),
    )
    def test_low_confidence_with_two_or_more_candidates_triggers_disambiguation(
        self, scores: list[str]
    ) -> None:
        """When all intent scores are below 0.4 and ≥ 2 candidates exist,
        the classifier SHALL return needs_disambiguation=True with the top 2
        candidate intents as options."""
        from app.features.tutor.algorithms.intent_classifier import (
            CONFIDENCE_THRESHOLD,
        )
        from hypothesis import assume
        import random

        # Generate random low scores (0 < score < 0.4) for each candidate intent
        random.seed(hash(tuple(scores)) & 0xFFFFFFFF)
        low_scores = [
            round(random.uniform(0.01, CONFIDENCE_THRESHOLD - 0.01), 3)
            for _ in scores
        ]

        # Sort to identify expected top 2
        scored_pairs = sorted(
            zip(scores, low_scores), key=lambda x: x[1], reverse=True
        )
        expected_top_two = [pair[0] for pair in scored_pairs[:2]]

        # Subclass IntentClassifier to inject controlled low scores
        # This tests the disambiguation logic branch in isolation.
        class _LowScoreClassifier(IntentClassifier):
            def _compute_scores(self, message, resolved_message, ctx):
                return [
                    IntentScore(intent=intent, score=score, source="pattern")
                    for intent, score in zip(scores, low_scores)
                ]

        ctx = ConversationContext(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[],
        )
        resolved = ResolvedMessage(
            original="test message",
            resolved="test message",
            confidence=1.0,
            candidates=[],
            referent=None,
        )

        classifier = _LowScoreClassifier()
        result: ClassificationResult = classifier.classify(
            message="test message",
            resolved_message=resolved,
            ctx=ctx,
        )

        assert result.needs_disambiguation is True, (
            f"Expected needs_disambiguation=True but got False.\n"
            f"Scores: {list(zip(scores, low_scores))}\n"
            f"Result intent: {result.intent}, confidence: {result.confidence}\n"
        )
        assert result.disambiguation_options is not None, (
            f"Expected disambiguation_options to be a list but got None.\n"
            f"Scores: {list(zip(scores, low_scores))}\n"
        )
        assert len(result.disambiguation_options) == 2, (
            f"Expected exactly 2 disambiguation options but got "
            f"{len(result.disambiguation_options)}.\n"
            f"Options: {result.disambiguation_options}\n"
        )
        assert result.disambiguation_options == expected_top_two, (
            f"Expected top 2 options {expected_top_two} but got "
            f"{result.disambiguation_options}.\n"
            f"All scores: {list(zip(scores, low_scores))}\n"
        )
        assert result.intent == "fallback", (
            f"Expected intent 'fallback' for disambiguation but got "
            f"'{result.intent}'.\n"
        )

    @settings(max_examples=100)
    @given(
        intent=sampled_from([
            "explain_section",
            "give_example",
            "summarize",
            "quiz_me",
            "relate_to_exam",
            "memory_aid",
            "next_step",
            "greeting",
            "thanks",
            "conceptual_question",
            "direct_answer_request",
            "quiz_answer_attempt",
            "complexity_adjustment",
            "cross_reference_request",
        ]),
    )
    def test_low_confidence_with_fewer_than_two_candidates_returns_clarifying_prompt(
        self, intent: str
    ) -> None:
        """When all intent scores are below 0.4 and fewer than 2 candidates
        exist, the classifier SHALL return needs_disambiguation=True with
        disambiguation_options=None (open-ended clarifying prompt)."""
        from app.features.tutor.algorithms.intent_classifier import (
            CONFIDENCE_THRESHOLD,
        )
        import random

        # Single candidate with a low score
        low_score = round(random.uniform(0.01, CONFIDENCE_THRESHOLD - 0.01), 3)

        class _SingleLowScoreClassifier(IntentClassifier):
            def _compute_scores(self, message, resolved_message, ctx):
                return [
                    IntentScore(intent=intent, score=low_score, source="pattern")
                ]

        ctx = ConversationContext(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[],
        )
        resolved = ResolvedMessage(
            original="test message",
            resolved="test message",
            confidence=1.0,
            candidates=[],
            referent=None,
        )

        classifier = _SingleLowScoreClassifier()
        result: ClassificationResult = classifier.classify(
            message="test message",
            resolved_message=resolved,
            ctx=ctx,
        )

        assert result.needs_disambiguation is True, (
            f"Expected needs_disambiguation=True but got False.\n"
            f"Single candidate: ({intent}, {low_score})\n"
            f"Result intent: {result.intent}, confidence: {result.confidence}\n"
        )
        assert result.disambiguation_options is None, (
            f"Expected disambiguation_options=None (clarifying prompt) but got "
            f"{result.disambiguation_options}.\n"
            f"Single candidate: ({intent}, {low_score})\n"
        )
        assert result.intent == "fallback", (
            f"Expected intent 'fallback' for clarifying prompt but got "
            f"'{result.intent}'.\n"
        )

    @settings(max_examples=100)
    @given(message=text(min_size=1, max_size=50))
    def test_no_candidates_returns_clarifying_prompt(self, message: str) -> None:
        """When a message matches no intent patterns at all (zero candidates),
        the classifier SHALL return needs_disambiguation=True with
        disambiguation_options=None."""

        # Use INITIAL state with no topic threads to avoid special-case paths
        # (no quiz_pending, no follow_up patterns)
        ctx = ConversationContext(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[],
        )
        resolved = ResolvedMessage(
            original=message,
            resolved=message,
            confidence=1.0,
            candidates=[],
            referent=None,
        )

        classifier = IntentClassifier()
        result: ClassificationResult = classifier.classify(
            message=message,
            resolved_message=resolved,
            ctx=ctx,
        )

        # Only assert if no patterns matched (precondition)
        if not result.all_scores:
            assert result.needs_disambiguation is True, (
                f"Expected needs_disambiguation=True for zero candidates.\n"
                f"Message: {message!r}\n"
            )
            assert result.disambiguation_options is None, (
                f"Expected disambiguation_options=None for zero candidates.\n"
                f"Message: {message!r}\n"
            )
            assert result.intent == "fallback", (
                f"Expected intent 'fallback' for zero candidates.\n"
                f"Message: {message!r}\n"
            )


# ---------------------------------------------------------------------------
# Feature: smart-chat-engine, Property 5: Discourse state disambiguates intent for identical messages
# ---------------------------------------------------------------------------

# Each scenario is a tuple of:
#   (message, state_a, expected_intent_a, state_b, expected_intent_b)
#
# These messages match patterns for BOTH intents (verified against the regex
# patterns in intent_classifier.py). The discourse bonus (+0.3) shifts
# the winning intent when one state aligns with intent A but NOT intent B,
# and vice versa.
#
# Discourse expected intents (from intent_classifier.py):
#   INITIAL:            greeting, explain_section, conceptual_question
#   FOLLOW_UP:          explain_section, conceptual_question, give_example,
#                       complexity_adjustment, cross_reference_request
#   QUIZ_PENDING:       quiz_answer_attempt
#   SOCRATIC_EXCHANGE:  direct_answer_request, quiz_answer_attempt, conceptual_question
#   CLARIFICATION:      explain_section, conceptual_question, direct_answer_request

_DISAMBIGUATION_SCENARIOS: list[
    tuple[str, DiscourseState, str, DiscourseState, str]
] = [
    # "just tell me in simple terms" matches:
    #   - direct_answer_request via "just tell me" (base 0.4)
    #   - complexity_adjustment via "in simple terms" (base 0.4)
    # SOCRATIC_EXCHANGE aligns with direct_answer_request (+0.3) but NOT complexity_adjustment
    # FOLLOW_UP aligns with complexity_adjustment (+0.3) but NOT direct_answer_request
    # With active thread: both get +0.1 thread bonus (both are continuing intents)
    # State A scores: direct=0.4+0.3+0.1=0.8, complexity=0.4+0+0.1=0.5 → direct wins
    # State B scores: direct=0.4+0+0.1=0.5, complexity=0.4+0.3+0.1=0.8 → complexity wins
    (
        "just tell me in simple terms",
        DiscourseState.SOCRATIC_EXCHANGE,
        "direct_answer_request",
        DiscourseState.FOLLOW_UP,
        "complexity_adjustment",
    ),
    # "i want the answer, help me understand why" matches:
    #   - direct_answer_request via "i want the answer" (base 0.4)
    #   - explain_section via "help me understand" (base 0.4)
    # SOCRATIC_EXCHANGE aligns with direct_answer_request (+0.3) but NOT explain_section
    # INITIAL aligns with explain_section (+0.3) but NOT direct_answer_request
    # With active thread: both get +0.1 (both are continuing intents)
    # State A: direct=0.8, explain=0.5 → direct wins
    # State B: direct=0.5, explain=0.8 → explain wins
    (
        "i want the answer, help me understand",
        DiscourseState.SOCRATIC_EXCHANGE,
        "direct_answer_request",
        DiscourseState.INITIAL,
        "explain_section",
    ),
    # "just give me more detail" matches:
    #   - direct_answer_request via "just give me" (base 0.4)
    #   - complexity_adjustment via "give me more detail" (base 0.4)
    # SOCRATIC_EXCHANGE aligns with direct_answer_request (+0.3) but NOT complexity_adjustment
    # FOLLOW_UP aligns with complexity_adjustment (+0.3) but NOT direct_answer_request
    (
        "just give me more detail",
        DiscourseState.SOCRATIC_EXCHANGE,
        "direct_answer_request",
        DiscourseState.FOLLOW_UP,
        "complexity_adjustment",
    ),
]


class TestDiscourseStateDisambiguatesIntent:
    """For any message that matches multiple intent patterns, the
    IntentClassifier SHALL produce different final intents when the
    DiscourseState differs, specifically: the discourse-aligned intent
    SHALL receive a scoring bonus that changes the winner.

    **Validates: Requirements 2.1**
    """

    @settings(max_examples=100)
    @given(
        scenario=sampled_from(_DISAMBIGUATION_SCENARIOS),
    )
    def test_discourse_state_changes_winning_intent(
        self,
        scenario: tuple[str, DiscourseState, str, DiscourseState, str],
    ) -> None:
        """The same message produces different intents under different
        discourse states because the discourse bonus shifts the winner."""
        message, state_a, expected_a, state_b, expected_b = scenario

        # Precondition: the two expected intents must differ
        assume(expected_a != expected_b)

        classifier = IntentClassifier()

        # Shared context structure — only discourse_state changes
        base_thread = TopicThread(
            subject="active topic",
            start_exchange_index=0,
            key_terms=["active", "topic", "concept"],
            is_active=True,
        )

        resolved = ResolvedMessage(
            original=message,
            resolved=message,
            confidence=1.0,
            candidates=[],
            referent=None,
        )

        # --- State A ---
        ctx_a = ConversationContext(
            discourse_state=state_a,
            topic_threads=[base_thread],
        )
        result_a: ClassificationResult = classifier.classify(
            message=message,
            resolved_message=resolved,
            ctx=ctx_a,
        )

        # --- State B ---
        ctx_b = ConversationContext(
            discourse_state=state_b,
            topic_threads=[base_thread],
        )
        result_b: ClassificationResult = classifier.classify(
            message=message,
            resolved_message=resolved,
            ctx=ctx_b,
        )

        # The core property: same message, different discourse states →
        # different intents (discourse bonus changed the winner)
        assert result_a.intent != result_b.intent, (
            f"Expected different intents for different discourse states but both "
            f"returned '{result_a.intent}'.\n"
            f"Message: {message!r}\n"
            f"State A ({state_a.value}): intent={result_a.intent}, "
            f"confidence={result_a.confidence}\n"
            f"State B ({state_b.value}): intent={result_b.intent}, "
            f"confidence={result_b.confidence}\n"
            f"All scores A: {[(s.intent, s.score) for s in result_a.all_scores]}\n"
            f"All scores B: {[(s.intent, s.score) for s in result_b.all_scores]}\n"
        )

        # Verify the expected intents are the winners
        assert result_a.intent == expected_a, (
            f"In state {state_a.value}, expected '{expected_a}' but got "
            f"'{result_a.intent}'.\n"
            f"Message: {message!r}\n"
            f"All scores: {[(s.intent, s.score) for s in result_a.all_scores]}\n"
        )
        assert result_b.intent == expected_b, (
            f"In state {state_b.value}, expected '{expected_b}' but got "
            f"'{result_b.intent}'.\n"
            f"Message: {message!r}\n"
            f"All scores: {[(s.intent, s.score) for s in result_b.all_scores]}\n"
        )
