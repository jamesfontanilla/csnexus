"""Smoke checks for the FastAPI app startup helpers."""

from __future__ import annotations


def test_startup_schema_helpers_are_defined() -> None:
    """Keep the startup schema patch helpers from disappearing silently."""
    from app import main as app_main

    assert callable(app_main._ensure_auth_session_schema)
    assert callable(app_main._ensure_question_difficulty_schema)
    assert callable(app_main._ensure_milestone_enrichment_schema)
