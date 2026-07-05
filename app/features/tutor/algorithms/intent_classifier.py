"""Scoring-based intent classifier for the Smart Chat Engine.

Replaces the first-match regex approach from the legacy chat engine with a
scoring system that considers:
- Base score from regex pattern match (0.0–0.6)
- Discourse bonus (+0.3) when intent aligns with current discourse state
- Thread continuity bonus (+0.1) when intent continues current topic thread
- Final score capped at 1.0

Special handling:
- quiz_pending state: messages ≤ 30 chars → quiz_answer_attempt
- Post-explanation follow-ups → deeper explanation requests
- Low confidence (<0.4 all candidates) → disambiguation or clarifying prompt
- Tied scores → prefer thread-continuing intent
"""

from __future__ import annotations

import re

from app.features.tutor.algorithms.chat_models import (
    ClassificationResult,
    ConversationContext,
    DiscourseState,
    IntentScore,
    ResolvedMessage,
)


# ---------------------------------------------------------------------------
# Intent regex patterns (base score source)
# ---------------------------------------------------------------------------

_INTENT_PATTERNS: dict[str, list[str]] = {
    "explain_section": [
        r"(?:explain|what does|what is|what are|why does|why do|tell me about|help me understand|i don'?t (?:get|understand))(?!\s+(?:more\s+)?(?:simply|simpler|easier|deeper))",
        r"(?:how does|how do)\b(?!\s+(?:this|it)\s+relate)",
        r"(?:confused about|unclear|clarify|elaborate|break down|what'?s the (?:meaning|difference))",
    ],
    "give_example": [
        r"(?:give|show|provide|another|more) (?:me )?(?:an? )?example",
        r"(?:can you|could you) (?:show|demonstrate|illustrate)",
        r"(?:sample|illustration|demonstrate|practice problem)",
    ],
    "summarize": [
        r"(?:summarize|summary|sum up|recap|overview|in short|tldr|tl;dr)",
        r"(?:main (?:points?|ideas?|concepts?)|key (?:points?|ideas?))",
    ],
    "quiz_me": [
        r"(?:quiz|test|assess|check) (?:me|my|myself)",
        r"(?:practice question|ask me|challenge me|try me)",
    ],
    "relate_to_exam": [
        r"(?:exam|cse|civil service|test|board)",
        r"(?:how (?:is|will) (?:this|it) (?:tested|asked|appear))",
        r"(?:exam (?:tip|strategy|trick)|test.taking)",
    ],
    "memory_aid": [
        r"(?:remember|memorize|mnemonic|memory (?:aid|tip|trick))",
        r"(?:how (?:do i|can i|to) remember|easy way to recall)",
    ],
    "next_step": [
        r"(?:what'?s next|what should i|where do i go|after this|move on)",
        r"(?:next (?:topic|section|lesson|step))",
    ],
    "greeting": [
        r"^(?:hi|hello|hey|good (?:morning|afternoon|evening)|sup|yo)[\s!?.]*$",
    ],
    "thanks": [
        r"(?:thanks?|thank you|thx|ty|appreciate|helpful)",
    ],
    # --- New intents ---
    "conceptual_question": [
        r"(?:why (?:is|does|do|are|can|would|should))",
        r"(?:how (?:come|is it that|can))",
        r"(?:what (?:is the (?:relationship|connection|difference)|causes|makes))",
        r"(?:what'?s the (?:relationship|connection|difference|reason))",
        r"(?:explain (?:why|how|the relationship|the connection))",
    ],
    "direct_answer_request": [
        r"(?:just (?:tell|give) me(?: the answer)?)",
        r"(?:give me the (?:answer|explanation))",
        r"(?:stop asking|don'?t ask|no more questions)",
        r"(?:i (?:just )?want the answer|tell me directly|straight answer)",
    ],
    "quiz_answer_attempt": [
        r"(?:my answer is|i think (?:it'?s|the answer is)|the answer is)",
        r"(?:is it|it'?s|i'?d say|i choose|i pick|option [a-d])",
    ],
    "complexity_adjustment": [
        r"(?:explain (?:more )?simply|too (?:complex|complicated|hard|difficult))",
        r"(?:dumb it down|simpler|easier|in simple terms|eli5)",
        r"(?:give me more detail|go deeper|more (?:depth|advanced|technical))",
        r"(?:too (?:simple|basic|easy)|more complex|elaborate more)",
    ],
    "cross_reference_request": [
        r"(?:how does (?:this|it) relate to|what'?s the connection (?:to|with|between))",
        r"(?:relate (?:this|it) to|connection (?:to|with|between))",
        r"(?:compared to|in relation to|how is (?:this|it) (?:related|connected))",
    ],
    # Off-topic: programming languages, tech, pop culture, general knowledge
    # unrelated to CSE exam subjects (verbal, numerical, analytical ability).
    "off_topic": [
        r"\b(?:python|java(?:script)?|typescript|kotlin|swift|rust|golang|c\+\+|php|ruby|html|css|react|angular|vue|django|flask|fastapi|node\.?js|sql|database|algorithm|data structure|machine learning|artificial intelligence|blockchain|cryptocurrency|bitcoin|ethereum)\b",
        r"\b(?:programming|coding|software|developer|devops|kubernetes|docker|git|github|linux|windows|macos|android|ios|smartphone)\b",
        r"\b(?:anime|manga|netflix|spotify|tiktok|facebook|instagram|twitter|youtube|twitch|gaming|esports|minecraft|roblox)\b",
        r"\b(?:recipe|cooking|baking|restaurant|food|nutrition|diet|workout|fitness|gym|sports|basketball|football|volleyball)\b",
        r"\b(?:movie|film|television|series|actor|actress|celebrity|music|band|singer|concert|album)\b",
        r"\b(?:stock market|forex|crypto|nft|investment|trading|real estate|mortgage)\b",
    ],
}

