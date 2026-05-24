"""Generate abstract reasoning shape pattern questions with SVG visuals.

Produces 50 questions (17 Easy, 17 Medium, 16 Hard) with mathematically
correct SVG diagrams for rotation, reflection, and transformation patterns.

Usage:
    python scripts/gen_shape_patterns_questions.py
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
    / "analytical-ability" / "abstract-reasoning" / "shape-patterns"
    / "questions.json"
)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------


def _svg_wrap(content: str, w: int = 200, h: int = 80) -> str:
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
    """Generate an arrow pointing in a direction at (cx, cy)."""
    # Directions map to angles (0=up, 90=right, 180=down, 270=left)
    angles = {"up": 0, "right": 90, "down": 180, "left": 270,
              "up-right": 45, "down-right": 135, "down-left": 225, "up-left": 315}
    angle = angles[direction]
    rad = math.radians(angle)

    # Arrow tip
    tx = cx + size * math.sin(rad)
    ty = cy - size * math.cos(rad)
    # Arrow tail
    bx = cx - size * math.sin(rad)
    by = cy + size * math.cos(rad)
    # Arrowhead wings
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



# ---------------------------------------------------------------------------
# Question generators
# ---------------------------------------------------------------------------

DIRECTIONS_CW = ["up", "right", "down", "left"]
DIRECTIONS_CCW = ["up", "left", "down", "right"]
DIRECTIONS_8 = ["up", "up-right", "right", "down-right", "down", "down-left", "left", "up-left"]

COLORS = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#E91E63", "#00BCD4"]


def _make_question(id_: int, difficulty: str, question: str,
                   svg_question: str, choices: list[dict],
                   answer: str, explanation: str, tags: list[str]) -> dict:
    """Build a question dict compatible with the seed script and quiz frontend.

    Format:
    - question (→ stem): text question + SVG diagram on a new line
    - choices (→ options): list of strings, each containing "LABEL: <svg>..."
    - answer (→ correct_answer): the full option string that matches
    """
    # Build stem: text question + SVG visual
    stem_with_svg = f"{question}\n\n{svg_question}"

    # Build options: each is "A: <svg...>" so the frontend can split label from SVG
    option_strings = [f"{c['label']}: {c['svg']}" for c in choices]

    # The correct answer must match one of the option strings exactly
    correct_option = next(o for o in option_strings if o.startswith(f"{answer}: "))

    return {
        "id": id_,
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Shape Patterns",
        "difficulty": difficulty,
        "question": stem_with_svg,
        "choices": option_strings,
        "answer": correct_option,
        "explanation": explanation,
        "tags": tags,
    }


# --- ROTATION QUESTIONS ---

def gen_arrow_rotation_90cw(id_: int, start_idx: int = 0) -> dict:
    """Arrow rotates 90° clockwise. Show 3 steps, ask for 4th."""
    dirs = DIRECTIONS_CW
    s = start_idx % 4
    seq = [dirs[(s + i) % 4] for i in range(4)]
    color = random.choice(COLORS)

    # Build question SVG: 3 arrows + question mark
    parts = []
    for i in range(3):
        cx = 30 + i * 55
        parts.append(_arrow_svg(cx, 40, seq[i], color=color))
        parts.append(_text_svg(cx, 72, f"Step {i+1}"))
    parts.append(_separator_svg(185, 5, 75))
    parts.append(_text_svg(210, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=240, h=80)

    # Build choices: correct + 3 wrong
    correct_dir = seq[3]
    wrong_dirs = [d for d in dirs if d != correct_dir]
    random.shuffle(wrong_dirs)
    wrong_dirs = wrong_dirs[:3]

    all_choices_dirs = wrong_dirs + [correct_dir]
    random.shuffle(all_choices_dirs)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, d in enumerate(all_choices_dirs):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="Which figure completes the sequence?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The arrow rotates 90° clockwise each step: {seq[0]} → {seq[1]} → {seq[2]} → {seq[3]}.",
        tags=["abstract reasoning", "rotation", "clockwise", "shape patterns"],
    )


def gen_arrow_rotation_90ccw(id_: int, start_idx: int = 0) -> dict:
    """Arrow rotates 90° counterclockwise."""
    dirs = DIRECTIONS_CCW
    s = start_idx % 4
    seq = [dirs[(s + i) % 4] for i in range(4)]
    color = random.choice(COLORS)

    parts = []
    for i in range(3):
        cx = 30 + i * 55
        parts.append(_arrow_svg(cx, 40, seq[i], color=color))
        parts.append(_text_svg(cx, 72, f"Step {i+1}"))
    parts.append(_separator_svg(185, 5, 75))
    parts.append(_text_svg(210, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=240, h=80)

    correct_dir = seq[3]
    wrong_dirs = [d for d in dirs if d != correct_dir]
    random.shuffle(wrong_dirs)
    wrong_dirs = wrong_dirs[:3]

    all_choices_dirs = wrong_dirs + [correct_dir]
    random.shuffle(all_choices_dirs)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, d in enumerate(all_choices_dirs):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="Which figure completes the sequence?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The arrow rotates 90° counterclockwise each step: {seq[0]} → {seq[1]} → {seq[2]} → {seq[3]}.",
        tags=["abstract reasoning", "rotation", "counterclockwise", "shape patterns"],
    )



def gen_arrow_rotation_180(id_: int, start_idx: int = 0) -> dict:
    """Arrow alternates 180° (up/down or left/right)."""
    pairs = [("up", "down"), ("left", "right")]
    pair = pairs[start_idx % 2]
    seq = [pair[i % 2] for i in range(4)]
    color = random.choice(COLORS)

    parts = []
    for i in range(3):
        cx = 30 + i * 55
        parts.append(_arrow_svg(cx, 40, seq[i], color=color))
        parts.append(_text_svg(cx, 72, f"Step {i+1}"))
    parts.append(_separator_svg(185, 5, 75))
    parts.append(_text_svg(210, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=240, h=80)

    correct_dir = seq[3]
    wrong_dirs = [d for d in DIRECTIONS_CW if d != correct_dir]
    random.shuffle(wrong_dirs)
    wrong_dirs = wrong_dirs[:3]

    all_choices_dirs = wrong_dirs + [correct_dir]
    random.shuffle(all_choices_dirs)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, d in enumerate(all_choices_dirs):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="Which figure completes the sequence?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The arrow rotates 180° each step, alternating between {pair[0]} and {pair[1]}.",
        tags=["abstract reasoning", "rotation", "180 degrees", "shape patterns"],
    )


def gen_polygon_sides_increase(id_: int, start_sides: int = 3) -> dict:
    """Polygon gains one side each step."""
    color = random.choice(COLORS)
    sides_seq = [start_sides + i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 30 + i * 55
        parts.append(_polygon_svg(cx, 40, sides_seq[i], radius=18, color=color))
        parts.append(_text_svg(cx, 72, f"{sides_seq[i]} sides"))
    parts.append(_separator_svg(185, 5, 75))
    parts.append(_text_svg(210, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=240, h=80)

    correct_sides = sides_seq[3]
    wrong_options = [correct_sides - 1, correct_sides + 1, correct_sides + 2]
    all_options = wrong_options + [correct_sides]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, s in enumerate(all_options):
        svg_c = _svg_choice_wrap(_polygon_svg(30, 30, s, radius=22, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct_sides:
            answer_label = labels[i]

    side_names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon",
                  7: "heptagon", 8: "octagon", 9: "nonagon"}

    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="Which figure completes the pattern?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The number of sides increases by 1 each step: {sides_seq[0]} → {sides_seq[1]} → {sides_seq[2]} → {sides_seq[3]} ({side_names.get(correct_sides, f'{correct_sides}-gon')}).",
        tags=["abstract reasoning", "transformation", "side count", "shape patterns"],
    )



def gen_dot_count_increase(id_: int, start: int = 1) -> dict:
    """Dots increase by 1 each step inside a square frame."""
    color = random.choice(COLORS)
    counts = [start + i for i in range(4)]

    def _dots_in_frame(cx: float, cy: float, count: int, frame_size: float = 30) -> str:
        parts = [_rect_svg(cx - frame_size/2, cy - frame_size/2, frame_size, frame_size, color="#666")]
        # Place dots in a grid pattern
        positions = []
        cols = math.ceil(math.sqrt(count))
        rows = math.ceil(count / cols) if cols > 0 else 1
        spacing_x = frame_size / (cols + 1)
        spacing_y = frame_size / (rows + 1)
        for idx in range(count):
            r = idx // cols
            c = idx % cols
            dx = cx - frame_size/2 + spacing_x * (c + 1)
            dy = cy - frame_size/2 + spacing_y * (r + 1)
            positions.append((dx, dy))
        for px, py in positions:
            parts.append(_dot_svg(px, py, r=3, color=color))
        return "".join(parts)

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_dots_in_frame(cx, 40, counts[i]))
        parts.append(_text_svg(cx, 72, f"{counts[i]} dot{'s' if counts[i]>1 else ''}"))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_count = counts[3]
    wrong_counts = [correct_count - 1, correct_count + 1, correct_count + 2]
    wrong_counts = [w for w in wrong_counts if w > 0 and w != correct_count][:3]
    if len(wrong_counts) < 3:
        wrong_counts.append(correct_count + 3)

    all_options = wrong_counts + [correct_count]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, cnt in enumerate(all_options):
        svg_c = _svg_choice_wrap(_dots_in_frame(30, 30, cnt, frame_size=40))
        choices.append({"label": labels[i], "svg": svg_c})
        if cnt == correct_count:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="How many dots should appear in the next figure?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The number of dots increases by 1 each step: {counts[0]} → {counts[1]} → {counts[2]} → {counts[3]}.",
        tags=["abstract reasoning", "transformation", "element count", "shape patterns"],
    )


def gen_size_progression(id_: int, shape: str = "circle") -> dict:
    """Shape grows larger each step."""
    color = random.choice(COLORS)
    sizes = [10, 16, 22, 28]

    def _shape_at_size(cx: float, cy: float, sz: float) -> str:
        if shape == "circle":
            return _circle_svg(cx, cy, r=sz, color=color)
        else:
            return _rect_svg(cx - sz, cy - sz, sz * 2, sz * 2, color=color)

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_shape_at_size(cx, 40, sizes[i]))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_size = sizes[3]
    # Wrong sizes must all be smaller or different from correct
    wrong_sizes = [sizes[0], sizes[1], sizes[2]]
    all_options = wrong_sizes + [correct_size]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, sz in enumerate(all_options):
        svg_c = _svg_choice_wrap(_shape_at_size(30, 30, sz))
        choices.append({"label": labels[i], "svg": svg_c})
        if sz == correct_size:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Easy",
        question="Which figure continues the size progression?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The {shape} grows larger by a fixed amount each step. The next figure should be the largest in the sequence.",
        tags=["abstract reasoning", "transformation", "size progression", "shape patterns"],
    )



# --- MEDIUM QUESTIONS ---

def gen_arrow_rotation_45(id_: int, start_idx: int = 0) -> dict:
    """Arrow rotates 45° each step (8 positions)."""
    s = start_idx % 8
    seq = [DIRECTIONS_8[(s + i) % 8] for i in range(4)]
    color = random.choice(COLORS)

    parts = []
    for i in range(3):
        cx = 30 + i * 55
        parts.append(_arrow_svg(cx, 40, seq[i], size=16, color=color))
        parts.append(_text_svg(cx, 72, f"Step {i+1}"))
    parts.append(_separator_svg(185, 5, 75))
    parts.append(_text_svg(210, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=240, h=80)

    correct_dir = seq[3]
    wrong_dirs = [d for d in DIRECTIONS_8 if d != correct_dir]
    random.shuffle(wrong_dirs)
    wrong_dirs = wrong_dirs[:3]

    all_choices_dirs = wrong_dirs + [correct_dir]
    random.shuffle(all_choices_dirs)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, d in enumerate(all_choices_dirs):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, size=16, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="Which figure completes the sequence?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The arrow rotates 45° clockwise each step: {seq[0]} → {seq[1]} → {seq[2]} → {seq[3]}.",
        tags=["abstract reasoning", "rotation", "45 degrees", "shape patterns"],
    )


def gen_reflection_vertical(id_: int, variant: int = 0) -> dict:
    """Shape alternates between normal and vertically reflected."""
    color = random.choice(COLORS)

    def _l_shape(cx: float, cy: float, orientation: int) -> str:
        """Draw L-shape in 4 distinct orientations.
        0=normal (arm right), 1=reflected (arm left),
        2=rotated 180 normal (arm right, flipped vertically),
        3=rotated 180 reflected (arm left, flipped vertically).
        """
        if orientation == 0:
            # L: vertical bar left, horizontal arm goes right at bottom
            return (
                f"<polyline points='{cx-12},{cy-15} {cx-12},{cy+15} {cx+12},{cy+15}' "
                f"fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round'/>"
                f"{_dot_svg(cx + 8, cy + 11, r=3, color=color)}"
            )
        elif orientation == 1:
            # Reflected L: vertical bar right, horizontal arm goes left at bottom
            return (
                f"<polyline points='{cx+12},{cy-15} {cx+12},{cy+15} {cx-12},{cy+15}' "
                f"fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round'/>"
                f"{_dot_svg(cx - 8, cy + 11, r=3, color=color)}"
            )
        elif orientation == 2:
            # Rotated 90° CW: horizontal bar top, vertical arm goes down on right
            return (
                f"<polyline points='{cx-15},{cy-12} {cx+15},{cy-12} {cx+15},{cy+12}' "
                f"fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round'/>"
                f"{_dot_svg(cx + 11, cy + 8, r=3, color=color)}"
            )
        else:
            # Rotated 90° CCW: horizontal bar bottom, vertical arm goes up on left
            return (
                f"<polyline points='{cx+15},{cy+12} {cx-15},{cy+12} {cx-15},{cy-12}' "
                f"fill='none' stroke='{color}' stroke-width='3' stroke-linecap='round'/>"
                f"{_dot_svg(cx - 11, cy - 8, r=3, color=color)}"
            )

    # Pattern: alternates between orientation 0 and 1
    start_reflected = variant % 2 == 1
    seq = [((i % 2) == 1) if not start_reflected else ((i % 2) == 0) for i in range(4)]
    # seq[i]: False=normal(0), True=reflected(1)

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        orient = 1 if seq[i] else 0
        parts.append(_l_shape(cx, 40, orient))
        label = "reflected" if seq[i] else "normal"
        parts.append(_text_svg(cx, 72, label, size=8))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_orient = 1 if seq[3] else 0
    # 4 distinct choices: correct orientation + 3 other orientations
    wrong_orients = [o for o in range(4) if o != correct_orient]

    all_options = wrong_orients + [correct_orient]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, orient in enumerate(all_options):
        svg_c = _svg_choice_wrap(_l_shape(30, 30, orient))
        choices.append({"label": labels[i], "svg": svg_c})
        if orient == correct_orient:
            answer_label = labels[i]

    state_name = "reflected" if seq[3] else "normal"
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="Which figure completes the alternating pattern?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The figure alternates between normal and vertically reflected. The next step should be {state_name}. The dot position confirms the reflection.",
        tags=["abstract reasoning", "reflection", "vertical", "alternating", "shape patterns"],
    )



def gen_rotation_plus_shading(id_: int, start_idx: int = 0) -> dict:
    """Arrow rotates 90° CW AND shading changes (empty→half→full cycle)."""
    color = random.choice(COLORS)
    dirs = DIRECTIONS_CW
    s = start_idx % 4
    dir_seq = [dirs[(s + i) % 4] for i in range(4)]
    shade_seq = [False, False, True, True]  # empty, empty, filled, filled (or cycle)
    # Simpler: alternate filled state
    shade_seq = [i % 2 == 1 for i in range(4)]  # F, T, F, T

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_arrow_svg(cx, 40, dir_seq[i], color=color, filled=shade_seq[i]))
        shade_label = "filled" if shade_seq[i] else "empty"
        parts.append(_text_svg(cx, 72, f"{dir_seq[i]},{shade_label}", size=7))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_dir = dir_seq[3]
    correct_filled = shade_seq[3]

    # Generate distractors: each must have a DIFFERENT direction from correct
    # to avoid confusion with simple rotation check
    other_dirs = [d for d in dirs if d != correct_dir]
    random.shuffle(other_dirs)
    distractors = [
        (other_dirs[0], correct_filled),       # wrong dir, right shade
        (other_dirs[1], not correct_filled),    # wrong dir, wrong shade
        (other_dirs[2], correct_filled),        # wrong dir, right shade
    ]

    all_options = distractors + [(correct_dir, correct_filled)]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, (d, f) in enumerate(all_options):
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, color=color, filled=f))
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir and f == correct_filled:
            answer_label = labels[i]

    shade_name = "filled" if correct_filled else "empty"
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="Which figure completes the pattern? (Two rules are operating.)",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"Rule 1: Arrow rotates 90° clockwise ({dir_seq[0]}→{dir_seq[1]}→{dir_seq[2]}→{dir_seq[3]}). Rule 2: Arrowhead alternates empty/filled. Answer: {correct_dir}, {shade_name}.",
        tags=["abstract reasoning", "rotation", "shading", "multi-rule", "shape patterns"],
    )


def gen_shape_alternation(id_: int, variant: int = 0) -> dict:
    """Two shapes alternate: circle-square-circle-square."""
    color = random.choice(COLORS)
    shapes_pool = [("circle", "square"), ("triangle", "circle"), ("square", "triangle")]
    pair = shapes_pool[variant % len(shapes_pool)]
    seq = [pair[i % 2] for i in range(4)]

    def _draw_shape(cx: float, cy: float, shape_name: str, sz: float = 18) -> str:
        if shape_name == "circle":
            return _circle_svg(cx, cy, r=sz, color=color)
        elif shape_name == "square":
            return _rect_svg(cx - sz, cy - sz, sz * 2, sz * 2, color=color)
        else:  # triangle
            return _polygon_svg(cx, cy, 3, radius=sz, color=color)

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_draw_shape(cx, 40, seq[i]))
        parts.append(_text_svg(cx, 72, seq[i], size=8))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_shape = seq[3]
    all_shape_names = ["circle", "square", "triangle", "pentagon"]
    wrong_shapes = [s for s in all_shape_names if s != correct_shape][:3]

    all_options = wrong_shapes + [correct_shape]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    sides_map = {"circle": 0, "square": 4, "triangle": 3, "pentagon": 5}
    for i, sn in enumerate(all_options):
        if sn == "circle":
            svg_c = _svg_choice_wrap(_circle_svg(30, 30, r=20, color=color))
        elif sn == "square":
            svg_c = _svg_choice_wrap(_rect_svg(10, 10, 40, 40, color=color))
        elif sn == "pentagon":
            svg_c = _svg_choice_wrap(_polygon_svg(30, 30, 5, radius=20, color=color))
        else:
            svg_c = _svg_choice_wrap(_polygon_svg(30, 30, 3, radius=20, color=color))
        choices.append({"label": labels[i], "svg": svg_c})
        if sn == correct_shape:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="Which shape comes next in the alternating pattern?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The shapes alternate: {pair[0]} → {pair[1]} → {pair[0]} → {pair[1]}. The next figure is a {correct_shape}.",
        tags=["abstract reasoning", "transformation", "alternation", "shape patterns"],
    )



def gen_polygon_rotation(id_: int, sides: int = 4, rot_per_step: float = 45) -> dict:
    """A polygon rotates by a fixed angle each step."""
    color = random.choice(COLORS)
    rotations = [rot_per_step * i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_polygon_svg(cx, 40, sides, radius=18, color=color,
                                  rotation_deg=-90 + rotations[i]))
        # Add a marker dot at the first vertex to show rotation
        angle = math.radians(-90 + rotations[i])
        dot_x = cx + 18 * math.cos(angle)
        dot_y = 40 + 18 * math.sin(angle)
        parts.append(_dot_svg(dot_x, dot_y, r=3, color="#F44336"))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_rot = rotations[3]
    wrong_rots = [correct_rot + 45, correct_rot - 45, correct_rot + 90]

    all_options = wrong_rots + [correct_rot]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, rot in enumerate(all_options):
        content = _polygon_svg(30, 30, sides, radius=22, color=color,
                               rotation_deg=-90 + rot)
        angle = math.radians(-90 + rot)
        dot_x = 30 + 22 * math.cos(angle)
        dot_y = 30 + 22 * math.sin(angle)
        content += _dot_svg(dot_x, dot_y, r=3, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if rot == correct_rot:
            answer_label = labels[i]

    side_names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon"}
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="The shape rotates by a fixed angle each step. Which figure comes next?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The {side_names.get(sides, 'polygon')} rotates {rot_per_step}° clockwise each step. Track the red dot to confirm orientation. The next position is at {correct_rot}° total rotation.",
        tags=["abstract reasoning", "rotation", "polygon", "shape patterns"],
    )


def gen_shading_progression(id_: int, variant: int = 0) -> dict:
    """Circle shading progresses from empty to full in quarters."""
    color = random.choice(COLORS)
    # 0=empty, 1=quarter, 2=half, 3=three-quarter, 4=full
    start = variant % 2  # start at 0 or 1
    shade_seq = [start + i for i in range(4)]

    def _shaded_circle(cx: float, cy: float, level: int, r: float = 18) -> str:
        parts = [_circle_svg(cx, cy, r=r, color=color)]
        if level >= 4:
            parts = [f"<circle cx='{cx}' cy='{cy}' r='{r}' fill='{color}' stroke='{color}' stroke-width='2'/>"]
        elif level == 3:
            # Three quarters filled (top-right empty)
            parts.append(f"<path d='M{cx},{cy} L{cx},{cy-r} A{r},{r} 0 1,1 {cx+r},{cy} Z' fill='{color}' opacity='0.7'/>")
            parts.append(f"<path d='M{cx},{cy} L{cx+r},{cy} A{r},{r} 0 0,1 {cx},{cy+r} Z' fill='{color}' opacity='0.7'/>")
            parts.append(f"<path d='M{cx},{cy} L{cx},{cy+r} A{r},{r} 0 0,1 {cx-r},{cy} Z' fill='{color}' opacity='0.7'/>")
        elif level == 2:
            # Half filled (left half)
            parts.append(f"<path d='M{cx},{cy-r} A{r},{r} 0 0,0 {cx},{cy+r} L{cx},{cy-r} Z' fill='{color}' opacity='0.7'/>")
        elif level == 1:
            # Quarter filled (top-left)
            parts.append(f"<path d='M{cx},{cy} L{cx},{cy-r} A{r},{r} 0 0,0 {cx-r},{cy} Z' fill='{color}' opacity='0.7'/>")
        return "".join(parts)

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_shaded_circle(cx, 40, shade_seq[i]))
        labels_shade = ["empty", "1/4", "1/2", "3/4", "full"]
        parts.append(_text_svg(cx, 72, labels_shade[shade_seq[i]], size=8))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_level = shade_seq[3]
    wrong_levels = [l for l in range(5) if l != correct_level]
    random.shuffle(wrong_levels)
    wrong_levels = wrong_levels[:3]

    all_options = wrong_levels + [correct_level]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, lvl in enumerate(all_options):
        svg_c = _svg_choice_wrap(_shaded_circle(30, 30, lvl, r=22))
        choices.append({"label": labels[i], "svg": svg_c})
        if lvl == correct_level:
            answer_label = labels[i]

    shade_names = ["empty", "one-quarter filled", "half filled", "three-quarters filled", "fully filled"]
    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="The shading increases each step. Which figure comes next?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The circle's shading increases by one quarter each step. The next figure should be {shade_names[correct_level]}.",
        tags=["abstract reasoning", "transformation", "shading", "progression", "shape patterns"],
    )



# --- HARD QUESTIONS ---

def gen_rotation_plus_sides(id_: int, start_sides: int = 3, rot_per_step: float = 90) -> dict:
    """Shape gains one side AND rotates each step."""
    color = random.choice(COLORS)
    sides_seq = [start_sides + i for i in range(4)]
    rot_seq = [rot_per_step * i for i in range(4)]

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_polygon_svg(cx, 40, sides_seq[i], radius=18, color=color,
                                  rotation_deg=-90 + rot_seq[i]))
        angle = math.radians(-90 + rot_seq[i])
        dot_x = cx + 18 * math.cos(angle)
        dot_y = 40 + 18 * math.sin(angle)
        parts.append(_dot_svg(dot_x, dot_y, r=3, color="#F44336"))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_sides = sides_seq[3]
    correct_rot = rot_seq[3]

    # Distractors: wrong sides, wrong rotation, or both
    distractors = [
        (correct_sides, correct_rot + 90),      # right sides, wrong rot
        (correct_sides - 1, correct_rot),        # wrong sides, right rot
        (correct_sides + 1, correct_rot - 90),   # wrong both
    ]

    all_options = distractors + [(correct_sides, correct_rot)]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, (s, r) in enumerate(all_options):
        content = _polygon_svg(30, 30, s, radius=22, color=color,
                               rotation_deg=-90 + r)
        angle = math.radians(-90 + r)
        dot_x = 30 + 22 * math.cos(angle)
        dot_y = 30 + 22 * math.sin(angle)
        content += _dot_svg(dot_x, dot_y, r=3, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if s == correct_sides and r == correct_rot:
            answer_label = labels[i]

    side_names = {3: "triangle", 4: "square", 5: "pentagon", 6: "hexagon",
                  7: "heptagon", 8: "octagon"}
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="Two rules operate simultaneously. Which figure comes next?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"Rule 1: Sides increase by 1 ({sides_seq[0]}→{sides_seq[1]}→{sides_seq[2]}→{sides_seq[3]}). Rule 2: Shape rotates {rot_per_step}° each step. Answer: {side_names.get(correct_sides, f'{correct_sides}-gon')} rotated {correct_rot}°.",
        tags=["abstract reasoning", "rotation", "transformation", "multi-rule", "shape patterns"],
    )


def gen_nested_shapes(id_: int, variant: int = 0) -> dict:
    """Outer shape rotates, inner shape cycles through types."""
    color_outer = "#FF9800"
    color_inner = "#2196F3"
    inner_cycle = ["circle", "square", "triangle"]
    outer_rot_per_step = 30

    outer_rots = [outer_rot_per_step * i for i in range(4)]
    inner_seq = [inner_cycle[(variant + i) % 3] for i in range(4)]

    def _draw_nested(cx: float, cy: float, outer_rot: float, inner_shape: str) -> str:
        # Outer: rotated square
        outer = _polygon_svg(cx, cy, 4, radius=22, color=color_outer,
                             rotation_deg=-90 + outer_rot)
        # Inner shape
        if inner_shape == "circle":
            inner = _circle_svg(cx, cy, r=8, color=color_inner)
        elif inner_shape == "square":
            inner = _rect_svg(cx - 7, cy - 7, 14, 14, color=color_inner)
        else:
            inner = _polygon_svg(cx, cy, 3, radius=9, color=color_inner)
        return outer + inner

    parts = []
    for i in range(3):
        cx = 35 + i * 60
        parts.append(_draw_nested(cx, 40, outer_rots[i], inner_seq[i]))
    parts.append(_separator_svg(200, 5, 75))
    parts.append(_text_svg(225, 45, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    correct_rot = outer_rots[3]
    correct_inner = inner_seq[3]

    # Distractors
    wrong_inners = [s for s in inner_cycle if s != correct_inner]
    distractors = [
        (correct_rot, wrong_inners[0]),
        (correct_rot + 30, correct_inner),
        (correct_rot - 30, wrong_inners[1] if len(wrong_inners) > 1 else wrong_inners[0]),
    ]

    all_options = distractors + [(correct_rot, correct_inner)]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, (rot, inner) in enumerate(all_options):
        svg_c = _svg_choice_wrap(_draw_nested(30, 30, rot, inner))
        choices.append({"label": labels[i], "svg": svg_c})
        if rot == correct_rot and inner == correct_inner:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="The outer and inner shapes follow independent rules. Which figure comes next?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"Rule 1: Outer square rotates {outer_rot_per_step}° each step (total {correct_rot}°). Rule 2: Inner shape cycles {inner_cycle[0]}→{inner_cycle[1]}→{inner_cycle[2]}→repeat. Answer: outer at {correct_rot}°, inner = {correct_inner}.",
        tags=["abstract reasoning", "rotation", "nested", "multi-rule", "shape patterns"],
    )



def gen_grid_reasoning(id_: int, variant: int = 0) -> dict:
    """3x3 grid: rows share shape, columns share shading. Find missing cell."""
    color = "#2196F3"
    shapes = ["circle", "square", "triangle"]
    shadings = ["none", "half", "full"]

    # Shuffle order based on variant
    random.seed(42 + variant)
    shape_order = shapes[:]
    shade_order = shadings[:]
    random.shuffle(shape_order)
    random.shuffle(shade_order)
    random.seed(42)  # Reset

    # Missing cell is always bottom-right (row 2, col 2)
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

    # Build 3x3 grid SVG
    grid_parts = []
    cell_size = 50
    for row in range(3):
        for col in range(3):
            cx = 30 + col * cell_size
            cy = 30 + row * cell_size
            # Draw cell border
            grid_parts.append(f"<rect x='{cx-22}' y='{cy-22}' width='44' height='44' fill='none' stroke='#555' stroke-width='0.5'/>")
            if row == 2 and col == 2:
                grid_parts.append(_text_svg(cx, cy + 4, "?", size=16, color="#888"))
            else:
                grid_parts.append(_draw_cell(shape_order[row], shade_order[col], cx, cy))

    svg_q = _svg_wrap("".join(grid_parts), w=180, h=180)

    # Choices: correct + 3 wrong
    correct = (missing_shape, missing_shade)
    distractors = [
        (missing_shape, shade_order[0]),  # right shape, wrong shade
        (shape_order[0], missing_shade),  # wrong shape, right shade
        (shape_order[1], shade_order[0]),  # both wrong
    ]

    all_options = distractors + [correct]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, (sh, sd) in enumerate(all_options):
        svg_c = _svg_choice_wrap(_draw_cell(sh, sd, 30, 30, r=20))
        choices.append({"label": labels[i], "svg": svg_c})
        if sh == correct[0] and sd == correct[1]:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="Which figure completes the 3×3 grid?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"Row rule: each row uses the same shape ({shape_order[0]}, {shape_order[1]}, {shape_order[2]}). Column rule: each column uses the same shading ({shade_order[0]}, {shade_order[1]}, {shade_order[2]}). The missing cell needs a {missing_shade}-shaded {missing_shape}.",
        tags=["abstract reasoning", "grid reasoning", "multi-rule", "shape patterns"],
    )


def gen_odd_one_out(id_: int, variant: int = 0) -> dict:
    """Four figures share a rule, one does not. Find the odd one."""
    color = random.choice(COLORS)
    # Use different shapes pointing in same direction, one points differently
    base_dir_idx = variant % 4
    base_dir = DIRECTIONS_CW[base_dir_idx]
    odd_dir = DIRECTIONS_CW[(base_dir_idx + 2) % 4]  # opposite direction

    odd_position = random.randint(0, 3)  # which choice is the odd one

    labels = ["A", "B", "C", "D"]
    # Make each arrow visually distinct using different sizes
    choice_sizes = [14, 16, 18, 20]
    random.shuffle(choice_sizes)

    parts = []
    choices = []
    answer_label = labels[odd_position]

    for i in range(4):
        cx = 30 + i * 55
        d = odd_dir if i == odd_position else base_dir
        sz = choice_sizes[i]
        parts.append(_arrow_svg(cx, 40, d, size=sz, color=color))
        parts.append(_text_svg(cx, 72, labels[i], size=10))
        # Each choice uses its own unique size
        svg_c = _svg_choice_wrap(_arrow_svg(30, 30, d, size=sz, color=color))
        choices.append({"label": labels[i], "svg": svg_c})

    svg_q = _svg_wrap("".join(parts), w=250, h=80)

    return _make_question(
        id_=id_,
        difficulty="Medium",
        question="Which figure is the odd one out?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"Three arrows point {base_dir}. Choice {answer_label} points {odd_dir}, making it the odd one out.",
        tags=["abstract reasoning", "odd one out", "direction", "shape patterns"],
    )



def gen_dot_movement(id_: int, variant: int = 0) -> dict:
    """A dot moves clockwise through corners of a square frame."""
    color = random.choice(COLORS)
    # Corners: TL=0, TR=1, BR=2, BL=3
    corner_positions = [(12, 12), (48, 12), (48, 48), (12, 48)]
    start = variant % 4
    seq = [(start + i) % 4 for i in range(4)]

    def _frame_with_dot(cx_offset: float, cy_offset: float, corner_idx: int) -> str:
        frame = _rect_svg(cx_offset, cy_offset, 40, 40, color="#666")
        dx, dy = corner_positions[corner_idx]
        dot = _dot_svg(cx_offset + dx, cy_offset + dy, r=5, color=color)
        return frame + dot

    parts = []
    for i in range(3):
        x_off = 10 + i * 60
        parts.append(_frame_with_dot(x_off, 15, seq[i]))
    parts.append(_separator_svg(195, 5, 75))
    parts.append(_text_svg(220, 40, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=250, h=75)

    correct_corner = seq[3]
    wrong_corners = [c for c in range(4) if c != correct_corner]
    random.shuffle(wrong_corners)

    all_options = wrong_corners[:3] + [correct_corner]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, corner in enumerate(all_options):
        svg_c = _svg_choice_wrap(_frame_with_dot(5, 5, corner))
        choices.append({"label": labels[i], "svg": svg_c})
        if corner == correct_corner:
            answer_label = labels[i]

    corner_names = ["top-left", "top-right", "bottom-right", "bottom-left"]
    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="The dot moves to a new corner each step. Where does it go next?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"The dot moves clockwise through the corners: {corner_names[seq[0]]} → {corner_names[seq[1]]} → {corner_names[seq[2]]} → {corner_names[seq[3]]}.",
        tags=["abstract reasoning", "transformation", "movement", "position", "shape patterns"],
    )


def gen_triple_rule(id_: int, variant: int = 0) -> dict:
    """Three simultaneous rules: rotation + dot count + size change."""
    color = random.choice(COLORS)
    dirs = DIRECTIONS_CW
    start_dir = variant % 4
    dir_seq = [dirs[(start_dir + i) % 4] for i in range(4)]
    dot_seq = [1 + i for i in range(4)]
    size_seq = [12, 15, 18, 21]

    parts = []
    for i in range(3):
        cx = 40 + i * 65
        # Arrow
        parts.append(_arrow_svg(cx, 35, dir_seq[i], size=size_seq[i], color=color))
        # Dots below arrow
        for d in range(dot_seq[i]):
            parts.append(_dot_svg(cx - 8 + d * 8, 65, r=2.5, color="#F44336"))
    parts.append(_separator_svg(210, 5, 75))
    parts.append(_text_svg(235, 40, "?", size=18, color="#888"))
    svg_q = _svg_wrap("".join(parts), w=260, h=80)

    correct_dir = dir_seq[3]
    correct_dots = dot_seq[3]
    correct_size = size_seq[3]

    # Distractors: each must have a DIFFERENT direction to avoid ambiguity
    other_dirs = [d for d in dirs if d != correct_dir]
    random.shuffle(other_dirs)
    distractors = [
        (other_dirs[0], correct_dots, correct_size),      # wrong dir only
        (other_dirs[1], correct_dots - 1, correct_size),  # wrong dir + wrong dots
        (other_dirs[2], correct_dots, size_seq[1]),        # wrong dir + wrong size
    ]

    all_options = distractors + [(correct_dir, correct_dots, correct_size)]
    random.shuffle(all_options)

    labels = ["A", "B", "C", "D"]
    choices = []
    answer_label = ""
    for i, (d, dots, sz) in enumerate(all_options):
        content = _arrow_svg(30, 25, d, size=sz, color=color)
        for di in range(dots):
            content += _dot_svg(30 - 8 + di * 6, 50, r=2.5, color="#F44336")
        svg_c = _svg_choice_wrap(content)
        choices.append({"label": labels[i], "svg": svg_c})
        if d == correct_dir and dots == correct_dots and sz == correct_size:
            answer_label = labels[i]

    return _make_question(
        id_=id_,
        difficulty="Hard",
        question="Three rules operate simultaneously. Which figure comes next?",
        svg_question=svg_q,
        choices=choices,
        answer=answer_label,
        explanation=f"Rule 1: Arrow rotates 90° CW ({dir_seq[0]}→{dir_seq[1]}→{dir_seq[2]}→{dir_seq[3]}). Rule 2: Dot count increases by 1 (1→2→3→4). Rule 3: Arrow size grows each step.",
        tags=["abstract reasoning", "rotation", "transformation", "multi-rule", "advanced", "shape patterns"],
    )



# ---------------------------------------------------------------------------
# Main generation
# ---------------------------------------------------------------------------

def generate_all_questions() -> list[dict]:
    """Generate 100 questions: 34 Easy, 33 Medium, 33 Hard."""
    questions: list[dict] = []
    id_counter = 1

    # ===================================================================
    # BATCH 1 (50 questions) — seed 42
    # ===================================================================
    random.seed(42)

    # --- EASY (17 questions) ---
    for i in range(4):
        questions.append(gen_arrow_rotation_90cw(id_counter, start_idx=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_arrow_rotation_90ccw(id_counter, start_idx=i))
        id_counter += 1

    for i in range(2):
        questions.append(gen_arrow_rotation_180(id_counter, start_idx=i))
        id_counter += 1

    for start in [3, 4, 5]:
        questions.append(gen_polygon_sides_increase(id_counter, start_sides=start))
        id_counter += 1

    for start in [1, 2, 3]:
        questions.append(gen_dot_count_increase(id_counter, start=start))
        id_counter += 1

    for shape in ["circle", "square"]:
        questions.append(gen_size_progression(id_counter, shape=shape))
        id_counter += 1

    # --- MEDIUM (17 questions) ---
    for i in range(4):
        questions.append(gen_arrow_rotation_45(id_counter, start_idx=i))
        id_counter += 1

    for i in range(2):
        questions.append(gen_reflection_vertical(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_rotation_plus_shading(id_counter, start_idx=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_shape_alternation(id_counter, variant=i))
        id_counter += 1

    for sides, rot in [(4, 45), (5, 72)]:
        questions.append(gen_polygon_rotation(id_counter, sides=sides, rot_per_step=rot))
        id_counter += 1

    for i in range(2):
        questions.append(gen_shading_progression(id_counter, variant=i))
        id_counter += 1

    questions.append(gen_odd_one_out(id_counter, variant=0))
    id_counter += 1

    # --- HARD (16 questions) ---
    for start in [3, 4, 5, 3]:
        rot = 90 if start != 5 else 72
        questions.append(gen_rotation_plus_sides(id_counter, start_sides=start, rot_per_step=rot))
        id_counter += 1

    for i in range(3):
        questions.append(gen_nested_shapes(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_grid_reasoning(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_dot_movement(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_triple_rule(id_counter, variant=i))
        id_counter += 1

    # ===================================================================
    # BATCH 2 (50 more questions) — guaranteed unique via different colors
    # The geometry for some questions is identical to batch 1 (same start_idx),
    # so we force a different color by overriding COLORS order.
    # ===================================================================
    random.seed(99)
    # Rotate the COLORS list so batch 2 picks different colors
    global COLORS
    COLORS_ORIG = COLORS[:]
    COLORS = COLORS[3:] + COLORS[:3]  # shift by 3

    # --- EASY (17 questions) ---
    for i in range(4):
        questions.append(gen_arrow_rotation_90cw(id_counter, start_idx=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_arrow_rotation_90ccw(id_counter, start_idx=i))
        id_counter += 1

    for i in range(2):
        questions.append(gen_arrow_rotation_180(id_counter, start_idx=i))
        id_counter += 1

    # Non-overlapping polygon starts
    for start in [6, 7, 8]:
        questions.append(gen_polygon_sides_increase(id_counter, start_sides=start))
        id_counter += 1

    # Non-overlapping dot counts
    for start in [5, 6, 7]:
        questions.append(gen_dot_count_increase(id_counter, start=start))
        id_counter += 1

    for shape in ["circle", "square"]:
        questions.append(gen_size_progression(id_counter, shape=shape))
        id_counter += 1

    # --- MEDIUM (17 questions) ---
    for i in [4, 5, 6, 7]:
        questions.append(gen_arrow_rotation_45(id_counter, start_idx=i))
        id_counter += 1

    for i in [2, 3]:
        questions.append(gen_reflection_vertical(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_rotation_plus_shading(id_counter, start_idx=i))
        id_counter += 1

    for i in [3, 4, 5]:
        questions.append(gen_shape_alternation(id_counter, variant=i))
        id_counter += 1

    for sides, rot in [(3, 120), (6, 30)]:
        questions.append(gen_polygon_rotation(id_counter, sides=sides, rot_per_step=rot))
        id_counter += 1

    for i in [2, 3]:
        questions.append(gen_shading_progression(id_counter, variant=i))
        id_counter += 1

    questions.append(gen_odd_one_out(id_counter, variant=2))
    id_counter += 1

    # --- HARD (16 questions) ---
    for start, rot in [(5, 72), (6, 60), (7, 45), (8, 40)]:
        questions.append(gen_rotation_plus_sides(id_counter, start_sides=start, rot_per_step=rot))
        id_counter += 1

    for i in [5, 6, 7]:
        questions.append(gen_nested_shapes(id_counter, variant=i))
        id_counter += 1

    for i in [5, 6, 7]:
        questions.append(gen_grid_reasoning(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_dot_movement(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_triple_rule(id_counter, variant=i))
        id_counter += 1

    # Restore COLORS
    COLORS = COLORS_ORIG

    # ===================================================================
    # BATCH 3 (50 more questions) — seed 777, reversed color palette
    # ===================================================================
    random.seed(777)
    COLORS = COLORS_ORIG[::-1]  # reverse the palette

    # --- EASY (17 questions) ---
    for i in range(4):
        questions.append(gen_arrow_rotation_90cw(id_counter, start_idx=i))
        id_counter += 1

    for i in range(4):
        questions.append(gen_arrow_rotation_90ccw(id_counter, start_idx=i))
        id_counter += 1

    for start in [9, 10, 11]:
        questions.append(gen_polygon_sides_increase(id_counter, start_sides=start))
        id_counter += 1

    for start in [8, 9, 10]:
        questions.append(gen_dot_count_increase(id_counter, start=start))
        id_counter += 1

    for i in range(2):
        questions.append(gen_arrow_rotation_180(id_counter, start_idx=i))
        id_counter += 1

    for shape in ["circle"]:
        questions.append(gen_size_progression(id_counter, shape=shape))
        id_counter += 1

    # --- MEDIUM (17 questions) ---
    for i in [2, 3, 5, 6]:
        questions.append(gen_arrow_rotation_45(id_counter, start_idx=i))
        id_counter += 1

    for i in [4, 5]:
        questions.append(gen_reflection_vertical(id_counter, variant=i))
        id_counter += 1

    for i in range(3):
        questions.append(gen_rotation_plus_shading(id_counter, start_idx=i))
        id_counter += 1

    for i in [6, 7, 8]:
        questions.append(gen_shape_alternation(id_counter, variant=i))
        id_counter += 1

    for sides, rot in [(4, 90), (7, 45)]:
        questions.append(gen_polygon_rotation(id_counter, sides=sides, rot_per_step=rot))
        id_counter += 1

    for i in [4, 5]:
        questions.append(gen_shading_progression(id_counter, variant=i))
        id_counter += 1

    questions.append(gen_odd_one_out(id_counter, variant=3))
    id_counter += 1

    # --- HARD (16 questions) ---
    for start, rot in [(3, 60), (4, 45), (9, 40), (10, 36)]:
        questions.append(gen_rotation_plus_sides(id_counter, start_sides=start, rot_per_step=rot))
        id_counter += 1

    for i in [8, 9, 10]:
        questions.append(gen_nested_shapes(id_counter, variant=i))
        id_counter += 1

    for i in [8, 9, 10]:
        questions.append(gen_grid_reasoning(id_counter, variant=i))
        id_counter += 1

    for i in [1, 2, 3]:
        questions.append(gen_dot_movement(id_counter, variant=i))
        id_counter += 1

    for i in [1, 2, 3]:
        questions.append(gen_triple_rule(id_counter, variant=i))
        id_counter += 1

    COLORS = COLORS_ORIG

    # --- POST-PROCESSING: Deduplicate by question text ---
    # Some generators produce identical SVGs when variant wraps around.
    # Remove duplicates and regenerate replacements with higher variant numbers.
    seen_svgs: set[str] = set()
    unique_questions: list[dict] = []
    for q in questions:
        if q["question"] not in seen_svgs:
            seen_svgs.add(q["question"])
            unique_questions.append(q)

    # Fill gaps with additional unique questions
    extra_id = id_counter
    extra_variant = 10
    generators_for_fill = [
        lambda v: gen_arrow_rotation_90cw(extra_id, start_idx=v % 4),
        lambda v: gen_arrow_rotation_90ccw(extra_id, start_idx=v % 4),
        lambda v: gen_arrow_rotation_45(extra_id, start_idx=v),
        lambda v: gen_polygon_rotation(extra_id, sides=3 + (v % 5), rot_per_step=30 + (v % 4) * 15),
        lambda v: gen_dot_movement(extra_id, variant=v % 4),
        lambda v: gen_nested_shapes(extra_id, variant=v),
        lambda v: gen_grid_reasoning(extra_id, variant=v),
        lambda v: gen_triple_rule(extra_id, variant=v % 4),
    ]

    fill_attempts = 0
    while len(unique_questions) < 150 and fill_attempts < 300:
        gen_fn = generators_for_fill[fill_attempts % len(generators_for_fill)]
        random.seed(200 + fill_attempts)
        COLORS = COLORS_ORIG[fill_attempts % len(COLORS_ORIG):] + COLORS_ORIG[:fill_attempts % len(COLORS_ORIG)]
        try:
            candidate = gen_fn(extra_variant + fill_attempts)
            candidate["id"] = extra_id
            if candidate["question"] not in seen_svgs:
                seen_svgs.add(candidate["question"])
                unique_questions.append(candidate)
                extra_id += 1
        except Exception:
            pass
        fill_attempts += 1

    COLORS = COLORS_ORIG

    # Re-number IDs sequentially
    for i, q in enumerate(unique_questions):
        q["id"] = i + 1

    return unique_questions[:150]


def main() -> None:
    questions = generate_all_questions()

    # Verify counts
    easy = [q for q in questions if q["difficulty"] == "Easy"]
    medium = [q for q in questions if q["difficulty"] == "Medium"]
    hard = [q for q in questions if q["difficulty"] == "Hard"]
    print(f"Generated: {len(questions)} total | Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Written to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
