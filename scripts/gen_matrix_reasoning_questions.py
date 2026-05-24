"""Generate abstract reasoning matrix reasoning questions with SVG visuals.

Produces 600 questions (200 Easy, 200 Medium, 200 Hard) with mathematically
correct SVG diagrams for matrix reasoning patterns including rotation,
shading, distribution, element count, size progression, and logical operations.

Usage:
    python scripts/gen_matrix_reasoning_questions.py
"""

from __future__ import annotations

import json
import math
import random
from pathlib import Path
from typing import Any

random.seed(42)

OUTPUT_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "analytical-ability" / "abstract-reasoning" / "matrix-reasoning"
    / "questions.json"
)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

COLORS = ["#2196F3", "#4CAF50", "#E91E63", "#FF9800", "#9C27B0",
           "#00BCD4", "#FF5722", "#607D8B", "#673AB7", "#009688"]


def _svg_wrap(content: str, w: int = 300, h: int = 300) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _choice_svg(content: str, w: int = 70, h: int = 70) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _grid_lines(cell_size: int = 90, margin: int = 5) -> str:
    """Generate 3x3 grid lines for a matrix."""
    w = cell_size * 3 + margin * 2
    lines = []
    # Outer border
    lines.append(f"<rect x='{margin}' y='{margin}' width='{w - margin*2}' "
                 f"height='{w - margin*2}' fill='none' stroke='#444' stroke-width='1' rx='3'/>")
    # Vertical lines
    for i in range(1, 3):
        x = margin + cell_size * i
        lines.append(f"<line x1='{x}' y1='{margin}' x2='{x}' y2='{w - margin}' "
                     f"stroke='#666' stroke-width='0.8'/>")
    # Horizontal lines
    for i in range(1, 3):
        y = margin + cell_size * i
        lines.append(f"<line x1='{margin}' y1='{y}' x2='{w - margin}' y2='{y}' "
                     f"stroke='#666' stroke-width='0.8'/>")
    return "".join(lines)


def _cell_center(row: int, col: int, cell_size: int = 90, margin: int = 5) -> tuple[float, float]:
    """Get center coordinates of a cell (0-indexed row, col)."""
    cx = margin + cell_size * col + cell_size / 2
    cy = margin + cell_size * row + cell_size / 2
    return cx, cy


def _arrow_svg(cx: float, cy: float, direction: str, size: float = 20,
               color: str = "#2196F3", filled: bool = False) -> str:
    """Generate an arrow pointing in a direction at (cx, cy)."""
    angles = {"up": 0, "right": 90, "down": 180, "left": 270,
              "up-right": 45, "down-right": 135, "down-left": 225, "up-left": 315}
    angle = angles[direction]
    rad = math.radians(angle)
    tx = cx + size * math.sin(rad)
    ty = cy - size * math.cos(rad)
    bx = cx - size * math.sin(rad)
    by = cy + size * math.cos(rad)
    wing_size = size * 0.4
    wing_angle1 = rad + math.radians(150)
    wing_angle2 = rad - math.radians(150)
    w1x = tx + wing_size * math.sin(wing_angle1)
    w1y = ty - wing_size * math.cos(wing_angle1)
    w2x = tx + wing_size * math.sin(wing_angle2)
    w2y = ty - wing_size * math.cos(wing_angle2)
    fill_attr = color if filled else "none"
    return (
        f"<line x1='{bx:.1f}' y1='{by:.1f}' x2='{tx:.1f}' y2='{ty:.1f}' "
        f"stroke='{color}' stroke-width='2'/>"
        f"<polygon points='{tx:.1f},{ty:.1f} {w1x:.1f},{w1y:.1f} {w2x:.1f},{w2y:.1f}' "
        f"fill='{fill_attr}' stroke='{color}' stroke-width='1.5'/>"
    )


def _polygon_svg(cx: float, cy: float, sides: int, radius: float = 25,
                 color: str = "#2196F3", fill: str = "none",
                 rotation_deg: float = -90) -> str:
    """Generate a regular polygon centered at (cx, cy)."""
    points = []
    for i in range(sides):
        angle = math.radians(rotation_deg + (360 / sides) * i)
        px = cx + radius * math.cos(angle)
        py = cy + radius * math.sin(angle)
        points.append(f"{px:.1f},{py:.1f}")
    pts_str = " ".join(points)
    return (
        f"<polygon points='{pts_str}' fill='{fill}' "
        f"stroke='{color}' stroke-width='2'/>"
    )


def _circle_svg(cx: float, cy: float, r: float = 25,
                color: str = "#2196F3", fill: str = "none") -> str:
    return (f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' "
            f"fill='{fill}' stroke='{color}' stroke-width='2'/>")


def _half_circle_svg(cx: float, cy: float, r: float = 25,
                     color: str = "#2196F3", half: str = "top") -> str:
    """Draw a circle with half shading."""
    outline = f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' fill='none' stroke='{color}' stroke-width='2'/>"
    if half == "top":
        path = f"<path d='M{cx-r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 0,1 {cx+r:.1f},{cy:.1f} Z' fill='{color}'/>"
    elif half == "bottom":
        path = f"<path d='M{cx-r:.1f},{cy:.1f} A{r:.1f},{r:.1f} 0 0,0 {cx+r:.1f},{cy:.1f} Z' fill='{color}'/>"
    elif half == "left":
        path = f"<path d='M{cx:.1f},{cy-r:.1f} A{r:.1f},{r:.1f} 0 0,0 {cx:.1f},{cy+r:.1f} Z' fill='{color}'/>"
    else:  # right
        path = f"<path d='M{cx:.1f},{cy-r:.1f} A{r:.1f},{r:.1f} 0 0,1 {cx:.1f},{cy+r:.1f} Z' fill='{color}'/>"
    return outline + path


def _rect_svg(cx: float, cy: float, size: float = 40,
              color: str = "#2196F3", fill: str = "none") -> str:
    x = cx - size / 2
    y = cy - size / 2
    return (f"<rect x='{x:.1f}' y='{y:.1f}' width='{size:.1f}' height='{size:.1f}' "
            f"fill='{fill}' stroke='{color}' stroke-width='2'/>")


def _dots_svg(cx: float, cy: float, count: int, color: str = "#F44336",
              radius: float = 5, spread: float = 15) -> str:
    """Draw a cluster of dots around center."""
    if count == 0:
        return ""
    positions = []
    if count == 1:
        positions = [(cx, cy)]
    elif count == 2:
        positions = [(cx - spread * 0.5, cy), (cx + spread * 0.5, cy)]
    elif count == 3:
        positions = [(cx, cy - spread * 0.5),
                     (cx - spread * 0.5, cy + spread * 0.4),
                     (cx + spread * 0.5, cy + spread * 0.4)]
    elif count == 4:
        positions = [(cx - spread * 0.4, cy - spread * 0.4),
                     (cx + spread * 0.4, cy - spread * 0.4),
                     (cx - spread * 0.4, cy + spread * 0.4),
                     (cx + spread * 0.4, cy + spread * 0.4)]
    elif count == 5:
        positions = [(cx, cy),
                     (cx - spread * 0.5, cy - spread * 0.5),
                     (cx + spread * 0.5, cy - spread * 0.5),
                     (cx - spread * 0.5, cy + spread * 0.5),
                     (cx + spread * 0.5, cy + spread * 0.5)]
    else:
        for i in range(count):
            angle = 2 * math.pi * i / count
            positions.append((cx + spread * 0.6 * math.cos(angle),
                              cy + spread * 0.6 * math.sin(angle)))
    parts = []
    for px, py in positions:
        parts.append(f"<circle cx='{px:.1f}' cy='{py:.1f}' r='{radius:.1f}' fill='{color}'/>")
    return "".join(parts)


