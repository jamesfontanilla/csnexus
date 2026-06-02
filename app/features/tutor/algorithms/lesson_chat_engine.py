"""Smart Chat Engine orchestrator for the pseudo-AI chatbot.

Provides the main entry point ``generate_chat_response`` which wires
together the full orchestration pipeline:

    ContextManager → AnaphoraResolver → IntentClassifier → SocraticModule → ResponseGenerator

The engine remains purely rule-based (no LLM, no external API calls).
All responses are assembled from the lesson's own content_json using
discourse-aware intent classification and template-based generation.

The old stateless signature is replaced with a keyword-arg interface
returning ``ChatResult``. Backward compatibility is maintained: when
``context_json`` is None, the engine starts a fresh conversation context.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

from app.features.tutor.algorithms.anaphora_resolver import AnaphoraResolver
from app.features.tutor.algorithms.chat_models import (
    ChatResult,
    ConversationContext,
    DiscourseState,
    MasteryLevel,
    SocraticPrompt,
)
from app.features.tutor.algorithms.context_manager import ContextManager
from app.features.tutor.algorithms.cross_lesson_registry import CrossLessonRegistry
from app.features.tutor.algorithms.intent_classifier import IntentClassifier
from app.features.tutor.algorithms.response_generator import (
    ResponseGenerator,
    activate_override,
    compute_complexity_level,
    resolve_effective_complexity,
)
from app.features.tutor.algorithms.socratic_module import SocraticModule
from app.features.tutor.algorithms.template_loader import TemplateLoader

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Module-level singletons (lazily initialized)
# ---------------------------------------------------------------------------

_context_manager = ContextManager()
_anaphora_resolver = AnaphoraResolver()
_intent_classifier = IntentClassifier()
_socratic_module = SocraticModule()
_response_generator = ResponseGenerator()

# Template loader — loaded once from the data directory.
_TEMPLATES_DIR = Path(__file__).resolve().parents[4] / "data" / "chat_templates"
_template_loader: TemplateLoader | None = None


def _get_template_loader() -> TemplateLoader:
    """Lazily initialize and return the template loader singleton."""
    global _template_loader
    if _template_loader is None:
        _template_loader = TemplateLoader.load(_TEMPLATES_DIR)
    return _template_loader


# ---------------------------------------------------------------------------
# Complexity adjustment detection
# ---------------------------------------------------------------------------

_SIMPLIFY_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:explain (?:more )?simply|too (?:complex|complicated|hard|difficult))", re.IGNORECASE),
    re.compile(r"(?:dumb it down|simpler|easier|in simple terms|eli5)", re.IGNORECASE),
]

_DEEPEN_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"(?:give me more detail|go deeper|more (?:depth|advanced|technical))", re.IGNORECASE),
    re.compile(r"(?:too (?:simple|basic|easy)|more complex|elaborate more)", re.IGNORECASE),
]


def _detect_complexity_direction(message: str) -> str | None:
    """Detect whether the message requests a complexity adjustment.

    Returns ``"simpler"`` or ``"deeper"`` if detected, else None.
    """
    for pattern in _SIMPLIFY_PATTERNS:
        if pattern.search(message):
            return "simpler"
    for pattern in _DEEPEN_PATTERNS:
        if pattern.search(message):
            return "deeper"
    return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------


def generate_chat_response(
    *,
    content_json: dict[str, Any],
    message: str,
    active_section_index: int | None = None,
    context_json: dict | None = None,
    mastery_score: float | None = None,
    mastery_level: str | None = None,
    cross_lesson_registry: CrossLessonRegistry | None = None,
) -> ChatResult:
    """Generate a contextual chat response for a lesson.

    Orchestrates the full pipeline:
    1. Build or restore conversation context.
    2. Resolve anaphoric references.
    3. Classify intent (with discourse awareness).
    4. Handle special cases (clarification, disambiguation, complexity).
    5. Apply Socratic module if appropriate.
    6. Generate response via templates.
    7. Update context and return ChatResult.

    Args:
        content_json: The lesson's full content_json dict.
        message: The user's chat message.
        active_section_index: Index of the section the user is viewing.
        context_json: Serialized ConversationContext from frontend (None starts fresh).
        mastery_score: User's mastery score for the subtopic (None if unavailable).
        mastery_level: User's mastery level string (None if unavailable).
        cross_lesson_registry: Registry for cross-lesson concept lookup.

    Returns:
        ChatResult with response_text, detected_intent, and serialized context_json.
    """
    # --- Step 1: Build conversation context ---
    ctx = _context_manager.build_context(context_json)

    # --- Step 2: Resolve anaphoric references ---
    resolved = _anaphora_resolver.resolve(message, ctx)

    # --- Handle clarification when anaphora resolution fails ---
    if _needs_clarification(resolved, ctx):
        response_text = _build_clarification_response(resolved)
        # Update context with the clarification exchange
        ctx = _context_manager.update_context(
            ctx, message, response_text, "clarification"
        )
        serialized = _context_manager.serialize(ctx)
        return ChatResult(
            response_text=response_text,
            detected_intent="clarification",
            context_json=serialized,
        )

    # --- Step 3: Classify intent ---
    classification = _intent_classifier.classify(message, resolved, ctx)

    # --- Handle disambiguation when confidence is too low ---
    if classification.needs_disambiguation:
        response_text = _build_disambiguation_response(classification)
        ctx.discourse_state = DiscourseState.CLARIFICATION
        ctx = _context_manager.update_context(
            ctx, message, response_text, "disambiguation"
        )
        serialized = _context_manager.serialize(ctx)
        return ChatResult(
            response_text=response_text,
            detected_intent="disambiguation",
            context_json=serialized,
        )

    detected_intent = classification.intent

    # --- Step 4: Handle complexity adjustment ---
    direction = _detect_complexity_direction(message)
    if detected_intent == "complexity_adjustment" or direction is not None:
        if direction is None:
            direction = "simpler"  # default if pattern not clear
        base_level = compute_complexity_level(mastery_score)
        activate_override(ctx, direction, base_level)
        detected_intent = "complexity_adjustment"

    # --- Step 5: Socratic module ---
    parsed_mastery_level = _parse_mastery_level(mastery_level)
    socratic_prompt: SocraticPrompt | None = None

    if _socratic_module.should_activate(detected_intent, parsed_mastery_level, ctx):
        # Determine section content for key term extraction
        section_content = _get_section_content(content_json, active_section_index)
        reasoning_type = _socratic_module.select_reasoning_type(ctx)
        concept = resolved.referent if resolved.referent else _extract_concept(message)

        socratic_prompt = _socratic_module.generate_guiding_question(
            concept=concept,
            section_content=section_content,
            reasoning_type=reasoning_type,
            attempts=ctx.socratic_state.attempts,
        )

        # Update Socratic state in context
        ctx.socratic_state.active = True
        ctx.socratic_state.target_concept = socratic_prompt.target_concept
        ctx.socratic_state.key_terms = socratic_prompt.key_terms
        ctx.socratic_state.attempts += 1
        ctx.socratic_state.reasoning_type = socratic_prompt.reasoning_type

    # --- Handle Socratic evaluation for quiz_answer_attempt in Socratic exchange ---
    if (
        detected_intent == "quiz_answer_attempt"
        and ctx.socratic_state.active
        and ctx.discourse_state == DiscourseState.SOCRATIC_EXCHANGE
    ):
        evaluation = _socratic_module.evaluate_response(message, ctx.socratic_state)
        if evaluation.understood:
            # Deactivate Socratic mode and provide confirmation
            ctx.socratic_state.active = False
            ctx.socratic_state.attempts = 0
            detected_intent = "explain_section"
            socratic_prompt = None  # Let response generator handle normally
        elif evaluation.should_escalate:
            # Max attempts — provide direct answer
            ctx.socratic_state.active = False
            ctx.socratic_state.attempts = 0
            detected_intent = "direct_answer_request"
            socratic_prompt = None

    # --- Step 6: Cross-lesson references ---
    cross_refs = []
    if cross_lesson_registry is not None:
        # Gather terms from the current topic thread for lookup
        terms = _gather_cross_ref_terms(ctx, resolved)
        # Get current subtopic_id from content_json metadata
        metadata = content_json.get("metadata") or {}
        current_subtopic_id = metadata.get("subtopic_id", -1)
        cross_refs = cross_lesson_registry.find_related(terms, current_subtopic_id)

    # --- Step 7: Generate response ---
    template_loader = _get_template_loader()

    effective_complexity = resolve_effective_complexity(mastery_score, ctx)
    template = template_loader.get_template(detected_intent, effective_complexity)

    response_text = _response_generator.generate(
        intent=detected_intent,
        content_json=content_json,
        ctx=ctx,
        mastery_score=mastery_score,
        cross_refs=cross_refs,
        socratic_prompt=socratic_prompt,
        active_section_index=active_section_index,
        template=template,
    )

    # --- Step 8: Update context with this exchange ---
    ctx = _context_manager.update_context(
        ctx, message, response_text, detected_intent
    )

    # --- Step 9: Serialize and return ---
    serialized = _context_manager.serialize(ctx)

    return ChatResult(
        response_text=response_text,
        detected_intent=detected_intent,
        context_json=serialized,
    )


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _needs_clarification(resolved, ctx: ConversationContext) -> bool:
    """Check if anaphora resolution failed and clarification is needed.

    Clarification is needed when:
    - The message contains anaphoric references (candidates were generated)
    - Resolution confidence is below threshold (referent is None)
    - There are candidates to present (≤ 2)
    """
    if resolved.referent is not None:
        return False
    if not resolved.candidates:
        return False
    # Resolution failed — confidence too low, present candidates
    return resolved.confidence < 0.4


def _build_clarification_response(resolved) -> str:
    """Build a clarification question when anaphora resolution fails.

    Presents at most 2 candidate interpretations.
    """
    candidates = resolved.candidates[:2]
    if len(candidates) == 1:
        return (
            f"I'm not sure what you're referring to. "
            f"Did you mean **{candidates[0]}**?"
        )
    return (
        f"I'm not sure what you're referring to. "
        f"Did you mean **{candidates[0]}** or **{candidates[1]}**?"
    )


def _build_disambiguation_response(classification) -> str:
    """Build a disambiguation question when intent confidence is low.

    Presents the top 2 candidate intents as options, or asks an open-ended
    clarifying question if fewer than 2 candidates exist.
    """
    options = classification.disambiguation_options
    if options and len(options) >= 2:
        # Map intent keys to user-friendly labels
        labels = {
            "explain_section": "get an explanation",
            "give_example": "see an example",
            "summarize": "get a summary",
            "quiz_me": "take a quiz",
            "relate_to_exam": "learn how this appears in exams",
            "memory_aid": "get memory tips",
            "next_step": "know what to do next",
            "conceptual_question": "understand why/how something works",
            "direct_answer_request": "get a direct answer",
            "cross_reference_request": "see how topics connect",
            "complexity_adjustment": "adjust explanation complexity",
        }
        label_1 = labels.get(options[0], options[0])
        label_2 = labels.get(options[1], options[1])
        return (
            f"I want to help, but I'm not sure what you need. "
            f"Would you like to **{label_1}** or **{label_2}**?"
        )
    # Open-ended clarifying prompt
    return (
        "I'm not quite sure what you're asking. "
        "Could you rephrase your question or tell me what you'd like help with?"
    )


def _parse_mastery_level(mastery_level: str | None) -> MasteryLevel:
    """Parse mastery level string to MasteryLevel enum.

    Defaults to BEGINNER if not provided or unrecognized.
    """
    if mastery_level is None:
        return MasteryLevel.BEGINNER
    try:
        return MasteryLevel(mastery_level)
    except (ValueError, KeyError):
        # Try uppercase match
        try:
            return MasteryLevel[mastery_level.upper()]
        except (KeyError, AttributeError):
            return MasteryLevel.BEGINNER


def _get_section_content(
    content_json: dict[str, Any], active_section_index: int | None
) -> str:
    """Extract section text for Socratic key term extraction."""
    sections = content_json.get("sections") or []
    if active_section_index is not None and 0 <= active_section_index < len(sections):
        section = sections[active_section_index]
        blocks = section.get("blocks", [])
        parts: list[str] = []
        for block in blocks:
            content = block.get("content", "")
            if isinstance(content, str):
                parts.append(content)
        return " ".join(parts)
    # Fall back to first section
    if sections:
        blocks = sections[0].get("blocks", [])
        parts = []
        for block in blocks:
            content = block.get("content", "")
            if isinstance(content, str):
                parts.append(content)
        return " ".join(parts)
    return ""


def _extract_concept(message: str) -> str:
    """Extract the likely concept from a user message.

    Strips common question prefixes to isolate the target concept.
    """
    cleaned = re.sub(
        r"^(?:can you |could you |please |help me |i (?:don'?t |can'?t )?"
        r"(?:understand|get) |explain |what (?:is|are|does) |how (?:do|does|to) |"
        r"tell me about |why (?:do|does|is) |why )",
        "",
        message.strip(),
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"[?.!]+$", "", cleaned).strip()
    return cleaned if cleaned else message.strip()


def _gather_cross_ref_terms(ctx: ConversationContext, resolved) -> list[str]:
    """Gather terms for cross-lesson registry lookup.

    Uses the active topic thread's key terms and the resolved referent.
    """
    terms: list[str] = []

    # Add resolved referent
    if resolved.referent:
        terms.append(resolved.referent)

    # Add active topic thread terms
    for thread in ctx.topic_threads:
        if thread.is_active:
            terms.extend(thread.key_terms)
            if thread.subject and thread.subject not in terms:
                terms.append(thread.subject)
            break

    return terms
