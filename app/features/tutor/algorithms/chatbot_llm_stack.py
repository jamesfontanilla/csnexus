"""Five-step LLM fallback stack for lesson-chat responses.

The stack keeps the existing lesson-grounded tutor engine in control of the
facts and uses external providers only as a polish layer. If every provider
fails or is unavailable, the caller can keep the local draft response.
"""

from __future__ import annotations

import json
import logging
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from app.features.tutor.algorithms.chat_models import ConversationContext

logger = logging.getLogger(__name__)

_GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
_GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

_DEFAULT_GEMINI_PRIMARY_MODEL = "gemini-3.5-flash"
_DEFAULT_GEMINI_FALLBACK_MODEL = "gemini-3.1-flash-lite"
_DEFAULT_GROQ_MODELS = (
    "qwen/qwen3-32b",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
)


class ChatProvider(ABC):
    """Common interface for a chat-completion provider."""

    provider_name: str
    model_name: str

    @abstractmethod
    def is_available(self) -> bool:
        """Return True when the provider has enough configuration to run."""

    @abstractmethod
    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        """Generate a single polished response string."""


@dataclass(slots=True)
class GeminiChatProvider(ChatProvider):
    """Google Gemini REST adapter."""

    model_name: str
    api_key: str | None = None
    timeout_seconds: float = 12.0

    provider_name: str = "gemini"

    def _resolve_api_key(self) -> str | None:
        return self.api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get(
            "GOOGLE_API_KEY"
        )

    def is_available(self) -> bool:
        return bool(self._resolve_api_key())

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        api_key = self._resolve_api_key()
        if not api_key:
            raise RuntimeError("Gemini API key is not configured")

        payload: dict[str, Any] = {
            "system_instruction": {
                "parts": [{"text": system_prompt}],
            },
            "contents": [
                {
                    "parts": [{"text": user_prompt}],
                }
            ],
            "generationConfig": {
                "temperature": 0.35,
                "maxOutputTokens": 500,
            },
        }
        url = _GEMINI_ENDPOINT.format(model=self.model_name)
        data = _post_json(
            url,
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": api_key,
            },
            payload=payload,
            timeout_seconds=self.timeout_seconds,
        )
        text = _extract_gemini_text(data)
        if not text:
            raise ValueError("Gemini response did not include text")
        return _normalize_response_text(text)


@dataclass(slots=True)
class GroqChatProvider(ChatProvider):
    """Groq OpenAI-compatible chat completion adapter."""

    model_name: str
    api_key: str | None = None
    timeout_seconds: float = 12.0

    provider_name: str = "groq"

    def _resolve_api_key(self) -> str | None:
        return self.api_key or os.environ.get("GROQ_API_KEY")

    def is_available(self) -> bool:
        return bool(self._resolve_api_key())

    def generate(self, *, system_prompt: str, user_prompt: str) -> str:
        api_key = self._resolve_api_key()
        if not api_key:
            raise RuntimeError("Groq API key is not configured")

        payload: dict[str, Any] = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.35,
            "max_tokens": 500,
        }
        data = _post_json(
            _GROQ_ENDPOINT,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            payload=payload,
            timeout_seconds=self.timeout_seconds,
        )
        text = _extract_groq_text(data)
        if not text:
            raise ValueError("Groq response did not include text")
        return _normalize_response_text(text)


@dataclass(slots=True)
class TutorChatFallbackStack:
    """Try a fixed provider order until one returns a usable answer."""

    providers: list[ChatProvider]

    @classmethod
    def from_environment(cls) -> TutorChatFallbackStack:
        return cls(
            providers=[
                GeminiChatProvider(model_name=_DEFAULT_GEMINI_PRIMARY_MODEL),
                GeminiChatProvider(model_name=_DEFAULT_GEMINI_FALLBACK_MODEL),
                GroqChatProvider(model_name=_DEFAULT_GROQ_MODELS[0]),
                GroqChatProvider(model_name=_DEFAULT_GROQ_MODELS[1]),
                GroqChatProvider(model_name=_DEFAULT_GROQ_MODELS[2]),
            ]
        )

    def polish_response(
        self,
        *,
        content_json: dict[str, Any],
        context: ConversationContext,
        message: str,
        detected_intent: str,
        draft_response: str,
        active_section_index: int | None = None,
    ) -> str | None:
        """Ask providers to polish the grounded draft response.

        The local engine remains the source of truth for facts. The provider
        stack only rewrites the draft in a more natural tutor voice.
        """
        if not draft_response.strip():
            return None

        system_prompt = (
            "You are CSNexus Tutor, a concise and supportive study assistant. "
            "Rewrite the draft response so it sounds natural and polished, "
            "but preserve the meaning, facts, numbers, and intent exactly. "
            "Do not add new facts. Do not mention policies or internal steps. "
            "Return only the final message text."
        )
        user_prompt = json.dumps(
            _build_prompt_payload(
                content_json=content_json,
                context=context,
                message=message,
                detected_intent=detected_intent,
                draft_response=draft_response,
                active_section_index=active_section_index,
            ),
            ensure_ascii=False,
            separators=(",", ":"),
        )

        for provider in self.providers:
            if not provider.is_available():
                continue
            try:
                response = provider.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning(
                    "Tutor chat provider failed provider=%s model=%s error=%s",
                    provider.provider_name,
                    provider.model_name,
                    exc,
                )
                continue

            if response:
                return response

        return None


