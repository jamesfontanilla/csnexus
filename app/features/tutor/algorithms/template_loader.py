"""Template Loader for the Smart Chat Engine.

Loads response templates from external JSON files under `data/chat_templates/`,
validates template structure, and provides lookup by intent + complexity level.
Falls back to `fallback.json` when a requested intent file is missing.

Requirements: 6.1, 6.3, 6.6
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ResponseTemplate,
    TemplatePart,
)

logger = logging.getLogger(__name__)

# Minimum number of variants required for opener and closing parts
# per intent-complexity combination (Requirement 6.3).
_MIN_VARIANTS = 3

# Template parts that support multiple variants (list of strings).
_LIST_PARTS = ("opener", "closing")

# The fallback intent filename used when a requested intent file is missing.
_FALLBACK_FILENAME = "fallback.json"


class TemplateValidationError(Exception):
    """Raised when a template file fails structural validation."""


class TemplateLoader:
    """Loads and serves response templates from JSON data files.

    Templates are indexed by (intent, ComplexityLevel) and returned as
    ``ResponseTemplate`` dataclass instances.
    """

    def __init__(
        self,
        templates: dict[str, dict[ComplexityLevel, ResponseTemplate]],
    ) -> None:
        self._templates = templates

    @classmethod
    def load(cls, templates_dir: Path) -> TemplateLoader:
        """Load all template JSON files from *templates_dir*.

        Each ``.json`` file in the directory is parsed and validated.
        Files that fail validation are logged as warnings and skipped.

        Returns a fully-initialized ``TemplateLoader``.
        """
        templates: dict[str, dict[ComplexityLevel, ResponseTemplate]] = {}

        if not templates_dir.exists():
            logger.warning(
                "Templates directory does not exist: %s. "
                "No templates loaded.",
                templates_dir,
            )
            return cls(templates)

        for filepath in sorted(templates_dir.glob("*.json")):
            try:
                intent_templates = _parse_template_file(filepath)
                intent = intent_templates[ComplexityLevel.SIMPLIFIED].intent
                templates[intent] = intent_templates
            except (TemplateValidationError, json.JSONDecodeError, KeyError) as exc:
                logger.warning(
                    "Skipping invalid template file %s: %s",
                    filepath.name,
                    exc,
                )

        logger.info(
            "Loaded %d template file(s) from %s",
            len(templates),
            templates_dir,
        )
        return cls(templates)

    def get_template(
        self,
        intent: str,
        complexity: ComplexityLevel,
    ) -> ResponseTemplate:
        """Return the ``ResponseTemplate`` for the given intent and complexity.

        Falls back to the ``fallback`` intent template when the requested
        intent is not loaded, logging a warning.

        If neither the requested intent nor the fallback template is available,
        returns a minimal empty ``ResponseTemplate`` so callers never receive
        ``None``.
        """
        intent_map = self._templates.get(intent)

        if intent_map is None:
            logger.warning(
                "No template loaded for intent '%s'; falling back to 'fallback'.",
                intent,
            )
            intent_map = self._templates.get("fallback")

        if intent_map is None:
            # Neither requested intent nor fallback available — return minimal.
            logger.warning(
                "Fallback template also unavailable. "
                "Returning empty template for intent '%s'.",
                intent,
            )
            return ResponseTemplate(intent=intent, complexity=complexity, parts={})

        template = intent_map.get(complexity)
        if template is None:
            # Complexity level not in file — try STANDARD as a safe default.
            template = intent_map.get(ComplexityLevel.STANDARD)

        if template is None:
            # Pick any available complexity as last resort.
            template = next(iter(intent_map.values()), None)

        if template is None:
            return ResponseTemplate(intent=intent, complexity=complexity, parts={})

        return template


def _parse_template_file(
    filepath: Path,
) -> dict[ComplexityLevel, ResponseTemplate]:
    """Parse and validate a single template JSON file.

    Expected structure matches the design doc:
    ```json
    {
      "intent": "explain_section",
      "variants": {
        "SIMPLIFIED": { "opener": [...], "core": "...", "closing": [...] },
        "STANDARD": { ... },
        "DETAILED": { ... }
      }
    }
    ```

    Raises ``TemplateValidationError`` on structural issues.
    """
    with open(filepath, encoding="utf-8") as fh:
        data = json.load(fh)

    if not isinstance(data, dict):
        raise TemplateValidationError(
            f"Root must be a JSON object, got {type(data).__name__}"
        )

    intent = data.get("intent")
    if not intent or not isinstance(intent, str):
        raise TemplateValidationError("Missing or invalid 'intent' field")

    variants = data.get("variants")
    if not isinstance(variants, dict):
        raise TemplateValidationError("Missing or invalid 'variants' field")

    result: dict[ComplexityLevel, ResponseTemplate] = {}

    for level in ComplexityLevel:
        level_data = variants.get(level.value)
        if level_data is None:
            raise TemplateValidationError(
                f"Missing complexity level '{level.value}' in variants"
            )

        if not isinstance(level_data, dict):
            raise TemplateValidationError(
                f"Variant for '{level.value}' must be an object"
            )

        parts: dict[str, TemplatePart] = {}

        for key, value in level_data.items():
            if isinstance(value, list):
                # Validate minimum variants for opener/closing
                if key in _LIST_PARTS and len(value) < _MIN_VARIANTS:
                    raise TemplateValidationError(
                        f"'{key}' in {level.value} has {len(value)} variant(s), "
                        f"need at least {_MIN_VARIANTS}"
                    )
                parts[key] = TemplatePart(key=key, variants=value)
            elif isinstance(value, str):
                # Single-string parts (e.g., "core", "cross_reference") are
                # stored as a single-element variant list for uniform access.
                parts[key] = TemplatePart(key=key, variants=[value])
            else:
                raise TemplateValidationError(
                    f"Part '{key}' in {level.value} must be a string or list, "
                    f"got {type(value).__name__}"
                )

        result[level] = ResponseTemplate(
            intent=intent,
            complexity=level,
            parts=parts,
        )

    return result
