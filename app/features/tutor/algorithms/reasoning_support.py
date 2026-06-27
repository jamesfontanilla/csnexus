"""Helpers for structured math and graph reasoning.

The tutor remains grounded in authored CSNexus content, but these helpers
let it reason about math expressions and graph-backed prompts in a more
deterministic way before the response is composed.
"""

from __future__ import annotations

import ast
import math
import operator
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class ReasoningMode(str, Enum):
    """High-level reasoning mode for a tutor prompt."""

    TEXT = "TEXT"
    ARITHMETIC = "ARITHMETIC"
    ALGEBRA = "ALGEBRA"
    LOGICAL_REASONING = "LOGICAL_REASONING"
    ABSTRACT_PATTERN = "ABSTRACT_PATTERN"
    GRAPH_INTERPRETATION = "GRAPH_INTERPRETATION"
    TABLE_INTERPRETATION = "TABLE_INTERPRETATION"
    FALLBACK = "FALLBACK"


@dataclass(slots=True)
class GraphPoint:
    x: float | int | str
    y: float | int | str


@dataclass(slots=True)
class GraphSeries:
    name: str = ""
    points: list[GraphPoint] = field(default_factory=list)


@dataclass(slots=True)
class GraphContext:
    graph_type: str = ""
    title: str = ""
    x_axis_label: str = ""
    y_axis_label: str = ""
    x_axis_unit: str | None = None
    y_axis_unit: str | None = None
    legend: list[str] = field(default_factory=list)
    series: list[GraphSeries] = field(default_factory=list)
    table_rows: list[list[str]] = field(default_factory=list)
    annotations: list[str] = field(default_factory=list)
    highlighted_points: list[str] = field(default_factory=list)
    source_text: str = ""
    confidence: float = 0.0


@dataclass(slots=True)
class MathSolution:
    expression: str
    normalized_expression: str
    answer: str
    steps: list[str] = field(default_factory=list)
    confidence: float = 1.0


@dataclass(slots=True)
class ReasoningPacket:
    mode: ReasoningMode
    summary: str
    math_solution: MathSolution | None = None
    graph_context: GraphContext | None = None


_LOGICAL_KEYWORDS = (
    "logic",
    "logical",
    "pattern",
    "sequence",
    "series",
    "abstract",
    "inference",
    "reasoning",
    "analogy",
)

_GRAPH_KEYWORDS = (
    "graph",
    "chart",
    "table",
    "diagram",
    "figure",
    "axis",
    "axes",
    "trend",
    "bar chart",
    "line graph",
    "scatter",
)

_MATH_KEYWORDS = (
    "math",
    "calculate",
    "compute",
    "solve",
    "equation",
    "fraction",
    "percent",
    "percentage",
    "ratio",
    "proportion",
    "algebra",
    "arithmetic",
    "difference",
    "sum",
    "product",
    "quotient",
)

