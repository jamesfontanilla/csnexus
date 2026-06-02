"""Response generator with adaptive complexity for the Smart Chat Engine.

Assembles final response text by:
1. Computing the effective complexity level from mastery score (with override support).
2. Selecting a template variant that avoids repetition.
3. Composing the response from parts: opener + core content + cross_reference + closing.

Complexity thresholds:
    score < 0.3        → SIMPLIFIED
    0.3 <= score <= 0.7 → STANDARD
    score > 0.7        → DETAILED
    None               → STANDARD

Override lifetime: active for the current response + the next 3 responses (remaining_responses
counts down from 3 to 0). After expiry, reverts to mastery-computed level.

Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 6.1, 6.2, 6.3, 6.4, 6.5
"""

from __future__ import annotations

import random
from typing import Any

from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ComplexityOverride,
    ConceptEntry,
    ConversationContext,
    ResponseTemplate,
    SocraticPrompt,
    TemplatePart,
)


# ---------------------------------------------------------------------------
# Complexity computation
# ---------------------------------------------------------------------------


def compute_complexity_level(mastery_score: float | None) -> ComplexityLevel:
    """Map mastery score to a complexity level.

    Returns STANDARD when *mastery_score* is None (no mastery data).
    """
    if mastery_score is None:
        return ComplexityLevel.STANDARD
    if mastery_score < 0.3:
        return ComplexityLevel.SIMPLIFIED
    if mastery_score > 0.7:
        return ComplexityLevel.DETAILED
    return ComplexityLevel.STANDARD


def resolve_effective_complexity(
    mastery_score: float | None,
    ctx: ConversationContext,
) -> ComplexityLevel:
    """Return the effective complexity level considering any active override.

    If a ComplexityOverride is active (remaining_responses >= 0), its level
    takes precedence. Otherwise the mastery-computed level is used.
    """
    if ctx.complexity_override is not None and ctx.complexity_override.remaining_responses >= 0:
        return ctx.complexity_override.level
    return compute_complexity_level(mastery_score)


def decrement_override(ctx: ConversationContext) -> None:
    """Decrement the complexity override counter after generating a response.

    When remaining_responses reaches below 0, the override is cleared.
    """
    if ctx.complexity_override is None:
        return
    ctx.complexity_override.remaining_responses -= 1
    if ctx.complexity_override.remaining_responses < 0:
        ctx.complexity_override = None


def activate_override(
    ctx: ConversationContext,
    direction: str,
    current_level: ComplexityLevel,
) -> ComplexityLevel:
    """Activate a complexity override, shifting one tier in *direction*.

    Args:
        ctx: Conversation context (mutated in place).
        direction: ``"simpler"`` to shift down, ``"deeper"`` to shift up.
        current_level: The mastery-computed level before override.

    Returns:
        The new overridden complexity level.
    """
    _LEVELS_ORDERED = [
        ComplexityLevel.SIMPLIFIED,
        ComplexityLevel.STANDARD,
        ComplexityLevel.DETAILED,
    ]
    current_idx = _LEVELS_ORDERED.index(current_level)

    if direction == "simpler":
        new_idx = max(0, current_idx - 1)
    else:  # "deeper"
        new_idx = min(len(_LEVELS_ORDERED) - 1, current_idx + 1)

    new_level = _LEVELS_ORDERED[new_idx]
    ctx.complexity_override = ComplexityOverride(level=new_level, remaining_responses=3)
    return new_level


# ---------------------------------------------------------------------------
# Template variant selection
# ---------------------------------------------------------------------------


def _select_variant_index(
    available_count: int,
    used_indices: list[int],
) -> int:
    """Pick a variant index avoiding the most recently used one.

    Rules:
    - If all variants have been used, reset and pick randomly.
    - Otherwise pick from unused indices.
    - Never repeat the last used index when possible (adjacent non-repetition).
    """
    if available_count <= 0:
        return 0

    last_used = used_indices[-1] if used_indices else -1

    # Determine which indices haven't been used yet.
    all_indices = set(range(available_count))
    used_set = set(used_indices)
    unused = all_indices - used_set

    if not unused:
        # All exhausted — reset. Pick randomly but avoid last_used if possible.
        candidates = [i for i in range(available_count) if i != last_used]
        if not candidates:
            candidates = list(range(available_count))
        return random.choice(candidates)

    # Pick from unused, avoiding the last used index.
    candidates = [i for i in unused if i != last_used]
    if not candidates:
        # Only the last_used index is the sole unused one — use it.
        candidates = list(unused)
    return random.choice(candidates)


