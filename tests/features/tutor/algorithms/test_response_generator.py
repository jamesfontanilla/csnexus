"""Unit tests for the Response Generator.

Tests complexity level computation, override activation/expiry,
variant non-repetition, composed response structure, and template fallback.

Requirements: 5.1, 5.5, 5.6, 6.1, 6.2, 6.4
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ComplexityOverride,
    ConceptEntry,
    ConversationContext,
    ResponseTemplate,
    SocraticPrompt,
    TemplatePart,
)
from app.features.tutor.algorithms.response_generator import (
    ResponseGenerator,
    activate_override,
    compose_response,
    compute_complexity_level,
    decrement_override,
    format_cross_references,
    resolve_effective_complexity,
    select_template_variant,
)
from app.features.tutor.algorithms.template_loader import TemplateLoader


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_ctx(**kwargs) -> ConversationContext:
    """Create a ConversationContext with sensible defaults."""
    return ConversationContext(**kwargs)


def _make_template(
    intent: str = "explain_section",
    complexity: ComplexityLevel = ComplexityLevel.STANDARD,
    openers: list[str] | None = None,
    closings: list[str] | None = None,
) -> ResponseTemplate:
    """Build a ResponseTemplate with configurable parts."""
    if openers is None:
        openers = ["Opener A. ", "Opener B. ", "Opener C. "]
    if closings is None:
        closings = ["Closing A?", "Closing B?", "Closing C?"]
    parts = {
        "opener": TemplatePart(key="opener", variants=openers),
        "core": TemplatePart(key="core", variants=["{content}"]),
        "closing": TemplatePart(key="closing", variants=closings),
    }
    return ResponseTemplate(intent=intent, complexity=complexity, parts=parts)


def _make_content_json(**kwargs) -> dict:
    """Build a minimal lesson content_json for testing."""
    defaults = {
        "subtopic_id": 1,
        "subtopic_title": "Test Topic",
        "key_takeaways": ["first takeaway", "second takeaway"],
        "metadata": {"title": "Test Topic"},
        "sections": [
            {
                "title": "Introduction",
                "blocks": [
                    {"type": "text", "content": "This is the introduction. It has multiple sentences. Here is more detail."}
                ],
            }
        ],
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# Tests: compute_complexity_level (Req 5.1, 5.7)
# ---------------------------------------------------------------------------


class TestComputeComplexityLevel:
    def test_none_returns_standard(self) -> None:
        assert compute_complexity_level(None) == ComplexityLevel.STANDARD

    def test_score_zero_returns_simplified(self) -> None:
        assert compute_complexity_level(0.0) == ComplexityLevel.SIMPLIFIED

    def test_score_just_below_03_returns_simplified(self) -> None:
        assert compute_complexity_level(0.29) == ComplexityLevel.SIMPLIFIED

    def test_score_exactly_03_returns_standard(self) -> None:
        assert compute_complexity_level(0.3) == ComplexityLevel.STANDARD

    def test_score_05_returns_standard(self) -> None:
        assert compute_complexity_level(0.5) == ComplexityLevel.STANDARD

    def test_score_exactly_07_returns_standard(self) -> None:
        assert compute_complexity_level(0.7) == ComplexityLevel.STANDARD

    def test_score_just_above_07_returns_detailed(self) -> None:
        assert compute_complexity_level(0.71) == ComplexityLevel.DETAILED

    def test_score_10_returns_detailed(self) -> None:
        assert compute_complexity_level(1.0) == ComplexityLevel.DETAILED


# ---------------------------------------------------------------------------
# Tests: activate_override and expiry (Req 5.5, 5.6)
# ---------------------------------------------------------------------------


class TestOverrideActivationAndExpiry:
    def test_activate_simpler_from_standard(self) -> None:
        ctx = _make_ctx()
        result = activate_override(ctx, "simpler", ComplexityLevel.STANDARD)

        assert result == ComplexityLevel.SIMPLIFIED
        assert ctx.complexity_override is not None
        assert ctx.complexity_override.level == ComplexityLevel.SIMPLIFIED
        assert ctx.complexity_override.remaining_responses == 3

    def test_activate_deeper_from_standard(self) -> None:
        ctx = _make_ctx()
        result = activate_override(ctx, "deeper", ComplexityLevel.STANDARD)

        assert result == ComplexityLevel.DETAILED
        assert ctx.complexity_override is not None
        assert ctx.complexity_override.level == ComplexityLevel.DETAILED
        assert ctx.complexity_override.remaining_responses == 3

    def test_activate_simpler_from_simplified_stays_simplified(self) -> None:
        ctx = _make_ctx()
        result = activate_override(ctx, "simpler", ComplexityLevel.SIMPLIFIED)

        assert result == ComplexityLevel.SIMPLIFIED
        assert ctx.complexity_override.remaining_responses == 3

    def test_activate_deeper_from_detailed_stays_detailed(self) -> None:
        ctx = _make_ctx()
        result = activate_override(ctx, "deeper", ComplexityLevel.DETAILED)

        assert result == ComplexityLevel.DETAILED
        assert ctx.complexity_override.remaining_responses == 3

    def test_decrement_counts_down(self) -> None:
        ctx = _make_ctx()
        activate_override(ctx, "simpler", ComplexityLevel.STANDARD)

        decrement_override(ctx)
        assert ctx.complexity_override.remaining_responses == 2

        decrement_override(ctx)
        assert ctx.complexity_override.remaining_responses == 1

        decrement_override(ctx)
        assert ctx.complexity_override.remaining_responses == 0

    def test_decrement_clears_override_after_expiry(self) -> None:
        ctx = _make_ctx()
        activate_override(ctx, "deeper", ComplexityLevel.STANDARD)

        # 4 decrements: 3 → 2 → 1 → 0 → cleared
        for _ in range(4):
            decrement_override(ctx)

        assert ctx.complexity_override is None

    def test_decrement_on_no_override_is_noop(self) -> None:
        ctx = _make_ctx()
        assert ctx.complexity_override is None
        decrement_override(ctx)
        assert ctx.complexity_override is None

    def test_resolve_effective_uses_override_when_active(self) -> None:
        ctx = _make_ctx()
        activate_override(ctx, "simpler", ComplexityLevel.STANDARD)

        effective = resolve_effective_complexity(0.5, ctx)
        assert effective == ComplexityLevel.SIMPLIFIED

    def test_resolve_effective_reverts_after_expiry(self) -> None:
        ctx = _make_ctx()
        activate_override(ctx, "deeper", ComplexityLevel.STANDARD)

        # Exhaust override (4 decrements)
        for _ in range(4):
            decrement_override(ctx)

        effective = resolve_effective_complexity(0.5, ctx)
        assert effective == ComplexityLevel.STANDARD


# ---------------------------------------------------------------------------
# Tests: variant non-repetition (Req 6.4)
# ---------------------------------------------------------------------------


class TestVariantNonRepetition:
    def test_consecutive_calls_do_not_repeat_variant(self) -> None:
        ctx = _make_ctx()
        results = []
        for _ in range(10):
            idx = select_template_variant("explain_section", "opener", 3, ctx)
            results.append(idx)

        # No two adjacent results should be the same
        for i in range(1, len(results)):
            assert results[i] != results[i - 1], (
                f"Repeated variant index {results[i]} at positions {i - 1} and {i}. "
                f"Full sequence: {results}"
            )

    def test_all_variants_eventually_used(self) -> None:
        ctx = _make_ctx()
        indices_seen: set[int] = set()
        for _ in range(20):
            idx = select_template_variant("test_intent", "closing", 3, ctx)
            indices_seen.add(idx)

        assert indices_seen == {0, 1, 2}

    def test_single_variant_always_returns_0(self) -> None:
        ctx = _make_ctx()
        for _ in range(5):
            idx = select_template_variant("single", "opener", 1, ctx)
            assert idx == 0

    def test_two_variants_alternate(self) -> None:
        ctx = _make_ctx()
        results = []
        for _ in range(6):
            idx = select_template_variant("duo", "opener", 2, ctx)
            results.append(idx)

        # With 2 variants and non-repetition, adjacent should differ
        for i in range(1, len(results)):
            assert results[i] != results[i - 1]

    def test_usage_tracking_resets_on_exhaustion(self) -> None:
        ctx = _make_ctx()
        # Use all 3 variants
        for _ in range(3):
            select_template_variant("reset_test", "opener", 3, ctx)

        # After exhaustion, tracking should reset — next call succeeds
        idx = select_template_variant("reset_test", "opener", 3, ctx)
        assert 0 <= idx < 3


# ---------------------------------------------------------------------------
# Tests: compose_response structure (Req 6.2, 4.8)
# ---------------------------------------------------------------------------


class TestComposeResponseStructure:
    def test_all_parts_present_in_order(self) -> None:
        result = compose_response("Hello. ", "Core content here.", "See also X.", "Any questions?")

        assert "Hello." in result
        assert "Core content here." in result
        assert "See also X." in result
        assert "Any questions?" in result

        # Verify ordering
        assert result.index("Hello.") < result.index("Core content here.")
        assert result.index("Core content here.") < result.index("See also X.")
        assert result.index("See also X.") < result.index("Any questions?")

    def test_empty_opener_omitted(self) -> None:
        result = compose_response("", "Core content.", "", "")
        assert result.startswith("Core content.")

    def test_empty_cross_reference_omitted(self) -> None:
        result = compose_response("Opener.", "Core.", "", "Closing?")
        assert "Opener." in result
        assert "Core." in result
        assert "Closing?" in result

    def test_empty_closing_omitted(self) -> None:
        result = compose_response("Start.", "Main content.", "Cross ref.", "")
        assert result.endswith("Cross ref.")

    def test_empty_core_triggers_fallback(self) -> None:
        result = compose_response("Opener.", "", "", "Closing?")
        assert "Here's what you need to know about this topic." in result

    def test_core_content_always_nonempty(self) -> None:
        result = compose_response("", "", "", "")
        assert len(result.strip()) > 0
        assert "Here's what you need to know about this topic." in result


# ---------------------------------------------------------------------------
# Tests: template fallback when intent file missing (Req 6.1)
# ---------------------------------------------------------------------------


class TestTemplateFallback:
    @pytest.fixture
    def loader_with_fallback(self, tmp_path: Path) -> TemplateLoader:
        """Create a TemplateLoader with only a fallback template."""
        fallback = {
            "intent": "fallback",
            "variants": {
                "SIMPLIFIED": {
                    "opener": ["Simple opener 1. ", "Simple opener 2. ", "Simple opener 3. "],
                    "core": "{content}",
                    "closing": ["Simple close 1?", "Simple close 2?", "Simple close 3?"],
                },
                "STANDARD": {
                    "opener": ["Standard opener 1. ", "Standard opener 2. ", "Standard opener 3. "],
                    "core": "{content}",
                    "closing": ["Standard close 1?", "Standard close 2?", "Standard close 3?"],
                },
                "DETAILED": {
                    "opener": ["Detailed opener 1. ", "Detailed opener 2. ", "Detailed opener 3. "],
                    "core": "{content}",
                    "closing": ["Detailed close 1?", "Detailed close 2?", "Detailed close 3?"],
                },
            },
        }
        (tmp_path / "fallback.json").write_text(json.dumps(fallback), encoding="utf-8")
        return TemplateLoader.load(tmp_path)

    def test_missing_intent_falls_back(self, loader_with_fallback: TemplateLoader) -> None:
        template = loader_with_fallback.get_template(
            "nonexistent_intent", ComplexityLevel.STANDARD
        )
        assert template.intent == "fallback"

    def test_fallback_template_has_valid_parts(self, loader_with_fallback: TemplateLoader) -> None:
        template = loader_with_fallback.get_template(
            "some_missing_intent", ComplexityLevel.SIMPLIFIED
        )
        assert "opener" in template.parts
        assert "closing" in template.parts
        assert len(template.parts["opener"].variants) >= 3

    def test_generator_uses_default_opener_when_no_template(self) -> None:
        """ResponseGenerator falls back to default openers when template is None."""
        gen = ResponseGenerator()
        ctx = _make_ctx()
        content = _make_content_json()

        response = gen.generate(
            intent="explain_section",
            content_json=content,
            ctx=ctx,
            message="Explain this section",
            reasoning_context=None,
            mastery_score=0.5,
            template=None,
        )

        # Should still produce a non-empty response with a default opener
        assert len(response) > 0
        # Default standard opener
        assert "Here's what you need to know." in response

    def test_generator_uses_template_opener_when_provided(self) -> None:
        """ResponseGenerator uses template openers when a template is provided."""
        gen = ResponseGenerator()
        ctx = _make_ctx()
        content = _make_content_json()
        template = _make_template(
            openers=["Custom opener A. ", "Custom opener B. ", "Custom opener C. "]
        )

        response = gen.generate(
            intent="explain_section",
            content_json=content,
            ctx=ctx,
            message="Explain this section",
            reasoning_context=None,
            mastery_score=0.5,
            template=template,
        )

        # One of the custom openers should be in the response
        assert any(opener.strip() in response for opener in template.parts["opener"].variants)


# ---------------------------------------------------------------------------
# Tests: ResponseGenerator.generate integration
# ---------------------------------------------------------------------------


class TestResponseGeneratorGenerate:
    def test_socratic_prompt_overrides_normal_generation(self) -> None:
        gen = ResponseGenerator()
        ctx = _make_ctx()
        content = _make_content_json()
        prompt = SocraticPrompt(
            question="What do you think happens when...?",
            target_concept="concept",
            key_terms=["a", "b"],
        )

        response = gen.generate(
            intent="conceptual_question",
            content_json=content,
            ctx=ctx,
            message="What do you think happens when...?",
            reasoning_context=None,
            mastery_score=0.5,
            socratic_prompt=prompt,
        )

        assert response == "What do you think happens when...?"

    def test_complexity_override_affects_opener(self) -> None:
        gen = ResponseGenerator()
        ctx = _make_ctx()
        content = _make_content_json()
        # Activate a SIMPLIFIED override
        activate_override(ctx, "simpler", ComplexityLevel.STANDARD)

        response = gen.generate(
            intent="explain_section",
            content_json=content,
            ctx=ctx,
            message="Explain this section",
            reasoning_context=None,
            mastery_score=0.5,
            template=None,
        )

        # Default SIMPLIFIED opener
        assert "Let me break this down simply." in response

    def test_cross_references_included_in_response(self) -> None:
        gen = ResponseGenerator()
        ctx = _make_ctx()
        content = _make_content_json()
        cross_refs = [
            ConceptEntry(
                term="related concept",
                subtopic_id=99,
                subtopic_title="Related Topic",
                source="key_takeaway",
            )
        ]

        response = gen.generate(
            intent="explain_section",
            content_json=content,
            ctx=ctx,
            message="Explain this section",
            reasoning_context=None,
            mastery_score=0.5,
            cross_refs=cross_refs,
            template=None,
        )

        assert "related concept" in response
        assert "Related Topic" in response
