"""Unit tests for the Socratic Module.

Tests activation rules, evaluation logic, escalation, direct answer bypass,
and question template selection.

Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8
"""

from __future__ import annotations

import pytest

from app.features.tutor.algorithms.chat_models import (
    ConversationContext,
    DiscourseState,
    MasteryLevel,
    SocraticState,
)
from app.features.tutor.algorithms.socratic_module import (
    MAX_SOCRATIC_ATTEMPTS,
    QUESTION_TEMPLATES,
    REASONING_TYPES,
    SocraticModule,
)


# ---------------------------------------------------------------------------
# Fixtures / Helpers
# ---------------------------------------------------------------------------


def _make_context(
    *,
    socratic_active: bool = False,
    attempts: int = 0,
    target_concept: str | None = None,
    key_terms: list[str] | None = None,
    reasoning_type: str | None = None,
    discourse_state: DiscourseState = DiscourseState.INITIAL,
) -> ConversationContext:
    """Build a ConversationContext with configurable Socratic state."""
    return ConversationContext(
        discourse_state=discourse_state,
        socratic_state=SocraticState(
            active=socratic_active,
            target_concept=target_concept,
            key_terms=key_terms or [],
            attempts=attempts,
            reasoning_type=reasoning_type,
        ),
    )


# ---------------------------------------------------------------------------
# Tests: should_activate (Req 3.1, 3.7)
# ---------------------------------------------------------------------------


class TestShouldActivate:
    """Test Socratic activation conditions."""

    @pytest.mark.parametrize(
        "mastery_level",
        [
            MasteryLevel.FAMILIAR,
            MasteryLevel.PROFICIENT,
            MasteryLevel.ADVANCED,
            MasteryLevel.MASTERED,
        ],
    )
    def test_activates_for_conceptual_question_at_familiar_plus(
        self, mastery_level: MasteryLevel
    ) -> None:
        """Socratic mode activates for conceptual_question at FAMILIAR+."""
        module = SocraticModule()
        ctx = _make_context()

        result = module.should_activate(
            intent="conceptual_question",
            mastery_level=mastery_level,
            ctx=ctx,
        )

        assert result is True

    def test_inactive_for_beginner_mastery(self) -> None:
        """Socratic mode does not activate for BEGINNER mastery."""
        module = SocraticModule()
        ctx = _make_context()

        result = module.should_activate(
            intent="conceptual_question",
            mastery_level=MasteryLevel.BEGINNER,
            ctx=ctx,
        )

        assert result is False

    def test_inactive_for_non_conceptual_intent(self) -> None:
        """Socratic mode does not activate for intents other than conceptual_question."""
        module = SocraticModule()
        ctx = _make_context()

        for intent in ["explain_section", "give_example", "quiz_me", "greeting"]:
            result = module.should_activate(
                intent=intent,
                mastery_level=MasteryLevel.PROFICIENT,
                ctx=ctx,
            )
            assert result is False, f"Activated unexpectedly for intent={intent}"

    def test_inactive_when_at_max_attempts(self) -> None:
        """Socratic mode does not activate when already at max attempts."""
        module = SocraticModule()
        ctx = _make_context(
            socratic_active=True,
            attempts=MAX_SOCRATIC_ATTEMPTS,
        )

        result = module.should_activate(
            intent="conceptual_question",
            mastery_level=MasteryLevel.FAMILIAR,
            ctx=ctx,
        )

        assert result is False

    def test_activates_when_below_max_attempts(self) -> None:
        """Socratic mode activates when attempts are below the max."""
        module = SocraticModule()
        ctx = _make_context(
            socratic_active=True,
            attempts=MAX_SOCRATIC_ATTEMPTS - 1,
        )

        result = module.should_activate(
            intent="conceptual_question",
            mastery_level=MasteryLevel.FAMILIAR,
            ctx=ctx,
        )

        assert result is True


# ---------------------------------------------------------------------------
# Tests: evaluate_response (Req 3.3, 3.4, 3.5)
# ---------------------------------------------------------------------------


