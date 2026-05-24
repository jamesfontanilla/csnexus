"""Rule-based lesson chat engine for the pseudo-AI chatbot.

Provides contextual, conversational responses about the lesson the student
is currently reading. No external LLM API calls — all responses are
assembled from the lesson's own content_json using intent classification
and template-based generation.

Intent classification uses keyword matching against a fixed set of intents.
Each intent handler extracts relevant content from the lesson and formats
it into a helpful, conversational response.
"""

from __future__ import annotations

import random
import re
from typing import Any


# ---------------------------------------------------------------------------
# Intent definitions
# ---------------------------------------------------------------------------

_INTENT_PATTERNS: dict[str, list[str]] = {
    "explain_section": [
        r"(?:explain|what does|what is|what are|how does|how do|why does|why do|tell me about|help me understand|i don'?t (?:get|understand))",
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
}

# Compiled patterns for performance
_COMPILED_INTENTS: dict[str, list[re.Pattern[str]]] = {
    intent: [re.compile(p, re.IGNORECASE) for p in patterns]
    for intent, patterns in _INTENT_PATTERNS.items()
}


def classify_intent(message: str) -> str:
    """Classify user message into one of the known intents.

    Returns the intent key, or 'fallback' if no pattern matches.
    """
    message = message.strip()

    for intent, patterns in _COMPILED_INTENTS.items():
        for pattern in patterns:
            if pattern.search(message):
                return intent

    return "fallback"


# ---------------------------------------------------------------------------
# Content extraction helpers
# ---------------------------------------------------------------------------


def _get_section_by_index(content: dict[str, Any], index: int) -> dict[str, Any] | None:
    """Get a section from the enhanced sections list by index."""
    sections = content.get("sections") or []
    if 0 <= index < len(sections):
        return sections[index]
    return None


def _get_section_text(section: dict[str, Any]) -> str:
    """Extract plain text from a section's blocks."""
    blocks = section.get("blocks", [])
    parts: list[str] = []
    for block in blocks:
        content = block.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, dict):
            # Table data — summarize
            headers = content.get("headers", [])
            if headers:
                parts.append(f"Table: {', '.join(headers)}")
    return "\n\n".join(parts)


def _find_section_by_keyword(content: dict[str, Any], keyword: str) -> dict[str, Any] | None:
    """Find the section whose title or content best matches a keyword."""
    sections = content.get("sections") or []
    keyword_lower = keyword.lower()

    # First pass: title match
    for section in sections:
        if keyword_lower in section.get("title", "").lower():
            return section

    # Second pass: content match
    for section in sections:
        text = _get_section_text(section).lower()
        if keyword_lower in text:
            return section

    return None


def _extract_keyword_from_message(message: str) -> str:
    """Extract the likely topic keyword from a user message.

    Strips common question prefixes to isolate what the user is asking about.
    """
    # Remove common question starters
    cleaned = re.sub(
        r"^(?:can you |could you |please |help me |i (?:don'?t |can'?t )?"
        r"(?:understand|get) |explain |what (?:is|are|does) |how (?:do|does|to) |"
        r"tell me about |why (?:do|does|is) )",
        "",
        message.strip(),
        flags=re.IGNORECASE,
    )
    # Remove trailing punctuation
    cleaned = re.sub(r"[?.!]+$", "", cleaned).strip()
    return cleaned if cleaned else message.strip()


def _get_practice_problems(content: dict[str, Any]) -> list[dict[str, Any]]:
    """Get practice problems from the lesson content."""
    return content.get("practice_problems") or []


def _get_exam_strategies(content: dict[str, Any]) -> list[str]:
    """Get exam strategies from the lesson content."""
    return content.get("exam_strategies") or []


def _get_memory_aids(content: dict[str, Any]) -> list[str]:
    """Get memory aids from the lesson content."""
    return content.get("memory_aids") or []


def _get_key_takeaways(content: dict[str, Any]) -> list[str]:
    """Get key takeaways from the lesson content."""
    return content.get("key_takeaways") or []


def _get_lesson_title(content: dict[str, Any]) -> str:
    """Get the lesson title from metadata."""
    metadata = content.get("metadata") or {}
    return metadata.get("title", "this topic")


def _get_all_sections(content: dict[str, Any]) -> list[dict[str, Any]]:
    """Get all sections from the lesson."""
    return content.get("sections") or []


