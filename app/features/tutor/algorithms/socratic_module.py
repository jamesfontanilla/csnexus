"""Socratic questioning module for the Smart Chat Engine.

Conditionally generates guiding questions instead of direct answers
based on mastery level and response history, promoting deeper thinking.

Activation rules:
- Intent is ``conceptual_question``
- Mastery level is FAMILIAR or higher (score >= 0.2)
- Not already at max attempts (3)
- User hasn't explicitly requested a direct answer

Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8
"""

from __future__ import annotations

from app.features.tutor.algorithms.chat_models import (
    ConversationContext,
    MasteryLevel,
    SocraticEvaluation,
    SocraticPrompt,
    SocraticState,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_SOCRATIC_ATTEMPTS = 3

# Mastery levels at which Socratic mode activates (FAMILIAR and above).
_SOCRATIC_ELIGIBLE_LEVELS: set[MasteryLevel] = {
    MasteryLevel.FAMILIAR,
    MasteryLevel.PROFICIENT,
    MasteryLevel.ADVANCED,
    MasteryLevel.MASTERED,
}

# ---------------------------------------------------------------------------
# Guiding question templates organized by reasoning type.
# Each type has >= 3 templates. Placeholders:
#   {concept} — the target concept being explored
# ---------------------------------------------------------------------------

QUESTION_TEMPLATES: dict[str, list[str]] = {
    "definition_recall": [
        "Before I explain, can you recall what {concept} means in your own words?",
        "How would you define {concept} if someone asked you right now?",
        "What do you already know about {concept}? Try describing it briefly.",
        "If you had to explain {concept} to a classmate, what would you say?",
    ],
    "comparison": [
        "How do you think {concept} differs from what we discussed earlier?",
        "What similarities and differences can you spot between {concept} and related ideas?",
        "Can you think of something that is similar to {concept} but not quite the same?",
        "What makes {concept} unique compared to other concepts in this topic?",
    ],
    "application": [
        "Can you think of a real-world situation where {concept} would apply?",
        "How would you use {concept} to solve a practical problem?",
        "If you encountered this in an exam, how would you apply {concept}?",
        "Where in everyday life might you see {concept} in action?",
    ],
    "cause_effect": [
        "What do you think happens as a result of {concept}?",
        "Why do you think {concept} works the way it does?",
        "What would change if {concept} were different or absent?",
        "Can you trace the cause-and-effect chain involving {concept}?",
    ],
}

# Ordered list of reasoning types for round-robin selection.
REASONING_TYPES: list[str] = list(QUESTION_TEMPLATES.keys())


# ---------------------------------------------------------------------------
# Module implementation
# ---------------------------------------------------------------------------


class SocraticModule:
    """Manages Socratic questioning activation, generation, and evaluation."""

    def should_activate(
        self,
        intent: str,
        mastery_level: MasteryLevel,
        ctx: ConversationContext,
    ) -> bool:
        """Determine whether Socratic mode should activate.

        Returns True when ALL conditions are met:
        1. Intent is ``conceptual_question``
        2. Mastery level is FAMILIAR or higher
        3. Not at max attempts (3) in the current Socratic sequence
        4. User hasn't explicitly requested a direct answer (no active
           ``direct_answer_request`` intent)
        """
        if intent != "conceptual_question":
            return False

        if mastery_level not in _SOCRATIC_ELIGIBLE_LEVELS:
            return False

        # If already in a Socratic exchange and at max attempts, don't activate.
        if ctx.socratic_state.active and ctx.socratic_state.attempts >= MAX_SOCRATIC_ATTEMPTS:
            return False

        return True

    def generate_guiding_question(
        self,
        concept: str,
        section_content: str,
        reasoning_type: str,
        attempts: int = 0,
    ) -> SocraticPrompt:
        """Generate a guiding question for the given concept.

        Selects from predefined templates categorized by reasoning type.
        Uses attempt count to cycle through templates (avoiding repetition
        within a sequence).

        Args:
            concept: The target concept being explored.
            section_content: The section text (used for key term extraction).
            reasoning_type: One of definition_recall, comparison, application,
                cause_effect.
            attempts: Current attempt number (0-indexed) for template cycling.

        Returns:
            SocraticPrompt with the guiding question and key terms.
        """
        # Normalize reasoning type — fall back to definition_recall.
        if reasoning_type not in QUESTION_TEMPLATES:
            reasoning_type = "definition_recall"

        templates = QUESTION_TEMPLATES[reasoning_type]
        # Cycle through templates based on attempt count.
        template_index = attempts % len(templates)
        question = templates[template_index].format(concept=concept)

        # Extract key terms from section content for evaluation.
        key_terms = self._extract_key_terms(concept, section_content)

        return SocraticPrompt(
            question=question,
            target_concept=concept,
            key_terms=key_terms,
            reasoning_type=reasoning_type,
        )

    def evaluate_response(
        self,
        message: str,
        socratic_state: SocraticState,
    ) -> SocraticEvaluation:
        """Evaluate a learner's response to a Socratic question.

        Checks how many stored key terms appear in the response:
        - >= 2 matched key terms → understood=True
        - < 2 matched key terms → understood=False

        After MAX_SOCRATIC_ATTEMPTS consecutive fails, signals escalation
        to a direct answer.

        Args:
            message: The learner's response text.
            socratic_state: Current Socratic tracking state.

        Returns:
            SocraticEvaluation with understanding status and escalation flag.
        """
        message_lower = message.lower()
        matched_terms: list[str] = []

        for term in socratic_state.key_terms:
            if term.lower() in message_lower:
                matched_terms.append(term)

        understood = len(matched_terms) >= 2

        # Escalation: after 3 consecutive failed attempts, signal direct answer.
        # The current attempt is the one being evaluated, so we check
        # attempts (which was already incremented before calling this).
        should_escalate = (
            not understood and socratic_state.attempts >= MAX_SOCRATIC_ATTEMPTS
        )

        return SocraticEvaluation(
            understood=understood,
            matched_terms=matched_terms,
            should_escalate=should_escalate,
        )

    def select_reasoning_type(self, ctx: ConversationContext) -> str:
        """Select the next reasoning type for a Socratic sequence.

        Cycles through reasoning types to provide variety. If a Socratic
        sequence is already active, continues with the current type.
        Otherwise, picks based on attempt history.
        """
        if ctx.socratic_state.active and ctx.socratic_state.reasoning_type:
            return ctx.socratic_state.reasoning_type

        # Pick a reasoning type based on total exchanges to distribute types.
        index = len(ctx.exchanges) % len(REASONING_TYPES)
        return REASONING_TYPES[index]

    def _extract_key_terms(self, concept: str, section_content: str) -> list[str]:
        """Extract up to 3 key terms from the concept and section content.

        Strategy:
        1. Split the concept itself into individual significant words.
        2. Look for common domain-relevant terms in the section content.
        3. Return up to 3 unique terms.
        """
        terms: list[str] = []

        # Add words from the concept itself (filtering short/common words).
        concept_words = [
            w.strip().lower()
            for w in concept.split()
            if len(w.strip()) > 2
        ]
        terms.extend(concept_words)

        # Extract additional terms from section content if needed.
        if len(terms) < 3 and section_content:
            # Simple heuristic: find words that appear multiple times
            # or are capitalized (indicating domain terms).
            content_words = section_content.split()
            word_freq: dict[str, int] = {}
            for word in content_words:
                cleaned = word.strip(".,;:!?()[]\"'").lower()
                if len(cleaned) > 3 and cleaned not in terms:
                    word_freq[cleaned] = word_freq.get(cleaned, 0) + 1

            # Sort by frequency descending and pick top terms.
            frequent = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            for word, _freq in frequent:
                if word not in terms:
                    terms.append(word)
                if len(terms) >= 3:
                    break

        # Cap at 3 terms.
        return terms[:3]
