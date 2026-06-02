"""Unit tests for TemplateLoader.

Tests file loading, validation, fallback behavior, and get_template lookup.
Requirements: 6.1, 6.3, 6.6
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from app.features.tutor.algorithms.chat_models import (
    ComplexityLevel,
    ResponseTemplate,
    TemplatePart,
)
from app.features.tutor.algorithms.template_loader import (
    TemplateLoader,
    TemplateValidationError,
    _parse_template_file,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _make_template_data(
    intent: str = "test_intent",
    opener_count: int = 3,
    closing_count: int = 3,
) -> dict:
    """Build a valid template dict with customizable variant counts."""
    levels = {}
    for level in ("SIMPLIFIED", "STANDARD", "DETAILED"):
        levels[level] = {
            "opener": [f"Opener {i} for {level}. " for i in range(opener_count)],
            "core": "{content}",
            "cross_reference": "Related to {related_topic}. ",
            "closing": [f"Closing {i} for {level}?" for i in range(closing_count)],
        }
    return {"intent": intent, "variants": levels}


@pytest.fixture
def templates_dir(tmp_path: Path) -> Path:
    """Create a temp directory with a valid template file and a fallback."""
    data = _make_template_data("explain_section")
    (tmp_path / "explain_section.json").write_text(
        json.dumps(data), encoding="utf-8"
    )

    fallback_data = _make_template_data("fallback")
    (tmp_path / "fallback.json").write_text(
        json.dumps(fallback_data), encoding="utf-8"
    )
    return tmp_path


# ---------------------------------------------------------------------------
# TemplateLoader.load()
# ---------------------------------------------------------------------------


class TestTemplateLoaderLoad:
    def test_loads_valid_files(self, templates_dir: Path) -> None:
        loader = TemplateLoader.load(templates_dir)
        template = loader.get_template("explain_section", ComplexityLevel.STANDARD)

        assert isinstance(template, ResponseTemplate)
        assert template.intent == "explain_section"
        assert template.complexity == ComplexityLevel.STANDARD
        assert "opener" in template.parts
        assert "closing" in template.parts
        assert len(template.parts["opener"].variants) == 3
        assert len(template.parts["closing"].variants) == 3

    def test_nonexistent_directory_returns_empty_loader(self, tmp_path: Path) -> None:
        loader = TemplateLoader.load(tmp_path / "does_not_exist")
        # Should not crash, returns empty templates
        template = loader.get_template("anything", ComplexityLevel.STANDARD)
        assert template.parts == {}

    def test_skips_invalid_files_without_crashing(self, tmp_path: Path) -> None:
        # Write an invalid JSON file
        (tmp_path / "bad.json").write_text("not json", encoding="utf-8")

        # Write a valid fallback
        valid = _make_template_data("fallback")
        (tmp_path / "fallback.json").write_text(
            json.dumps(valid), encoding="utf-8"
        )

        loader = TemplateLoader.load(tmp_path)
        # Should have loaded fallback despite bad.json failing
        template = loader.get_template("fallback", ComplexityLevel.SIMPLIFIED)
        assert template.intent == "fallback"

    def test_loads_real_explain_section_template(self) -> None:
        """Integration sanity check against the actual data file."""
        real_dir = Path(__file__).resolve().parents[4] / "data" / "chat_templates"
        if not real_dir.exists():
            pytest.skip("data/chat_templates/ not found from test location")

        loader = TemplateLoader.load(real_dir)
        template = loader.get_template("explain_section", ComplexityLevel.SIMPLIFIED)
        assert template.intent == "explain_section"
        assert len(template.parts["opener"].variants) >= 3


# ---------------------------------------------------------------------------
# TemplateLoader.get_template() — fallback behavior
# ---------------------------------------------------------------------------


class TestGetTemplate:
    def test_returns_fallback_when_intent_missing(
        self, templates_dir: Path
    ) -> None:
        loader = TemplateLoader.load(templates_dir)
        template = loader.get_template("nonexistent_intent", ComplexityLevel.STANDARD)

        # Should fall back to the fallback template
        assert template.intent == "fallback"
        assert template.complexity == ComplexityLevel.STANDARD

    def test_returns_empty_template_when_fallback_also_missing(
        self, tmp_path: Path
    ) -> None:
        # Only load a non-fallback file
        data = _make_template_data("explain_section")
        (tmp_path / "explain_section.json").write_text(
            json.dumps(data), encoding="utf-8"
        )
        loader = TemplateLoader.load(tmp_path)

        template = loader.get_template("missing_intent", ComplexityLevel.DETAILED)
        assert template.parts == {}
        assert template.intent == "missing_intent"

    def test_returns_correct_complexity_level(self, templates_dir: Path) -> None:
        loader = TemplateLoader.load(templates_dir)

        for level in ComplexityLevel:
            template = loader.get_template("explain_section", level)
            assert template.complexity == level


# ---------------------------------------------------------------------------
# Template validation — _parse_template_file
# ---------------------------------------------------------------------------


class TestTemplateValidation:
    def test_rejects_missing_intent_field(self, tmp_path: Path) -> None:
        data = {"variants": {"SIMPLIFIED": {}, "STANDARD": {}, "DETAILED": {}}}
        filepath = tmp_path / "bad.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(TemplateValidationError, match="intent"):
            _parse_template_file(filepath)

    def test_rejects_missing_variants_field(self, tmp_path: Path) -> None:
        data = {"intent": "test"}
        filepath = tmp_path / "bad.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(TemplateValidationError, match="variants"):
            _parse_template_file(filepath)

    def test_rejects_missing_complexity_level(self, tmp_path: Path) -> None:
        data = {
            "intent": "test",
            "variants": {
                "SIMPLIFIED": {"opener": ["a", "b", "c"], "core": "{c}", "closing": ["x", "y", "z"]},
                "STANDARD": {"opener": ["a", "b", "c"], "core": "{c}", "closing": ["x", "y", "z"]},
                # Missing DETAILED
            },
        }
        filepath = tmp_path / "bad.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(TemplateValidationError, match="DETAILED"):
            _parse_template_file(filepath)

    def test_rejects_fewer_than_3_opener_variants(self, tmp_path: Path) -> None:
        data = _make_template_data("test", opener_count=2)
        filepath = tmp_path / "bad.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(TemplateValidationError, match="opener"):
            _parse_template_file(filepath)

    def test_rejects_fewer_than_3_closing_variants(self, tmp_path: Path) -> None:
        data = _make_template_data("test", closing_count=1)
        filepath = tmp_path / "bad.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        with pytest.raises(TemplateValidationError, match="closing"):
            _parse_template_file(filepath)

    def test_accepts_valid_template(self, tmp_path: Path) -> None:
        data = _make_template_data("valid_intent")
        filepath = tmp_path / "valid.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        result = _parse_template_file(filepath)
        assert set(result.keys()) == {
            ComplexityLevel.SIMPLIFIED,
            ComplexityLevel.STANDARD,
            ComplexityLevel.DETAILED,
        }
        for level, template in result.items():
            assert template.intent == "valid_intent"
            assert template.complexity == level

    def test_single_string_parts_stored_as_single_variant(
        self, tmp_path: Path
    ) -> None:
        data = _make_template_data("test")
        filepath = tmp_path / "test.json"
        filepath.write_text(json.dumps(data), encoding="utf-8")

        result = _parse_template_file(filepath)
        # "core" is a string in the template, stored as single-element list
        core_part = result[ComplexityLevel.STANDARD].parts["core"]
        assert core_part.variants == ["{content}"]