class TestEvaluateResponse:
    """Test Socratic evaluation logic."""

    def test_understood_when_two_or_more_key_terms_matched(self) -> None:
        """Response with >=2 key terms → understood=True."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="photosynthesis",
            key_terms=["light", "energy", "chlorophyll"],
            attempts=1,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(
            message="Plants use light and energy from the sun",
            socratic_state=state,
        )

        assert result.understood is True
        assert len(result.matched_terms) >= 2
        assert "light" in result.matched_terms
        assert "energy" in result.matched_terms

    def test_not_understood_when_fewer_than_two_key_terms(self) -> None:
        """Response with <2 key terms → understood=False."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="photosynthesis",
            key_terms=["light", "energy", "chlorophyll"],
            attempts=1,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(
            message="I think plants grow taller when watered",
            socratic_state=state,
        )

        assert result.understood is False
        assert len(result.matched_terms) < 2

    def test_not_understood_with_single_key_term(self) -> None:
        """Response with exactly 1 key term → understood=False."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="photosynthesis",
            key_terms=["light", "energy", "chlorophyll"],
            attempts=1,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(
            message="I know it involves light somehow",
            socratic_state=state,
        )

        assert result.understood is False
        assert result.matched_terms == ["light"]

    def test_key_term_matching_is_case_insensitive(self) -> None:
        """Key term matching is case-insensitive."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="gravity",
            key_terms=["force", "mass", "attraction"],
            attempts=1,
            reasoning_type="cause_effect",
        )

        result = module.evaluate_response(
            message="FORCE and MASS determine the strength",
            socratic_state=state,
        )

        assert result.understood is True
        assert len(result.matched_terms) >= 2

    def test_escalation_after_max_failed_attempts(self) -> None:
        """After 3 failed attempts, should_escalate is True."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="recursion",
            key_terms=["base", "case", "function"],
            attempts=MAX_SOCRATIC_ATTEMPTS,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(
            message="I have no idea what this is",
            socratic_state=state,
        )

        assert result.understood is False
        assert result.should_escalate is True

    def test_no_escalation_when_below_max_attempts(self) -> None:
        """Before reaching max attempts, should_escalate is False."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="recursion",
            key_terms=["base", "case", "function"],
            attempts=1,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(
            message="I have no idea what this is",
            socratic_state=state,
        )

        assert result.understood is False
        assert result.should_escalate is False

    def test_no_escalation_when_understood(self) -> None:
        """When the learner understands, escalation is never triggered."""
        module = SocraticModule()
        state = SocraticState(
            active=True,
            target_concept="recursion",
            key_terms=["base", "case", "function"],
            attempts=MAX_SOCRATIC_ATTEMPTS,
            reasoning_type="definition_recall",
        )

        result = module.evaluate_response(
            message="A function calls itself until it hits the base case",
            socratic_state=state,
        )

        assert result.understood is True
        assert result.should_escalate is False


# ---------------------------------------------------------------------------
# Tests: direct answer request bypass (Req 3.6)
# ---------------------------------------------------------------------------


class TestDirectAnswerBypass:
    """Test that direct_answer_request intent prevents Socratic activation."""

    def test_direct_answer_request_does_not_activate(self) -> None:
        """Intent 'direct_answer_request' bypasses Socratic mode."""
        module = SocraticModule()
        ctx = _make_context()

        result = module.should_activate(
            intent="direct_answer_request",
            mastery_level=MasteryLevel.PROFICIENT,
            ctx=ctx,
        )

        assert result is False


# ---------------------------------------------------------------------------
# Tests: generate_guiding_question (Req 3.2, 3.8)
# ---------------------------------------------------------------------------