def _question_mark(cx: float, cy: float) -> str:
    return (f"<text x='{cx:.1f}' y='{cy + 8:.1f}' text-anchor='middle' "
            f"font-size='24' fill='#888' font-family='sans-serif'>?</text>")


# ---------------------------------------------------------------------------
# Question generators by type
# ---------------------------------------------------------------------------

DIRECTIONS_CW = ["up", "right", "down", "left"]
DIRECTIONS_CCW = ["up", "left", "down", "right"]
DIRECTIONS_8 = ["up", "up-right", "right", "down-right", "down", "down-left", "left", "up-left"]
SHAPES_BY_SIDES = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon", 7: "heptagon", 8: "octagon"}
SHADINGS = ["none", "half", "full"]


def _make_matrix_svg(cells: list[str], cell_size: int = 90, margin: int = 5) -> str:
    """Build a 3x3 matrix SVG from 9 cell content strings (last one is '?')."""
    w = cell_size * 3 + margin * 2
    grid = _grid_lines(cell_size, margin)
    content = grid
    for idx, cell_content in enumerate(cells):
        content += cell_content
    return _svg_wrap(content, w, w)


def _generate_rotation_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate a rotation-based matrix question."""
    if difficulty == "Easy":
        # Simple 90° CW rotation across rows, same direction down columns
        start_idx = random.randint(0, 3)
        dirs = DIRECTIONS_CW
        cells = []
        for row in range(3):
            for col in range(3):
                idx = (start_idx + row + col) % 4
                r, c_row = row, col
                cx, cy = _cell_center(r, c_row)
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_arrow_svg(cx, cy, dirs[idx], color=color))
        answer_idx = (start_idx + 2 + 2) % 4
        answer_dir = dirs[answer_idx]
        # Generate distractors
        other_dirs = [d for d in dirs if d != answer_dir]
        random.shuffle(other_dirs)
        choices_dirs = [answer_dir] + other_dirs[:3]
        random.shuffle(choices_dirs)
        answer_label = chr(65 + choices_dirs.index(answer_dir))
        choices = []
        for i, d in enumerate(choices_dirs):
            label = chr(65 + i)
            svg = _choice_svg(_arrow_svg(35, 35, d, size=18, color=color))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_arrow_svg(35, 35, answer_dir, size=18, color=color))
        explanation = (f"The arrow rotates 90° clockwise across each row and down each column. "
                       f"Row 3 and Column 3 both require an arrow pointing {answer_dir}.")
        tags = ["abstract reasoning", "matrix reasoning", "rotation", "clockwise"]

    elif difficulty == "Medium":
        # Rotation with filled/unfilled arrowheads
        start_idx = random.randint(0, 3)
        dirs = DIRECTIONS_CW if random.random() > 0.5 else DIRECTIONS_CCW
        rot_name = "clockwise" if dirs == DIRECTIONS_CW else "counterclockwise"
        fill_states = [False, True, False]  # alternating fill per row
        cells = []
        for row in range(3):
            for col in range(3):
                idx = (start_idx + col) % 4
                cx, cy = _cell_center(row, col)
                filled = fill_states[row]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_arrow_svg(cx, cy, dirs[idx], color=color, filled=filled))
        answer_idx = (start_idx + 2) % 4
        answer_dir = dirs[answer_idx]
        answer_filled = fill_states[2]
        # Distractors: wrong direction or wrong fill
        distractor_options = []
        for d in dirs:
            for f in [True, False]:
                if d != answer_dir or f != answer_filled:
                    distractor_options.append((d, f))
        random.shuffle(distractor_options)
        choices_data = [(answer_dir, answer_filled)] + distractor_options[:3]
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index((answer_dir, answer_filled)))
        choices = []
        for i, (d, f) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_arrow_svg(35, 35, d, size=18, color=color, filled=f))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_arrow_svg(35, 35, answer_dir, size=18, color=color, filled=answer_filled))
        fill_desc = "filled" if answer_filled else "unfilled"
        explanation = (f"The arrow rotates 90° {rot_name} across each row. "
                       f"Row 3 has {fill_desc} arrowheads. The missing cell needs a "
                       f"{fill_desc} arrow pointing {answer_dir}.")
        tags = ["abstract reasoning", "matrix reasoning", "rotation", rot_name, "shading"]

    else:  # Hard
        # 8-direction rotation (45° increments)
        start_idx = random.randint(0, 7)
        step = random.choice([1, 2, 3])  # 45°, 90°, or 135° per cell
        cells = []
        for row in range(3):
            for col in range(3):
                idx = (start_idx + (row * 3 + col) * step) % 8
                cx, cy = _cell_center(row, col)
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_arrow_svg(cx, cy, DIRECTIONS_8[idx], color=color))
        answer_idx = (start_idx + 8 * step) % 8
        answer_dir = DIRECTIONS_8[answer_idx]
        other_dirs = [d for d in DIRECTIONS_8 if d != answer_dir]
        random.shuffle(other_dirs)
        choices_dirs = [answer_dir] + other_dirs[:3]
        random.shuffle(choices_dirs)
        answer_label = chr(65 + choices_dirs.index(answer_dir))
        choices = []
        for i, d in enumerate(choices_dirs):
            label = chr(65 + i)
            svg = _choice_svg(_arrow_svg(35, 35, d, size=18, color=color))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_arrow_svg(35, 35, answer_dir, size=18, color=color))
        deg = step * 45
        explanation = (f"The arrow rotates {deg}° per cell position in the matrix. "
                       f"Following the pattern, the missing cell requires an arrow pointing {answer_dir}.")
        tags = ["abstract reasoning", "matrix reasoning", "rotation", "diagonal", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_dot_count_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate a dot/element count matrix question."""
    dot_color = color

    if difficulty == "Easy":
        # Dots increase across rows; starting count varies
        start = random.choice([1, 2, 3])
        step = random.choice([1, 2])
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                count = start + col * step
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_dots_svg(cx, cy, count, color=dot_color))
        answer_count = start + 2 * step
        # Choices: answer and 3 distractors
        choices_counts = list({answer_count, max(1, answer_count - step),
                              answer_count + step, max(1, answer_count - 2 * step)})
        while len(choices_counts) < 4:
            choices_counts.append(answer_count + 2 * step)
        choices_counts = choices_counts[:4]
        random.shuffle(choices_counts)
        answer_label = chr(65 + choices_counts.index(answer_count))
        choices = []
        for i, c in enumerate(choices_counts):
            label = chr(65 + i)
            svg = _choice_svg(_dots_svg(35, 35, c, color=dot_color, spread=12))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_dots_svg(35, 35, answer_count, color=dot_color, spread=12))
        seq_str = ", ".join(str(start + col * step) for col in range(3))
        explanation = (f"Each row contains {seq_str} dots from left to right "
                       f"(increasing by {step}). The missing cell needs {answer_count} dots.")
        tags = ["abstract reasoning", "matrix reasoning", "element count", "progression"]

    elif difficulty == "Medium":
        # Rows increase by different amounts; columns also have a pattern
        row_starts = [1, 2, 3]
        col_increment = 1
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                count = row_starts[row] + col * col_increment
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_dots_svg(cx, cy, count, color=dot_color))
        answer_count = row_starts[2] + 2 * col_increment  # row 3, col 3
        choices_counts = list({answer_count, answer_count - 1, answer_count + 1,
                              answer_count - 2})[:4]
        if len(choices_counts) < 4:
            choices_counts.append(answer_count + 2)
        choices_counts = choices_counts[:4]
        random.shuffle(choices_counts)
        answer_label = chr(65 + choices_counts.index(answer_count))
        choices = []
        for i, c in enumerate(choices_counts):
            label = chr(65 + i)
            svg = _choice_svg(_dots_svg(35, 35, c, color=dot_color, spread=12))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_dots_svg(35, 35, answer_count, color=dot_color, spread=12))
        explanation = (f"Each row starts with an increasing number of dots (1, 2, 3) and adds 1 per column. "
                       f"Row 3 starts at 3, so Column 3 needs {answer_count} dots.")
        tags = ["abstract reasoning", "matrix reasoning", "element count", "progression", "dual rule"]

    else:  # Hard
        # Dot count follows multiplication or non-linear pattern
        # Row determines base, column determines multiplier
        bases = [1, 2, 3]
        multipliers = [1, 2, 3]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                count = bases[row] * multipliers[col]
                if count > 6:
                    count = min(count, 6)  # cap for visual clarity
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_dots_svg(cx, cy, count, color=dot_color))
        answer_count = min(bases[2] * multipliers[2], 6)
        choices_counts = list({answer_count, answer_count - 1, answer_count + 1,
                              max(1, answer_count - 2)})
        while len(choices_counts) < 4:
            choices_counts.append(answer_count + 2)
        choices_counts = choices_counts[:4]
        random.shuffle(choices_counts)
        answer_label = chr(65 + choices_counts.index(answer_count))
        choices = []
        for i, c in enumerate(choices_counts):
            label = chr(65 + i)
            svg = _choice_svg(_dots_svg(35, 35, c, color=dot_color, spread=12))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_dots_svg(35, 35, answer_count, color=dot_color, spread=12))
        explanation = (f"The dot count equals row number × column number. "
                       f"Row 3 × Column 3 = {answer_count} dots.")
        tags = ["abstract reasoning", "matrix reasoning", "element count", "multiplication", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_shape_progression_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate a shape (polygon sides) progression matrix question."""

    if difficulty == "Easy":
        # Each row: shapes with increasing sides
        start_sides = random.choice([3, 4, 5])
        base_sides = [start_sides, start_sides + 1, start_sides + 2]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                sides = base_sides[col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_polygon_svg(cx, cy, sides, radius=25, color=color))
        answer_sides = base_sides[2]
        choices_sides = list({answer_sides, answer_sides - 1, answer_sides + 1,
                             max(3, answer_sides - 2)})
        while len(choices_sides) < 4:
            choices_sides.append(answer_sides + 2)
        choices_sides = choices_sides[:4]
        random.shuffle(choices_sides)
        answer_label = chr(65 + choices_sides.index(answer_sides))
        choices = []
        for i, s in enumerate(choices_sides):
            label = chr(65 + i)
            svg = _choice_svg(_polygon_svg(35, 35, max(3, s), radius=22, color=color))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_polygon_svg(35, 35, answer_sides, radius=22, color=color))
        names = [SHAPES_BY_SIDES.get(s, f"{s}-gon") for s in base_sides]
        answer_name = SHAPES_BY_SIDES.get(answer_sides, f"{answer_sides}-gon")
        explanation = (f"Each row shows shapes with increasing sides: "
                       f"{names[0]} ({base_sides[0]}) → {names[1]} ({base_sides[1]}) → "
                       f"{names[2]} ({base_sides[2]}). The missing cell needs a {answer_name}.")
        tags = ["abstract reasoning", "matrix reasoning", "shape progression", "polygon"]

    elif difficulty == "Medium":
        # Rows have different starting shapes; sides increase by 1 across columns
        row_starts = random.sample([3, 4, 5], 3)
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                sides = row_starts[row] + col
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_polygon_svg(cx, cy, sides, radius=25, color=color))
        answer_sides = row_starts[2] + 2
        choices_sides = list({answer_sides, answer_sides - 1, answer_sides + 1, answer_sides - 2})
        while len(choices_sides) < 4:
            choices_sides.append(answer_sides + 2)
        choices_sides = choices_sides[:4]
        random.shuffle(choices_sides)
        answer_label = chr(65 + choices_sides.index(answer_sides))
        choices = []
        for i, s in enumerate(choices_sides):
            label = chr(65 + i)
            svg = _choice_svg(_polygon_svg(35, 35, max(3, s), radius=22, color=color))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_polygon_svg(35, 35, answer_sides, radius=22, color=color))
        shape_name = SHAPES_BY_SIDES.get(answer_sides, f"{answer_sides}-gon")
        explanation = (f"Each row adds one side per column. Row 3 starts at "
                       f"{SHAPES_BY_SIDES.get(row_starts[2], str(row_starts[2]))} ({row_starts[2]} sides), "
                       f"so Column 3 needs {answer_sides} sides ({shape_name}).")
        tags = ["abstract reasoning", "matrix reasoning", "shape progression", "polygon", "dual rule"]

    else:  # Hard
        # Shape progression + size progression combined
        row_starts = [3, 4, 5]
        size_by_col = [18, 22, 28]  # small, medium, large
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                sides = row_starts[row] + col
                radius = size_by_col[col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_polygon_svg(cx, cy, sides, radius=radius, color=color))
        answer_sides = row_starts[2] + 2
        answer_radius = size_by_col[2]
        # Distractors: wrong sides or wrong size
        choices_data = [(answer_sides, answer_radius)]
        choices_data.append((answer_sides - 1, answer_radius))
        choices_data.append((answer_sides, size_by_col[1]))
        choices_data.append((answer_sides + 1, size_by_col[0]))
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index((answer_sides, answer_radius)))
        choices = []
        for i, (s, r) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_polygon_svg(35, 35, max(3, s), radius=min(r, 28), color=color))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_polygon_svg(35, 35, answer_sides, radius=min(answer_radius, 28), color=color))
        shape_name = SHAPES_BY_SIDES.get(answer_sides, f"{answer_sides}-gon")
        explanation = (f"Two rules operate: sides increase across rows ({row_starts[2]}→{row_starts[2]+1}→{answer_sides}), "
                       f"and size increases across columns (small→medium→large). "
                       f"The answer is a large {shape_name}.")
        tags = ["abstract reasoning", "matrix reasoning", "shape progression", "size", "multi-rule"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_shading_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate a shading progression matrix question."""

    def _draw_shape_with_shading(cx: float, cy: float, shape: str, shading: str,
                                  color: str, radius: float = 25) -> str:
        if shape == "circle":
            if shading == "none":
                return _circle_svg(cx, cy, radius, color=color)
            elif shading == "half":
                return _half_circle_svg(cx, cy, radius, color=color, half="top")
            else:  # full
                return _circle_svg(cx, cy, radius, color=color, fill=color)
        elif shape == "square":
            if shading == "none":
                return _rect_svg(cx, cy, radius * 1.8, color=color)
            elif shading == "half":
                size = radius * 1.8
                x = cx - size / 2
                y = cy - size / 2
                outline = f"<rect x='{x:.1f}' y='{y:.1f}' width='{size:.1f}' height='{size:.1f}' fill='none' stroke='{color}' stroke-width='2'/>"
                half_fill = f"<rect x='{x:.1f}' y='{y:.1f}' width='{size/2:.1f}' height='{size:.1f}' fill='{color}'/>"
                return outline + half_fill
            else:  # full
                return _rect_svg(cx, cy, radius * 1.8, color=color, fill=color)
        else:  # triangle
            if shading == "none":
                return _polygon_svg(cx, cy, 3, radius=radius, color=color)
            elif shading == "half":
                outline = _polygon_svg(cx, cy, 3, radius=radius, color=color)
                # Add a simple half-fill indicator line
                line = f"<line x1='{cx:.1f}' y1='{cy - radius:.1f}' x2='{cx:.1f}' y2='{cy + radius:.1f}' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
                return outline + line
            else:  # full
                return _polygon_svg(cx, cy, 3, radius=radius, color=color, fill=color)

    if difficulty == "Easy":
        # Same shape, shading progresses: none → half → full across rows
        shape = random.choice(["circle", "square", "triangle"])
        shading_order = ["none", "half", "full"]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                shading = shading_order[col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_shape_with_shading(cx, cy, shape, shading, color))
        answer_shading = "full"
        choices_shadings = ["full", "none", "half", "none"]
        random.shuffle(choices_shadings)
        answer_label = chr(65 + choices_shadings.index(answer_shading))
        choices = []
        for i, s in enumerate(choices_shadings):
            label = chr(65 + i)
            svg = _choice_svg(_draw_shape_with_shading(35, 35, shape, s, color, radius=22))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_shape_with_shading(35, 35, shape, answer_shading, color, radius=22))
        explanation = (f"Each row shows the same {shape} with progressive shading: "
                       f"empty → half-filled → fully filled. The missing cell needs a fully filled {shape}.")
        tags = ["abstract reasoning", "matrix reasoning", "shading", "progression"]

    elif difficulty == "Medium":
        # Distribution: each row has one of each shading, different arrangement
        shape = random.choice(["circle", "square", "triangle"])
        # Each row is a permutation of shadings
        perms = [
            ["none", "half", "full"],
            ["full", "none", "half"],
            ["half", "full", "none"],
        ]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                shading = perms[row][col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_shape_with_shading(cx, cy, shape, shading, color))
        answer_shading = perms[2][2]  # "none"
        choices_shadings = ["none", "half", "full", "half"]
        random.shuffle(choices_shadings)
        answer_label = chr(65 + choices_shadings.index(answer_shading))
        choices = []
        for i, s in enumerate(choices_shadings):
            label = chr(65 + i)
            svg = _choice_svg(_draw_shape_with_shading(35, 35, shape, s, color, radius=22))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_shape_with_shading(35, 35, shape, answer_shading, color, radius=22))
        explanation = (f"Each row contains exactly one empty, one half-filled, and one fully filled {shape}. "
                       f"Row 3 already has half and full, so the missing cell needs an empty {shape}. "
                       f"Column 3 confirms: it has full and half, so needs empty.")
        tags = ["abstract reasoning", "matrix reasoning", "shading", "distribution"]

    else:  # Hard
        # Shape changes by row + shading distribution
        shapes = ["circle", "square", "triangle"]
        perms = [
            ["none", "half", "full"],
            ["half", "full", "none"],
            ["full", "none", "half"],
        ]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                shape = shapes[row]
                shading = perms[row][col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_shape_with_shading(cx, cy, shape, shading, color))
        answer_shape = shapes[2]  # triangle
        answer_shading = perms[2][2]  # "half"
        # Distractors: wrong shape or wrong shading
        choices_data = [
            (answer_shape, answer_shading),
            (answer_shape, "none"),
            (answer_shape, "full"),
            ("circle", answer_shading),
        ]
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index((answer_shape, answer_shading)))
        choices = []
        for i, (sh, sd) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_draw_shape_with_shading(35, 35, sh, sd, color, radius=22))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_shape_with_shading(35, 35, answer_shape, answer_shading, color, radius=22))
        explanation = (f"Row rule: shape changes by row (circle, square, triangle). "
                       f"Shading rule: each row has one of each shading (distribution). "
                       f"Row 3 (triangles) has full and none, so needs half-filled. "
                       f"Answer: half-filled triangle.")
        tags = ["abstract reasoning", "matrix reasoning", "shading", "shape", "distribution", "multi-rule"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_size_progression_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate a size progression matrix question."""

    if difficulty == "Easy":
        # Same shape, size increases across columns
        shape_sides = random.choice([0, 3, 4, 5, 6])  # 0 = circle
        # Vary the actual size values
        size_base = random.choice([12, 14, 16])
        size_step = random.choice([6, 7, 8])
        sizes = [size_base, size_base + size_step, size_base + 2 * size_step]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                r = sizes[col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    if shape_sides == 0:
                        cells.append(_circle_svg(cx, cy, r, color=color))
                    else:
                        cells.append(_polygon_svg(cx, cy, shape_sides, radius=r, color=color))
        answer_size = sizes[2]
        choices_sizes = [sizes[2], sizes[0], sizes[1], sizes[2] + size_step]
        random.shuffle(choices_sizes)
        answer_label = chr(65 + choices_sizes.index(answer_size))
        choices = []
        for i, s in enumerate(choices_sizes):
            label = chr(65 + i)
            if shape_sides == 0:
                svg = _choice_svg(_circle_svg(35, 35, min(s, 28), color=color))
            else:
                svg = _choice_svg(_polygon_svg(35, 35, shape_sides, radius=min(s, 28), color=color))
            choices.append(f"{label}: {svg}")
        if shape_sides == 0:
            answer_svg = _choice_svg(_circle_svg(35, 35, min(answer_size, 28), color=color))
            shape_name = "circle"
        else:
            answer_svg = _choice_svg(_polygon_svg(35, 35, shape_sides, radius=min(answer_size, 28), color=color))
            shape_name = SHAPES_BY_SIDES.get(shape_sides, "polygon")
        explanation = (f"Each row shows the same {shape_name} growing from small to medium to large. "
                       f"The missing cell needs the largest {shape_name}.")
        tags = ["abstract reasoning", "matrix reasoning", "size progression"]

    elif difficulty == "Medium":
        # Size increases across rows, shape changes across columns
        shapes = [0, 4, 3]  # circle, square, triangle
        sizes_by_row = [15, 22, 30]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                r = sizes_by_row[row]
                s = shapes[col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    if s == 0:
                        cells.append(_circle_svg(cx, cy, r, color=color))
                    else:
                        cells.append(_polygon_svg(cx, cy, s, radius=r, color=color))
        answer_shape = shapes[2]  # triangle
        answer_size = sizes_by_row[2]  # large
        choices_data = [
            (3, 30), (3, 15), (4, 30), (0, 30)
        ]
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index((answer_shape, answer_size)))
        choices = []
        for i, (s, r) in enumerate(choices_data):
            label = chr(65 + i)
            if s == 0:
                svg = _choice_svg(_circle_svg(35, 35, min(r, 28), color=color))
            else:
                svg = _choice_svg(_polygon_svg(35, 35, s, radius=min(r, 28), color=color))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_polygon_svg(35, 35, answer_shape, radius=min(answer_size, 28), color=color))
        explanation = ("Row rule: size increases (small → medium → large). "
                       "Column rule: shape changes (circle → square → triangle). "
                       "Missing cell: large triangle.")
        tags = ["abstract reasoning", "matrix reasoning", "size progression", "shape", "dual rule"]

    else:  # Hard
        # Size + shading + shape all vary
        shapes = [0, 4, 3]
        sizes_by_row = [15, 22, 30]
        shadings = ["none", "half", "full"]
        # Shading distributed: each row has one of each
        shading_perms = [
            [0, 1, 2],
            [2, 0, 1],
            [1, 2, 0],
        ]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                r = sizes_by_row[row]
                s = shapes[col]
                shading_idx = shading_perms[row][col]
                shading = shadings[shading_idx]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    if s == 0:
                        if shading == "none":
                            cells.append(_circle_svg(cx, cy, r, color=color))
                        elif shading == "full":
                            cells.append(_circle_svg(cx, cy, r, color=color, fill=color))
                        else:
                            cells.append(_half_circle_svg(cx, cy, r, color=color))
                    else:
                        if shading == "none":
                            cells.append(_polygon_svg(cx, cy, s, radius=r, color=color))
                        elif shading == "full":
                            cells.append(_polygon_svg(cx, cy, s, radius=r, color=color, fill=color))
                        else:
                            cells.append(_polygon_svg(cx, cy, s, radius=r, color=color) +
                                         f"<line x1='{cx:.1f}' y1='{cy-r:.1f}' x2='{cx:.1f}' y2='{cy+r:.1f}' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>")
        answer_shape = shapes[2]  # triangle
        answer_size = sizes_by_row[2]  # large
        answer_shading = shadings[shading_perms[2][2]]  # index 0 = "none"
        # Distractors
        choices_data = [
            (3, 30, "none"),
            (3, 30, "full"),
            (3, 22, "none"),
            (4, 30, "none"),
        ]
        random.shuffle(choices_data)
        answer_tuple = (answer_shape, answer_size, answer_shading)
        if answer_tuple not in choices_data:
            choices_data[0] = answer_tuple
            random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index(answer_tuple))
        choices = []
        for i, (s, r, sd) in enumerate(choices_data):
            label = chr(65 + i)
            fill = color if sd == "full" else "none"
            if s == 0:
                if sd == "half":
                    inner = _half_circle_svg(35, 35, min(r, 28), color=color)
                else:
                    inner = _circle_svg(35, 35, min(r, 28), color=color, fill=fill)
            else:
                inner = _polygon_svg(35, 35, s, radius=min(r, 28), color=color, fill=fill)
                if sd == "half":
                    inner += f"<line x1='35' y1='{35-r}' x2='35' y2='{35+r}' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
            svg = _choice_svg(inner)
            choices.append(f"{label}: {svg}")
        fill = color if answer_shading == "full" else "none"
        inner = _polygon_svg(35, 35, answer_shape, radius=min(answer_size, 28), color=color, fill=fill)
        if answer_shading == "half":
            inner += f"<line x1='35' y1='{35-answer_size}' x2='35' y2='{35+answer_size}' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
        answer_svg = _choice_svg(inner)
        explanation = ("Three rules: shape changes by column (circle→square→triangle), "
                       "size increases by row (small→medium→large), "
                       f"shading is distributed (each row has empty, half, full). "
                       f"Answer: large empty triangle.")
        tags = ["abstract reasoning", "matrix reasoning", "size", "shape", "shading", "multi-rule", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_distribution_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate a distribution-of-three matrix question (each row/col has one of each)."""

    shapes_list = ["circle", "square", "triangle"]

    def _draw_simple_shape(cx, cy, shape, color, radius=25):
        if shape == "circle":
            return _circle_svg(cx, cy, radius, color=color)
        elif shape == "square":
            return _rect_svg(cx, cy, radius * 1.8, color=color)
        else:
            return _polygon_svg(cx, cy, 3, radius=radius, color=color)

    if difficulty == "Easy":
        # Each row has circle, square, triangle in different order
        # Randomize the permutation arrangement
        all_perms = [
            [0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]
        ]
        selected_perms = random.sample(all_perms, 3)
        perms = selected_perms
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                shape = shapes_list[perms[row][col]]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_simple_shape(cx, cy, shape, color))
        answer_shape = shapes_list[perms[2][2]]
        choices_shapes = list(shapes_list) + [random.choice(shapes_list)]
        random.shuffle(choices_shapes)
        # Ensure answer is in choices
        if answer_shape not in choices_shapes:
            choices_shapes[0] = answer_shape
        choices_shapes = choices_shapes[:4]
        if answer_shape not in choices_shapes:
            choices_shapes[3] = answer_shape
        random.shuffle(choices_shapes)
        answer_label = chr(65 + choices_shapes.index(answer_shape))
        choices = []
        for i, sh in enumerate(choices_shapes):
            label = chr(65 + i)
            svg = _choice_svg(_draw_simple_shape(35, 35, sh, color, radius=22))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_simple_shape(35, 35, answer_shape, color, radius=22))
        explanation = (f"Each row contains one circle, one square, and one triangle. "
                       f"Row 3 has {shapes_list[perms[2][0]]} and {shapes_list[perms[2][1]]}, "
                       f"so it needs a {answer_shape}.")
        tags = ["abstract reasoning", "matrix reasoning", "distribution", "shape"]

    elif difficulty == "Medium":
        # Distribution of shapes AND sizes
        sizes = ["small", "medium", "large"]
        size_radii = {"small": 15, "medium": 22, "large": 30}
        shape_perms = [[0, 1, 2], [2, 0, 1], [1, 2, 0]]
        size_perms = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                shape = shapes_list[shape_perms[row][col]]
                size = sizes[size_perms[row][col]]
                r = size_radii[size]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_simple_shape(cx, cy, shape, color, radius=r))
        answer_shape = shapes_list[shape_perms[2][2]]
        answer_size = sizes[size_perms[2][2]]
        answer_r = size_radii[answer_size]
        choices_data = [
            (answer_shape, answer_r),
            (answer_shape, size_radii["small"] if answer_size != "small" else size_radii["large"]),
            (shapes_list[(shape_perms[2][2] + 1) % 3], answer_r),
            (shapes_list[(shape_perms[2][2] + 2) % 3], size_radii["medium"]),
        ]
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index((answer_shape, answer_r)))
        choices = []
        for i, (sh, r) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_draw_simple_shape(35, 35, sh, color, radius=min(r, 28)))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_simple_shape(35, 35, answer_shape, color, radius=min(answer_r, 28)))
        explanation = (f"Each row has one of each shape (circle, square, triangle) AND one of each size "
                       f"(small, medium, large). Row 3 needs a {answer_size} {answer_shape}.")
        tags = ["abstract reasoning", "matrix reasoning", "distribution", "shape", "size", "dual rule"]

    else:  # Hard
        # Distribution of shapes, sizes, AND shadings (triple distribution)
        sizes = ["small", "medium", "large"]
        size_radii = {"small": 15, "medium": 22, "large": 30}
        shadings_list = ["none", "half", "full"]
        # Use Latin squares for each attribute
        shape_perms = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        size_perms = [[0, 1, 2], [2, 0, 1], [1, 2, 0]]
        shading_perms = [[0, 1, 2], [1, 2, 0], [2, 0, 1]]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                shape = shapes_list[shape_perms[row][col]]
                size = sizes[size_perms[row][col]]
                shading = shadings_list[shading_perms[row][col]]
                r = size_radii[size]
                fill = color if shading == "full" else "none"
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    base = _draw_simple_shape(cx, cy, shape, color, radius=r)
                    if shading == "full":
                        if shape == "circle":
                            base = _circle_svg(cx, cy, r, color=color, fill=color)
                        elif shape == "square":
                            base = _rect_svg(cx, cy, r * 1.8, color=color, fill=color)
                        else:
                            base = _polygon_svg(cx, cy, 3, radius=r, color=color, fill=color)
                    elif shading == "half":
                        if shape == "circle":
                            base = _half_circle_svg(cx, cy, r, color=color)
                        else:
                            base += f"<line x1='{cx:.1f}' y1='{cy-r:.1f}' x2='{cx:.1f}' y2='{cy+r:.1f}' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
                    cells.append(base)
        answer_shape = shapes_list[shape_perms[2][2]]
        answer_size = sizes[size_perms[2][2]]
        answer_shading = shadings_list[shading_perms[2][2]]
        answer_r = size_radii[answer_size]
        # Build answer and distractors
        choices_data = [
            (answer_shape, answer_r, answer_shading),
            (answer_shape, answer_r, "full" if answer_shading != "full" else "none"),
            (answer_shape, size_radii["small"] if answer_size != "small" else size_radii["large"], answer_shading),
            ("circle" if answer_shape != "circle" else "square", answer_r, answer_shading),
        ]
        random.shuffle(choices_data)
        answer_tuple = (answer_shape, answer_r, answer_shading)
        answer_label = chr(65 + choices_data.index(answer_tuple))
        choices = []
        for i, (sh, r, sd) in enumerate(choices_data):
            label = chr(65 + i)
            fill = color if sd == "full" else "none"
            if sh == "circle":
                if sd == "half":
                    inner = _half_circle_svg(35, 35, min(r, 28), color=color)
                else:
                    inner = _circle_svg(35, 35, min(r, 28), color=color, fill=fill)
            elif sh == "square":
                inner = _rect_svg(35, 35, min(r * 1.8, 50), color=color, fill=fill)
                if sd == "half":
                    inner += f"<line x1='35' y1='10' x2='35' y2='60' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
            else:
                inner = _polygon_svg(35, 35, 3, radius=min(r, 28), color=color, fill=fill)
                if sd == "half":
                    inner += f"<line x1='35' y1='10' x2='35' y2='60' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
            svg = _choice_svg(inner)
            choices.append(f"{label}: {svg}")
        # Build answer SVG
        fill = color if answer_shading == "full" else "none"
        if answer_shape == "circle":
            if answer_shading == "half":
                inner = _half_circle_svg(35, 35, min(answer_r, 28), color=color)
            else:
                inner = _circle_svg(35, 35, min(answer_r, 28), color=color, fill=fill)
        elif answer_shape == "square":
            inner = _rect_svg(35, 35, min(answer_r * 1.8, 50), color=color, fill=fill)
            if answer_shading == "half":
                inner += f"<line x1='35' y1='10' x2='35' y2='60' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
        else:
            inner = _polygon_svg(35, 35, 3, radius=min(answer_r, 28), color=color, fill=fill)
            if answer_shading == "half":
                inner += f"<line x1='35' y1='10' x2='35' y2='60' stroke='{color}' stroke-width='1' stroke-dasharray='2,2'/>"
        answer_svg = _choice_svg(inner)
        explanation = (f"Triple distribution: each row has one of each shape, size, and shading. "
                       f"Missing cell needs: {answer_size} {answer_shading} {answer_shape}.")
        tags = ["abstract reasoning", "matrix reasoning", "distribution", "triple rule", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_rotation_shading_combo_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate questions combining rotation and shading rules."""

    if difficulty == "Easy":
        # Arrow rotates CW, all same shading
        start_idx = random.randint(0, 3)
        filled = random.choice([True, False])
        cells = []
        for row in range(3):
            for col in range(3):
                idx = (start_idx + col) % 4
                cx, cy = _cell_center(row, col)
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_arrow_svg(cx, cy, DIRECTIONS_CW[idx], color=color, filled=filled))
        answer_dir = DIRECTIONS_CW[(start_idx + 2) % 4]
        other_dirs = [d for d in DIRECTIONS_CW if d != answer_dir]
        random.shuffle(other_dirs)
        choices_dirs = [answer_dir] + other_dirs[:3]
        random.shuffle(choices_dirs)
        answer_label = chr(65 + choices_dirs.index(answer_dir))
        choices = []
        for i, d in enumerate(choices_dirs):
            label = chr(65 + i)
            svg = _choice_svg(_arrow_svg(35, 35, d, size=18, color=color, filled=filled))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_arrow_svg(35, 35, answer_dir, size=18, color=color, filled=filled))
        fill_word = "filled" if filled else "unfilled"
        explanation = (f"All arrows are {fill_word}. They rotate 90° clockwise across each row. "
                       f"The missing cell needs a {fill_word} arrow pointing {answer_dir}.")
        tags = ["abstract reasoning", "matrix reasoning", "rotation", "shading"]

    elif difficulty == "Medium":
        # Arrow rotates CW across rows; shading changes down columns
        start_idx = random.randint(0, 3)
        fill_by_row = [False, False, True]  # rows 1-2 unfilled, row 3 filled
        cells = []
        for row in range(3):
            for col in range(3):
                idx = (start_idx + col) % 4
                cx, cy = _cell_center(row, col)
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_arrow_svg(cx, cy, DIRECTIONS_CW[idx], color=color, filled=fill_by_row[row]))
        answer_dir = DIRECTIONS_CW[(start_idx + 2) % 4]
        answer_filled = fill_by_row[2]
        # Distractors
        choices_data = [(answer_dir, True), (answer_dir, False),
                        (DIRECTIONS_CW[(start_idx + 1) % 4], True),
                        (DIRECTIONS_CW[(start_idx + 3) % 4], True)]
        # Ensure answer is in choices
        answer_tuple = (answer_dir, answer_filled)
        if answer_tuple not in choices_data:
            choices_data[0] = answer_tuple
        choices_data = list(dict.fromkeys(choices_data))[:4]
        while len(choices_data) < 4:
            choices_data.append((DIRECTIONS_CW[(start_idx) % 4], False))
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index(answer_tuple))
        choices = []
        for i, (d, f) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_arrow_svg(35, 35, d, size=18, color=color, filled=f))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_arrow_svg(35, 35, answer_dir, size=18, color=color, filled=answer_filled))
        explanation = (f"Row rule: arrows rotate 90° CW (direction changes per column). "
                       f"Column rule: Row 3 has filled arrowheads. "
                       f"Answer: filled arrow pointing {answer_dir}.")
        tags = ["abstract reasoning", "matrix reasoning", "rotation", "shading", "dual rule"]

    else:  # Hard
        # Rotation direction alternates by row + shading progresses
        start_idx = random.randint(0, 3)
        # Row 1: CW, Row 2: CCW, Row 3: CW
        row_dirs = [DIRECTIONS_CW, DIRECTIONS_CCW, DIRECTIONS_CW]
        fill_states = [False, True, False]  # alternating
        cells = []
        for row in range(3):
            for col in range(3):
                dirs = row_dirs[row]
                if row % 2 == 0:
                    idx = (start_idx + col) % 4
                else:
                    idx = (start_idx + col) % 4
                cx, cy = _cell_center(row, col)
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_arrow_svg(cx, cy, dirs[idx], color=color, filled=fill_states[row]))
        answer_dir = row_dirs[2][(start_idx + 2) % 4]
        answer_filled = fill_states[2]
        choices_data = [
            (answer_dir, answer_filled),
            (answer_dir, not answer_filled),
            (DIRECTIONS_CW[(start_idx + 1) % 4], answer_filled),
            (DIRECTIONS_CCW[(start_idx + 2) % 4], answer_filled),
        ]
        random.shuffle(choices_data)
        answer_tuple = (answer_dir, answer_filled)
        answer_label = chr(65 + choices_data.index(answer_tuple))
        choices = []
        for i, (d, f) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_arrow_svg(35, 35, d, size=18, color=color, filled=f))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_arrow_svg(35, 35, answer_dir, size=18, color=color, filled=answer_filled))
        fill_word = "unfilled" if not answer_filled else "filled"
        explanation = (f"Rows alternate rotation direction: Row 1 CW, Row 2 CCW, Row 3 CW. "
                       f"Shading alternates by row (unfilled, filled, unfilled). "
                       f"Answer: {fill_word} arrow pointing {answer_dir}.")
        tags = ["abstract reasoning", "matrix reasoning", "rotation", "alternating", "shading", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_line_count_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate questions based on line/stroke count in cells."""

    def _draw_lines(cx: float, cy: float, count: int, color: str, length: float = 30) -> str:
        """Draw vertical lines evenly spaced."""
        if count == 0:
            return ""
        parts = []
        total_width = (count - 1) * 12 if count > 1 else 0
        start_x = cx - total_width / 2
        for i in range(count):
            x = start_x + i * 12
            parts.append(f"<line x1='{x:.1f}' y1='{cy - length/2:.1f}' "
                         f"x2='{x:.1f}' y2='{cy + length/2:.1f}' "
                         f"stroke='{color}' stroke-width='2.5' stroke-linecap='round'/>")
        return "".join(parts)

    if difficulty == "Easy":
        # Lines increase across each row with variable start and step
        start = random.choice([1, 2])
        step = random.choice([1, 2])
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                count = start + col * step
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_lines(cx, cy, count, color))
        answer_count = start + 2 * step
        choices_counts = list({answer_count, max(1, answer_count - step),
                              answer_count + step, max(1, answer_count - 2)})
        while len(choices_counts) < 4:
            choices_counts.append(answer_count + 2)
        choices_counts = choices_counts[:4]
        random.shuffle(choices_counts)
        answer_label = chr(65 + choices_counts.index(answer_count))
        choices = []
        for i, c in enumerate(choices_counts):
            label = chr(65 + i)
            svg = _choice_svg(_draw_lines(35, 35, c, color, length=25))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_lines(35, 35, answer_count, color, length=25))
        seq_str = ", ".join(str(start + col * step) for col in range(3))
        explanation = (f"Each row has {seq_str} lines from left to right "
                       f"(increasing by {step}). The missing cell needs {answer_count} lines.")
        tags = ["abstract reasoning", "matrix reasoning", "line count", "progression"]

    elif difficulty == "Medium":
        # Lines: row determines starting count, increases by step per column
        step = random.choice([1, 2])
        row_starts = [random.randint(1, 2), random.randint(2, 3), random.randint(3, 4)]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                count = row_starts[row] + col * step
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_lines(cx, cy, count, color))
        answer_count = row_starts[2] + 2 * step
        choices_counts = [answer_count, answer_count - 1, answer_count + 1, max(1, answer_count - 2)]
        choices_counts = list(set(max(1, c) for c in choices_counts))
        while len(choices_counts) < 4:
            choices_counts.append(answer_count + 2)
        choices_counts = choices_counts[:4]
        random.shuffle(choices_counts)
        answer_label = chr(65 + choices_counts.index(answer_count))
        choices = []
        for i, c in enumerate(choices_counts):
            label = chr(65 + i)
            svg = _choice_svg(_draw_lines(35, 35, c, color, length=25))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_lines(35, 35, answer_count, color, length=25))
        explanation = (f"Row 3 starts with {row_starts[2]} lines and adds {step} per column. "
                       f"Column 3 needs {answer_count} lines.")
        tags = ["abstract reasoning", "matrix reasoning", "line count", "progression", "dual rule"]

    else:  # Hard
        # Lines follow: Cell 3 = Cell 1 + Cell 2 (addition rule)
        a1 = random.randint(1, 3)
        b1 = random.randint(1, 3)
        a2 = random.randint(1, 3)
        b2 = random.randint(2, 4)
        a3 = random.randint(2, 4)
        b3 = random.randint(1, 3)
        row_data = [(a1, b1, a1 + b1), (a2, b2, a2 + b2), (a3, b3, a3 + b3)]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                count = row_data[row][col]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_lines(cx, cy, min(count, 6), color))
        answer_count = row_data[2][2]
        choices_counts = [answer_count, answer_count - 1, answer_count + 1, max(1, answer_count - 2)]
        choices_counts = list(set(max(1, c) for c in choices_counts))
        while len(choices_counts) < 4:
            choices_counts.append(answer_count + 2)
        choices_counts = choices_counts[:4]
        random.shuffle(choices_counts)
        answer_label = chr(65 + choices_counts.index(answer_count))
        choices = []
        for i, c in enumerate(choices_counts):
            label = chr(65 + i)
            svg = _choice_svg(_draw_lines(35, 35, min(c, 6), color, length=25))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_lines(35, 35, min(answer_count, 6), color, length=25))
        explanation = (f"In each row, the third cell's line count equals the sum of the first two cells. "
                       f"Row 3: {row_data[2][0]} + {row_data[2][1]} = {answer_count} lines.")
        tags = ["abstract reasoning", "matrix reasoning", "line count", "addition rule", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


def _generate_position_movement_question(q_id: int, difficulty: str, color: str) -> dict:
    """Generate questions where a dot/element moves position within cells."""

    positions = {
        "top-left": (0.3, 0.3),
        "top-right": (0.7, 0.3),
        "bottom-left": (0.3, 0.7),
        "bottom-right": (0.7, 0.7),
        "center": (0.5, 0.5),
        "top-center": (0.5, 0.3),
        "bottom-center": (0.5, 0.7),
        "left-center": (0.3, 0.5),
        "right-center": (0.7, 0.5),
    }

    corner_cycle = ["top-left", "top-right", "bottom-right", "bottom-left"]

    def _draw_dot_in_box(cx: float, cy: float, pos_name: str, color: str,
                          cell_size: int = 90) -> str:
        half = cell_size * 0.4
        px_frac, py_frac = positions[pos_name]
        dot_x = cx - half + px_frac * half * 2
        dot_y = cy - half + py_frac * half * 2
        box = (f"<rect x='{cx - half:.1f}' y='{cy - half:.1f}' "
               f"width='{half*2:.1f}' height='{half*2:.1f}' "
               f"fill='none' stroke='#666' stroke-width='1' stroke-dasharray='2,2'/>")
        dot = f"<circle cx='{dot_x:.1f}' cy='{dot_y:.1f}' r='6' fill='{color}'/>"
        return box + dot

    if difficulty == "Easy":
        # Dot moves clockwise through corners across each row
        start_idx = random.randint(0, 3)
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                pos_idx = (start_idx + col) % 4
                pos = corner_cycle[pos_idx]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_dot_in_box(cx, cy, pos, color))
        answer_pos = corner_cycle[(start_idx + 2) % 4]
        other_positions = [p for p in corner_cycle if p != answer_pos]
        random.shuffle(other_positions)
        choices_positions = [answer_pos] + other_positions[:3]
        random.shuffle(choices_positions)
        answer_label = chr(65 + choices_positions.index(answer_pos))
        choices = []
        for i, p in enumerate(choices_positions):
            label = chr(65 + i)
            svg = _choice_svg(_draw_dot_in_box(35, 35, p, color, cell_size=70))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_dot_in_box(35, 35, answer_pos, color, cell_size=70))
        explanation = (f"The dot moves clockwise through the corners of the box in each row. "
                       f"The missing cell needs the dot in the {answer_pos} position.")
        tags = ["abstract reasoning", "matrix reasoning", "position", "movement", "clockwise"]

    elif difficulty == "Medium":
        # Dot moves CW across rows, and also shifts position down columns
        row_offsets = [0, 1, 2]
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                pos_idx = (col + row_offsets[row]) % 4
                pos = corner_cycle[pos_idx]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    cells.append(_draw_dot_in_box(cx, cy, pos, color))
        answer_pos = corner_cycle[(2 + row_offsets[2]) % 4]
        other_positions = [p for p in corner_cycle if p != answer_pos]
        random.shuffle(other_positions)
        choices_positions = [answer_pos] + other_positions[:3]
        random.shuffle(choices_positions)
        answer_label = chr(65 + choices_positions.index(answer_pos))
        choices = []
        for i, p in enumerate(choices_positions):
            label = chr(65 + i)
            svg = _choice_svg(_draw_dot_in_box(35, 35, p, color, cell_size=70))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_draw_dot_in_box(35, 35, answer_pos, color, cell_size=70))
        explanation = (f"The dot moves clockwise across each row, and each row starts one position "
                       f"further in the cycle. The missing cell needs the dot at {answer_pos}.")
        tags = ["abstract reasoning", "matrix reasoning", "position", "movement", "offset"]

    else:  # Hard
        # Two dots moving in opposite directions
        start1 = random.randint(0, 3)
        start2 = (start1 + 2) % 4  # opposite corner
        cells = []
        for row in range(3):
            for col in range(3):
                cx, cy = _cell_center(row, col)
                step = row * 3 + col
                pos1_idx = (start1 + step) % 4
                pos2_idx = (start2 - step) % 4
                pos1 = corner_cycle[pos1_idx]
                pos2 = corner_cycle[pos2_idx]
                if row == 2 and col == 2:
                    cells.append(_question_mark(cx, cy))
                else:
                    half = 90 * 0.4
                    px1, py1 = positions[pos1]
                    px2, py2 = positions[pos2]
                    dot1_x = cx - half + px1 * half * 2
                    dot1_y = cy - half + py1 * half * 2
                    dot2_x = cx - half + px2 * half * 2
                    dot2_y = cy - half + py2 * half * 2
                    box = (f"<rect x='{cx - half:.1f}' y='{cy - half:.1f}' "
                           f"width='{half*2:.1f}' height='{half*2:.1f}' "
                           f"fill='none' stroke='#666' stroke-width='1' stroke-dasharray='2,2'/>")
                    d1 = f"<circle cx='{dot1_x:.1f}' cy='{dot1_y:.1f}' r='5' fill='{color}'/>"
                    d2 = f"<circle cx='{dot2_x:.1f}' cy='{dot2_y:.1f}' r='5' fill='#F44336'/>"
                    cells.append(box + d1 + d2)
        # Answer
        step = 8
        ans_pos1 = corner_cycle[(start1 + step) % 4]
        ans_pos2 = corner_cycle[(start2 - step) % 4]
        # Build answer and distractors
        def _build_two_dot_choice(p1, p2, color1, color2):
            half = 70 * 0.4
            cx, cy = 35, 35
            px1, py1 = positions[p1]
            px2, py2 = positions[p2]
            d1x = cx - half + px1 * half * 2
            d1y = cy - half + py1 * half * 2
            d2x = cx - half + px2 * half * 2
            d2y = cy - half + py2 * half * 2
            box = (f"<rect x='{cx - half:.1f}' y='{cy - half:.1f}' "
                   f"width='{half*2:.1f}' height='{half*2:.1f}' "
                   f"fill='none' stroke='#666' stroke-width='1' stroke-dasharray='2,2'/>")
            d1 = f"<circle cx='{d1x:.1f}' cy='{d1y:.1f}' r='5' fill='{color1}'/>"
            d2 = f"<circle cx='{d2x:.1f}' cy='{d2y:.1f}' r='5' fill='{color2}'/>"
            return box + d1 + d2

        answer_key = (ans_pos1, ans_pos2)
        distractors = []
        for _ in range(10):
            d1 = corner_cycle[random.randint(0, 3)]
            d2 = corner_cycle[random.randint(0, 3)]
            if (d1, d2) != answer_key:
                distractors.append((d1, d2))
        distractors = list(set(distractors))[:3]
        while len(distractors) < 3:
            distractors.append((corner_cycle[(start1 + 1) % 4], corner_cycle[(start2 + 1) % 4]))
        choices_data = [answer_key] + distractors[:3]
        random.shuffle(choices_data)
        answer_label = chr(65 + choices_data.index(answer_key))
        choices = []
        for i, (p1, p2) in enumerate(choices_data):
            label = chr(65 + i)
            svg = _choice_svg(_build_two_dot_choice(p1, p2, color, "#F44336"))
            choices.append(f"{label}: {svg}")
        answer_svg = _choice_svg(_build_two_dot_choice(ans_pos1, ans_pos2, color, "#F44336"))
        explanation = (f"Two dots move in opposite directions: the blue dot moves clockwise, "
                       f"the red dot moves counterclockwise. Following the pattern, "
                       f"the blue dot should be at {ans_pos1} and the red dot at {ans_pos2}.")
        tags = ["abstract reasoning", "matrix reasoning", "position", "dual movement", "advanced"]

    matrix_svg = _make_matrix_svg(cells)
    return {
        "id": q_id,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Matrix Reasoning",
        "difficulty": difficulty,
        "question": f"Which figure correctly completes the matrix?\n\n{matrix_svg}",
        "choices": choices,
        "answer": f"{answer_label}: {answer_svg}",
        "explanation": explanation,
        "tags": tags,
    }