# Compiled patterns for performance
_COMPILED_INTENTS: dict[str, list[re.Pattern[str]]] = {
    intent: [re.compile(p, re.IGNORECASE) for p in patterns]
    for intent, patterns in _INTENT_PATTERNS.items()
}

# ---------------------------------------------------------------------------
# Discourse state expectations — maps discourse state to expected intents
# ---------------------------------------------------------------------------

_DISCOURSE_EXPECTED_INTENTS: dict[DiscourseState, list[str]] = {
    DiscourseState.INITIAL: ["greeting", "explain_section", "conceptual_question"],
    DiscourseState.FOLLOW_UP: [
        "explain_section",
        "conceptual_question",
        "give_example",
        "complexity_adjustment",
        "cross_reference_request",
    ],
    DiscourseState.QUIZ_PENDING: ["quiz_answer_attempt"],
    DiscourseState.SOCRATIC_EXCHANGE: [
        "direct_answer_request",
        "quiz_answer_attempt",
        "conceptual_question",
    ],
    DiscourseState.CLARIFICATION: [
        "explain_section",
        "conceptual_question",
        "direct_answer_request",
    ],
}

# Short follow-up patterns that indicate deeper explanation requests
_FOLLOW_UP_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"^why\??$", re.IGNORECASE),
    re.compile(r"^how come\??$", re.IGNORECASE),
    re.compile(r"^why is that\??$", re.IGNORECASE),
    re.compile(r"^what do you mean\??$", re.IGNORECASE),
    re.compile(r"^can you explain (?:more|further|that)\??$", re.IGNORECASE),
    re.compile(r"^what\??$", re.IGNORECASE),
    re.compile(r"^huh\??$", re.IGNORECASE),
    re.compile(r"^really\??$", re.IGNORECASE),
]

# Confidence threshold below which disambiguation is triggered
CONFIDENCE_THRESHOLD: float = 0.4

# Maximum base score from pattern match
_MAX_PATTERN_SCORE: float = 0.6

# Bonus values
_DISCOURSE_BONUS: float = 0.3
_THREAD_CONTINUITY_BONUS: float = 0.1


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