class TestGenerateGuidingQuestion:
    """Test guiding question generation and template selection."""

    def test_returns_socratic_prompt_with_valid_fields(self) -> None:
        """Generated prompt has non-empty question, target concept, and key terms."""
        module = SocraticModule()

        prompt = module.generate_guiding_question(
            concept="binary search",
            section_content="Binary search divides the sorted array in half each step.",
            reasoning_type="definition_recall",
        )

        assert prompt.question
        assert prompt.target_concept == "binary search"
        assert 1 <= len(prompt.key_terms) <= 3
        assert prompt.reasoning_type == "definition_recall"

    def test_question_contains_concept_name(self) -> None:
        """The guiding question includes the target concept."""
        module = SocraticModule()

        prompt = module.generate_guiding_question(
            concept="polymorphism",
            section_content="Polymorphism allows objects of different types to be treated uniformly.",
            reasoning_type="application",
        )

        assert "polymorphism" in prompt.question.lower()

    @pytest.mark.parametrize("reasoning_type", REASONING_TYPES)
    def test_all_reasoning_types_produce_questions(
        self, reasoning_type: str
    ) -> None:
        """Each reasoning type generates a valid guiding question."""
        module = SocraticModule()

        prompt = module.generate_guiding_question(
            concept="variables",
            section_content="Variables store data values in memory for later use.",
            reasoning_type=reasoning_type,
        )

        assert prompt.question
        assert prompt.reasoning_type == reasoning_type

    def test_template_cycling_avoids_repetition(self) -> None:
        """Different attempt numbers produce different questions."""
        module = SocraticModule()
        reasoning_type = "definition_recall"
        questions = set()

        for attempt in range(len(QUESTION_TEMPLATES[reasoning_type])):
            prompt = module.generate_guiding_question(
                concept="loops",
                section_content="Loops repeat a block of code multiple times.",
                reasoning_type=reasoning_type,
                attempts=attempt,
            )
            questions.add(prompt.question)

        # Each attempt should produce a distinct question
        assert len(questions) == len(QUESTION_TEMPLATES[reasoning_type])

    def test_invalid_reasoning_type_falls_back_to_definition_recall(self) -> None:
        """An unrecognized reasoning type falls back to definition_recall."""
        module = SocraticModule()

        prompt = module.generate_guiding_question(
            concept="encapsulation",
            section_content="Encapsulation hides internal details.",
            reasoning_type="nonexistent_type",
        )

        assert prompt.reasoning_type == "definition_recall"
        assert prompt.question


# ---------------------------------------------------------------------------
# Tests: question templates cover all reasoning types (Req 3.8)
# ---------------------------------------------------------------------------


class TestQuestionTemplates:
    """Test template structure meets requirements."""

    def test_all_reasoning_types_have_at_least_3_templates(self) -> None:
        """Each reasoning type has a minimum of 3 question templates."""
        for rtype, templates in QUESTION_TEMPLATES.items():
            assert len(templates) >= 3, (
                f"Reasoning type '{rtype}' has only {len(templates)} templates, "
                f"minimum is 3."
            )

    def test_reasoning_types_list_matches_template_keys(self) -> None:
        """REASONING_TYPES list is consistent with QUESTION_TEMPLATES keys."""
        assert set(REASONING_TYPES) == set(QUESTION_TEMPLATES.keys())

    def test_all_templates_use_concept_placeholder(self) -> None:
        """Every template string contains the {concept} placeholder."""
        for rtype, templates in QUESTION_TEMPLATES.items():
            for i, template in enumerate(templates):
                assert "{concept}" in template, (
                    f"Template {i} in reasoning type '{rtype}' "
                    f"is missing {{concept}} placeholder: {template!r}"
                )


# ---------------------------------------------------------------------------
# Tests: select_reasoning_type
# ---------------------------------------------------------------------------


class TestSelectReasoningType:
    """Test reasoning type selection logic."""

    def test_returns_current_type_when_socratic_active(self) -> None:
        """When a Socratic exchange is active, continues with current type."""
        module = SocraticModule()
        ctx = _make_context(
            socratic_active=True,
            reasoning_type="comparison",
        )

        result = module.select_reasoning_type(ctx)

        assert result == "comparison"

    def test_cycles_through_types_when_inactive(self) -> None:
        """When no active Socratic exchange, cycles based on exchange count."""
        module = SocraticModule()
        types_seen = set()

        for i in range(len(REASONING_TYPES)):
            ctx = ConversationContext(
                exchanges=[
                    # Add i exchanges to simulate different positions
                ]
                * i,
            )
            # Manually set exchange count via list comprehension
            from app.features.tutor.algorithms.chat_models import Exchange

            ctx.exchanges = [
                Exchange(
                    user_message="msg",
                    assistant_response="resp",
                    intent="explain_section",
                    topic_thread_subject="topic",
                )
            ] * i
            rtype = module.select_reasoning_type(ctx)
            types_seen.add(rtype)

        # Should cycle through all available types
        assert types_seen == set(REASONING_TYPES)