# ---------------------------------------------------------------------------
# Main generation logic
# ---------------------------------------------------------------------------

GENERATORS = [
    _generate_rotation_question,
    _generate_dot_count_question,
    _generate_shape_progression_question,
    _generate_shading_question,
    _generate_size_progression_question,
    _generate_distribution_question,
    _generate_rotation_shading_combo_question,
    _generate_line_count_question,
    _generate_position_movement_question,
]


def generate_questions() -> list[dict]:
    """Generate 600 matrix reasoning questions: 200 Easy, 200 Medium, 200 Hard."""
    questions: list[dict] = []
    q_id = 1

    difficulties = ["Easy", "Medium", "Hard"]
    questions_per_difficulty = 200

    for diff in difficulties:
        # Distribute evenly across generator types
        qs_per_gen = questions_per_difficulty // len(GENERATORS)
        remainder = questions_per_difficulty % len(GENERATORS)

        for gen_idx, generator in enumerate(GENERATORS):
            count = qs_per_gen + (1 if gen_idx < remainder else 0)
            for i in range(count):
                # Use a unique seed per question that produces different random states
                # The seed combines question index, generator, and iteration
                # to ensure no two questions get the same random sequence
                unique_seed = 1000 * gen_idx + 10000 * i + q_id * 31 + ord(diff[0]) * 97
                random.seed(unique_seed)
                color = random.choice(COLORS)
                q = generator(q_id, diff, color)
                questions.append(q)
                q_id += 1

    # Deduplicate: if any question SVGs are identical, regenerate with new seeds
    seen_svgs: set[str] = set()
    for idx, q in enumerate(questions):
        svg = q["question"]
        attempts = 0
        while svg in seen_svgs and attempts < 200:
            attempts += 1
            # Deterministic retry seed based on index and attempt
            retry_seed = 2000000 + idx * 997 + attempts * 31
            random.seed(retry_seed)
            color = random.choice(COLORS)
            # Try different generators to maximize variety
            gen_idx = (idx + attempts) % len(GENERATORS)
            new_q = GENERATORS[gen_idx](q["id"], q["difficulty"], color)
            q.update(new_q)
            svg = q["question"]
        seen_svgs.add(svg)

    # Final shuffle within each difficulty band to mix question types
    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]

    random.seed(42)
    random.shuffle(easy)
    random.shuffle(medium)
    random.shuffle(hard)

    # Reassign IDs after shuffle
    all_questions = easy + medium + hard
    for idx, q in enumerate(all_questions):
        q["id"] = idx + 1

    return all_questions


def main() -> None:
    questions = generate_questions()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(questions)} matrix reasoning questions → {OUTPUT_PATH}")
    # Verify distribution
    for diff in ["Easy", "Medium", "Hard"]:
        count = sum(1 for q in questions if q["difficulty"] == diff)
        print(f"  {diff}: {count}")


if __name__ == "__main__":
    main()