class IntentClassifier:
    """Scoring-based intent classifier with discourse and context awareness."""

    def classify(
        self,
        message: str,
        resolved_message: ResolvedMessage,
        ctx: ConversationContext,
    ) -> ClassificationResult:
        """Classify the user message into an intent using scoring.

        Args:
            message: The raw user message.
            resolved_message: Message after anaphora resolution.
            ctx: Current conversation context.

        Returns:
            ClassificationResult with detected intent, confidence, and
            disambiguation info if needed.
        """
        message_stripped = message.strip()

        # --- Special case: quiz_pending + short message ---
        if (
            ctx.discourse_state == DiscourseState.QUIZ_PENDING
            and len(message_stripped) <= 30
        ):
            return ClassificationResult(
                intent="quiz_answer_attempt",
                confidence=1.0,
                all_scores=[
                    IntentScore(
                        intent="quiz_answer_attempt",
                        score=1.0,
                        source="discourse",
                    )
                ],
                needs_disambiguation=False,
                disambiguation_options=None,
            )

        # --- Special case: post-explanation follow-up ---
        if ctx.discourse_state == DiscourseState.FOLLOW_UP:
            if self._is_follow_up_inquiry(message_stripped):
                return ClassificationResult(
                    intent="explain_section",
                    confidence=0.9,
                    all_scores=[
                        IntentScore(
                            intent="explain_section",
                            score=0.9,
                            source="discourse",
                        )
                    ],
                    needs_disambiguation=False,
                    disambiguation_options=None,
                )

        # --- General scoring ---
        scores = self._compute_scores(message_stripped, resolved_message, ctx)

        if not scores:
            # No candidates at all — open-ended clarifying prompt
            return ClassificationResult(
                intent="fallback",
                confidence=0.0,
                all_scores=[],
                needs_disambiguation=True,
                disambiguation_options=None,
            )

        # Sort by score descending
        scores.sort(key=lambda s: s.score, reverse=True)

        top_score = scores[0].score

        # --- Low confidence: all below threshold ---
        if top_score < CONFIDENCE_THRESHOLD:
            candidates_above_zero = [s for s in scores if s.score > 0.0]
            if len(candidates_above_zero) >= 2:
                # Disambiguation with top 2
                top_two = [s.intent for s in candidates_above_zero[:2]]
                return ClassificationResult(
                    intent="fallback",
                    confidence=top_score,
                    all_scores=scores,
                    needs_disambiguation=True,
                    disambiguation_options=top_two,
                )
            else:
                # Open-ended clarifying prompt
                return ClassificationResult(
                    intent="fallback",
                    confidence=top_score,
                    all_scores=scores,
                    needs_disambiguation=True,
                    disambiguation_options=None,
                )

        # --- Tie-breaking: prefer thread-continuing intent ---
        tied = [s for s in scores if s.score == top_score]
        if len(tied) > 1:
            winner = self._break_tie(tied, ctx)
        else:
            winner = scores[0]

        return ClassificationResult(
            intent=winner.intent,
            confidence=winner.score,
            all_scores=scores,
            needs_disambiguation=False,
            disambiguation_options=None,
        )

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _is_follow_up_inquiry(self, message: str) -> bool:
        """Check if message is a short follow-up inquiry."""
        for pattern in _FOLLOW_UP_PATTERNS:
            if pattern.match(message):
                return True
        return False

    def _compute_scores(
        self,
        message: str,
        resolved_message: ResolvedMessage,
        ctx: ConversationContext,
    ) -> list[IntentScore]:
        """Compute scores for all intents based on the message and context."""
        scores: list[IntentScore] = []
        # Use the resolved message text for pattern matching
        match_text = resolved_message.resolved if resolved_message.resolved else message

        for intent, patterns in _COMPILED_INTENTS.items():
            base_score = self._compute_base_score(match_text, patterns)

            if base_score <= 0.0:
                continue

            # Apply discourse bonus
            discourse_bonus = 0.0
            expected = _DISCOURSE_EXPECTED_INTENTS.get(ctx.discourse_state, [])
            if intent in expected:
                discourse_bonus = _DISCOURSE_BONUS

            # Apply thread continuity bonus
            thread_bonus = 0.0
            if self._continues_thread(intent, ctx):
                thread_bonus = _THREAD_CONTINUITY_BONUS

            # Final score capped at 1.0
            final_score = min(base_score + discourse_bonus + thread_bonus, 1.0)

            source = "pattern"
            if discourse_bonus > 0:
                source = "discourse"
            if thread_bonus > 0 and discourse_bonus == 0:
                source = "context"

            scores.append(IntentScore(intent=intent, score=final_score, source=source))

        return scores

    def _compute_base_score(
        self, message: str, patterns: list[re.Pattern[str]]
    ) -> float:
        """Compute base score from regex pattern matches.

        Returns a value between 0.0 and 0.6.
        Multiple pattern matches increase the score slightly.
        """
        match_count = 0
        for pattern in patterns:
            if pattern.search(message):
                match_count += 1

        if match_count == 0:
            return 0.0

        # First match gives 0.4, additional matches add up to 0.2 more
        # (0.1 per extra match, capped at 0.6 total)
        score = 0.4 + min((match_count - 1) * 0.1, 0.2)
        return min(score, _MAX_PATTERN_SCORE)

    def _continues_thread(self, intent: str, ctx: ConversationContext) -> bool:
        """Check if the intent would continue the current active topic thread.

        An intent continues the thread if it's a follow-up type intent and
        there is an active thread with the same broad topic category.
        """
        if not ctx.topic_threads:
            return False

        active_threads = [t for t in ctx.topic_threads if t.is_active]
        if not active_threads:
            return False

        # Intents that naturally continue a topic thread
        continuing_intents = {
            "explain_section",
            "give_example",
            "summarize",
            "conceptual_question",
            "complexity_adjustment",
            "cross_reference_request",
            "direct_answer_request",
        }

        # Intents that start new threads or are standalone
        new_thread_intents = {
            "greeting",
            "next_step",
            "quiz_me",
        }

        if intent in continuing_intents:
            return True
        if intent in new_thread_intents:
            return False

        # For other intents, check if there's an active thread
        # (conservative: don't give bonus for ambiguous cases)
        return False

    def _break_tie(
        self, tied: list[IntentScore], ctx: ConversationContext
    ) -> IntentScore:
        """Break a tie between equal-scored intents.

        Prefers the intent that continues the current active topic thread.
        If neither or both continue the thread, returns the first one.
        """
        for score in tied:
            if self._continues_thread(score.intent, ctx):
                return score

        # No thread-continuing intent found — return first
        return tied[0]