def select_template_variant(
    intent: str,
    part_key: str,
    available_count: int,
    ctx: ConversationContext,
) -> int:
    """Select a variant index for a given intent+part, updating usage tracking.

    The context's ``template_usage`` maps ``"{intent}:{part_key}"`` to the list
    of variant indices used so far.

    Returns the chosen variant index (0-based).
    """
    usage_key = f"{intent}:{part_key}"
    used_indices = ctx.template_usage.get(usage_key, [])

    chosen = _select_variant_index(available_count, used_indices)

    # Update tracking — if all were exhausted we reset tracking to just this pick.
    all_used = set(range(available_count))
    if set(used_indices) >= all_used:
        ctx.template_usage[usage_key] = [chosen]
    else:
        if usage_key not in ctx.template_usage:
            ctx.template_usage[usage_key] = []
        ctx.template_usage[usage_key].append(chosen)

    return chosen


# ---------------------------------------------------------------------------
# Cross-reference formatting
# ---------------------------------------------------------------------------

_MAX_CROSS_REFS = 2
_MAX_CROSS_REF_CHARS = 150


def format_cross_references(cross_refs: list[ConceptEntry]) -> str:
    """Format cross-reference entries into response text.

    Limits to at most 2 references, each at most 150 characters and a single
    sentence.
    """
    if not cross_refs:
        return ""

    parts: list[str] = []
    for entry in cross_refs[:_MAX_CROSS_REFS]:
        ref_text = f"This connects to {entry.term} in {entry.subtopic_title}."
        # Truncate to 150 chars if needed.
        if len(ref_text) > _MAX_CROSS_REF_CHARS:
            ref_text = ref_text[: _MAX_CROSS_REF_CHARS - 1] + "."
        parts.append(ref_text)

    return " ".join(parts)


# ---------------------------------------------------------------------------
# Response composition
# ---------------------------------------------------------------------------


def compose_response(
    opener: str,
    core_content: str,
    cross_reference: str,
    closing: str,
) -> str:
    """Assemble a response from its parts in the correct order.

    Order: opener + core_content + cross_reference + closing.
    Core content is always included (must be non-empty).
    Cross-reference and closing may be empty/omitted.
    """
    parts: list[str] = []

    if opener:
        parts.append(opener)

    # Core content is mandatory — if somehow empty, provide a minimal fallback.
    if core_content:
        parts.append(core_content)
    else:
        parts.append("Here's what you need to know about this topic.")

    if cross_reference:
        parts.append(cross_reference)

    if closing:
        parts.append(closing)

    return " ".join(parts)


# ---------------------------------------------------------------------------
# ResponseGenerator class
# ---------------------------------------------------------------------------


