"""Tests for the lesson-chat LLM fallback stack."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.features.tutor.algorithms.chatbot_llm_stack import TutorChatFallbackStack
from app.features.tutor.algorithms.chat_models import ConversationContext
from app.features.tutor.algorithms.lesson_chat_engine import generate_chat_response


class _FakeProvider:
    def __init__(
        self,
        *,
        provider_name: str,
        model_name: str,
        available: bool = True,
        response: str | None = None,
        exc: Exception | None = None,
    ) -> None:
        self.provider_name = provider_name
        self.model_name = model_name
        self._available = available
        self._response = response
        self._exc = exc

    def is_available(self) -> bool:
        return self._available

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        if self._exc is not None:
            raise self._exc
        assert "CSNexus Tutor" in system_prompt
        assert "draft_response" in user_prompt
        return self._response or ""


def test_stack_uses_first_successful_provider() -> None:
    stack = TutorChatFallbackStack(
        providers=[
            _FakeProvider(
                provider_name="gemini",
                model_name="gemini-3.5-flash",
                available=False,
            ),
            _FakeProvider(
                provider_name="gemini",
                model_name="gemini-3.1-flash-lite",
                exc=RuntimeError("temporary failure"),
            ),
            _FakeProvider(
                provider_name="groq",
                model_name="qwen/qwen3-32b",
                response="Polished tutor answer.",
            ),
        ]
    )

    result = stack.polish_response(
        content_json={
            "metadata": {"title": "Lesson"},
            "sections": [{"title": "Intro", "blocks": []}],
            "key_takeaways": ["Point one"],
        },
        context=ConversationContext(),
        message="Explain this.",
        detected_intent="explain_section",
        draft_response="Draft tutor answer.",
    )

    assert result == "Polished tutor answer."


def test_engine_prefers_polished_response_when_available() -> None:
    fake_stack = MagicMock()
    fake_stack.polish_response.return_value = "Polished tutor answer."

    with patch(
        "app.features.tutor.algorithms.lesson_chat_engine._chat_fallback_stack",
        fake_stack,
    ), patch(
        "app.features.tutor.algorithms.lesson_chat_engine._response_generator.generate",
        return_value="Draft tutor answer.",
    ):
        result = generate_chat_response(
            content_json={
                "metadata": {"title": "Lesson"},
                "sections": [{"title": "Intro", "blocks": []}],
                "key_takeaways": ["Point one"],
            },
            message="Explain this.",
        )

    assert result.response_text == "Polished tutor answer."
    fake_stack.polish_response.assert_called_once()


def test_engine_falls_back_to_local_draft_when_stack_unavailable() -> None:
    fake_stack = MagicMock()
    fake_stack.polish_response.return_value = None

    with patch(
        "app.features.tutor.algorithms.lesson_chat_engine._chat_fallback_stack",
        fake_stack,
    ), patch(
        "app.features.tutor.algorithms.lesson_chat_engine._response_generator.generate",
        return_value="Draft tutor answer.",
    ):
        result = generate_chat_response(
            content_json={
                "metadata": {"title": "Lesson"},
                "sections": [{"title": "Intro", "blocks": []}],
                "key_takeaways": ["Point one"],
            },
            message="Explain this.",
        )

    assert result.response_text == "Draft tutor answer."
    fake_stack.polish_response.assert_called_once()
