"""Generate abstract reasoning figure series questions with SVG visuals.

Produces 600 questions (200 Easy, 200 Medium, 200 Hard) with mathematically
correct SVG diagrams for figure series patterns including:
- Next figure prediction
- Missing figure identification
- Rotation-based sequences
- Transformation-based sequences
- Grid-based reasoning

Usage:
    python scripts/gen_figure_series_questions.py
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
    / "analytical-ability" / "abstract-reasoning" / "figure-series"
    / "questions.json"
)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

COLORS = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#E91E63", "#00BCD4"]
DIRECTIONS_4 = ["up", "right", "down", "left"]
DIRECTIONS_8 = ["up", "up-right", "right", "down-right", "down", "down-left", "left", "up-left"]


def _svg_wrap(content: str, w: int = 280, h: int = 80) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>"
        f"{content}</svg>"
    )


def _svg_choice_wrap(content: str, w: int = 60, h: int = 60) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>"
        f"{content}</svg>"
    )


def _arrow_svg(cx: float, cy: float, direction: str, size: float = 18,
               color: str = "#2196F3", filled: bool = False) -> str:
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


def _polygon_svg(cx: float, cy: float, sides: int, radius: float = 20,
                 color: str = "#2196F3", fill: str = "none",
                 rotation_deg: float = -90) -> str:
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


def _circle_svg(cx: float, cy: float, r: float = 20,
                color: str = "#2196F3", fill: str = "none") -> str:
    return f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' fill='{fill}' stroke='{color}' stroke-width='2'/>"


def _rect_svg(x: float, y: float, w: float, h: float,
              color: str = "#2196F3", fill: str = "none") -> str:
    return f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' fill='{fill}' stroke='{color}' stroke-width='2'/>"


def _dot_svg(cx: float, cy: float, r: float = 4, color: str = "#F44336") -> str:
    return f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' fill='{color}'/>"


def _text_svg(x: float, y: float, text: str, size: int = 10,
              color: str = "#888") -> str:
    return (
        f"<text x='{x:.1f}' y='{y:.1f}' text-anchor='middle' "
        f"font-size='{size}' fill='{color}' font-family='sans-serif'>{text}</text>"
    )


def _separator_svg(x: float, y1: float, y2: float) -> str:
    return f"<line x1='{x:.1f}' y1='{y1:.1f}' x2='{x:.1f}' y2='{y2:.1f}' stroke='#666' stroke-width='1' stroke-dasharray='3,2'/>"


def _star_svg(cx: float, cy: float, points: int = 5, outer_r: float = 20,
              inner_r: float = 10, color: str = "#FF9800", fill: str = "none",
              rotation_deg: float = -90) -> str:
    coords = []
    for i in range(points * 2):
        r = outer_r if i % 2 == 0 else inner_r
        angle = math.radians(rotation_deg + (360 / (points * 2)) * i)
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        coords.append(f"{px:.1f},{py:.1f}")
    return f"<polygon points='{' '.join(coords)}' fill='{fill}' stroke='{color}' stroke-width='2'/>"


def _cross_svg(cx: float, cy: float, size: float = 16, color: str = "#2196F3",
               rotation_deg: float = 0) -> str:
    """Draw a plus/cross shape."""
    t = size * 0.3  # thickness
    # Horizontal bar + vertical bar
    rad = math.radians(rotation_deg)
    # Simple approach: use a transform
    bars = (
        f"<rect x='{cx - size}' y='{cy - t}' width='{size * 2}' height='{t * 2}' "
        f"fill='{color}' transform='rotate({rotation_deg},{cx},{cy})'/>"
        f"<rect x='{cx - t}' y='{cy - size}' width='{t * 2}' height='{size * 2}' "
        f"fill='{color}' transform='rotate({rotation_deg},{cx},{cy})'/>"
    )
    return bars


def _line_svg(x1: float, y1: float, x2: float, y2: float,
              color: str = "#2196F3", width: float = 2) -> str:
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{color}' stroke-width='{width}'/>"


# ---------------------------------------------------------------------------
# Question builder
# ---------------------------------------------------------------------------


def _make_question(id_: int, difficulty: str, question: str,
                   svg_question: str, choices: list[dict],
                   answer: str, explanation: str, tags: list[str]) -> dict:
    stem_with_svg = f"{question}\n\n{svg_question}"
    option_strings = [f"{c['label']}: {c['svg']}" for c in choices]
    correct_option = next(o for o in option_strings if o.startswith(f"{answer}: "))
    return {
        "id": id_,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Figure Series",
        "difficulty": difficulty,
        "question": stem_with_svg,
        "choices": option_strings,
        "answer": correct_option,
        "explanation": explanation,
        "tags": tags,
    }


# ---------------------------------------------------------------------------
# EASY generators — single-rule sequences
# ---------------------------------------------------------------------------


def gen_arrow_rotation_cw(id_: int, start: int = 0, steps: int = 4) -> dict:
    """Arrow rotates 90° clockwise each step. Predict next."""
    color = random.choice(COLORS)
    seq = [DIRECTIONS_4[(start + i) % 4] for i in range(steps)]
    show = seq[:-1]
    correct = seq[-1]

    parts = []
    for i, d in enumerate(show):
        cx = 30 + i * 55
        parts.append(_arrow_svg(cx, 40, d, color=color))
    parts.append(_separator_svg(30 + len(show) * 55 - 20, 5, 75))
    parts.append(_text_svg(30 + len(show) * 55 + 10, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=30 + (len(show) + 1) * 55, h=80)

    wrong = [d for d in DIRECTIONS_4 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Easy",
        question="Which figure comes next in the series?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow rotates 90° clockwise each step: {' → '.join(show)} → {correct}.",
        tags=["figure series", "next figure prediction", "rotation", "clockwise"],
    )


def gen_arrow_rotation_ccw(id_: int, start: int = 0) -> dict:
    """Arrow rotates 90° counterclockwise."""
    color = random.choice(COLORS)
    ccw = ["up", "left", "down", "right"]
    seq = [ccw[(start + i) % 4] for i in range(4)]
    show = seq[:3]
    correct = seq[3]

    parts = []
    for i, d in enumerate(show):
        cx = 30 + i * 55
        parts.append(_arrow_svg(cx, 40, d, color=color))
    parts.append(_separator_svg(190, 5, 75))
    parts.append(_text_svg(220, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    wrong = [d for d in DIRECTIONS_4 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Easy",
        question="Which figure comes next in the series?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow rotates 90° counterclockwise each step: {' → '.join(show)} → {correct}.",
        tags=["figure series", "next figure prediction", "rotation", "counterclockwise"],
    )


def gen_shape_count_increase(id_: int, start: int = 1, step: int = 1,
                             shape: str = "circle") -> dict:
    """Number of shapes increases by a fixed step."""
    color = random.choice(COLORS)
    counts = [start + step * i for i in range(4)]
    show_counts = counts[:3]
    correct_count = counts[3]

    def _draw_shapes(cx: float, cy: float, count: int, sz: float = 6) -> str:
        elems = []
        cols = min(count, 4)
        rows = math.ceil(count / cols) if cols > 0 else 1
        sx = cx - (cols - 1) * sz
        sy = cy - (rows - 1) * sz
        for idx in range(count):
            r = idx // cols
            c = idx % cols
            px = sx + c * sz * 2
            py = sy + r * sz * 2
            if shape == "circle":
                elems.append(_circle_svg(px, py, r=sz * 0.7, color=color, fill=color))
            elif shape == "square":
                elems.append(_rect_svg(px - sz * 0.6, py - sz * 0.6, sz * 1.2, sz * 1.2, color=color, fill=color))
            else:
                elems.append(_polygon_svg(px, py, 3, radius=sz * 0.7, color=color, fill=color))
        return "".join(elems)

    parts = []
    for i, cnt in enumerate(show_counts):
        cx = 40 + i * 70
        parts.append(_rect_svg(cx - 28, 10, 56, 56, color="#999"))
        parts.append(_draw_shapes(cx, 38, cnt))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    wrong_counts = [correct_count + 1, correct_count - 1, correct_count + 2]
    wrong_counts = [w for w in wrong_counts if w > 0 and w != correct_count][:3]
    while len(wrong_counts) < 3:
        wrong_counts.append(correct_count + 3)
    all_opts = wrong_counts + [correct_count]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, cnt in enumerate(all_opts):
        content = _rect_svg(5, 5, 50, 50, color="#999")
        content += _draw_shapes(30, 30, cnt, sz=5)
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if cnt == correct_count:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Easy",
        question="How many shapes should appear in the next figure?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The number of {shape}s increases by {step} each step: {' → '.join(str(c) for c in counts)}.",
        tags=["figure series", "next figure prediction", "count progression", "transformation"],
    )


def gen_size_growth(id_: int, shape: str = "circle") -> dict:
    """Shape grows larger each step."""
    color = random.choice(COLORS)
    sizes = [8, 13, 18, 23]

    def _draw(cx: float, cy: float, sz: float) -> str:
        if shape == "circle":
            return _circle_svg(cx, cy, r=sz, color=color)
        elif shape == "square":
            return _rect_svg(cx - sz, cy - sz, sz * 2, sz * 2, color=color)
        else:
            return _polygon_svg(cx, cy, 3, radius=sz, color=color)

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_draw(cx, 40, sizes[i]))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_sz = sizes[3]
    wrong_szs = [sizes[0], sizes[1], sizes[2]]
    all_opts = wrong_szs + [correct_sz]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, sz in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_draw(30, 30, sz))
        choices.append({"label": labels[i], "svg": svg_c})
        if sz == correct_sz:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Easy",
        question="Which figure continues the size progression?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The {shape} grows larger by a fixed amount each step. The next figure is the largest.",
        tags=["figure series", "next figure prediction", "size progression", "transformation"],
    )


def gen_alternating_shapes(id_: int, variant: int = 0) -> dict:
    """Two shapes alternate: A-B-A-B."""
    color = random.choice(COLORS)
    pairs = [("circle", "square"), ("triangle", "circle"), ("square", "triangle"),
             ("circle", "triangle"), ("square", "circle"), ("triangle", "square")]
    pair = pairs[variant % len(pairs)]
    seq = [pair[i % 2] for i in range(4)]
    show = seq[:3]
    correct = seq[3]

    def _draw(cx: float, cy: float, name: str, sz: float = 18) -> str:
        if name == "circle":
            return _circle_svg(cx, cy, r=sz, color=color)
        elif name == "square":
            return _rect_svg(cx - sz, cy - sz, sz * 2, sz * 2, color=color)
        else:
            return _polygon_svg(cx, cy, 3, radius=sz, color=color)

    parts = []
    for i, s in enumerate(show):
        cx = 40 + i * 70
        parts.append(_draw(cx, 40, s))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    all_shapes = ["circle", "square", "triangle", "pentagon"]
    wrong = [s for s in all_shapes if s != correct][:3]
    all_opts = wrong + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, s in enumerate(all_opts):
        if s == "pentagon":
            svg_c = _svg_choice_wrap(_polygon_svg(30, 30, 5, radius=20, color=color))
        else:
            svg_c = _svg_choice_wrap(_draw(30, 30, s))
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Easy",
        question="Which figure comes next in the alternating series?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The shapes alternate: {pair[0]} → {pair[1]} → {pair[0]} → {pair[1]}. Next is {correct}.",
        tags=["figure series", "next figure prediction", "alternating pattern"],
    )


def gen_shading_progression(id_: int, variant: int = 0) -> dict:
    """Shading increases from empty to full in quarters."""
    color = random.choice(COLORS)
    start = variant % 2
    levels = [start + i for i in range(4)]

    def _shaded_circle(cx: float, cy: float, level: int, r: float = 18) -> str:
        base = _circle_svg(cx, cy, r=r, color=color)
        if level >= 4:
            return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{color}' stroke='{color}' stroke-width='2'/>"
        elif level == 3:
            return base + f"<path d='M{cx},{cy} L{cx},{cy-r} A{r},{r} 0 1,1 {cx+r},{cy} Z' fill='{color}' opacity='0.6'/><path d='M{cx},{cy} L{cx+r},{cy} A{r},{r} 0 0,1 {cx},{cy+r} Z' fill='{color}' opacity='0.6'/><path d='M{cx},{cy} L{cx},{cy+r} A{r},{r} 0 0,1 {cx-r},{cy} Z' fill='{color}' opacity='0.6'/>"
        elif level == 2:
            return base + f"<path d='M{cx},{cy-r} A{r},{r} 0 0,0 {cx},{cy+r} L{cx},{cy-r} Z' fill='{color}' opacity='0.6'/>"
        elif level == 1:
            return base + f"<path d='M{cx},{cy} L{cx},{cy-r} A{r},{r} 0 0,0 {cx-r},{cy} Z' fill='{color}' opacity='0.6'/>"
        return base

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_shaded_circle(cx, 40, levels[i]))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_level = levels[3]
    wrong_levels = [l for l in range(5) if l != correct_level]
    random.shuffle(wrong_levels)
    all_opts = wrong_levels[:3] + [correct_level]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, lvl in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_shaded_circle(30, 30, lvl, r=22))
        choices.append({"label": labels[i], "svg": svg_c})
        if lvl == correct_level:
            ans = labels[i]

    shade_names = ["empty", "quarter-filled", "half-filled", "three-quarter-filled", "fully filled"]
    return _make_question(
        id_=id_, difficulty="Easy",
        question="The shading increases each step. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The circle's shading increases by one quarter each step. Next: {shade_names[correct_level]}.",
        tags=["figure series", "next figure prediction", "shading progression"],
    )


def gen_sides_increase(id_: int, start: int = 3) -> dict:
    """Polygon gains one side each step."""
    color = random.choice(COLORS)
    sides_seq = [start + i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_polygon_svg(cx, 40, sides_seq[i], radius=18, color=color))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct = sides_seq[3]
    wrong = [correct - 2, correct + 1, correct + 2]
    wrong = [w for w in wrong if w >= 3 and w != correct][:3]
    while len(wrong) < 3:
        wrong.append(correct + 3)
    all_opts = wrong + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, s in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_polygon_svg(30, 30, s, radius=22, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct:
            ans = labels[i]

    names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon",
             7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon"}
    return _make_question(
        id_=id_, difficulty="Easy",
        question="Which figure comes next in the series?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Sides increase by 1: {sides_seq[0]} → {sides_seq[1]} → {sides_seq[2]} → {sides_seq[3]} ({names.get(correct, f'{correct}-gon')}).",
        tags=["figure series", "next figure prediction", "side count", "transformation"],
    )


def gen_arrow_180_alternation(id_: int, variant: int = 0) -> dict:
    """Arrow alternates 180° (up/down or left/right)."""
    pairs = [("up", "down"), ("left", "right"), ("up-right", "down-left"), ("up-left", "down-right")]
    pair = pairs[variant % len(pairs)]
    seq = [pair[i % 2] for i in range(4)]
    color = random.choice(COLORS)

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 40, seq[i], color=color))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct = seq[3]
    wrong = [d for d in DIRECTIONS_8 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Easy",
        question="Which figure comes next in the series?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow alternates 180°: {pair[0]} ↔ {pair[1]}. Next: {correct}.",
        tags=["figure series", "next figure prediction", "alternating", "180 degrees"],
    )



def gen_dot_position_movement(id_: int, variant: int = 0) -> dict:
    """A dot moves through positions in a frame (clockwise corners)."""
    color = random.choice(COLORS)
    corners = [(12, 12), (48, 12), (48, 48), (12, 48)]
    start = variant % 4
    seq = [(start + i) % 4 for i in range(4)]

    def _frame_dot(x_off: float, y_off: float, corner_idx: int) -> str:
        frame = _rect_svg(x_off, y_off, 40, 40, color="#666")
        dx, dy = corners[corner_idx]
        return frame + _dot_svg(x_off + dx, y_off + dy, r=5, color=color)

    parts = []
    for i in range(3):
        x = 15 + i * 65
        parts.append(_frame_dot(x, 15, seq[i]))
    parts.append(_separator_svg(215, 5, 75))
    parts.append(_text_svg(240, 40, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=265, h=75)

    correct = seq[3]
    wrong = [c for c in range(4) if c != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, c in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_frame_dot(5, 5, c))
        choices.append({"label": labels[i], "svg": svg_c})
        if c == correct:
            ans = labels[i]

    corner_names = ["top-left", "top-right", "bottom-right", "bottom-left"]
    path = " → ".join(corner_names[seq[i]] for i in range(4))
    return _make_question(
        id_=id_, difficulty="Easy",
        question="The dot moves to a new position each step. Where does it go next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The dot moves clockwise through corners: {path}.",
        tags=["figure series", "next figure prediction", "movement", "position"],
    )


# ---------------------------------------------------------------------------
# MEDIUM generators — two-rule or missing-figure sequences
# ---------------------------------------------------------------------------


def gen_rotation_45(id_: int, start: int = 0) -> dict:
    """Arrow rotates 45° each step (8 positions)."""
    color = random.choice(COLORS)
    seq = [DIRECTIONS_8[(start + i) % 8] for i in range(4)]
    show = seq[:3]
    correct = seq[3]

    parts = []
    for i, d in enumerate(show):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 40, d, size=16, color=color))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    wrong = [d for d in DIRECTIONS_8 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, size=16, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Medium",
        question="Which figure comes next in the series?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow rotates 45° clockwise each step: {' → '.join(seq)}.",
        tags=["figure series", "next figure prediction", "rotation", "45 degrees"],
    )


def gen_rotation_plus_shading(id_: int, start: int = 0) -> dict:
    """Arrow rotates 90° CW AND alternates filled/empty."""
    color = random.choice(COLORS)
    dir_seq = [DIRECTIONS_4[(start + i) % 4] for i in range(4)]
    fill_seq = [i % 2 == 1 for i in range(4)]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 40, dir_seq[i], color=color, filled=fill_seq[i]))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_dir = dir_seq[3]
    correct_fill = fill_seq[3]
    other_dirs = [d for d in DIRECTIONS_4 if d != correct_dir]
    random.shuffle(other_dirs)
    distractors = [
        (other_dirs[0], correct_fill),
        (other_dirs[1], not correct_fill),
        (correct_dir, not correct_fill),
    ]
    all_opts = distractors + [(correct_dir, correct_fill)]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (d, f) in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color, filled=f))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir and f == correct_fill:
            ans = labels[i]

    fill_name = "filled" if correct_fill else "empty"
    return _make_question(
        id_=id_, difficulty="Medium",
        question="Two rules operate. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Arrow rotates 90° CW. Rule 2: Fill alternates empty/filled. Next: {correct_dir}, {fill_name}.",
        tags=["figure series", "next figure prediction", "rotation", "shading", "multi-rule"],
    )


def gen_missing_middle(id_: int, start: int = 0) -> dict:
    """Show positions 1, ?, 3, 4 — find the missing 2nd figure (rotation)."""
    color = random.choice(COLORS)
    seq = [DIRECTIONS_4[(start + i) % 4] for i in range(4)]
    # Show 1st, gap, 3rd, 4th
    correct = seq[1]

    parts = []
    positions = [0, 2, 3]
    labels_pos = ["1", "3", "4"]
    for idx, pos in enumerate(positions):
        cx = 30 + idx * 60
        parts.append(_arrow_svg(cx, 40, seq[pos], color=color))
        parts.append(_text_svg(cx, 72, labels_pos[idx], size=9))
    # Insert question mark for position 2
    parts.append(_text_svg(210, 40, "2 = ?", size=14, color="#E91E63"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    wrong = [d for d in DIRECTIONS_4 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Medium",
        question="Which figure belongs in position 2?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow rotates 90° CW each step: {seq[0]} → ? → {seq[2]} → {seq[3]}. The missing figure points {correct}.",
        tags=["figure series", "missing figure identification", "rotation"],
    )


def gen_polygon_rotation_series(id_: int, sides: int = 4, rot_step: float = 45) -> dict:
    """A polygon rotates by a fixed angle each step."""
    color = random.choice(COLORS)
    rots = [rot_step * i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        content = _polygon_svg(cx, 40, sides, radius=18, color=color, rotation_deg=-90 + rots[i])
        angle = math.radians(-90 + rots[i])
        dot_x = cx + 18 * math.cos(angle)
        dot_y = 40 + 18 * math.sin(angle)
        content += _dot_svg(dot_x, dot_y, r=3, color="#F44336")
        parts.append(content)
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_rot = rots[3]
    wrong_rots = [correct_rot + 45, correct_rot - 45, correct_rot + 90]
    all_opts = wrong_rots + [correct_rot]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, rot in enumerate(all_opts):
        content = _polygon_svg(30, 30, sides, radius=22, color=color, rotation_deg=-90 + rot)
        angle = math.radians(-90 + rot)
        dx = 30 + 22 * math.cos(angle)
        dy = 30 + 22 * math.sin(angle)
        content += _dot_svg(dx, dy, r=3, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if rot == correct_rot:
            ans = labels[i]

    names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon"}
    return _make_question(
        id_=id_, difficulty="Medium",
        question="The shape rotates by a fixed angle. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The {names.get(sides, 'polygon')} rotates {rot_step}° each step. Track the red dot. Next rotation: {correct_rot}° total.",
        tags=["figure series", "next figure prediction", "rotation", "polygon"],
    )


def gen_count_plus_rotation(id_: int, start_dir: int = 0, start_count: int = 1) -> dict:
    """Dots increase AND arrow rotates simultaneously."""
    color = random.choice(COLORS)
    dir_seq = [DIRECTIONS_4[(start_dir + i) % 4] for i in range(4)]
    count_seq = [start_count + i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 30, dir_seq[i], size=14, color=color))
        for d in range(count_seq[i]):
            parts.append(_dot_svg(cx - 8 + d * 7, 60, r=3, color="#F44336"))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_dir = dir_seq[3]
    correct_count = count_seq[3]
    other_dirs = [d for d in DIRECTIONS_4 if d != correct_dir]
    random.shuffle(other_dirs)
    distractors = [
        (other_dirs[0], correct_count),
        (other_dirs[1], correct_count - 1),
        (correct_dir, correct_count - 1),
    ]
    all_opts = distractors + [(correct_dir, correct_count)]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (d, cnt) in enumerate(all_opts):
        content = _arrow_svg(30, 22, d, size=12, color=color)
        for di in range(cnt):
            content += _dot_svg(30 - 6 + di * 6, 48, r=3, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir and cnt == correct_count:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Medium",
        question="Two rules operate. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Arrow rotates 90° CW ({' → '.join(dir_seq)}). Rule 2: Dot count increases by 1 ({' → '.join(str(c) for c in count_seq)}).",
        tags=["figure series", "next figure prediction", "rotation", "count", "multi-rule"],
    )


def gen_shape_cycle_3(id_: int, variant: int = 0) -> dict:
    """Three shapes cycle: A-B-C-A-B-C. Show 4, predict 5th."""
    color = random.choice(COLORS)
    cycles = [
        ["circle", "square", "triangle"],
        ["triangle", "circle", "square"],
        ["square", "triangle", "circle"],
    ]
    cycle = cycles[variant % len(cycles)]
    seq = [cycle[i % 3] for i in range(5)]
    show = seq[:4]
    correct = seq[4]

    def _draw(cx: float, cy: float, name: str, sz: float = 16) -> str:
        if name == "circle":
            return _circle_svg(cx, cy, r=sz, color=color)
        elif name == "square":
            return _rect_svg(cx - sz, cy - sz, sz * 2, sz * 2, color=color)
        else:
            return _polygon_svg(cx, cy, 3, radius=sz, color=color)

    parts = []
    for i, s in enumerate(show):
        cx = 30 + i * 55
        parts.append(_draw(cx, 40, s))
    parts.append(_separator_svg(250, 5, 75))
    parts.append(_text_svg(275, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=300, h=80)

    all_shapes = ["circle", "square", "triangle"]
    wrong = [s for s in all_shapes if s != correct]
    wrong.append("pentagon")
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, s in enumerate(all_opts):
        if s == "pentagon":
            svg_c = _svg_choice_wrap(_polygon_svg(30, 30, 5, radius=20, color=color))
        else:
            svg_c = _svg_choice_wrap(_draw(30, 30, s))
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Medium",
        question="The shapes follow a repeating cycle. Which comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The cycle is {cycle[0]} → {cycle[1]} → {cycle[2]} → repeat. After showing {' → '.join(show)}, next is {correct}.",
        tags=["figure series", "next figure prediction", "cyclic pattern"],
    )


def gen_star_rotation(id_: int, rot_step: float = 36, variant: int = 0) -> dict:
    """A star rotates by a fixed angle each step."""
    color = random.choice(COLORS)
    rots = [rot_step * (variant + i) for i in range(4)]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_star_svg(cx, 40, points=5, outer_r=18, inner_r=9,
                               color=color, rotation_deg=-90 + rots[i]))
        # Marker dot at first outer point
        angle = math.radians(-90 + rots[i])
        dx = cx + 18 * math.cos(angle)
        dy = 40 + 18 * math.sin(angle)
        parts.append(_dot_svg(dx, dy, r=3, color="#F44336"))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_rot = rots[3]
    wrong_rots = [correct_rot + rot_step, correct_rot - rot_step, correct_rot + rot_step * 2]
    all_opts = wrong_rots + [correct_rot]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, rot in enumerate(all_opts):
        content = _star_svg(30, 30, points=5, outer_r=22, inner_r=11,
                            color=color, rotation_deg=-90 + rot)
        angle = math.radians(-90 + rot)
        dx = 30 + 22 * math.cos(angle)
        dy = 30 + 22 * math.sin(angle)
        content += _dot_svg(dx, dy, r=3, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if rot == correct_rot:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Medium",
        question="The star rotates each step. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The star rotates {rot_step}° each step. Track the red marker dot to confirm orientation.",
        tags=["figure series", "next figure prediction", "rotation", "star"],
    )


def gen_missing_in_count_series(id_: int, start: int = 2, step: int = 2) -> dict:
    """Count series with missing middle: show 1st, ?, 3rd, 4th."""
    color = random.choice(COLORS)
    counts = [start + step * i for i in range(4)]
    correct_count = counts[1]

    def _draw_dots(cx: float, cy: float, count: int) -> str:
        elems = [_rect_svg(cx - 25, cy - 25, 50, 50, color="#999")]
        cols = min(count, 4)
        rows = math.ceil(count / cols) if cols > 0 else 1
        for idx in range(count):
            r = idx // cols
            c = idx % cols
            px = cx - (cols - 1) * 6 + c * 12
            py = cy - (rows - 1) * 6 + r * 12
            elems.append(_dot_svg(px, py, r=4, color=color))
        return "".join(elems)

    parts = []
    # Show positions 1, 3, 4 with labels
    shown = [(0, counts[0], "1"), (2, counts[2], "3"), (3, counts[3], "4")]
    for idx, (_, cnt, lbl) in enumerate(shown):
        cx = 35 + idx * 65
        parts.append(_draw_dots(cx, 38, cnt))
        parts.append(_text_svg(cx, 72, lbl, size=9))
    parts.append(_text_svg(240, 38, "2 = ?", size=14, color="#E91E63"))
    svg_q = _svg_wrap("".join(parts), w=270, h=80)

    wrong_counts = [correct_count + step, correct_count - step, correct_count + 1]
    wrong_counts = [w for w in wrong_counts if w > 0 and w != correct_count][:3]
    while len(wrong_counts) < 3:
        wrong_counts.append(correct_count + step * 2)
    all_opts = wrong_counts + [correct_count]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, cnt in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_draw_dots(30, 30, cnt))
        choices.append({"label": labels[i], "svg": svg_c})
        if cnt == correct_count:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Medium",
        question="Which figure belongs in position 2?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Dots increase by {step} each step: {counts[0]} → ? → {counts[2]} → {counts[3]}. Missing: {correct_count}.",
        tags=["figure series", "missing figure identification", "count progression"],
    )


# ---------------------------------------------------------------------------
# HARD generators — multi-rule, grid, nested, complex sequences
# ---------------------------------------------------------------------------


def gen_triple_rule(id_: int, variant: int = 0) -> dict:
    """Three simultaneous rules: rotation + dot count + size."""
    color = random.choice(COLORS)
    start_dir = variant % 4
    dir_seq = [DIRECTIONS_4[(start_dir + i) % 4] for i in range(4)]
    dot_seq = [1 + i for i in range(4)]
    size_seq = [12, 15, 18, 21]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 30, dir_seq[i], size=size_seq[i], color=color))
        for d in range(dot_seq[i]):
            parts.append(_dot_svg(cx - 6 + d * 7, 60, r=2.5, color="#F44336"))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 40, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_dir = dir_seq[3]
    correct_dots = dot_seq[3]
    correct_size = size_seq[3]
    other_dirs = [d for d in DIRECTIONS_4 if d != correct_dir]
    random.shuffle(other_dirs)
    distractors = [
        (other_dirs[0], correct_dots, correct_size),
        (other_dirs[1], correct_dots - 1, correct_size),
        (correct_dir, correct_dots, size_seq[1]),
    ]
    all_opts = distractors + [(correct_dir, correct_dots, correct_size)]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (d, dots, sz) in enumerate(all_opts):
        content = _arrow_svg(30, 22, d, size=sz, color=color)
        for di in range(dots):
            content += _dot_svg(30 - 6 + di * 6, 50, r=2.5, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir and dots == correct_dots and sz == correct_size:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Hard",
        question="Three rules operate simultaneously. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Arrow rotates 90° CW. Rule 2: Dots increase by 1. Rule 3: Arrow grows larger.",
        tags=["figure series", "next figure prediction", "multi-rule", "advanced"],
    )


def gen_nested_shapes_series(id_: int, variant: int = 0) -> dict:
    """Outer shape rotates, inner shape cycles through types."""
    color_outer = "#FF9800"
    color_inner = "#2196F3"
    inner_cycle = ["circle", "square", "triangle"]
    outer_rot_step = 30
    outer_rots = [outer_rot_step * i for i in range(4)]
    inner_seq = [inner_cycle[(variant + i) % 3] for i in range(4)]

    def _draw_nested(cx: float, cy: float, rot: float, inner: str) -> str:
        outer = _polygon_svg(cx, cy, 4, radius=22, color=color_outer, rotation_deg=-90 + rot)
        if inner == "circle":
            inn = _circle_svg(cx, cy, r=8, color=color_inner)
        elif inner == "square":
            inn = _rect_svg(cx - 7, cy - 7, 14, 14, color=color_inner)
        else:
            inn = _polygon_svg(cx, cy, 3, radius=9, color=color_inner)
        return outer + inn

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        parts.append(_draw_nested(cx, 40, outer_rots[i], inner_seq[i]))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_rot = outer_rots[3]
    correct_inner = inner_seq[3]
    wrong_inners = [s for s in inner_cycle if s != correct_inner]
    distractors = [
        (correct_rot, wrong_inners[0]),
        (correct_rot + 30, correct_inner),
        (correct_rot - 30, wrong_inners[1] if len(wrong_inners) > 1 else wrong_inners[0]),
    ]
    all_opts = distractors + [(correct_rot, correct_inner)]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (rot, inn) in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_draw_nested(30, 30, rot, inn))
        choices.append({"label": labels[i], "svg": svg_c})
        if rot == correct_rot and inn == correct_inner:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Hard",
        question="Outer and inner shapes follow independent rules. Which comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Outer square rotates {outer_rot_step}° each step. Rule 2: Inner shape cycles {' → '.join(inner_cycle)}.",
        tags=["figure series", "next figure prediction", "nested", "multi-rule", "advanced"],
    )


def gen_grid_3x3(id_: int, variant: int = 0) -> dict:
    """3x3 grid: rows share shape, columns share shading. Find missing cell."""
    color = "#2196F3"
    shapes = ["circle", "square", "triangle"]
    shadings = ["none", "half", "full"]

    random.seed(42 + variant)
    shape_order = shapes[:]
    shade_order = shadings[:]
    random.shuffle(shape_order)
    random.shuffle(shade_order)

    missing_shape = shape_order[2]
    missing_shade = shade_order[2]

    def _draw_cell(shape: str, shade: str, cx: float, cy: float, r: float = 14) -> str:
        fill = "none"
        opacity = ""
        if shade == "full":
            fill = color
        elif shade == "half":
            fill = color
            opacity = " opacity='0.4'"
        if shape == "circle":
            return f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{fill}'{opacity} stroke='{color}' stroke-width='1.5'/>"
        elif shape == "square":
            return f"<rect x='{cx-r}' y='{cy-r}' width='{r*2}' height='{r*2}' fill='{fill}'{opacity} stroke='{color}' stroke-width='1.5'/>"
        else:
            pts = " ".join(f"{cx + r*math.cos(math.radians(-90 + 120*i)):.1f},{cy + r*math.sin(math.radians(-90 + 120*i)):.1f}" for i in range(3))
            return f"<polygon points='{pts}' fill='{fill}'{opacity} stroke='{color}' stroke-width='1.5'/>"

    grid_parts = []
    cell_size = 50
    for row in range(3):
        for col in range(3):
            cx = 30 + col * cell_size
            cy = 30 + row * cell_size
            grid_parts.append(f"<rect x='{cx-22}' y='{cy-22}' width='44' height='44' fill='none' stroke='#555' stroke-width='0.5'/>")
            if row == 2 and col == 2:
                grid_parts.append(_text_svg(cx, cy + 4, "?", size=16, color="#888"))
            else:
                grid_parts.append(_draw_cell(shape_order[row], shade_order[col], cx, cy))
    svg_q = _svg_wrap("".join(grid_parts), w=180, h=180)

    correct = (missing_shape, missing_shade)
    distractors = [
        (missing_shape, shade_order[0]),
        (shape_order[0], missing_shade),
        (shape_order[1], shade_order[0]),
    ]
    all_opts = distractors + [correct]
    random.shuffle(all_opts)

    # Reset seed
    random.seed(42)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (sh, sd) in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_draw_cell(sh, sd, 30, 30, r=20))
        choices.append({"label": labels[i], "svg": svg_c})
        if sh == correct[0] and sd == correct[1]:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Hard",
        question="Which figure completes the 3×3 grid?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Row rule: same shape per row. Column rule: same shading per column. Missing: {missing_shade}-shaded {missing_shape}.",
        tags=["figure series", "missing figure identification", "grid reasoning", "advanced"],
    )


def gen_rotation_plus_sides_increase(id_: int, start_sides: int = 3,
                                      rot_step: float = 90) -> dict:
    """Shape gains one side AND rotates each step."""
    color = random.choice(COLORS)
    sides_seq = [start_sides + i for i in range(4)]
    rot_seq = [rot_step * i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        content = _polygon_svg(cx, 40, sides_seq[i], radius=18, color=color,
                               rotation_deg=-90 + rot_seq[i])
        angle = math.radians(-90 + rot_seq[i])
        dx = cx + 18 * math.cos(angle)
        dy = 40 + 18 * math.sin(angle)
        content += _dot_svg(dx, dy, r=3, color="#F44336")
        parts.append(content)
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_sides = sides_seq[3]
    correct_rot = rot_seq[3]
    distractors = [
        (correct_sides, correct_rot + 90),
        (correct_sides - 1, correct_rot),
        (correct_sides + 1, correct_rot - 90),
    ]
    all_opts = distractors + [(correct_sides, correct_rot)]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (s, r) in enumerate(all_opts):
        content = _polygon_svg(30, 30, s, radius=22, color=color, rotation_deg=-90 + r)
        angle = math.radians(-90 + r)
        dx = 30 + 22 * math.cos(angle)
        dy = 30 + 22 * math.sin(angle)
        content += _dot_svg(dx, dy, r=3, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct_sides and r == correct_rot:
            ans = labels[i]

    names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon",
             7: "heptagon", 8: "octagon", 9: "nonagon", 10: "decagon"}
    return _make_question(
        id_=id_, difficulty="Hard",
        question="Two rules operate simultaneously. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Sides increase ({' → '.join(str(s) for s in sides_seq)}). Rule 2: Shape rotates {rot_step}° each step.",
        tags=["figure series", "next figure prediction", "rotation", "transformation", "multi-rule"],
    )


def gen_cross_rotation_shading(id_: int, variant: int = 0) -> dict:
    """Cross rotates 45° each step AND shading alternates."""
    color = random.choice(COLORS)
    rots = [45 * i for i in range(4)]
    fills = [variant % 2 == i % 2 for i in range(4)]  # alternating

    parts = []
    for i in range(3):
        cx = 40 + i * 70
        fill_color = color if fills[i] else "none"
        # Use a simplified cross with rotation
        parts.append(
            f"<rect x='{cx-14}' y='{cx-4 + 40 - cx}' width='28' height='8' "
            f"fill='{fill_color}' stroke='{color}' stroke-width='1.5' "
            f"transform='rotate({rots[i]},{cx},40)'/>"
            f"<rect x='{cx-4}' y='{40-14}' width='8' height='28' "
            f"fill='{fill_color}' stroke='{color}' stroke-width='1.5' "
            f"transform='rotate({rots[i]},{cx},40)'/>"
        )
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    correct_rot = rots[3]
    correct_fill = fills[3]
    distractors = [
        (correct_rot, not correct_fill),
        (correct_rot + 45, correct_fill),
        (correct_rot - 45, not correct_fill),
    ]
    all_opts = distractors + [(correct_rot, correct_fill)]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (rot, fl) in enumerate(all_opts):
        fill_c = color if fl else "none"
        content = (
            f"<rect x='16' y='26' width='28' height='8' "
            f"fill='{fill_c}' stroke='{color}' stroke-width='1.5' "
            f"transform='rotate({rot},30,30)'/>"
            f"<rect x='26' y='16' width='8' height='28' "
            f"fill='{fill_c}' stroke='{color}' stroke-width='1.5' "
            f"transform='rotate({rot},30,30)'/>"
        )
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if rot == correct_rot and fl == correct_fill:
            ans = labels[i]

    fill_name = "filled" if correct_fill else "empty"
    return _make_question(
        id_=id_, difficulty="Hard",
        question="The cross follows two rules. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Cross rotates 45° each step (total {correct_rot}°). Rule 2: Fill alternates. Next: {fill_name} at {correct_rot}°.",
        tags=["figure series", "next figure prediction", "rotation", "shading", "multi-rule"],
    )


def gen_directional_progression_8(id_: int, start: int = 0, step: int = 2) -> dict:
    """Arrow moves through 8 directions with a step > 1 (e.g., every 2nd position)."""
    color = random.choice(COLORS)
    seq = [DIRECTIONS_8[(start + step * i) % 8] for i in range(4)]
    show = seq[:3]
    correct = seq[3]

    parts = []
    for i, d in enumerate(show):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 40, d, size=16, color=color))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    wrong = [d for d in DIRECTIONS_8 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, size=16, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    angle_step = step * 45
    return _make_question(
        id_=id_, difficulty="Hard",
        question="The arrow rotates by a non-obvious angle. Which comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow rotates {angle_step}° each step (skipping positions): {' → '.join(seq)}.",
        tags=["figure series", "next figure prediction", "rotation", "advanced"],
    )


def gen_missing_in_grid_row(id_: int, variant: int = 0) -> dict:
    """A row of 4 figures with position 3 missing. Shapes transform progressively."""
    color = random.choice(COLORS)
    # Progressive sides: 3, 4, 5, 6
    base = 3 + (variant % 3)
    sides_seq = [base + i for i in range(4)]
    correct_sides = sides_seq[2]  # missing position 3

    parts = []
    shown_positions = [(0, "1"), (1, "2"), (3, "4")]
    for idx, (pos, lbl) in enumerate(shown_positions):
        cx = 35 + idx * 65
        parts.append(_polygon_svg(cx, 40, sides_seq[pos], radius=18, color=color))
        parts.append(_text_svg(cx, 72, lbl, size=9))
    parts.append(_text_svg(240, 40, "3 = ?", size=14, color="#E91E63"))
    svg_q = _svg_wrap("".join(parts), w=270, h=80)

    wrong = [correct_sides - 1, correct_sides + 1, correct_sides + 2]
    wrong = [w for w in wrong if w >= 3 and w != correct_sides][:3]
    while len(wrong) < 3:
        wrong.append(correct_sides + 3)
    all_opts = wrong + [correct_sides]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, s in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_polygon_svg(30, 30, s, radius=22, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct_sides:
            ans = labels[i]

    names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon",
             7: "heptagon", 8: "octagon", 9: "nonagon"}
    return _make_question(
        id_=id_, difficulty="Hard",
        question="Which figure belongs in position 3?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Sides increase by 1: {sides_seq[0]} → {sides_seq[1]} → ? → {sides_seq[3]}. Missing: {names.get(correct_sides, f'{correct_sides}-gon')}.",
        tags=["figure series", "missing figure identification", "transformation", "advanced"],
    )


def gen_layered_transformation(id_: int, variant: int = 0) -> dict:
    """Shape changes size AND shading AND position simultaneously."""
    color = random.choice(COLORS)
    sizes = [10, 14, 18, 22]
    # Position moves right
    x_positions = [20, 30, 40, 50]
    # Shading cycles: none, half, full, none
    shade_cycle = ["none", "half", "full", "none"]
    shade_seq = [shade_cycle[(variant + i) % 3] for i in range(4)]

    def _draw(cx: float, cy: float, sz: float, shade: str) -> str:
        fill = "none"
        opacity = ""
        if shade == "full":
            fill = color
        elif shade == "half":
            fill = color
            opacity = " opacity='0.4'"
        return f"<circle cx='{cx}' cy='{cy}' r='{sz}' fill='{fill}'{opacity} stroke='{color}' stroke-width='2'/>"

    parts = []
    for i in range(3):
        frame_x = 10 + i * 70
        parts.append(_rect_svg(frame_x, 8, 60, 60, color="#999"))
        cx = frame_x + x_positions[i]
        parts.append(_draw(cx, 38, sizes[i], shade_seq[i]))
    parts.append(_separator_svg(225, 5, 75))
    parts.append(_text_svg(250, 40, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=275, h=80)

    correct = (sizes[3], x_positions[3], shade_seq[3])
    # Distractors: wrong size, wrong position, wrong shade
    distractors = [
        (sizes[2], x_positions[3], shade_seq[3]),
        (sizes[3], x_positions[2], shade_seq[3]),
        (sizes[3], x_positions[3], shade_seq[1] if shade_seq[3] != shade_seq[1] else "full"),
    ]
    all_opts = distractors + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, (sz, xp, sh) in enumerate(all_opts):
        content = _rect_svg(2, 2, 56, 56, color="#999")
        content += _draw(2 + xp, 30, sz, sh)
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if sz == correct[0] and xp == correct[1] and sh == correct[2]:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Hard",
        question="Three transformations occur simultaneously. Which comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"Rule 1: Circle grows. Rule 2: Position shifts right. Rule 3: Shading changes. All three must match.",
        tags=["figure series", "next figure prediction", "multi-rule", "transformation", "advanced"],
    )


def gen_alternating_rotation_direction(id_: int, variant: int = 0) -> dict:
    """Arrow alternates between CW and CCW rotation: +90, -90, +90, -90."""
    color = random.choice(COLORS)
    start = variant % 4
    # Alternating: +1, -1, +1, -1 in terms of 4-direction index
    positions = [start]
    for i in range(3):
        if i % 2 == 0:
            positions.append((positions[-1] + 1) % 4)
        else:
            positions.append((positions[-1] - 1) % 4)
    seq = [DIRECTIONS_4[p] for p in positions]
    show = seq[:3]
    correct = seq[3]

    parts = []
    for i, d in enumerate(show):
        cx = 40 + i * 70
        parts.append(_arrow_svg(cx, 40, d, color=color))
    parts.append(_separator_svg(240, 5, 75))
    parts.append(_text_svg(265, 45, "?", size=18))
    svg_q = _svg_wrap("".join(parts), w=290, h=80)

    wrong = [d for d in DIRECTIONS_4 if d != correct]
    random.shuffle(wrong)
    all_opts = wrong[:3] + [correct]
    random.shuffle(all_opts)

    labels = ["A", "B", "C", "D"]
    choices = []
    ans = ""
    for i, d in enumerate(all_opts):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct:
            ans = labels[i]

    return _make_question(
        id_=id_, difficulty="Hard",
        question="The rotation direction alternates. Which figure comes next?",
        svg_question=svg_q, choices=choices, answer=ans,
        explanation=f"The arrow alternates: +90° then -90° then +90° then -90°. Sequence: {' → '.join(seq)}.",
        tags=["figure series", "next figure prediction", "alternating rotation", "advanced"],
    )


# ---------------------------------------------------------------------------
# Main generation — 600 questions (200 Easy, 200 Medium, 200 Hard)
# Uses deduplication to guarantee unique SVG content per question.
# ---------------------------------------------------------------------------


def _extract_svg(question_text: str) -> str:
    """Extract the SVG portion from a question for dedup comparison."""
    import re
    match = re.search(r"<svg.*?</svg>", question_text, re.DOTALL)
    return match.group() if match else ""


def _generate_unique(generators: list, target: int, seed_base: int) -> list[dict]:
    """Generate questions using a list of (gen_fn, params_list) until target reached.

    Deduplicates by SVG content. Retries with shifted parameters if needed.
    """
    questions: list[dict] = []
    seen_svgs: set[str] = set()
    id_ = 1
    attempt = 0
    max_attempts = target * 5  # safety valve

    # Flatten all generator calls into a schedule
    schedule: list[tuple] = []
    for gen_fn, params_list in generators:
        for params in params_list:
            schedule.append((gen_fn, params))

    # Shuffle schedule to distribute question types
    random.seed(seed_base)

    idx = 0
    color_shift = 0
    while len(questions) < target and attempt < max_attempts:
        gen_fn, params = schedule[idx % len(schedule)]
        random.seed(seed_base + attempt * 7 + idx * 13)

        try:
            q = gen_fn(id_, **params)
            svg = _extract_svg(q["question"])

            if svg and svg not in seen_svgs:
                # Also verify choices are unique
                choice_svgs = [c.split(": ", 1)[1] if ": " in c else c for c in q["choices"]]
                if len(set(choice_svgs)) == 4:
                    seen_svgs.add(svg)
                    questions.append(q)
                    id_ += 1
        except Exception:
            pass

        idx += 1
        attempt += 1

        # If we've exhausted the schedule, loop with different seeds
        if idx >= len(schedule):
            idx = 0
            color_shift += 1

    return questions[:target]


def _generate_easy(start_id: int) -> list[dict]:
    """Generate 200 unique Easy questions."""
    generators = [
        # Arrow rotation CW — 4 starts
        (gen_arrow_rotation_cw, [{"start": s} for s in range(4)] * 8),
        # Arrow rotation CCW — 4 starts
        (gen_arrow_rotation_ccw, [{"start": s} for s in range(4)] * 8),
        # Shape count increase — varied starts/steps/shapes
        (gen_shape_count_increase, [
            {"start": st, "step": stp, "shape": sh}
            for st in range(1, 8) for stp in [1, 2, 3] for sh in ["circle", "square", "triangle"]
        ]),
        # Size growth
        (gen_size_growth, [{"shape": sh} for sh in ["circle", "square", "triangle"]] * 10),
        # Alternating shapes
        (gen_alternating_shapes, [{"variant": v} for v in range(30)]),
        # Shading progression
        (gen_shading_progression, [{"variant": v} for v in range(20)]),
        # Sides increase
        (gen_sides_increase, [{"start": s} for s in range(3, 20)]),
        # Arrow 180 alternation
        (gen_arrow_180_alternation, [{"variant": v} for v in range(20)]),
        # Dot position movement
        (gen_dot_position_movement, [{"variant": v} for v in range(16)]),
    ]
    questions = _generate_unique(generators, 200, seed_base=42)
    # Re-assign IDs
    for i, q in enumerate(questions):
        q["id"] = start_id + i
    return questions


def _generate_medium(start_id: int) -> list[dict]:
    """Generate 200 unique Medium questions."""
    generators = [
        # Rotation 45°
        (gen_rotation_45, [{"start": s} for s in range(8)] * 5),
        # Rotation + shading
        (gen_rotation_plus_shading, [{"start": s} for s in range(4)] * 8),
        # Missing middle
        (gen_missing_middle, [{"start": s} for s in range(4)] * 8),
        # Polygon rotation
        (gen_polygon_rotation_series, [
            {"sides": sides, "rot_step": rot}
            for sides in [3, 4, 5, 6, 7, 8] for rot in [30, 45, 60, 72, 90, 120]
        ]),
        # Count + rotation
        (gen_count_plus_rotation, [
            {"start_dir": d, "start_count": c}
            for d in range(4) for c in range(1, 8)
        ]),
        # Shape cycle 3
        (gen_shape_cycle_3, [{"variant": v} for v in range(24)]),
        # Star rotation
        (gen_star_rotation, [
            {"rot_step": rs, "variant": v}
            for rs in [36, 45, 60, 72] for v in range(8)
        ]),
        # Missing in count series
        (gen_missing_in_count_series, [
            {"start": st, "step": stp}
            for st in range(1, 8) for stp in [1, 2, 3]
        ]),
    ]
    questions = _generate_unique(generators, 200, seed_base=1000)
    for i, q in enumerate(questions):
        q["id"] = start_id + i
    return questions


def _generate_hard(start_id: int) -> list[dict]:
    """Generate 200 unique Hard questions."""
    generators = [
        # Triple rule
        (gen_triple_rule, [{"variant": v} for v in range(24)]),
        # Nested shapes
        (gen_nested_shapes_series, [{"variant": v} for v in range(24)]),
        # Grid 3x3
        (gen_grid_3x3, [{"variant": v} for v in range(30)]),
        # Rotation + sides increase
        (gen_rotation_plus_sides_increase, [
            {"start_sides": s, "rot_step": r}
            for s in range(3, 10) for r in [45, 60, 72, 90]
        ]),
        # Cross rotation + shading
        (gen_cross_rotation_shading, [{"variant": v} for v in range(20)]),
        # Directional progression 8
        (gen_directional_progression_8, [
            {"start": s, "step": st}
            for s in range(8) for st in [2, 3, 5]
        ]),
        # Missing in grid row
        (gen_missing_in_grid_row, [{"variant": v} for v in range(24)]),
        # Layered transformation
        (gen_layered_transformation, [{"variant": v} for v in range(18)]),
        # Alternating rotation direction
        (gen_alternating_rotation_direction, [{"variant": v} for v in range(16)]),
    ]
    questions = _generate_unique(generators, 200, seed_base=2000)
    for i, q in enumerate(questions):
        q["id"] = start_id + i
    return questions


def generate_all_questions() -> list[dict]:
    """Generate 600 questions: 200 Easy, 200 Medium, 200 Hard."""
    easy = _generate_easy(start_id=1)
    medium = _generate_medium(start_id=201)
    hard = _generate_hard(start_id=401)

    all_questions = easy + medium + hard

    # Re-number IDs sequentially
    for i, q in enumerate(all_questions):
        q["id"] = i + 1

    return all_questions


def main() -> None:
    questions = generate_all_questions()

    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]
    print(f"Generated: {len(questions)} total | Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