def _build_prompt_payload(
    *,
    content_json: dict[str, Any],
    context: ConversationContext,
    message: str,
    detected_intent: str,
    draft_response: str,
    active_section_index: int | None,
) -> dict[str, Any]:
    lesson_title = _resolve_lesson_title(content_json)
    section_title, section_text = _resolve_section_snapshot(
        content_json, active_section_index
    )

    payload: dict[str, Any] = {
        "lesson_title": lesson_title,
        "subtopic_title": content_json.get("subtopic_title")
        or content_json.get("metadata", {}).get("title"),
        "section_title": section_title,
        "section_text": _truncate(section_text, 1200),
        "key_takeaways": _coerce_text_list(content_json.get("key_takeaways"), 5),
        "recent_exchanges": _summarize_exchanges(context),
        "active_topic": _resolve_active_topic(context),
        "message": _truncate(message, 400),
        "detected_intent": detected_intent,
        "draft_response": _truncate(draft_response, 1200),
        "response_rules": [
            "Preserve the meaning of the draft.",
            "Do not add new facts.",
            "Keep the tone warm, grounded, and helpful.",
            "Keep questions as questions.",
            "Keep the response concise.",
        ],
    }
    return payload


def _resolve_lesson_title(content_json: dict[str, Any]) -> str:
    metadata = content_json.get("metadata") or {}
    title = metadata.get("title") or content_json.get("title")
    if isinstance(title, str) and title.strip():
        return title.strip()
    return "this lesson"


def _resolve_section_snapshot(
    content_json: dict[str, Any], active_section_index: int | None
) -> tuple[str, str]:
    sections = content_json.get("sections") or []
    if not sections:
        return "", ""

    index = active_section_index
    if index is None or not (0 <= index < len(sections)):
        index = 0

    section = sections[index] or {}
    section_title = (
        section.get("title")
        or section.get("heading")
        or section.get("section_title")
        or ""
    )
    section_text = _extract_section_text(section)
    return str(section_title), section_text


def _extract_section_text(section: dict[str, Any]) -> str:
    blocks = section.get("blocks") or []
    if not isinstance(blocks, list):
        return ""

    parts: list[str] = []
    for block in blocks:
        if not isinstance(block, dict):
            continue
        content = block.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, dict):
            headers = content.get("headers", [])
            if isinstance(headers, list) and headers:
                parts.append(", ".join(str(header) for header in headers))
    return " ".join(parts)


def _summarize_exchanges(context: ConversationContext) -> list[dict[str, str]]:
    recent = context.exchanges[-3:]
    summary: list[dict[str, str]] = []
    for exchange in recent:
        summary.append(
            {
                "user": _truncate(exchange.user_message, 200),
                "assistant": _truncate(exchange.assistant_response, 240),
                "intent": exchange.intent,
            }
        )
    return summary


def _resolve_active_topic(context: ConversationContext) -> dict[str, Any] | None:
    for thread in context.topic_threads:
        if thread.is_active:
            return {
                "subject": thread.subject,
                "key_terms": thread.key_terms[:5],
                "start_exchange_index": thread.start_exchange_index,
            }
    return None


def _coerce_text_list(value: Any, limit: int) -> list[str]:
    if not isinstance(value, list):
        return []
    result: list[str] = []
    for item in value[:limit]:
        if isinstance(item, str) and item.strip():
            result.append(item.strip())
    return result


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1] + "..."


def _extract_gemini_text(data: dict[str, Any]) -> str | None:
    candidates = data.get("candidates") or []
    if not isinstance(candidates, list) or not candidates:
        return None
    first = candidates[0]
    if not isinstance(first, dict):
        return None
    content = first.get("content") or {}
    if not isinstance(content, dict):
        return None
    parts = content.get("parts") or []
    if not isinstance(parts, list):
        return None

    chunks: list[str] = []
    for part in parts:
        if isinstance(part, dict):
            text = part.get("text")
            if isinstance(text, str) and text.strip():
                chunks.append(text.strip())
    if not chunks:
        return None
    return "\n".join(chunks)


def _extract_groq_text(data: dict[str, Any]) -> str | None:
    choices = data.get("choices") or []
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    if not isinstance(first, dict):
        return None
    message = first.get("message") or {}
    if not isinstance(message, dict):
        return None
    text = message.get("content")
    if isinstance(text, str) and text.strip():
        return text.strip()
    return None


def _normalize_response_text(text: str) -> str:
    cleaned = text.strip()
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def _post_json(
    url: str,
    *,
    headers: dict[str, str],
    payload: dict[str, Any],
    timeout_seconds: float,
) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib_request.Request(
        url,
        data=body,
        headers=headers,
        method="POST",
    )
    try:
        with urllib_request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"HTTP {exc.code} from provider endpoint: {detail[:200]}"
        ) from exc
    except urllib_error.URLError as exc:
        raise RuntimeError(f"Provider request failed: {exc.reason}") from exc

    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("Provider response was not a JSON object")
    return data