# ---------------------------------------------------------------------------
# Response generators per intent
# ---------------------------------------------------------------------------


def _respond_explain_section(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Generate an explanation response."""
    keyword = _extract_keyword_from_message(message)

    # Try to find a relevant section by keyword first
    section = _find_section_by_keyword(content, keyword)

    # Fall back to the active section
    if section is None and active_section_index is not None:
        section = _get_section_by_index(content, active_section_index)

    if section is None:
        # Fall back to first non-preamble section
        sections = _get_all_sections(content)
        for s in sections:
            title = s.get("title", "").lower()
            if not any(
                kw in title
                for kw in ["introduction", "why ", "learning objective", "common mistakes"]
            ):
                section = s
                break

    if section is None:
        return (
            "I couldn't find a specific section matching your question. "
            "Could you be more specific about which part of the lesson you'd like me to explain? "
            "You can mention a section title or a specific concept."
        )

    title = section.get("title", "this section")
    text = _get_section_text(section)

    # Build a simplified explanation
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    # Take the first few sentences as the core explanation
    core = ". ".join(sentences[:4]) + "." if sentences else text[:300]

    response_parts: list[str] = []
    response_parts.append(f"**{title}** — here's the key idea:\n")
    response_parts.append(core)

    # Add a tip if available
    takeaways = _get_key_takeaways(content)
    if takeaways:
        relevant = [t for t in takeaways if keyword.lower() in t.lower()]
        if relevant:
            response_parts.append(f"\n\n💡 **Key point:** {relevant[0]}")
        elif len(takeaways) > 0:
            response_parts.append(f"\n\n💡 **Remember:** {random.choice(takeaways)}")

    return "\n".join(response_parts)


def _respond_give_example(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Provide an example from the lesson content."""
    problems = _get_practice_problems(content)

    if problems:
        # Pick a random problem (avoid repeating if possible)
        used_numbers = set()
        for msg in history:
            if msg.get("role") == "assistant":
                # Extract problem numbers mentioned in previous responses
                nums = re.findall(r"#(\d+)", msg.get("content", ""))
                used_numbers.update(int(n) for n in nums)

        available = [p for p in problems if p.get("number") not in used_numbers]
        if not available:
            available = problems

        problem = random.choice(available)
        parts: list[str] = []
        parts.append("Here's a practice example:\n")
        parts.append(f"**Problem #{problem.get('number', '?')}:** {problem.get('question', '')}\n")
        parts.append("Try to solve it, then ask me to reveal the answer when you're ready!")
        return "\n".join(parts)

    # Fall back to worked examples from explanations
    sections = _get_all_sections(content)
    for section in sections:
        for block in section.get("blocks", []):
            if block.get("type") in ("example", "step_by_step"):
                content_text = block.get("content", "")
                if isinstance(content_text, str) and content_text:
                    return f"Here's an example from the lesson:\n\n{content_text}"

    return (
        "This lesson doesn't have standalone practice examples in this section. "
        "Try asking me to explain a specific concept, and I'll walk you through it step by step!"
    )


def _respond_summarize(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Summarize the lesson or current section."""
    # If asking about a specific section, summarize that
    if active_section_index is not None:
        section = _get_section_by_index(content, active_section_index)
        if section:
            title = section.get("title", "this section")
            text = _get_section_text(section)
            sentences = [s.strip() for s in text.split(".") if s.strip()]
            summary = ". ".join(sentences[:3]) + "." if sentences else text[:200]
            return f"**Quick summary of {title}:**\n\n{summary}"

    # Otherwise, use the lesson's built-in summary
    summary = content.get("summary", "")
    if summary:
        return f"**Lesson Summary:**\n\n{summary}"

    # Fall back to key takeaways
    takeaways = _get_key_takeaways(content)
    if takeaways:
        parts = ["**Key points from this lesson:**\n"]
        for i, t in enumerate(takeaways[:5], 1):
            parts.append(f"{i}. {t}")
        return "\n".join(parts)

    return "I don't have a summary available for this lesson. Try asking about a specific section!"


def _respond_quiz_me(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Serve a practice question from the lesson."""
    problems = _get_practice_problems(content)

    if not problems:
        # Generate a simple recall question from key takeaways
        takeaways = _get_key_takeaways(content)
        if takeaways:
            takeaway = random.choice(takeaways)
            return (
                "**Quick check:** Can you explain this concept in your own words?\n\n"
                f"*\"{takeaway}\"*\n\n"
                "Try to rephrase it without looking at the lesson. "
                "When you're done, I'll let you know if you've got the right idea!"
            )
        return "This lesson doesn't have practice problems yet. Try reviewing the key takeaways instead!"

    # Pick a problem not yet used in this conversation
    used_numbers = set()
    for msg in history:
        if msg.get("role") == "assistant" and "Problem #" in msg.get("content", ""):
            nums = re.findall(r"Problem #(\d+)", msg.get("content", ""))
            used_numbers.update(int(n) for n in nums)

    available = [p for p in problems if p.get("number") not in used_numbers]
    if not available:
        available = problems

    problem = random.choice(available)
    difficulty = problem.get("difficulty", "medium")
    emoji = {"easy": "🟢", "medium": "🟡", "hard": "🔴"}.get(difficulty, "🟡")

    parts: list[str] = []
    parts.append(f"{emoji} **Problem #{problem.get('number', '?')}** ({difficulty}):\n")
    parts.append(f"{problem.get('question', '')}\n")
    parts.append("Take your time! When you're ready, say **\"show answer\"** or tell me your answer.")
    return "\n".join(parts)


def _respond_relate_to_exam(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Explain how this topic appears in the CSE."""
    strategies = _get_exam_strategies(content)
    title = _get_lesson_title(content)

    parts: list[str] = []
    parts.append(f"**How \"{title}\" appears in the Civil Service Exam:**\n")

    if strategies:
        for i, strategy in enumerate(strategies[:4], 1):
            parts.append(f"{i}. {strategy}")
    else:
        parts.append(
            "This topic is commonly tested through multiple-choice questions "
            "that require you to apply the concepts directly. Focus on understanding "
            "the rules and practicing with timed conditions."
        )

    # Add memory aids if available
    aids = _get_memory_aids(content)
    if aids:
        parts.append(f"\n🧠 **Quick memory tip:** {random.choice(aids)}")

    return "\n".join(parts)


def _respond_memory_aid(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Provide memory aids and mnemonics."""
    aids = _get_memory_aids(content)
    title = _get_lesson_title(content)

    if aids:
        parts: list[str] = []
        parts.append(f"**Memory aids for {title}:**\n")
        for aid in aids:
            parts.append(f"🧠 {aid}")
        return "\n".join(parts)

    # Fall back to key takeaways formatted as memory points
    takeaways = _get_key_takeaways(content)
    if takeaways:
        parts = [f"**Key things to remember about {title}:**\n"]
        for i, t in enumerate(takeaways[:4], 1):
            parts.append(f"📌 {t}")
        parts.append(
            "\n*Tip: Try creating your own mnemonic by taking the first letter "
            "of each key point!*"
        )
        return "\n".join(parts)

    return (
        "I don't have specific memory aids for this lesson, but here's a general tip: "
        "try teaching the concept to someone else (or even to yourself out loud). "
        "If you can explain it simply, you understand it!"
    )


def _respond_next_step(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Suggest what to do next."""
    sections = _get_all_sections(content)
    problems = _get_practice_problems(content)
    title = _get_lesson_title(content)

    parts: list[str] = []
    parts.append("**Suggested next steps:**\n")

    if active_section_index is not None and active_section_index < len(sections) - 1:
        next_section = sections[active_section_index + 1]
        parts.append(f"1. 📖 Continue to the next section: **{next_section.get('title', 'Next')}**")
    else:
        parts.append("1. ✅ You've reached the end of the lesson content!")

    if problems:
        parts.append(f"2. 🎯 Try the practice problems ({len(problems)} available) — say \"quiz me\"")

    parts.append("3. 📝 Review the key takeaways to solidify your understanding")
    parts.append("4. 🔄 Mark the lesson complete and move to the next subtopic")

    return "\n".join(parts)


def _respond_greeting(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Respond to a greeting."""
    title = _get_lesson_title(content)
    greetings = [
        f"Hey! 👋 I'm here to help you with **{title}**. What would you like to know?",
        f"Hi there! Ready to dive into **{title}**? Ask me anything about what you're reading.",
        f"Hello! I'm your study buddy for **{title}**. Feel free to ask questions, request examples, or say \"quiz me\" to test yourself!",
    ]
    return random.choice(greetings)


def _respond_thanks(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Respond to thanks."""
    responses = [
        "You're welcome! Let me know if you have more questions. 📚",
        "Happy to help! Keep going — you're doing great. 💪",
        "Anytime! Feel free to ask more questions or say \"quiz me\" when you're ready to test yourself.",
        "No problem! Remember, understanding beats memorizing. Ask away if anything else is unclear.",
    ]
    return random.choice(responses)


def _respond_reveal_answer(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Reveal the answer to the last quiz question asked."""
    # Find the last problem number mentioned in assistant messages
    for msg in reversed(history):
        if msg.get("role") == "assistant":
            nums = re.findall(r"Problem #(\d+)", msg.get("content", ""))
            if nums:
                problem_num = int(nums[-1])
                problems = _get_practice_problems(content)
                for p in problems:
                    if p.get("number") == problem_num:
                        parts: list[str] = []
                        parts.append(f"**Answer to Problem #{problem_num}:**\n")
                        parts.append(f"✅ **{p.get('answer', 'N/A')}**\n")
                        if p.get("explanation"):
                            parts.append(f"**Why:** {p['explanation']}")
                        parts.append("\nWant another question? Say \"quiz me\" or ask about something else!")
                        return "\n".join(parts)

    return "I don't see a pending question to reveal. Say \"quiz me\" and I'll give you a fresh problem!"


def _respond_fallback(
    content: dict[str, Any],
    message: str,
    active_section_index: int | None,
    history: list[dict[str, str]],
) -> str:
    """Handle unrecognized messages with a helpful fallback."""
    title = _get_lesson_title(content)

    # Check if they might be answering a quiz question
    if _has_pending_quiz(history):
        return (
            "Hmm, I'm not sure if that's the right answer. "
            "Say **\"show answer\"** to see the correct answer, or try again!"
        )

    suggestions = [
        f"I'm not sure I understood that. Here's what I can help with for **{title}**:\n\n"
        "• **\"Explain [concept]\"** — I'll break down a specific part\n"
        "• **\"Give me an example\"** — I'll show a practice problem\n"
        "• **\"Summarize\"** — Quick recap of the current section\n"
        "• **\"Quiz me\"** — Test your understanding\n"
        "• **\"How is this tested?\"** — CSE exam tips\n"
        "• **\"Help me remember\"** — Memory aids and mnemonics",
    ]
    return suggestions[0]


def _has_pending_quiz(history: list[dict[str, str]]) -> bool:
    """Check if the last assistant message was a quiz question."""
    for msg in reversed(history):
        if msg.get("role") == "assistant":
            content = msg.get("content", "")
            return "Problem #" in content and "show answer" in content.lower()
    return False


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

_INTENT_HANDLERS = {
    "explain_section": _respond_explain_section,
    "give_example": _respond_give_example,
    "summarize": _respond_summarize,
    "quiz_me": _respond_quiz_me,
    "relate_to_exam": _respond_relate_to_exam,
    "memory_aid": _respond_memory_aid,
    "next_step": _respond_next_step,
    "greeting": _respond_greeting,
    "thanks": _respond_thanks,
    "fallback": _respond_fallback,
}


def generate_chat_response(
    *,
    content_json: dict[str, Any],
    message: str,
    active_section_index: int | None = None,
    history: list[dict[str, str]] | None = None,
) -> tuple[str, str]:
    """Generate a contextual chat response for a lesson.

    Args:
        content_json: The lesson's full content_json dict.
        message: The user's chat message.
        active_section_index: Index of the section the user is currently viewing.
        history: List of previous messages [{"role": "user"|"assistant", "content": "..."}].

    Returns:
        A tuple of (response_text, detected_intent).
    """
    if history is None:
        history = []

    message_stripped = message.strip()

    # Special case: "show answer" / "reveal answer" — check before intent classification
    if re.search(r"(?:show|reveal|tell me|what'?s) (?:the )?answer", message_stripped, re.IGNORECASE):
        response = _respond_reveal_answer(content_json, message_stripped, active_section_index, history)
        return response, "reveal_answer"

    intent = classify_intent(message_stripped)
    handler = _INTENT_HANDLERS.get(intent, _respond_fallback)
    response = handler(content_json, message_stripped, active_section_index, history)

    return response, intent