_ALLOWED_BINOPS: dict[type[ast.AST], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARYOPS: dict[type[ast.AST], Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


def classify_reasoning_mode(
    *,
    text: str,
    reasoning_context: Mapping[str, Any] | None = None,
) -> ReasoningMode:
    """Pick a tutor reasoning mode from text and optional structured context."""
    context = _normalize_context(reasoning_context)

    if context.get("graph_context"):
        graph_context = context["graph_context"]
        graph_type = str(graph_context.get("graph_type", "")).lower()
        if "table" in graph_type:
            return ReasoningMode.TABLE_INTERPRETATION
        return ReasoningMode.GRAPH_INTERPRETATION

    if context.get("math_expression"):
        return _classify_math_expression(str(context["math_expression"]))

    lowered = text.lower()
    if any(keyword in lowered for keyword in _GRAPH_KEYWORDS):
        return ReasoningMode.GRAPH_INTERPRETATION
    if any(keyword in lowered for keyword in _MATH_KEYWORDS):
        return _classify_math_expression(text)
    if any(keyword in lowered for keyword in _LOGICAL_KEYWORDS):
        return ReasoningMode.LOGICAL_REASONING

    if _looks_like_math_expression(text):
        return _classify_math_expression(text)

    return ReasoningMode.TEXT


def build_reasoning_packet(
    *,
    text: str,
    reasoning_context: Mapping[str, Any] | None = None,
) -> ReasoningPacket | None:
    """Build a compact reasoning summary for tutor responses.

    Returns None when no structured reasoning payload is available.
    """
    context = _normalize_context(reasoning_context)
    mode = classify_reasoning_mode(text=text, reasoning_context=context)

    graph_context = _parse_graph_context(context.get("graph_context"))
    math_solution = None

    if context.get("math_expression"):
        math_solution = solve_math_expression(str(context["math_expression"]))
    elif _looks_like_math_expression(text):
        math_solution = solve_math_expression(text)

    summary_parts: list[str] = [f"Reasoning mode: {mode.value}"]

    if math_solution is not None:
        summary_parts.extend(_format_math_solution(math_solution))

    if graph_context is not None:
        summary_parts.append(summarize_graph_context(graph_context))

    notes = context.get("notes")
    if isinstance(notes, str) and notes.strip():
        summary_parts.append(notes.strip())

    if len(summary_parts) == 1 and mode == ReasoningMode.TEXT:
        return None

    return ReasoningPacket(
        mode=mode,
        summary="\n".join(summary_parts),
        math_solution=math_solution,
        graph_context=graph_context,
    )


def render_reasoning_brief(packet: ReasoningPacket | None) -> str:
    """Render a concise user-facing explanation for a reasoning packet."""
    if packet is None:
        return ""

    if packet.mode == ReasoningMode.GRAPH_INTERPRETATION and packet.graph_context is not None:
        return _render_graph_brief(packet.graph_context)

    if packet.math_solution is not None:
        return _render_math_brief(packet.math_solution, packet.mode)

    return packet.summary.strip()


def solve_math_expression(expression: str) -> MathSolution | None:
    """Solve a math expression safely when it can be reduced deterministically."""
    normalized = _normalize_expression(expression)
    if not normalized:
        return None

    normalized = _expand_simple_percentages(normalized)
    normalized = _expand_simple_multiplication(normalized)

    if "=" in normalized:
        equation_solution = _solve_simple_linear_equation(normalized)
        if equation_solution is not None:
            return equation_solution

    if not _looks_like_math_expression(normalized):
        return None

    try:
        value = _safe_eval(normalized)
    except ValueError:
        return None

    return MathSolution(
        expression=expression.strip(),
        normalized_expression=normalized,
        answer=_format_number(value),
        steps=[
            f"Normalize the expression to: {normalized}",
            f"Evaluate the expression to get { _format_number(value) }.",
        ],
    )


def summarize_graph_context(graph_context: GraphContext) -> str:
    """Summarize graph data in a learner-friendly way."""
    parts: list[str] = []
    title = graph_context.title.strip() or "the graph"
    parts.append(f"Graph summary for {title}:")

    if graph_context.graph_type:
        parts.append(f"- Type: {graph_context.graph_type}")
    if graph_context.x_axis_label or graph_context.y_axis_label:
        axis = f"- Axes: x={graph_context.x_axis_label or 'unspecified'}"
        axis += f", y={graph_context.y_axis_label or 'unspecified'}"
        parts.append(axis)
    if graph_context.legend:
        parts.append(f"- Legend: {', '.join(graph_context.legend[:5])}")
    if graph_context.annotations:
        parts.append(f"- Notes: {', '.join(graph_context.annotations[:3])}")
    if graph_context.highlighted_points:
        parts.append(
            f"- Highlighted points: {', '.join(graph_context.highlighted_points[:5])}"
        )

    trend_summary = _summarize_series_trends(graph_context.series)
    if trend_summary:
        parts.append(f"- Trend: {trend_summary}")

    if graph_context.table_rows:
        row_count = len(graph_context.table_rows)
        parts.append(f"- Table rows: {row_count}")

    if graph_context.source_text:
        parts.append(f"- Source: {graph_context.source_text[:200].strip()}")

    if graph_context.confidence > 0:
        parts.append(f"- Extraction confidence: {graph_context.confidence:.2f}")

    return "\n".join(parts)


def _normalize_context(
    reasoning_context: Mapping[str, Any] | None,
) -> dict[str, Any]:
    if reasoning_context is None:
        return {}
    if hasattr(reasoning_context, "model_dump"):
        return reasoning_context.model_dump()  # type: ignore[no-any-return]
    return dict(reasoning_context)


def _classify_math_expression(text: str) -> ReasoningMode:
    lowered = text.lower()
    if any(keyword in lowered for keyword in ("algebra", "equation", "solve for", "x =")):
        return ReasoningMode.ALGEBRA
    if any(keyword in lowered for keyword in ("ratio", "proportion", "percent", "%")):
        return ReasoningMode.ARITHMETIC
    if _looks_like_math_expression(text):
        return ReasoningMode.ARITHMETIC
    return ReasoningMode.FALLBACK


def _looks_like_math_expression(text: str) -> bool:
    return bool(re.search(r"[0-9][0-9\s\.\+\-\*/\^\(\)%=x×÷]", text))


def _normalize_expression(expression: str) -> str:
    expr = expression.strip()
    expr = expr.replace("×", "*").replace("÷", "/").replace("^", "**")
    expr = re.sub(r"\s+", "", expr)
    return expr


def _expand_simple_percentages(expression: str) -> str:
    expression = re.sub(
        r"(\d+(?:\.\d+)?)%\s*of\s*(\d+(?:\.\d+)?)",
        lambda m: f"({m.group(1)}/100)*({m.group(2)})",
        expression,
        flags=re.IGNORECASE,
    )
    return re.sub(r"(\d+(?:\.\d+)?)%", lambda m: f"({m.group(1)}/100)", expression)


def _expand_simple_multiplication(expression: str) -> str:
    """Expand common implicit multiplication patterns like 2x -> 2*x."""
    return re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expression)


def _safe_eval(expression: str) -> float:
    tree = ast.parse(expression, mode="eval")
    return float(_eval_node(tree.body))


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.Num):  # pragma: no cover - Py<=3.7 compatibility
        return float(node.n)
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return float(_ALLOWED_BINOPS[type(node.op)](left, right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARYOPS:
        operand = _eval_node(node.operand)
        return float(_ALLOWED_UNARYOPS[type(node.op)](operand))
    raise ValueError(f"Unsupported expression node: {type(node).__name__}")


def _solve_simple_linear_equation(expression: str) -> MathSolution | None:
    """Solve a very small set of single-variable linear equations."""
    left, right = expression.split("=", 1)
    variable = _find_single_variable(left + right)
    if variable is None:
        return None

    # Supported forms are intentionally narrow and deterministic.
    patterns = [
        rf"^\s*(?P<a>[-+]?\d*(?:\.\d+)?)\*?{variable}\s*(?P<op>[+-])\s*(?P<b>\d+(?:\.\d+)?)\s*$",
        rf"^\s*(?P<a>[-+]?\d*(?:\.\d+)?)\*?{variable}\s*/\s*(?P<b>\d+(?:\.\d+)?)\s*$",
        rf"^\s*{variable}\s*(?P<op>[+-])\s*(?P<b>\d+(?:\.\d+)?)\s*$",
        rf"^\s*(?P<a>[-+]?\d*(?:\.\d+)?)\*?{variable}\s*$",
    ]

    # Normalize "2x" to "2*x" so the equation patterns can read coefficients.
    normalized_left = _expand_simple_multiplication(left)
    normalized_right = _expand_simple_multiplication(right)

    for pattern in patterns:
        match = re.match(pattern, normalized_left)
        if not match:
            continue

        groups = match.groupdict()
        a_raw = groups.get("a", "")
        op = groups.get("op")
        b_raw = groups.get("b")
        coefficient = float(a_raw) if a_raw not in {"", "+", "-"} else 1.0
        if a_raw == "-":
            coefficient = -1.0
        if a_raw == "+":
            coefficient = 1.0
        if coefficient == 0:
            coefficient = 1.0

        rhs_value = _safe_eval(normalized_right)

        if pattern.endswith(rf"^\s*(?P<a>[-+]?\d*(?:\.\d+)?)\*?{variable}\s*$"):
            steps = [
                f"Normalize the equation: {normalized_left} = {normalized_right}",
                f"Divide both sides by {coefficient:g} to isolate {variable}.",
            ]
            answer = rhs_value / coefficient
            steps.append(f"{variable} = {_format_number(answer)}")
            return MathSolution(
                expression=f"{left}={right}",
                normalized_expression=f"{normalized_left}={normalized_right}",
                answer=_format_number(answer),
                steps=steps,
            )

        if pattern.endswith(rf"^\s*{variable}\s*(?P<op>[+-])\s*(?P<b>\d+(?:\.\d+)?)\s*$"):
            offset = float(b_raw or 0)
            if op == "-":
                answer = rhs_value + offset
                transform = f"Add {offset:g} to both sides."
            else:
                answer = rhs_value - offset
                transform = f"Subtract {offset:g} from both sides."
            return MathSolution(
                expression=f"{left}={right}",
                normalized_expression=f"{normalized_left}={normalized_right}",
                answer=_format_number(answer),
                steps=[
                    f"Normalize the equation: {normalized_left} = {normalized_right}",
                    transform,
                    f"{variable} = {_format_number(answer)}",
                ],
            )

        if pattern.endswith(
            rf"^\s*(?P<a>[-+]?\d*(?:\.\d+)?)\*?{variable}\s*(?P<op>[+-])\s*(?P<b>\d+(?:\.\d+)?)\s*$"
        ):
            offset = float(b_raw or 0)
            if op == "-":
                intermediate = rhs_value + offset
                transform = f"Add {offset:g} to both sides."
            else:
                intermediate = rhs_value - offset
                transform = f"Subtract {offset:g} from both sides."
            answer = intermediate / coefficient
            return MathSolution(
                expression=f"{left}={right}",
                normalized_expression=f"{normalized_left}={normalized_right}",
                answer=_format_number(answer),
                steps=[
                    f"Normalize the equation: {normalized_left} = {normalized_right}",
                    transform,
                    f"Divide both sides by {coefficient:g}.",
                    f"{variable} = {_format_number(answer)}",
                ],
            )

        if pattern.endswith(rf"^\s*(?P<a>[-+]?\d*(?:\.\d+)?)\*?{variable}\s*/\s*(?P<b>\d+(?:\.\d+)?)\s*$"):
            divisor = float(b_raw or 1)
            answer = rhs_value * divisor / coefficient
            return MathSolution(
                expression=f"{left}={right}",
                normalized_expression=f"{normalized_left}={normalized_right}",
                answer=_format_number(answer),
                steps=[
                    f"Normalize the equation: {normalized_left} = {normalized_right}",
                    f"Multiply both sides by {divisor:g}.",
                    f"Divide by {coefficient:g} to isolate {variable}.",
                    f"{variable} = {_format_number(answer)}",
                ],
            )

    return None


def _find_single_variable(expression: str) -> str | None:
    letters = sorted(set(re.findall(r"[a-zA-Z]", expression)))
    if len(letters) == 1:
        return letters[0]
    return None


def _format_number(value: float) -> str:
    if math.isfinite(value) and abs(value - round(value)) < 1e-9:
        return str(int(round(value)))
    return f"{value:.6g}"


def _format_math_solution(solution: MathSolution) -> list[str]:
    parts = [f"- Math expression: {solution.expression}"]
    if solution.normalized_expression != solution.expression:
        parts.append(f"- Normalized: {solution.normalized_expression}")
    if solution.steps:
        parts.append("- Steps:")
        parts.extend([f"  {step}" for step in solution.steps[:6]])
    parts.append(f"- Answer: {solution.answer}")
    return parts


def _parse_graph_context(payload: Any) -> GraphContext | None:
    if payload is None:
        return None
    if hasattr(payload, "model_dump"):
        payload = payload.model_dump()
    if not isinstance(payload, Mapping):
        return None

    def _axis(data: Any) -> tuple[str, str | None]:
        if hasattr(data, "model_dump"):
            data = data.model_dump()
        if not isinstance(data, Mapping):
            return ("", None)
        label = str(data.get("label", "") or "")
        unit = data.get("unit")
        return (label, str(unit) if unit is not None else None)

    x_axis_label, x_axis_unit = _axis(payload.get("x_axis"))
    y_axis_label, y_axis_unit = _axis(payload.get("y_axis"))

    series_payload = payload.get("series") or []
    series: list[GraphSeries] = []
    for item in series_payload:
        if hasattr(item, "model_dump"):
            item = item.model_dump()
        if not isinstance(item, Mapping):
            continue
        points: list[GraphPoint] = []
        for point in item.get("points") or []:
            if hasattr(point, "model_dump"):
                point = point.model_dump()
            if not isinstance(point, Mapping):
                continue
            if "x" in point and "y" in point:
                points.append(GraphPoint(x=point["x"], y=point["y"]))
        series.append(GraphSeries(name=str(item.get("name", "") or ""), points=points))

    return GraphContext(
        graph_type=str(payload.get("graph_type", "") or ""),
        title=str(payload.get("title", "") or ""),
        x_axis_label=x_axis_label,
        y_axis_label=y_axis_label,
        x_axis_unit=x_axis_unit,
        y_axis_unit=y_axis_unit,
        legend=[str(item) for item in payload.get("legend") or [] if str(item).strip()],
        series=series,
        table_rows=[
            [str(cell) for cell in row]
            for row in payload.get("table_rows") or []
            if isinstance(row, list)
        ],
        annotations=[str(item) for item in payload.get("annotations") or [] if str(item).strip()],
        highlighted_points=[
            str(item) for item in payload.get("highlighted_points") or [] if str(item).strip()
        ],
        source_text=str(payload.get("source_text", "") or ""),
        confidence=float(payload.get("confidence", 0.0) or 0.0),
    )


def _summarize_series_trends(series: list[GraphSeries]) -> str:
    if not series:
        return ""

    summaries: list[str] = []
    for item in series[:3]:
        numeric_points = [
            point
            for point in item.points
            if isinstance(point.y, (int, float)) and isinstance(point.x, (int, float))
        ]
        if len(numeric_points) < 2:
            if item.name:
                summaries.append(f"{item.name}: not enough numeric points to infer a trend")
            continue

        first = numeric_points[0]
        last = numeric_points[-1]
        direction = "rising" if float(last.y) > float(first.y) else "falling" if float(last.y) < float(first.y) else "flat"
        highs = max(numeric_points, key=lambda p: float(p.y))
        lows = min(numeric_points, key=lambda p: float(p.y))
        label = item.name or "series"
        summaries.append(
            f"{label} is {direction}; lowest at ({_format_number(float(lows.x))}, {_format_number(float(lows.y))}) "
            f"and highest at ({_format_number(float(highs.x))}, {_format_number(float(highs.y))})"
        )

    return "; ".join(summaries)


def _render_math_brief(solution: MathSolution, mode: ReasoningMode) -> str:
    """Turn a math solution into a short natural-language answer."""
    intro = "Let's work it out step by step."
    if mode == ReasoningMode.ALGEBRA:
        intro = "Let's isolate the unknown step by step."
    elif mode == ReasoningMode.ARITHMETIC:
        intro = "Let's calculate it step by step."

    lines = [intro]
    if solution.steps:
        lines.extend(solution.steps[:3])
    lines.append(f"The answer is {solution.answer}.")
    return " ".join(part.strip() for part in lines if part.strip())


def _render_graph_brief(graph_context: GraphContext) -> str:
    """Turn graph context into a short learner-friendly summary."""
    title = graph_context.title.strip() or "the graph"
    parts = [f"Looking at {title},"]

    trend_summary = _summarize_series_trends(graph_context.series)
    if trend_summary:
        parts.append(trend_summary + ".")

    if graph_context.highlighted_points:
        parts.append(
            f"Key points include {', '.join(graph_context.highlighted_points[:3])}."
        )
    elif graph_context.annotations:
        parts.append(f"Notable notes: {', '.join(graph_context.annotations[:2])}.")

    if graph_context.table_rows:
        parts.append(f"The table includes {len(graph_context.table_rows)} rows.")

    return " ".join(part.strip() for part in parts if part.strip())
