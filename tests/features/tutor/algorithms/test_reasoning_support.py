"""Tests for structured tutor reasoning helpers."""

from __future__ import annotations

from app.features.tutor.algorithms.reasoning_support import (
    ReasoningMode,
    build_reasoning_packet,
    classify_reasoning_mode,
    render_reasoning_brief,
    solve_math_expression,
)


def test_solve_math_expression_linear_equation() -> None:
    solution = solve_math_expression("2x + 4 = 10")

    assert solution is not None
    assert solution.answer == "3"
    assert any("x = 3" in step for step in solution.steps)


def test_classify_reasoning_mode_prefers_graph_context() -> None:
    mode = classify_reasoning_mode(
        text="What does the graph show?",
        reasoning_context={
            "graph_context": {
                "graph_type": "line_graph",
                "title": "Attendance trend",
            }
        },
    )

    assert mode == ReasoningMode.GRAPH_INTERPRETATION


def test_build_reasoning_packet_includes_graph_summary() -> None:
    packet = build_reasoning_packet(
        text="Interpret this chart",
        reasoning_context={
            "graph_context": {
                "graph_type": "line_graph",
                "title": "Sales over time",
                "series": [
                    {
                        "name": "Sales",
                        "points": [{"x": 1, "y": 10}, {"x": 2, "y": 16}],
                    }
                ],
                "annotations": ["steady growth"],
            }
        },
    )

    assert packet is not None
    assert packet.mode == ReasoningMode.GRAPH_INTERPRETATION
    assert "Reasoning mode: GRAPH_INTERPRETATION" in packet.summary
    assert "Trend" in packet.summary
    assert "steady growth" in packet.summary


def test_render_reasoning_brief_for_math() -> None:
    packet = build_reasoning_packet(
        text="Solve 2x + 4 = 10",
        reasoning_context={"math_expression": "2x + 4 = 10"},
    )

    assert packet is not None
    brief = render_reasoning_brief(packet)

    assert "The answer is 3." in brief
    assert "step by step" in brief or "isolate the unknown" in brief
