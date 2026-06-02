"""Unit tests for the Intent Classifier.

Tests scoring logic, discourse-aware classification, special-case handling
(quiz_pending, post-explanation follow-ups), tie-breaking behavior,
low-confidence disambiguation, and all new intent pattern coverage.

Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6
"""

from __future__ import annotations

import pytest

from app.features.tutor.algorithms.chat_models import (
    ClassificationResult,
    ConversationContext,
    DiscourseState,
    IntentScore,
    ResolvedMessage,
    TopicThread,
)
from app.features.tutor.algorithms.intent_classifier import (
    CONFIDENCE_THRESHOLD,
    IntentClassifier,
    _COMPILED_INTENTS,
    _DISCOURSE_BONUS,
    _THREAD_CONTINUITY_BONUS,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_resolved(message: str) -> ResolvedMessage:
    """Build a ResolvedMessage with no anaphora resolution."""
    return ResolvedMessage(
        original=message,
        resolved=message,
        confidence=1.0,
        candidates=[],
        referent=None,
    )


def _make_ctx(
    discourse_state: DiscourseState = DiscourseState.INITIAL,
    topic_threads: list[TopicThread] | None = None,
) -> ConversationContext:
    """Build a ConversationContext with sensible defaults."""
    return ConversationContext(
        discourse_state=discourse_state,
        topic_threads=topic_threads or [],
    )


def _active_thread(subject: str = "active topic") -> TopicThread:
    """Build an active TopicThread."""
    return TopicThread(
        subject=subject,
        start_exchange_index=0,
        key_terms=[subject.split()[0], "concept"],
        is_active=True,
    )


# ---------------------------------------------------------------------------
# Tests: quiz_pending + short message → quiz_answer_attempt (Req 2.2)
# ---------------------------------------------------------------------------


class TestQuizPendingShortMessage:
    """WHEN the previous assistant response was a quiz question and the
    user sends a message of 30 characters or fewer, THE Intent_Classifier
    SHALL classify it as a quiz answer attempt."""

    def test_single_letter_answer(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.QUIZ_PENDING)
        classifier = IntentClassifier()
        result = classifier.classify("B", _make_resolved("B"), ctx)

        assert result.intent == "quiz_answer_attempt"
        assert result.confidence == 1.0
        assert result.needs_disambiguation is False

    def test_short_phrase_answer(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.QUIZ_PENDING)
        classifier = IntentClassifier()
        result = classifier.classify("the answer is 42", _make_resolved("the answer is 42"), ctx)

        assert result.intent == "quiz_answer_attempt"
        assert result.confidence == 1.0

    def test_exactly_30_chars(self) -> None:
        msg = "a" * 30
        ctx = _make_ctx(discourse_state=DiscourseState.QUIZ_PENDING)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        assert result.intent == "quiz_answer_attempt"
        assert result.confidence == 1.0

    def test_31_chars_does_not_trigger_special_case(self) -> None:
        msg = "a" * 31
        ctx = _make_ctx(discourse_state=DiscourseState.QUIZ_PENDING)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        # Should NOT get the automatic quiz_answer_attempt classification
        # (it goes through normal scoring instead)
        assert result.confidence != 1.0 or result.intent != "quiz_answer_attempt"

    def test_message_with_explain_keyword_still_classified_as_quiz_answer(self) -> None:
        """Even if the message matches other intent patterns, quiz_pending
        state + short message overrides everything."""
        msg = "explain it"
        ctx = _make_ctx(discourse_state=DiscourseState.QUIZ_PENDING)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        assert result.intent == "quiz_answer_attempt"
        assert result.confidence == 1.0

    def test_non_quiz_state_short_message_not_auto_classified(self) -> None:
        """Short message without quiz_pending goes through normal scoring."""
        msg = "hello"
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        # Should be classified normally (likely greeting or fallback)
        assert result.intent != "quiz_answer_attempt" or result.confidence != 1.0


# ---------------------------------------------------------------------------
# Tests: post-explanation follow-up → deeper explanation (Req 2.3)
# ---------------------------------------------------------------------------


class TestPostExplanationFollowUp:
    """WHEN the previous assistant response was an explanation and the user
    sends a single-sentence follow-up inquiry, THE Intent_Classifier SHALL
    classify it as a request for deeper explanation."""

    def test_why_question_mark(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify("why?", _make_resolved("why?"), ctx)

        assert result.intent == "explain_section"
        assert result.confidence == 0.9

    def test_how_come(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify("how come?", _make_resolved("how come?"), ctx)

        assert result.intent == "explain_section"
        assert result.confidence == 0.9

    def test_why_is_that(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify("why is that?", _make_resolved("why is that?"), ctx)

        assert result.intent == "explain_section"
        assert result.confidence == 0.9

    def test_what_do_you_mean(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify("what do you mean?", _make_resolved("what do you mean?"), ctx)

        assert result.intent == "explain_section"
        assert result.confidence == 0.9

    def test_can_you_explain_more(self) -> None:
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(
            "can you explain more?", _make_resolved("can you explain more?"), ctx
        )

        assert result.intent == "explain_section"
        assert result.confidence == 0.9

    def test_follow_up_not_triggered_in_initial_state(self) -> None:
        """Follow-up patterns only trigger in FOLLOW_UP discourse state."""
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify("why?", _make_resolved("why?"), ctx)

        # Should go through normal scoring, not the follow-up shortcut
        assert result.confidence != 0.9 or result.intent != "explain_section"


# ---------------------------------------------------------------------------
# Tests: discourse bonus changes winner (Req 2.1)
# ---------------------------------------------------------------------------


class TestDiscourseBonusChangesWinner:
    """WHEN classifying intent, THE Intent_Classifier SHALL weight the
    DiscourseState such that the same message may yield different intents
    depending on the current DiscourseState."""

    def test_direct_answer_vs_complexity_adjustment(self) -> None:
        """'just tell me in simple terms' matches both direct_answer_request
        and complexity_adjustment. Discourse state determines winner."""
        msg = "just tell me in simple terms"
        classifier = IntentClassifier()

        # SOCRATIC_EXCHANGE favors direct_answer_request
        ctx_socratic = _make_ctx(
            discourse_state=DiscourseState.SOCRATIC_EXCHANGE,
            topic_threads=[_active_thread()],
        )
        result_socratic = classifier.classify(msg, _make_resolved(msg), ctx_socratic)

        # FOLLOW_UP favors complexity_adjustment
        ctx_follow = _make_ctx(
            discourse_state=DiscourseState.FOLLOW_UP,
            topic_threads=[_active_thread()],
        )
        result_follow = classifier.classify(msg, _make_resolved(msg), ctx_follow)

        assert result_socratic.intent == "direct_answer_request"
        assert result_follow.intent == "complexity_adjustment"

    def test_direct_answer_vs_explain(self) -> None:
        """'i want the answer, help me understand' matches both
        direct_answer_request and explain_section."""
        msg = "i want the answer, help me understand"
        classifier = IntentClassifier()

        ctx_socratic = _make_ctx(
            discourse_state=DiscourseState.SOCRATIC_EXCHANGE,
            topic_threads=[_active_thread()],
        )
        result_socratic = classifier.classify(msg, _make_resolved(msg), ctx_socratic)

        ctx_initial = _make_ctx(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[_active_thread()],
        )
        result_initial = classifier.classify(msg, _make_resolved(msg), ctx_initial)

        assert result_socratic.intent == "direct_answer_request"
        assert result_initial.intent == "explain_section"

    def test_same_message_different_states_different_intents(self) -> None:
        """'just give me more detail' matches direct_answer_request
        and complexity_adjustment."""
        msg = "just give me more detail"
        classifier = IntentClassifier()

        ctx_socratic = _make_ctx(
            discourse_state=DiscourseState.SOCRATIC_EXCHANGE,
            topic_threads=[_active_thread()],
        )
        result_a = classifier.classify(msg, _make_resolved(msg), ctx_socratic)

        ctx_follow = _make_ctx(
            discourse_state=DiscourseState.FOLLOW_UP,
            topic_threads=[_active_thread()],
        )
        result_b = classifier.classify(msg, _make_resolved(msg), ctx_follow)

        assert result_a.intent != result_b.intent


# ---------------------------------------------------------------------------
# Tests: tie-breaking favors thread-continuing intent (Req 2.4)
# ---------------------------------------------------------------------------


class TestTieBreakingFavorsThreadContinuing:
    """WHEN the user sends a message that matches multiple intents with
    equal confidence, THE Intent_Classifier SHALL select the intent that
    continues the current TopicThread."""

    def test_continuing_intent_beats_non_continuing(self) -> None:
        ctx = _make_ctx(
            discourse_state=DiscourseState.FOLLOW_UP,
            topic_threads=[_active_thread()],
        )
        classifier = IntentClassifier()

        # Construct tied scores with one continuing and one non-continuing
        tied = [
            IntentScore(intent="greeting", score=0.7, source="pattern"),
            IntentScore(intent="explain_section", score=0.7, source="pattern"),
        ]
        winner = classifier._break_tie(tied, ctx)
        assert winner.intent == "explain_section"

    def test_non_continuing_wins_only_when_no_continuing_present(self) -> None:
        ctx = _make_ctx(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[_active_thread()],
        )
        classifier = IntentClassifier()

        # Both are non-continuing
        tied = [
            IntentScore(intent="greeting", score=0.7, source="pattern"),
            IntentScore(intent="next_step", score=0.7, source="pattern"),
        ]
        winner = classifier._break_tie(tied, ctx)
        # Should return first since neither continues the thread
        assert winner.intent == "greeting"

    def test_tie_with_no_active_thread(self) -> None:
        """Without an active thread, _continues_thread returns False for all."""
        ctx = _make_ctx(
            discourse_state=DiscourseState.INITIAL,
            topic_threads=[],
        )
        classifier = IntentClassifier()

        tied = [
            IntentScore(intent="explain_section", score=0.5, source="pattern"),
            IntentScore(intent="give_example", score=0.5, source="pattern"),
        ]
        winner = classifier._break_tie(tied, ctx)
        # Returns first since neither has a thread advantage
        assert winner.intent == "explain_section"

    def test_order_does_not_matter(self) -> None:
        """Thread-continuing intent wins regardless of list position."""
        ctx = _make_ctx(
            discourse_state=DiscourseState.FOLLOW_UP,
            topic_threads=[_active_thread()],
        )
        classifier = IntentClassifier()

        # Non-continuing first
        tied_a = [
            IntentScore(intent="quiz_me", score=0.6, source="pattern"),
            IntentScore(intent="summarize", score=0.6, source="pattern"),
        ]
        assert classifier._break_tie(tied_a, ctx).intent == "summarize"

        # Non-continuing last
        tied_b = [
            IntentScore(intent="summarize", score=0.6, source="pattern"),
            IntentScore(intent="quiz_me", score=0.6, source="pattern"),
        ]
        assert classifier._break_tie(tied_b, ctx).intent == "summarize"


# ---------------------------------------------------------------------------
# Tests: low confidence returns disambiguation (Req 2.5, 2.6)
# ---------------------------------------------------------------------------


class TestLowConfidenceDisambiguation:
    """IF the Intent_Classifier confidence is below 0.4 for all candidate
    intents, THEN THE Chat_Engine SHALL ask a disambiguation question (≥ 2
    candidates) or open-ended clarifying question (< 2 candidates)."""

    def test_two_or_more_low_candidates_returns_top_two(self) -> None:
        """≥ 2 candidates below threshold → disambiguation with top 2."""

        class _LowScoreClassifier(IntentClassifier):
            def _compute_scores(self, message, resolved_message, ctx):
                return [
                    IntentScore(intent="explain_section", score=0.3, source="pattern"),
                    IntentScore(intent="give_example", score=0.2, source="pattern"),
                    IntentScore(intent="summarize", score=0.1, source="pattern"),
                ]

        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = _LowScoreClassifier()
        result = classifier.classify("something", _make_resolved("something"), ctx)

        assert result.needs_disambiguation is True
        assert result.disambiguation_options == ["explain_section", "give_example"]
        assert result.intent == "fallback"

    def test_single_low_candidate_returns_clarifying_prompt(self) -> None:
        """< 2 candidates below threshold → open-ended clarifying prompt."""

        class _SingleLowClassifier(IntentClassifier):
            def _compute_scores(self, message, resolved_message, ctx):
                return [
                    IntentScore(intent="summarize", score=0.2, source="pattern"),
                ]

        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = _SingleLowClassifier()
        result = classifier.classify("something", _make_resolved("something"), ctx)

        assert result.needs_disambiguation is True
        assert result.disambiguation_options is None
        assert result.intent == "fallback"

    def test_no_candidates_returns_clarifying_prompt(self) -> None:
        """Zero candidates → disambiguation=True, options=None."""

        class _NoScoreClassifier(IntentClassifier):
            def _compute_scores(self, message, resolved_message, ctx):
                return []

        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = _NoScoreClassifier()
        result = classifier.classify("something", _make_resolved("something"), ctx)

        assert result.needs_disambiguation is True
        assert result.disambiguation_options is None
        assert result.intent == "fallback"

    def test_above_threshold_does_not_trigger_disambiguation(self) -> None:
        """When top score ≥ 0.4, no disambiguation needed."""

        class _HighScoreClassifier(IntentClassifier):
            def _compute_scores(self, message, resolved_message, ctx):
                return [
                    IntentScore(intent="explain_section", score=0.5, source="pattern"),
                    IntentScore(intent="give_example", score=0.3, source="pattern"),
                ]

        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = _HighScoreClassifier()
        result = classifier.classify("something", _make_resolved("something"), ctx)

        assert result.needs_disambiguation is False
        assert result.intent == "explain_section"


# ---------------------------------------------------------------------------
# Tests: all new intent patterns match expected messages (Req 2.6)
# ---------------------------------------------------------------------------


class TestNewIntentPatterns:
    """The IntentClassifier SHALL support new intents: conceptual_question,
    direct_answer_request, quiz_answer_attempt, complexity_adjustment,
    cross_reference_request."""

    def test_conceptual_question_why_pattern(self) -> None:
        msg = "why is the subject placed before the verb?"
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        # Should score conceptual_question among top results
        intent_names = [s.intent for s in result.all_scores]
        assert "conceptual_question" in intent_names

    def test_conceptual_question_how_come(self) -> None:
        msg = "how come this rule applies here?"
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "conceptual_question" in intent_names

    def test_conceptual_question_relationship(self) -> None:
        msg = "what is the relationship between subject and predicate?"
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "conceptual_question" in intent_names

    def test_direct_answer_request_just_tell_me(self) -> None:
        msg = "just tell me the answer"
        ctx = _make_ctx(discourse_state=DiscourseState.SOCRATIC_EXCHANGE)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        assert result.intent == "direct_answer_request"

    def test_direct_answer_request_stop_asking(self) -> None:
        msg = "stop asking me questions"
        ctx = _make_ctx(discourse_state=DiscourseState.SOCRATIC_EXCHANGE)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "direct_answer_request" in intent_names

    def test_quiz_answer_attempt_pattern(self) -> None:
        msg = "i think it's option B"
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "quiz_answer_attempt" in intent_names

    def test_quiz_answer_attempt_my_answer_is(self) -> None:
        msg = "my answer is the second choice"
        ctx = _make_ctx(discourse_state=DiscourseState.INITIAL)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "quiz_answer_attempt" in intent_names

    def test_complexity_adjustment_simpler(self) -> None:
        msg = "explain more simply"
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        assert result.intent == "complexity_adjustment"

    def test_complexity_adjustment_dumb_it_down(self) -> None:
        msg = "dumb it down for me"
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "complexity_adjustment" in intent_names

    def test_complexity_adjustment_go_deeper(self) -> None:
        msg = "go deeper into this topic"
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "complexity_adjustment" in intent_names

    def test_cross_reference_request_relate(self) -> None:
        msg = "how does this relate to fractions?"
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        assert result.intent == "cross_reference_request"

    def test_cross_reference_request_connection(self) -> None:
        msg = "what's the connection between these topics?"
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "cross_reference_request" in intent_names

    def test_cross_reference_request_compared_to(self) -> None:
        msg = "compared to addition, how is this different?"
        ctx = _make_ctx(discourse_state=DiscourseState.FOLLOW_UP)
        classifier = IntentClassifier()
        result = classifier.classify(msg, _make_resolved(msg), ctx)

        intent_names = [s.intent for s in result.all_scores]
        assert "cross_reference_request" in intent_names
