"""Generate abstract reasoning odd-one-out questions with SVG visuals.

Produces 600 questions (200 Easy, 200 Medium, 200 Hard) with
mathematically correct SVG diagrams for classification-based reasoning.

Usage:
    python scripts/gen_odd_one_out_questions.py
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path

random.seed(42)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "analytical-ability" / "abstract-reasoning" / "odd-one-out-problems"
    / "questions.json"
)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

def _svg_wrap(content: str, w: int = 280, h: int = 80) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _svg_choice_wrap(content: str, w: int = 60, h: int = 60) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _polygon_svg(cx: float, cy: float, sides: int, radius: float = 20,
                 color: str = "#2196F3", fill: str = "none",
                 rotation_deg: float = -90) -> str:
    points = []
    for i in range(sides):
        angle = math.radians(rotation_deg + (360 / sides) * i)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append(f"{px:.1f},{py:.1f}")
    return (
        f"<polygon points='{' '.join(points)}' fill='{fill}' "
        f"stroke='{color}' stroke-width='2'/>"
    )