class ResponseGenerator:
    """Generates adaptive-complexity responses using the template system.

    Integrates with:
    - Template system (TemplateLoader / ResponseTemplate)
    - Cross-lesson registry (ConceptEntry)
    - Socratic module (SocraticPrompt)
    """

    def generate(
        self,
        *,
        intent: str,
        content_json: dict[str, Any],
        ctx: ConversationContext,
        mastery_score: float | None,
        cross_refs: list[ConceptEntry] | None = None,
        socratic_prompt: SocraticPrompt | None = None,
        active_section_index: int | None = None,
        template: ResponseTemplate | None = None,
    ) -> str:
        """Generate the full response text.

        Args:
            intent: Detected intent string.
            content_json: Lesson content data.
            ctx: Current conversation context (mutated: override counter,
                template usage tracking).
            mastery_score: User mastery score (None if not available).
            cross_refs: Related concepts from the cross-lesson registry.
            socratic_prompt: If set, the Socratic module's guiding question
                overrides normal response generation.
            active_section_index: Section the user is viewing.
            template: Pre-loaded response template. If None, a minimal
                fallback is used.

        Returns:
            The composed response text string.
        """
        if cross_refs is None:
            cross_refs = []

        # If Socratic mode produced a prompt, return it directly.
        if socratic_prompt is not None:
            return socratic_prompt.question

        # Resolve effective complexity (accounts for override).
        complexity = resolve_effective_complexity(mastery_score, ctx)

        # Decrement override counter for this response.
        decrement_override(ctx)

        # Select template parts.
        opener = self._select_opener(intent, complexity, ctx, template)
        core_content = self._build_core_content(
            intent, content_json, active_section_index, complexity
        )
        cross_ref_text = format_cross_references(cross_refs)
        closing = self._select_closing(intent, complexity, ctx, template)

        return compose_response(opener, core_content, cross_ref_text, closing)

    def _select_opener(
        self,
        intent: str,
        complexity: ComplexityLevel,
        ctx: ConversationContext,
        template: ResponseTemplate | None,
    ) -> str:
        """Select an opener variant from the template, avoiding repetition."""
        if template is None or "opener" not in template.parts:
            return self._default_opener(complexity)

        part = template.parts["opener"]
        if not part.variants:
            return self._default_opener(complexity)

        idx = select_template_variant(intent, "opener", len(part.variants), ctx)
        return part.variants[idx]

    def _select_closing(
        self,
        intent: str,
        complexity: ComplexityLevel,
        ctx: ConversationContext,
        template: ResponseTemplate | None,
    ) -> str:
        """Select a closing variant from the template, avoiding repetition."""
        if template is None or "closing" not in template.parts:
            return self._default_closing(complexity)

        part = template.parts["closing"]
        if not part.variants:
            return self._default_closing(complexity)

        idx = select_template_variant(intent, "closing", len(part.variants), ctx)
        return part.variants[idx]

    def _build_core_content(
        self,
        intent: str,
        content_json: dict[str, Any],
        active_section_index: int | None,
        complexity: ComplexityLevel,
    ) -> str:
        """Build the core content portion of the response.

        Extracts relevant information from the lesson content based on
        intent and the active section. Always returns a non-empty string.
        """
        sections = content_json.get("sections") or []
        key_takeaways = content_json.get("key_takeaways") or []
        metadata = content_json.get("metadata") or {}
        title = metadata.get("title", "this topic")

        # Get the active section if available.
        active_section: dict[str, Any] | None = None
        if active_section_index is not None and 0 <= active_section_index < len(sections):
            active_section = sections[active_section_index]

        # Build content based on intent.
        if intent == "explain_section":
            return self._core_explain(active_section, sections, key_takeaways, complexity)
        if intent == "give_example":
            return self._core_example(content_json, complexity)
        if intent == "summarize":
            return self._core_summarize(content_json, key_takeaways, title, complexity)
        if intent in ("quiz_me", "quiz_answer_attempt"):
            return self._core_quiz(content_json)
        if intent == "relate_to_exam":
            return self._core_exam(content_json, title)
        if intent == "memory_aid":
            return self._core_memory_aid(content_json, title)
        if intent == "greeting":
            return f"I'm here to help you with {title}. Ask me anything about what you're reading."
        if intent == "thanks":
            return "Let me know if you have more questions."
        if intent == "conceptual_question":
            return self._core_explain(active_section, sections, key_takeaways, complexity)
        if intent == "direct_answer_request":
            return self._core_explain(active_section, sections, key_takeaways, complexity)
        if intent == "complexity_adjustment":
            return "I've adjusted the complexity of my responses."
        if intent == "cross_reference_request":
            return self._core_cross_reference(content_json, key_takeaways)

        # Fallback — always returns non-empty.
        if key_takeaways:
            return key_takeaways[0]
        return f"Let me help you with {title}."

    # ------------------------------------------------------------------
    # Core content builders per intent
    # ------------------------------------------------------------------

    def _core_explain(
        self,
        active_section: dict[str, Any] | None,
        sections: list[dict[str, Any]],
        key_takeaways: list[str],
        complexity: ComplexityLevel,
    ) -> str:
        """Build explanation core content."""
        section = active_section
        if section is None and sections:
            section = sections[0]

        if section is None:
            return key_takeaways[0] if key_takeaways else "This concept is fundamental to the topic."

        section_text = self._extract_section_text(section)
        if not section_text:
            return key_takeaways[0] if key_takeaways else "This concept is fundamental to the topic."

        # Adapt length based on complexity.
        sentences = [s.strip() for s in section_text.split(".") if s.strip()]
        if complexity == ComplexityLevel.SIMPLIFIED:
            core = ". ".join(sentences[:2]) + "." if sentences else section_text[:150]
        elif complexity == ComplexityLevel.DETAILED:
            core = ". ".join(sentences[:6]) + "." if sentences else section_text[:500]
        else:
            core = ". ".join(sentences[:4]) + "." if sentences else section_text[:300]

        return core

    def _core_example(
        self,
        content_json: dict[str, Any],
        complexity: ComplexityLevel,
    ) -> str:
        """Build example core content."""
        problems = content_json.get("practice_problems") or []
        if problems:
            problem = problems[0]
            question = problem.get("question", "")
            if question:
                return f"Here's a practice problem: {question}"

        sections = content_json.get("sections") or []
        for section in sections:
            for block in section.get("blocks", []):
                if block.get("type") in ("example", "step_by_step"):
                    content = block.get("content", "")
                    if isinstance(content, str) and content:
                        return content[:300]

        return "Try applying the concept to a specific scenario to see how it works."

    def _core_summarize(
        self,
        content_json: dict[str, Any],
        key_takeaways: list[str],
        title: str,
        complexity: ComplexityLevel,
    ) -> str:
        """Build summary core content."""
        summary = content_json.get("summary", "")
        if summary:
            return summary

        if key_takeaways:
            items = key_takeaways[:3] if complexity == ComplexityLevel.SIMPLIFIED else key_takeaways[:5]
            return "Key points: " + "; ".join(items) + "."

        return f"The main ideas of {title} cover the core principles discussed in each section."

    def _core_quiz(self, content_json: dict[str, Any]) -> str:
        """Build quiz core content."""
        problems = content_json.get("practice_problems") or []
        if problems:
            problem = random.choice(problems)
            return problem.get("question", "Can you explain this concept in your own words?")
        key_takeaways = content_json.get("key_takeaways") or []
        if key_takeaways:
            return f"Can you explain this concept in your own words: {random.choice(key_takeaways)}"
        return "Can you explain the main idea of this section in your own words?"

    def _core_exam(self, content_json: dict[str, Any], title: str) -> str:
        """Build exam relevance core content."""
        strategies = content_json.get("exam_strategies") or []
        if strategies:
            return " ".join(strategies[:2])
        return f"{title} is commonly tested through questions that require direct application of the rules."

    def _core_memory_aid(self, content_json: dict[str, Any], title: str) -> str:
        """Build memory aid core content."""
        aids = content_json.get("memory_aids") or []
        if aids:
            return " ".join(aids[:2])
        key_takeaways = content_json.get("key_takeaways") or []
        if key_takeaways:
            return f"Remember these key points about {title}: {'; '.join(key_takeaways[:3])}"
        return f"Try creating associations between {title} concepts and real-world scenarios."

    def _core_cross_reference(
        self,
        content_json: dict[str, Any],
        key_takeaways: list[str],
    ) -> str:
        """Build cross-reference request core content."""
        if key_takeaways:
            return f"The main idea here is: {key_takeaways[0]}"
        return "Let me explain how this topic connects to others."

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _extract_section_text(self, section: dict[str, Any]) -> str:
        """Extract plain text from a section's blocks."""
        blocks = section.get("blocks", [])
        parts: list[str] = []
        for block in blocks:
            content = block.get("content", "")
            if isinstance(content, str):
                parts.append(content)
            elif isinstance(content, dict):
                headers = content.get("headers", [])
                if headers:
                    parts.append(f"Table: {', '.join(headers)}")
        return " ".join(parts)

    def _default_opener(self, complexity: ComplexityLevel) -> str:
        """Provide a sensible default opener when no template is available."""
        if complexity == ComplexityLevel.SIMPLIFIED:
            return "Let me break this down simply."
        if complexity == ComplexityLevel.DETAILED:
            return "Here's a thorough explanation."
        return "Here's what you need to know."

    def _default_closing(self, complexity: ComplexityLevel) -> str:
        """Provide a sensible default closing when no template is available."""
        if complexity == ComplexityLevel.SIMPLIFIED:
            return "Want me to explain any part differently?"
        if complexity == ComplexityLevel.DETAILED:
            return "Would you like to explore any edge cases or applications?"
        return "Does that help? Let me know if you have more questions."
