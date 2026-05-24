"""Generate abstract reasoning spatial relationship questions with SVG visuals.

Produces 600 questions (200 Easy, 200 Medium, 200 Hard) with mathematically
correct SVG diagrams for spatial reasoning: object positioning, direction/orientation,
mental rotation, spatial visualization, and grid-based reasoning.

Usage:
    python scripts/gen_spatial_relationships_questions.py
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
    / "analytical-ability" / "abstract-reasoning" / "spatial-relationships"
    / "questions.json"
)

# ---------------------------------------------------------------------------
# SVG helpers
# ---------------------------------------------------------------------------

COLORS = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336", "#00BCD4", "#E91E63"]


def _svg_wrap(content: str, w: int = 280, h: int = 100) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _svg_choice(content: str, w: int = 70, h: int = 70) -> str:
    return (
        f"<svg width='{w}' height='{h}' viewBox='0 0 {w} {h}' "
        f"xmlns='http://www.w3.org/2000/svg'>{content}</svg>"
    )


def _arrow_svg(cx: float, cy: float, direction: str, size: float = 16,
               color: str = "#2196F3") -> str:
    """Generate an arrow pointing in a cardinal/intercardinal direction."""
    angles = {
        "up": 0, "right": 90, "down": 180, "left": 270,
        "up-right": 45, "down-right": 135, "down-left": 225, "up-left": 315
    }
    angle = angles[direction]
    rad = math.radians(angle)
    tx = cx + size * math.sin(rad)
    ty = cy - size * math.cos(rad)
    bx = cx - size * math.sin(rad)
    by = cy + size * math.cos(rad)
    wing = size * 0.4
    w1_rad = rad + math.radians(150)
    w2_rad = rad - math.radians(150)
    w1x = tx + wing * math.sin(w1_rad)
    w1y = ty - wing * math.cos(w1_rad)
    w2x = tx + wing * math.sin(w2_rad)
    w2y = ty - wing * math.cos(w2_rad)
    return (
        f"<line x1='{bx:.1f}' y1='{by:.1f}' x2='{tx:.1f}' y2='{ty:.1f}' "
        f"stroke='{color}' stroke-width='2'/>"
        f"<polygon points='{tx:.1f},{ty:.1f} {w1x:.1f},{w1y:.1f} {w2x:.1f},{w2y:.1f}' "
        f"fill='{color}' stroke='{color}' stroke-width='1'/>"
    )


def _circle(cx: float, cy: float, r: float = 10, color: str = "#2196F3",
            fill: str = "none") -> str:
    return f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' fill='{fill}' stroke='{color}' stroke-width='1.5'/>"


def _rect(x: float, y: float, w: float, h: float, color: str = "#4CAF50",
          fill: str = "none") -> str:
    return f"<rect x='{x:.1f}' y='{y:.1f}' width='{w:.1f}' height='{h:.1f}' fill='{fill}' stroke='{color}' stroke-width='1.5'/>"


def _triangle(cx: float, cy: float, size: float = 12, color: str = "#FF9800",
              fill: str = "none", rotation: float = 0) -> str:
    """Equilateral triangle centered at (cx, cy)."""
    pts = []
    for i in range(3):
        a = math.radians(rotation + 120 * i - 90)
        px = cx + size * math.cos(a)
        py = cy + size * math.sin(a)
        pts.append(f"{px:.1f},{py:.1f}")
    return f"<polygon points='{' '.join(pts)}' fill='{fill}' stroke='{color}' stroke-width='1.5'/>"


def _polygon_svg(cx: float, cy: float, sides: int, radius: float = 12,
                 color: str = "#2196F3", fill: str = "none",
                 rotation_deg: float = -90) -> str:
    pts = []
    for i in range(sides):
        a = math.radians(rotation_deg + (360 / sides) * i)
        px = cx + radius * math.cos(a)
        py = cy + radius * math.sin(a)
        pts.append(f"{px:.1f},{py:.1f}")
    return f"<polygon points='{' '.join(pts)}' fill='{fill}' stroke='{color}' stroke-width='1.5'/>"


def _dot(cx: float, cy: float, r: float = 3, color: str = "#FF9800") -> str:
    return f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r:.1f}' fill='{color}' stroke='none'/>"


def _l_shape(cx: float, cy: float, size: float = 20, rotation: int = 0,
             color: str = "#4CAF50", reflected: bool = False) -> str:
    """L-shape at various rotations (0, 90, 180, 270). Rotation in degrees CW."""
    half = size / 2
    # Base L: vertical down + horizontal right from bottom
    points_base = [
        (cx - half, cy - half),  # top of vertical
        (cx - half, cy + half),  # bottom-left corner
        (cx + half, cy + half),  # end of horizontal
    ]
    if reflected:
        points_base = [(2 * cx - px, py) for px, py in points_base]
    rad = math.radians(rotation)
    cos_r, sin_r = math.cos(rad), math.sin(rad)
    rotated = []
    for px, py in points_base:
        dx, dy = px - cx, py - cy
        rx = cx + dx * cos_r - dy * sin_r
        ry = cy + dx * sin_r + dy * cos_r
        rotated.append((rx, ry))
    path_d = f"M {rotated[0][0]:.1f},{rotated[0][1]:.1f}"
    for p in rotated[1:]:
        path_d += f" L {p[0]:.1f},{p[1]:.1f}"
    return f"<path d='{path_d}' fill='none' stroke='{color}' stroke-width='2.5' stroke-linecap='round'/>"


# ---------------------------------------------------------------------------
# Question generators
# ---------------------------------------------------------------------------

DIRECTIONS_4 = ["up", "right", "down", "left"]
DIRECTIONS_8 = ["up", "up-right", "right", "down-right", "down", "down-left", "left", "up-left"]

questions: list[dict] = []
_id_counter = 0


def _next_id() -> int:
    global _id_counter
    _id_counter += 1
    return _id_counter


def _make_question(difficulty: str, question: str, svg_question: str,
                   choices: list[dict], answer: str, explanation: str,
                   tags: list[str]) -> dict:
    return {
        "id": _next_id(),
        "subtest": "Analytical Ability",
        "module": "Abstract Reasoning",
        "subtopic": "Spatial Relationships",
        "difficulty": difficulty,
        "question": question,
        "svg_question": svg_question,
        "choices": choices,
        "answer": answer,
        "explanation": explanation,
        "tags": ["abstract reasoning", "spatial relationships"] + tags,
    }


# ===========================================================================
# TYPE 1: Arrow rotation sequences (Easy - 60 questions)
# ===========================================================================

def gen_arrow_rotation_easy() -> list[dict]:
    """Arrow rotates by fixed angle each step. Predict next direction."""
    results = []
    configs = []
    # 90° CW rotations starting from each direction with various colors
    for start_idx in range(4):
        for color in COLORS:
            configs.append((start_idx, 1, color, "90° clockwise"))
    # 90° CCW rotations
    for start_idx in range(4):
        for color in COLORS:
            configs.append((start_idx, -1, color, "90° counterclockwise"))
    # 180° rotations
    for start_idx in range(4):
        for color in COLORS:
            configs.append((start_idx, 2, color, "180°"))

    random.shuffle(configs)
    configs = configs[:60]
    # Ensure we have exactly 60 by repeating with different colors if needed
    while len(configs) < 60:
        extra = (random.randint(0, 3), random.choice([1, -1, 2]), random.choice(COLORS),
                 random.choice(["90° clockwise", "90° counterclockwise", "180°"]))
        configs.append(extra)
    for cfg in configs[:60]:
        start_idx, step, color, desc = cfg
        seq = []
        for i in range(3):
            idx = (start_idx + step * i) % 4
            seq.append(DIRECTIONS_4[idx])
        answer_idx = (start_idx + step * 3) % 4
        answer_dir = DIRECTIONS_4[answer_idx]

        # Build SVG question
        svg_parts = []
        positions = [50, 120, 190]
        for i, (pos, d) in enumerate(zip(positions, seq)):
            svg_parts.append(_arrow_svg(pos, 50, d, 18, color))
            svg_parts.append(
                f"<text x='{pos}' y='85' text-anchor='middle' font-size='9' "
                f"fill='#888' font-family='sans-serif'>Step {i+1}</text>"
            )
        svg_parts.append(
            f"<text x='250' y='55' text-anchor='middle' font-size='16' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 280, 95)

        # Build choices
        used = {answer_dir}
        distractors = []
        for d in DIRECTIONS_4:
            if d != answer_dir:
                distractors.append(d)
        random.shuffle(distractors)
        all_dirs = [answer_dir] + distractors[:3]
        random.shuffle(all_dirs)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, d in zip(labels, all_dirs):
            svg_c = _svg_choice(_arrow_svg(35, 35, d, 16, color))
            choices.append({"label": label, "svg": svg_c})
            if d == answer_dir:
                correct_label = label

        results.append(_make_question(
            "Easy",
            "Which arrow comes next in the sequence?",
            svg_q,
            choices,
            correct_label,
            f"The arrow rotates {desc} each step: {' → '.join(seq)} → {answer_dir}.",
            ["rotation", "direction", "arrow sequence"]
        ))
    return results


# ===========================================================================
# TYPE 2: Object positioning - relative position matching (Easy - 50 questions)
# ===========================================================================

def gen_position_matching_easy() -> list[dict]:
    """Given a reference arrangement, find the choice that preserves relative positions."""
    results = []
    shapes = ["circle", "square", "triangle"]
    positions_desc = [
        ("above", "below"),
        ("left of", "right of"),
        ("above-left of", "below-right of"),
        ("above-right of", "below-left of"),
    ]

    def _draw_shape(shape: str, cx: float, cy: float, size: float = 10,
                    color: str = "#2196F3") -> str:
        if shape == "circle":
            return _circle(cx, cy, size, color)
        elif shape == "square":
            return _rect(cx - size, cy - size, size * 2, size * 2, color)
        else:
            return _triangle(cx, cy, size, color)

    shape_colors = {"circle": "#2196F3", "square": "#4CAF50", "triangle": "#FF9800"}

    for q_num in range(50):
        random.shuffle(shapes)
        s1, s2, s3 = shapes[0], shapes[1], shapes[2]
        pos_type = random.choice(positions_desc)

        # Reference: s1 is pos_type[0] s2, s3 is to the right
        # Correct arrangement positions
        if "above" in pos_type[0] and "left" not in pos_type[0] and "right" not in pos_type[0]:
            # s1 above s2
            ref_positions = [(35, 25), (35, 55), (65, 55)]
            correct_positions = [(35, 25), (35, 55), (65, 55)]
            wrong1 = [(35, 55), (35, 25), (65, 55)]  # swapped s1/s2
            wrong2 = [(65, 55), (35, 55), (35, 25)]  # all wrong
            wrong3 = [(35, 25), (65, 55), (35, 55)]  # s2/s3 swapped
        elif "left" in pos_type[0] and "above" not in pos_type[0]:
            ref_positions = [(20, 40), (55, 40), (55, 65)]
            correct_positions = [(20, 40), (55, 40), (55, 65)]
            wrong1 = [(55, 40), (20, 40), (55, 65)]
            wrong2 = [(55, 65), (55, 40), (20, 40)]
            wrong3 = [(20, 40), (55, 65), (55, 40)]
        elif "above-left" in pos_type[0]:
            ref_positions = [(20, 20), (55, 55), (55, 20)]
            correct_positions = [(20, 20), (55, 55), (55, 20)]
            wrong1 = [(55, 55), (20, 20), (55, 20)]
            wrong2 = [(55, 20), (55, 55), (20, 20)]
            wrong3 = [(20, 20), (55, 20), (55, 55)]
        else:  # above-right
            ref_positions = [(55, 20), (20, 55), (20, 20)]
            correct_positions = [(55, 20), (20, 55), (20, 20)]
            wrong1 = [(20, 55), (55, 20), (20, 20)]
            wrong2 = [(20, 20), (20, 55), (55, 20)]
            wrong3 = [(55, 20), (20, 20), (20, 55)]

        # Build reference SVG
        ref_svg = ""
        for shape, (cx, cy) in zip([s1, s2, s3], ref_positions):
            ref_svg += _draw_shape(shape, cx, cy, 9, shape_colors[shape])

        svg_q = _svg_wrap(
            f"<text x='140' y='12' text-anchor='middle' font-size='9' fill='#888'>"
            f"Which choice preserves the spatial arrangement?</text>"
            f"<rect x='5' y='18' width='80' height='75' fill='none' stroke='#888' stroke-width='1' rx='3'/>"
            f"<text x='45' y='30' text-anchor='middle' font-size='8' fill='#888'>Reference</text>"
            + ref_svg.replace("cx='", "cx='").replace("cy='", "cy='") +
            f"<line x1='95' y1='18' x2='95' y2='93' stroke='#666' stroke-width='1' stroke-dasharray='3,2'/>",
            280, 98
        )

        # Build choices
        arrangements = [correct_positions, wrong1, wrong2, wrong3]
        random.shuffle(arrangements)
        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, arr in zip(labels, arrangements):
            c_svg = ""
            for shape, (cx, cy) in zip([s1, s2, s3], arr):
                c_svg += _draw_shape(shape, cx, cy, 8, shape_colors[shape])
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if arr == correct_positions:
                correct_label = label

        desc = f"{s1} is {pos_type[0]} {s2}, with {s3} nearby"
        results.append(_make_question(
            "Easy",
            "Which figure preserves the spatial arrangement shown in the reference?",
            svg_q,
            choices,
            correct_label,
            f"The correct answer preserves the relationship: {desc}. "
            f"Other choices swap or rearrange the objects incorrectly.",
            ["object positioning", "relative position"]
        ))
    return results


# ===========================================================================
# TYPE 3: Simple direction identification (Easy - 40 questions)
# ===========================================================================

def gen_direction_identification_easy() -> list[dict]:
    """Identify which direction an arrow/shape is pointing."""
    results = []
    for q_num in range(50):
        color = random.choice(COLORS)
        if q_num < 25:
            # Cardinal directions
            target_dir = random.choice(DIRECTIONS_4)
            all_options = DIRECTIONS_4[:]
        else:
            # Intercardinal
            target_dir = random.choice(DIRECTIONS_8)
            all_options = DIRECTIONS_8[:]

        svg_q = _svg_wrap(
            f"<text x='140' y='15' text-anchor='middle' font-size='10' fill='#888'>"
            f"Which direction is this arrow pointing?</text>"
            + _arrow_svg(140, 55, target_dir, 22, color),
            280, 90
        )

        # Choices are direction labels (text-based for this type)
        random.shuffle(all_options)
        options = [target_dir]
        for d in all_options:
            if d != target_dir and len(options) < 4:
                options.append(d)
        random.shuffle(options)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, d in zip(labels, options):
            # Draw a small arrow in the choice
            svg_c = _svg_choice(_arrow_svg(35, 35, d, 14, color) +
                               f"<text x='35' y='65' text-anchor='middle' font-size='8' fill='#888'>{d}</text>")
            choices.append({"label": label, "svg": svg_c})
            if d == target_dir:
                correct_label = label

        results.append(_make_question(
            "Easy",
            "Which direction is the arrow pointing?",
            svg_q,
            choices,
            correct_label,
            f"The arrow is pointing {target_dir}.",
            ["direction", "orientation", "identification"]
        ))
    return results


# ===========================================================================
# TYPE 4: Containment/nesting (Easy - 50 questions)
# ===========================================================================

def gen_containment_easy() -> list[dict]:
    """Identify correct nesting order of shapes."""
    results = []
    shape_types = ["circle", "square", "triangle"]

    for q_num in range(60):
        random.shuffle(shape_types)
        outer, middle, inner = shape_types[0], shape_types[1], shape_types[2]
        colors = random.sample(COLORS, 3)

        def _nested(o, m, i, cx, cy, s_outer=28, s_mid=18, s_inner=9,
                    c_o="#2196F3", c_m="#4CAF50", c_i="#FF9800"):
            svg = ""
            if o == "circle":
                svg += _circle(cx, cy, s_outer, c_o)
            elif o == "square":
                svg += _rect(cx - s_outer, cy - s_outer, s_outer * 2, s_outer * 2, c_o)
            else:
                svg += _triangle(cx, cy, s_outer, c_o)
            if m == "circle":
                svg += _circle(cx, cy, s_mid, c_m)
            elif m == "square":
                svg += _rect(cx - s_mid, cy - s_mid, s_mid * 2, s_mid * 2, c_m)
            else:
                svg += _triangle(cx, cy, s_mid, c_m)
            if i == "circle":
                svg += _circle(cx, cy, s_inner, c_i)
            elif i == "square":
                svg += _rect(cx - s_inner, cy - s_inner, s_inner * 2, s_inner * 2, c_i)
            else:
                svg += _triangle(cx, cy, s_inner, c_i)
            return svg

        ref_svg = _nested(outer, middle, inner, 50, 55, 28, 18, 9,
                         colors[0], colors[1], colors[2])
        svg_q = _svg_wrap(
            f"<text x='140' y='12' text-anchor='middle' font-size='9' fill='#888'>"
            f"Which choice shows the same nesting order?</text>"
            f"<rect x='10' y='20' width='80' height='75' fill='none' stroke='#888' stroke-width='1' rx='3'/>"
            + ref_svg +
            f"<line x1='100' y1='20' x2='100' y2='95' stroke='#666' stroke-width='1' stroke-dasharray='3,2'/>",
            280, 100
        )

        # Correct: same nesting order
        # Wrong: various permutations
        orderings = [
            (outer, middle, inner),   # correct
            (outer, inner, middle),   # swap middle/inner
            (middle, outer, inner),   # swap outer/middle
            (inner, middle, outer),   # reversed
        ]
        random.shuffle(orderings)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, (o, m, i) in zip(labels, orderings):
            c_svg = _nested(o, m, i, 35, 35, 22, 14, 7, colors[0], colors[1], colors[2])
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if (o, m, i) == (outer, middle, inner):
                correct_label = label

        results.append(_make_question(
            "Easy",
            "Which figure shows the same nesting order as the reference?",
            svg_q,
            choices,
            correct_label,
            f"The correct nesting order is {outer} (outermost) > {middle} (middle) > "
            f"{inner} (innermost). The correct answer preserves this containment hierarchy.",
            ["containment", "nesting", "object positioning"]
        ))
    return results


# ===========================================================================
# TYPE 5: L-shape rotation (Medium - 50 questions)
# ===========================================================================

def gen_l_rotation_medium() -> list[dict]:
    """Identify the correct rotation of an L-shape with anchor dot."""
    results = []

    for q_num in range(50):
        color = random.choice(COLORS[:4])
        start_rot = random.choice([0, 90, 180, 270])
        rotation_step = random.choice([90, -90, 180])
        num_steps = random.choice([1, 2, 3])
        target_rot = (start_rot + rotation_step * num_steps) % 360

        # Dot position relative to L-shape corner
        size = 18
        half = size / 2

        def _get_dot_pos(cx, cy, rot):
            """Dot at the tip of the vertical arm of the L."""
            rad = math.radians(rot)
            cos_r, sin_r = math.cos(rad), math.sin(rad)
            # Tip of vertical arm is at (cx - half, cy - half) in base orientation
            dx, dy = -half, -half
            rx = cx + dx * cos_r - dy * sin_r
            ry = cy + dx * sin_r + dy * cos_r
            return rx, ry

        # Build question SVG showing the sequence
        svg_parts = []
        positions_x = [45, 115, 185]
        if num_steps <= 2:
            positions_x = [60, 140, 220]
        for i in range(min(num_steps + 1, 3)):
            rot_i = (start_rot + rotation_step * i) % 360
            cx = positions_x[i] if i < len(positions_x) else 185
            cy = 50
            svg_parts.append(_l_shape(cx, cy, size, rot_i, color))
            dx, dy = _get_dot_pos(cx, cy, rot_i)
            svg_parts.append(_dot(dx, dy, 3, "#FF9800"))
            svg_parts.append(
                f"<text x='{cx}' y='82' text-anchor='middle' font-size='8' fill='#888'>Step {i+1}</text>"
            )

        if num_steps >= 3:
            svg_parts.append(
                f"<text x='250' y='55' text-anchor='middle' font-size='14' fill='#888'>?</text>"
            )
        else:
            svg_parts.append(
                f"<text x='250' y='55' text-anchor='middle' font-size='14' fill='#888'>?</text>"
            )

        rot_desc = f"{abs(rotation_step)}° {'CW' if rotation_step > 0 else 'CCW'}"
        svg_q = _svg_wrap("".join(svg_parts), 280, 92)

        # Build choices: correct rotation, reflected, wrong rotations
        correct_rot = target_rot
        wrong_rots = []
        for r in [0, 90, 180, 270]:
            if r != correct_rot:
                wrong_rots.append((r, False))
        # Add a reflected version as distractor
        wrong_rots.append((correct_rot, True))
        random.shuffle(wrong_rots)

        all_choices_data = [(correct_rot, False)] + wrong_rots[:3]
        random.shuffle(all_choices_data)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, (rot, refl) in zip(labels, all_choices_data):
            c_svg = _l_shape(35, 35, 14, rot, color, reflected=refl)
            dx, dy = _get_dot_pos(35, 35, rot)
            if refl:
                dx = 70 - dx  # mirror x
            c_svg += _dot(dx, dy, 2.5, "#FF9800")
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if rot == correct_rot and not refl:
                correct_label = label

        results.append(_make_question(
            "Medium",
            f"The L-shape rotates {rot_desc} each step. Which figure comes next?",
            svg_q,
            choices,
            correct_label,
            f"The L-shape rotates {rot_desc} each step. After {num_steps} step(s) from "
            f"{start_rot}°, the final orientation is {target_rot}°. The dot (anchor) "
            f"tracks the rotation and confirms the correct orientation.",
            ["mental rotation", "L-shape", "anchor tracking"]
        ))
    return results


# ===========================================================================
# TYPE 6: 8-direction arrow sequences (Medium - 40 questions)
# ===========================================================================

def gen_8dir_rotation_medium() -> list[dict]:
    """Arrow rotates in 45° increments through 8 directions."""
    results = []

    for q_num in range(40):
        color = random.choice(COLORS)
        step = random.choice([1, 2, 3, -1, -2, -3])  # steps in DIRECTIONS_8
        start_idx = random.randint(0, 7)

        seq = []
        for i in range(3):
            idx = (start_idx + step * i) % 8
            seq.append(DIRECTIONS_8[idx])
        answer_idx = (start_idx + step * 3) % 8
        answer_dir = DIRECTIONS_8[answer_idx]

        svg_parts = []
        positions = [50, 120, 190]
        for i, (pos, d) in enumerate(zip(positions, seq)):
            svg_parts.append(_arrow_svg(pos, 45, d, 16, color))
            svg_parts.append(
                f"<text x='{pos}' y='78' text-anchor='middle' font-size='8' fill='#888'>Step {i+1}</text>"
            )
        svg_parts.append(
            f"<text x='250' y='50' text-anchor='middle' font-size='14' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 280, 85)

        # Choices
        options = [answer_dir]
        for d in DIRECTIONS_8:
            if d != answer_dir and len(options) < 4:
                options.append(d)
        random.shuffle(options)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, d in zip(labels, options):
            choices.append({"label": label, "svg": _svg_choice(_arrow_svg(35, 35, d, 14, color))})
            if d == answer_dir:
                correct_label = label

        angle_step = step * 45
        desc = f"{abs(angle_step)}° {'CW' if angle_step > 0 else 'CCW'}"
        results.append(_make_question(
            "Medium",
            "Which arrow comes next in the sequence?",
            svg_q,
            choices,
            correct_label,
            f"The arrow rotates {desc} each step: {' → '.join(seq)} → {answer_dir}.",
            ["rotation", "8-direction", "intercardinal"]
        ))
    return results


# ===========================================================================
# TYPE 7: Grid movement tracking (Medium - 50 questions)
# ===========================================================================

def gen_grid_movement_medium() -> list[dict]:
    """Track object movement on a 4x4 grid."""
    results = []

    for q_num in range(55):
        grid_size = 4
        cell_size = 16
        # Movement patterns: (dr, dc) per step
        movements = [
            (0, 1, "one cell right"),
            (1, 0, "one cell down"),
            (0, -1, "one cell left"),
            (-1, 0, "one cell up"),
            (1, 1, "one cell diagonally down-right"),
            (-1, 1, "one cell diagonally up-right"),
            (1, -1, "one cell diagonally down-left"),
        ]
        dr, dc, move_desc = random.choice(movements)
        start_r = random.randint(0, 2)
        start_c = random.randint(0, 2)

        # Generate 3 visible positions + answer
        positions_seq = []
        valid = True
        for i in range(4):
            r = start_r + dr * i
            c = start_c + dc * i
            if 0 <= r < grid_size and 0 <= c < grid_size:
                positions_seq.append((r, c))
            else:
                valid = False
                break

        if not valid or len(positions_seq) < 4:
            # Adjust start to ensure all positions are valid
            start_r = max(0, min(grid_size - 1 - abs(dr) * 3, start_r))
            start_c = max(0, min(grid_size - 1 - abs(dc) * 3, start_c))
            if dr < 0:
                start_r = min(grid_size - 1, max(abs(dr) * 3, start_r))
            if dc < 0:
                start_c = min(grid_size - 1, max(abs(dc) * 3, start_c))
            positions_seq = []
            for i in range(4):
                r = start_r + dr * i
                c = start_c + dc * i
                r = max(0, min(grid_size - 1, r))
                c = max(0, min(grid_size - 1, c))
                positions_seq.append((r, c))

        answer_pos = positions_seq[3]

        # Build grid SVG
        grid_offset_x = 20
        grid_offset_y = 15
        svg_parts = []
        # Draw grid
        for row in range(grid_size):
            for col in range(grid_size):
                x = grid_offset_x + col * cell_size
                y = grid_offset_y + row * cell_size
                svg_parts.append(
                    f"<rect x='{x}' y='{y}' width='{cell_size}' height='{cell_size}' "
                    f"fill='none' stroke='#ccc' stroke-width='0.5'/>"
                )

        # Draw first 3 positions with numbers
        for i in range(3):
            r, c = positions_seq[i]
            cx = grid_offset_x + c * cell_size + cell_size / 2
            cy = grid_offset_y + r * cell_size + cell_size / 2
            opacity = 0.4 + i * 0.25
            svg_parts.append(
                f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{cell_size/3:.1f}' "
                f"fill='#2196F3' opacity='{opacity:.1f}'/>"
            )
            svg_parts.append(
                f"<text x='{cx:.1f}' y='{cy + 3:.1f}' text-anchor='middle' "
                f"font-size='7' fill='white'>{i+1}</text>"
            )

        # Question mark at step 4 area
        svg_parts.append(
            f"<text x='{grid_offset_x + grid_size * cell_size + 20}' y='{grid_offset_y + grid_size * cell_size / 2}' "
            f"text-anchor='middle' font-size='12' fill='#888'>Step 4 = ?</text>"
        )

        svg_q = _svg_wrap("".join(svg_parts), 160, 90)

        # Build choices: 4 grid positions
        wrong_positions = []
        for r in range(grid_size):
            for c in range(grid_size):
                if (r, c) != answer_pos and (r, c) not in positions_seq[:3]:
                    wrong_positions.append((r, c))
        random.shuffle(wrong_positions)

        all_positions = [answer_pos] + wrong_positions[:3]
        random.shuffle(all_positions)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, (r, c) in zip(labels, all_positions):
            # Small grid showing the position
            c_parts = []
            for gr in range(grid_size):
                for gc in range(grid_size):
                    x = 5 + gc * 14
                    y = 5 + gr * 14
                    fill = "#2196F3" if (gr, gc) == (r, c) else "none"
                    c_parts.append(
                        f"<rect x='{x}' y='{y}' width='14' height='14' "
                        f"fill='{fill}' stroke='#ccc' stroke-width='0.5'/>"
                    )
            choices.append({"label": label, "svg": _svg_choice("".join(c_parts), 66, 66)})
            if (r, c) == answer_pos:
                correct_label = label

        results.append(_make_question(
            "Medium",
            f"A dot moves {move_desc} each step. Where is it at Step 4?",
            svg_q,
            choices,
            correct_label,
            f"The dot moves {move_desc} each step. Starting at row {start_r+1}, "
            f"column {start_c+1}, after 3 moves it reaches row {answer_pos[0]+1}, "
            f"column {answer_pos[1]+1}.",
            ["grid reasoning", "movement tracking", "spatial progression"]
        ))
    return results


# ===========================================================================
# TYPE 8: Position cycling (Medium - 30 questions)
# ===========================================================================

def gen_position_cycling_medium() -> list[dict]:
    """Objects cycle through positions (top moves to bottom, etc.)."""
    results = []
    shape_set = [
        ("circle", "#2196F3"),
        ("square", "#4CAF50"),
        ("triangle", "#FF9800"),
    ]

    def _draw_at(shape, color, cx, cy, size=10):
        if shape == "circle":
            return _circle(cx, cy, size, color)
        elif shape == "square":
            return _rect(cx - size, cy - size, size * 2, size * 2, color)
        else:
            return _triangle(cx, cy, size, color)

    for q_num in range(30):
        # 3 shapes cycle: each step, top goes to bottom
        random.shuffle(shape_set)
        order_0 = list(range(3))  # indices into shape_set
        # After each step, rotate the order
        shift = random.choice([1, -1])  # 1=top-to-bottom, -1=bottom-to-top

        steps = []
        for s in range(4):
            current = [(order_0[(i - shift * s) % 3]) for i in range(3)]
            steps.append(current)

        # Vertical positions: top, middle, bottom
        y_positions = [25, 50, 75]

        svg_parts = []
        x_positions = [40, 100, 160]
        for s_idx in range(3):
            cx = x_positions[s_idx]
            for pos_idx, shape_idx in enumerate(steps[s_idx]):
                shape_name, color = shape_set[shape_idx]
                svg_parts.append(_draw_at(shape_name, color, cx, y_positions[pos_idx], 8))
            svg_parts.append(
                f"<text x='{cx}' y='92' text-anchor='middle' font-size='8' fill='#888'>Step {s_idx+1}</text>"
            )

        svg_parts.append(
            f"<text x='230' y='50' text-anchor='middle' font-size='14' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 260, 98)

        # Answer is steps[3]
        answer_order = steps[3]
        # Generate wrong orders
        wrong_orders = []
        for perm in [[0, 1, 2], [1, 0, 2], [2, 0, 1], [0, 2, 1], [1, 2, 0]]:
            if perm != answer_order:
                wrong_orders.append(perm)
        random.shuffle(wrong_orders)

        all_orders = [answer_order] + wrong_orders[:3]
        random.shuffle(all_orders)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, order in zip(labels, all_orders):
            c_svg = ""
            for pos_idx, shape_idx in enumerate(order):
                shape_name, color = shape_set[shape_idx]
                c_svg += _draw_at(shape_name, color, 35, 15 + pos_idx * 20, 7)
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if order == answer_order:
                correct_label = label

        cycle_desc = "top to bottom" if shift == 1 else "bottom to top"
        results.append(_make_question(
            "Medium",
            f"Each step, the {cycle_desc} shape cycles. What comes next?",
            svg_q,
            choices,
            correct_label,
            f"The shapes cycle positions: the {'top' if shift == 1 else 'bottom'} shape "
            f"moves to the {'bottom' if shift == 1 else 'top'} each step, and others shift. "
            f"Following this pattern gives the correct arrangement.",
            ["position cycling", "object positioning", "sequence"]
        ))
    return results


# ===========================================================================
# TYPE 9: Polygon rotation with internal marking (Medium - 30 questions)
# ===========================================================================

def gen_polygon_rotation_medium() -> list[dict]:
    """Regular polygon with a dot on one vertex rotates."""
    results = []

    for q_num in range(30):
        sides = random.choice([4, 5, 6])  # square, pentagon, hexagon
        color = random.choice(COLORS[:4])
        start_vertex = random.randint(0, sides - 1)
        vertex_step = random.choice([1, -1, 2])
        rotation_per_step = vertex_step * (360 / sides)

        # Show 3 steps, ask for 4th
        svg_parts = []
        x_positions = [50, 120, 190]
        for s in range(3):
            cx = x_positions[s]
            cy = 45
            rot = rotation_per_step * s
            svg_parts.append(_polygon_svg(cx, cy, sides, 18, color, "none", -90 + rot))
            # Dot on the marked vertex
            dot_angle = math.radians(-90 + rot + (360 / sides) * start_vertex)
            dx = cx + 18 * math.cos(dot_angle)
            dy = cy + 18 * math.sin(dot_angle)
            svg_parts.append(_dot(dx, dy, 3, "#FF9800"))
            svg_parts.append(
                f"<text x='{cx}' y='78' text-anchor='middle' font-size='8' fill='#888'>Step {s+1}</text>"
            )

        svg_parts.append(
            f"<text x='250' y='50' text-anchor='middle' font-size='14' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 280, 85)

        # Answer: rotation at step 3
        answer_rot = rotation_per_step * 3

        # Choices: correct + 3 wrong rotations (ensure all unique)
        # Generate all possible distinct rotations for this polygon
        all_possible = set()
        for i in range(sides * 2):  # enough to cover all unique positions
            r = rotation_per_step * i
            normalized = round(r % 360, 2)
            all_possible.add(normalized)
        # Also add some offset rotations for variety
        for offset in [30, 45, 60, 72, 90, 120, 150, 180]:
            all_possible.add(round((answer_rot + offset) % 360, 2))
            all_possible.add(round((answer_rot - offset) % 360, 2))

        answer_norm = round(answer_rot % 360, 2)
        wrong_rots = sorted([r for r in all_possible if abs(r - answer_norm) > 1])
        random.shuffle(wrong_rots)

        all_rots = [answer_norm] + wrong_rots[:3]
        # Ensure we have exactly 4 unique rotations
        if len(set(all_rots)) < 4:
            extras = [r for r in range(0, 360, 15) if r not in all_rots]
            random.shuffle(extras)
            while len(set(all_rots)) < 4 and extras:
                all_rots.append(extras.pop())
            all_rots = list(dict.fromkeys(all_rots))[:4]  # deduplicate, keep order

        random.shuffle(all_rots)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, rot in zip(labels, all_rots):
            c_svg = _polygon_svg(35, 32, sides, 14, color, "none", -90 + rot)
            dot_angle = math.radians(-90 + rot + (360 / sides) * start_vertex)
            dx = 35 + 14 * math.cos(dot_angle)
            dy = 32 + 14 * math.sin(dot_angle)
            c_svg += _dot(dx, dy, 2.5, "#FF9800")
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if abs(rot - answer_norm) < 1:
                correct_label = label

        if not correct_label:
            correct_label = "A"  # fallback

        results.append(_make_question(
            "Medium",
            f"The {sides}-sided polygon rotates each step. Which comes next?",
            svg_q,
            choices,
            correct_label,
            f"The polygon rotates {abs(rotation_per_step):.0f}° "
            f"{'CW' if rotation_per_step > 0 else 'CCW'} each step. "
            f"Track the orange dot to confirm the correct orientation.",
            ["mental rotation", "polygon", "vertex tracking"]
        ))
    return results


# ===========================================================================
# TYPE 10: Dual transformation - rotation + position change (Hard - 50 questions)
# ===========================================================================

def gen_dual_transform_hard() -> list[dict]:
    """Object rotates AND changes position simultaneously."""
    results = []

    for q_num in range(55):
        color = random.choice(COLORS[:4])
        # Arrow rotates + moves across positions
        rot_step = random.choice([1, -1, 2])  # in DIRECTIONS_4 indices
        # Position moves in a grid pattern
        pos_pattern = random.choice([
            [(20, 30), (45, 30), (70, 30), (95, 30)],  # horizontal
            [(50, 15), (50, 35), (50, 55), (50, 75)],  # vertical
            [(20, 15), (45, 35), (70, 55), (95, 75)],  # diagonal
            [(95, 15), (70, 35), (45, 55), (20, 75)],  # reverse diagonal
        ])

        start_dir_idx = random.randint(0, 3)
        directions = []
        for i in range(4):
            idx = (start_dir_idx + rot_step * i) % 4
            directions.append(DIRECTIONS_4[idx])

        # Build question SVG
        svg_parts = []
        for i in range(3):
            cx, cy = pos_pattern[i]
            # Scale positions for wider SVG
            sx = cx * 2 + 10
            sy = cy + 5
            svg_parts.append(_arrow_svg(sx, sy, directions[i], 12, color))
            svg_parts.append(
                f"<text x='{sx}' y='{sy + 20}' text-anchor='middle' font-size='7' fill='#888'>{i+1}</text>"
            )

        svg_parts.append(
            f"<text x='230' y='45' text-anchor='middle' font-size='12' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 260, 90)

        answer_dir = directions[3]

        # Choices: correct direction at correct position concept
        wrong_dirs = [d for d in DIRECTIONS_4 if d != answer_dir]
        random.shuffle(wrong_dirs)
        all_dirs = [answer_dir] + wrong_dirs[:3]
        random.shuffle(all_dirs)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, d in zip(labels, all_dirs):
            choices.append({"label": label, "svg": _svg_choice(_arrow_svg(35, 35, d, 14, color))})
            if d == answer_dir:
                correct_label = label

        rot_desc = f"{abs(rot_step * 90)}° {'CW' if rot_step > 0 else 'CCW'}"
        results.append(_make_question(
            "Hard",
            "The arrow rotates AND moves each step. Which arrow comes next?",
            svg_q,
            choices,
            correct_label,
            f"Two transformations occur simultaneously: (1) the arrow rotates {rot_desc} "
            f"each step, and (2) it translates along a path. The direction sequence is "
            f"{' → '.join(directions[:3])} → {answer_dir}.",
            ["dual transformation", "rotation", "translation", "advanced"]
        ))
    return results


# ===========================================================================
# TYPE 11: Reflection identification (Hard - 40 questions)
# ===========================================================================

def gen_reflection_hard() -> list[dict]:
    """Distinguish rotated from reflected figures."""
    results = []

    for q_num in range(40):
        color = random.choice(COLORS[:4])
        # Use L-shape which is asymmetric
        original_rot = random.choice([0, 90, 180, 270])
        target_rot = random.choice([r for r in [0, 90, 180, 270] if r != original_rot])

        # Build question: show original, ask which is the ROTATION (not reflection)
        svg_parts = []
        svg_parts.append(
            f"<text x='140' y='12' text-anchor='middle' font-size='9' fill='#888'>"
            f"Which is the {target_rot - original_rot if target_rot > original_rot else target_rot - original_rot + 360}° "
            f"CW rotation (NOT reflection)?</text>"
        )
        svg_parts.append(_l_shape(60, 55, 22, original_rot, color))
        dot_x = 60 + 11 * math.cos(math.radians(original_rot - 90))
        dot_y = 55 + 11 * math.sin(math.radians(original_rot - 90))
        svg_parts.append(_dot(dot_x, dot_y, 3, "#FF9800"))
        svg_parts.append(
            f"<text x='60' y='88' text-anchor='middle' font-size='8' fill='#888'>Original</text>"
        )
        svg_parts.append(
            f"<line x1='110' y1='18' x2='110' y2='88' stroke='#666' stroke-width='1' stroke-dasharray='3,2'/>"
        )

        svg_q = _svg_wrap("".join(svg_parts), 280, 92)

        # Choices: 1 correct rotation, 1 reflection, 2 wrong rotations
        choices_data = [
            (target_rot, False, True),   # correct rotation
            (target_rot, True, False),   # reflection at same angle (trap!)
        ]
        other_rots = [r for r in [0, 90, 180, 270] if r != target_rot and r != original_rot]
        random.shuffle(other_rots)
        for r in other_rots[:2]:
            choices_data.append((r, False, False))

        random.shuffle(choices_data)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, (rot, refl, is_correct) in zip(labels, choices_data):
            c_svg = _l_shape(35, 35, 16, rot, color, reflected=refl)
            d_x = 35 + 8 * math.cos(math.radians(rot - 90))
            d_y = 35 + 8 * math.sin(math.radians(rot - 90))
            if refl:
                d_x = 70 - d_x
            c_svg += _dot(d_x, d_y, 2.5, "#FF9800")
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if is_correct:
                correct_label = label

        results.append(_make_question(
            "Hard",
            "Which figure is the correct ROTATION (not reflection) of the original?",
            svg_q,
            choices,
            correct_label,
            f"The correct answer is the L-shape rotated to {target_rot}° without reflection. "
            f"The reflected version (mirror image) reverses the handedness — the dot appears "
            f"on the wrong side. Always check handedness to distinguish rotation from reflection.",
            ["reflection vs rotation", "handedness", "mental rotation", "advanced"]
        ))
    return results


# ===========================================================================
# TYPE 12: Multi-object spatial arrangement (Hard - 40 questions)
# ===========================================================================

def gen_multi_object_hard() -> list[dict]:
    """Multiple objects each transform independently."""
    results = []

    shape_configs = [
        ("circle", "#2196F3"),
        ("square", "#4CAF50"),
        ("triangle", "#FF9800"),
    ]

    def _draw(shape, color, cx, cy, rot=0, size=8):
        if shape == "circle":
            return _circle(cx, cy, size, color)
        elif shape == "square":
            return _rect(cx - size, cy - size, size * 2, size * 2, color)
        else:
            return _triangle(cx, cy, size, color, rotation=rot)

    for q_num in range(40):
        # 2 objects, each with independent movement
        random.shuffle(shape_configs)
        s1_name, s1_color = shape_configs[0]
        s2_name, s2_color = shape_configs[1]

        # Object 1 moves horizontally, Object 2 moves vertically
        # 3x3 grid positions
        s1_positions = []
        s2_positions = []

        s1_start_r, s1_start_c = random.randint(0, 2), 0
        s2_start_r, s2_start_c = 0, random.randint(0, 2)

        s1_dr, s1_dc = 0, 1  # moves right
        s2_dr, s2_dc = 1, 0  # moves down

        for i in range(4):
            s1_r = (s1_start_r + s1_dr * i) % 3
            s1_c = (s1_start_c + s1_dc * i) % 3
            s2_r = (s2_start_r + s2_dr * i) % 3
            s2_c = (s2_start_c + s2_dc * i) % 3
            s1_positions.append((s1_r, s1_c))
            s2_positions.append((s2_r, s2_c))

        cell = 18
        grid_x, grid_y = 10, 15

        def _draw_grid_state(step_idx, offset_x):
            parts = []
            # Draw 3x3 grid
            for r in range(3):
                for c in range(3):
                    x = offset_x + c * cell
                    y = grid_y + r * cell
                    parts.append(
                        f"<rect x='{x}' y='{y}' width='{cell}' height='{cell}' "
                        f"fill='none' stroke='#ddd' stroke-width='0.5'/>"
                    )
            # Draw objects
            s1_r, s1_c = s1_positions[step_idx]
            s2_r, s2_c = s2_positions[step_idx]
            cx1 = offset_x + s1_c * cell + cell / 2
            cy1 = grid_y + s1_r * cell + cell / 2
            cx2 = offset_x + s2_c * cell + cell / 2
            cy2 = grid_y + s2_r * cell + cell / 2
            parts.append(_draw(s1_name, s1_color, cx1, cy1, size=6))
            parts.append(_draw(s2_name, s2_color, cx2, cy2, size=6))
            return "".join(parts)

        svg_parts = []
        offsets = [10, 75, 140]
        for i in range(3):
            svg_parts.append(_draw_grid_state(i, offsets[i]))
            svg_parts.append(
                f"<text x='{offsets[i] + cell * 1.5}' y='{grid_y + cell * 3 + 12}' "
                f"text-anchor='middle' font-size='7' fill='#888'>Step {i+1}</text>"
            )

        svg_parts.append(
            f"<text x='230' y='40' text-anchor='middle' font-size='12' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 260, 82)

        # Answer: step 3 positions
        answer = (s1_positions[3], s2_positions[3])

        # Wrong answers: various wrong position combinations
        wrong_answers = []
        for _ in range(20):
            w1 = (random.randint(0, 2), random.randint(0, 2))
            w2 = (random.randint(0, 2), random.randint(0, 2))
            if (w1, w2) != answer and (w1, w2) not in wrong_answers:
                wrong_answers.append((w1, w2))
        random.shuffle(wrong_answers)

        all_answers = [answer] + wrong_answers[:3]
        # Ensure all 4 choices are unique
        seen = set()
        unique_answers = []
        for a in all_answers:
            if a not in seen:
                seen.add(a)
                unique_answers.append(a)
        while len(unique_answers) < 4:
            w1 = (random.randint(0, 2), random.randint(0, 2))
            w2 = (random.randint(0, 2), random.randint(0, 2))
            candidate = (w1, w2)
            if candidate not in seen:
                seen.add(candidate)
                unique_answers.append(candidate)
        all_answers = unique_answers
        random.shuffle(all_answers)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, (pos1, pos2) in zip(labels, all_answers):
            c_parts = []
            for r in range(3):
                for c in range(3):
                    x = 5 + c * 18
                    y = 5 + r * 18
                    c_parts.append(
                        f"<rect x='{x}' y='{y}' width='18' height='18' "
                        f"fill='none' stroke='#ddd' stroke-width='0.5'/>"
                    )
            cx1 = 5 + pos1[1] * 18 + 9
            cy1 = 5 + pos1[0] * 18 + 9
            cx2 = 5 + pos2[1] * 18 + 9
            cy2 = 5 + pos2[0] * 18 + 9
            c_parts.append(_draw(s1_name, s1_color, cx1, cy1, size=5))
            c_parts.append(_draw(s2_name, s2_color, cx2, cy2, size=5))
            choices.append({"label": label, "svg": _svg_choice("".join(c_parts), 62, 62)})
            if (pos1, pos2) == answer:
                correct_label = label

        results.append(_make_question(
            "Hard",
            "Two objects move independently on the grid. Where are they at Step 4?",
            svg_q,
            choices,
            correct_label,
            f"The {s1_name} moves one cell right each step (wrapping), while the "
            f"{s2_name} moves one cell down each step (wrapping). Track each object "
            f"independently to find their positions at Step 4.",
            ["multi-object", "grid reasoning", "independent movement", "advanced"]
        ))
    return results


# ===========================================================================
# TYPE 13: Cube net face identification (Hard - 35 questions)
# ===========================================================================

def gen_cube_net_hard() -> list[dict]:
    """Identify which face is opposite a given face on a cube net."""
    results = []

    # Standard cross-shaped cube net positions (row, col)
    # The cross: top at (0,1), left at (1,0), front at (1,1), right at (1,2), back at (1,3), bottom at (2,1)
    face_labels = ["★", "●", "■", "▲", "◆", "♥"]
    opposite_pairs_cross = [(0, 4), (1, 3), (2, 5)]  # indices that are opposite

    symbols_svg = {
        "★": lambda cx, cy, s, c: f"<text x='{cx}' y='{cy+s/3}' text-anchor='middle' font-size='{s}' fill='{c}'>★</text>",
        "●": lambda cx, cy, s, c: f"<circle cx='{cx}' cy='{cy}' r='{s/3}' fill='{c}'/>",
        "■": lambda cx, cy, s, c: f"<rect x='{cx-s/3}' y='{cy-s/3}' width='{s*2/3}' height='{s*2/3}' fill='{c}'/>",
        "▲": lambda cx, cy, s, c: f"<polygon points='{cx},{cy-s/3} {cx-s/3},{cy+s/3} {cx+s/3},{cy+s/3}' fill='{c}'/>",
        "◆": lambda cx, cy, s, c: f"<polygon points='{cx},{cy-s/3} {cx+s/3},{cy} {cx},{cy+s/3} {cx-s/3},{cy}' fill='{c}'/>",
        "♥": lambda cx, cy, s, c: f"<text x='{cx}' y='{cy+s/3}' text-anchor='middle' font-size='{s}' fill='{c}'>♥</text>",
    }

    for q_num in range(35):
        random.shuffle(face_labels)
        assigned = face_labels[:6]
        # Cross net positions: (row, col) -> face index
        net_positions = [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3), (2, 1)]
        # Opposite pairs by position: (0,1)↔(2,1), (1,0)↔(1,2) wait no...
        # In cross net: top(0,1) opposite bottom(2,1), left(1,0) opposite right(1,2)... 
        # Actually: top opposite back(1,3)... Let me use standard:
        # Position 0 (top) is opposite position 5 (bottom)
        # Position 1 (left) is opposite position 3 (right)  
        # Position 2 (front) is opposite position 4 (back)
        opposites = {0: 5, 5: 0, 1: 3, 3: 1, 2: 4, 4: 2}

        # Pick a face to ask about
        ask_idx = random.randint(0, 5)
        answer_idx = opposites[ask_idx]
        answer_symbol = assigned[answer_idx]

        # Draw the net
        cell = 22
        net_x, net_y = 30, 10
        svg_parts = []
        for i, (r, c) in enumerate(net_positions):
            x = net_x + c * cell
            y = net_y + r * cell
            svg_parts.append(
                f"<rect x='{x}' y='{y}' width='{cell}' height='{cell}' "
                f"fill='{'#FFF9C4' if i == ask_idx else 'none'}' stroke='#888' stroke-width='1'/>"
            )
            sym = assigned[i]
            color = "#F44336" if i == ask_idx else "#333"
            svg_parts.append(symbols_svg[sym](x + cell/2, y + cell/2, cell * 0.7, color))

        svg_parts.append(
            f"<text x='200' y='25' text-anchor='middle' font-size='9' fill='#888'>"
            f"Which symbol is</text>"
            f"<text x='200' y='38' text-anchor='middle' font-size='9' fill='#888'>"
            f"OPPOSITE the</text>"
            f"<text x='200' y='51' text-anchor='middle' font-size='9' fill='#F44336'>"
            f"highlighted face?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 260, 85)

        # Choices: the 4 non-asked, non-answer faces + the answer
        other_symbols = [assigned[i] for i in range(6) if i != ask_idx and i != answer_idx]
        random.shuffle(other_symbols)
        all_symbols = [answer_symbol] + other_symbols[:3]
        random.shuffle(all_symbols)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, sym in zip(labels, all_symbols):
            c_svg = symbols_svg[sym](35, 35, 28, "#333")
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if sym == answer_symbol:
                correct_label = label

        face_names = ["top", "left", "front", "right", "back", "bottom"]
        results.append(_make_question(
            "Hard",
            "When this net is folded into a cube, which symbol is opposite the highlighted face?",
            svg_q,
            choices,
            correct_label,
            f"In this cross-shaped net, the {face_names[ask_idx]} face (highlighted) is "
            f"opposite the {face_names[answer_idx]} face. The symbol on the opposite face "
            f"is {answer_symbol}. Remember: faces separated by two squares in a cross net are opposite.",
            ["cube net", "spatial visualization", "opposite faces", "3D reasoning"]
        ))
    return results


# ===========================================================================
# TYPE 14: Complex rotation sequence with size change (Hard - 35 questions)
# ===========================================================================

def gen_rotation_size_hard() -> list[dict]:
    """Shape rotates AND changes size each step."""
    results = []

    for q_num in range(35):
        color = random.choice(COLORS[:4])
        sides = random.choice([3, 4, 5, 6])
        rot_step = random.choice([45, 60, 72, 90, 120])
        size_pattern = random.choice([
            [10, 14, 18, 22],  # growing
            [22, 18, 14, 10],  # shrinking
            [10, 18, 10, 18],  # alternating
            [12, 16, 20, 24],  # growing
        ])

        svg_parts = []
        x_positions = [45, 105, 165]
        for i in range(3):
            cx = x_positions[i]
            cy = 45
            rot = rot_step * i
            size = size_pattern[i]
            svg_parts.append(_polygon_svg(cx, cy, sides, size, color, "none", -90 + rot))
            svg_parts.append(
                f"<text x='{cx}' y='80' text-anchor='middle' font-size='7' fill='#888'>Step {i+1}</text>"
            )

        svg_parts.append(
            f"<text x='230' y='48' text-anchor='middle' font-size='12' fill='#888'>?</text>"
        )
        svg_q = _svg_wrap("".join(svg_parts), 260, 88)

        # Answer: step 3 rotation and size
        answer_rot = rot_step * 3
        answer_size = size_pattern[3]

        # Choices: vary rotation and/or size
        choices_data = [(answer_rot, answer_size, True)]
        # Wrong: correct rotation, wrong size
        wrong_size = random.choice([s for s in [10, 14, 18, 22] if s != answer_size])
        choices_data.append((answer_rot, wrong_size, False))
        # Wrong: wrong rotation, correct size
        wrong_rot = answer_rot + rot_step
        choices_data.append((wrong_rot, answer_size, False))
        # Wrong: wrong both
        choices_data.append((wrong_rot, wrong_size, False))

        random.shuffle(choices_data)

        labels = ["A", "B", "C", "D"]
        choices = []
        correct_label = ""
        for label, (rot, size, is_correct) in zip(labels, choices_data):
            c_svg = _polygon_svg(35, 35, sides, size * 0.7, color, "none", -90 + rot)
            choices.append({"label": label, "svg": _svg_choice(c_svg)})
            if is_correct:
                correct_label = label

        size_desc = "grows" if size_pattern[1] > size_pattern[0] else (
            "shrinks" if size_pattern[1] < size_pattern[0] else "alternates in size"
        )
        results.append(_make_question(
            "Hard",
            "The shape rotates AND changes size. Which comes next?",
            svg_q,
            choices,
            correct_label,
            f"Two transformations: (1) the {sides}-sided polygon rotates {rot_step}° each step, "
            f"and (2) it {size_desc}. At Step 4, the rotation is {answer_rot}° and the size "
            f"follows the pattern. Track both changes independently.",
            ["dual transformation", "rotation", "scaling", "advanced"]
        ))
    return results


# ===========================================================================
# Main generation
# ===========================================================================

def main():
    global questions, _id_counter
    questions = []
    _id_counter = 0

    # Easy (200 total)
    print("Generating Easy questions...")
    easy_qs = []
    easy_qs.extend(gen_arrow_rotation_easy())        # 60
    easy_qs.extend(gen_position_matching_easy())      # 50
    easy_qs.extend(gen_direction_identification_easy())  # 50
    easy_qs.extend(gen_containment_easy())            # 60
    # Trim to exactly 200 (no padding with duplicates)
    easy_qs = easy_qs[:220]  # generate extra to compensate for dedup
    questions.extend(easy_qs)

    easy_count = len(questions)
    print(f"  Easy: {easy_count} questions")

    # Medium (200 total)
    print("Generating Medium questions...")
    medium_qs = []
    medium_qs.extend(gen_l_rotation_medium())           # 50
    medium_qs.extend(gen_8dir_rotation_medium())        # 40
    medium_qs.extend(gen_grid_movement_medium())        # 50
    medium_qs.extend(gen_position_cycling_medium())     # 30
    medium_qs.extend(gen_polygon_rotation_medium())     # 30
    medium_qs = medium_qs[:230]  # generate extra to compensate for dedup
    questions.extend(medium_qs)

    medium_count = len(questions) - easy_count
    print(f"  Medium: {medium_count} questions")

    # Hard (200 total)
    print("Generating Hard questions...")
    hard_qs = []
    hard_qs.extend(gen_dual_transform_hard())         # 50
    hard_qs.extend(gen_reflection_hard())             # 40
    hard_qs.extend(gen_multi_object_hard())           # 40
    hard_qs.extend(gen_cube_net_hard())               # 35
    hard_qs.extend(gen_rotation_size_hard())          # 35
    hard_qs = hard_qs[:230]  # generate extra to compensate for dedup
    questions.extend(hard_qs)

    hard_count = len(questions) - easy_count - medium_count
    print(f"  Hard: {hard_count} questions")
    print(f"  Total: {len(questions)} questions")

    # Reassign IDs sequentially
    for i, q in enumerate(questions, 1):
        q["id"] = i

    # Post-processing: remove questions with duplicate choices, report count
    clean_questions = []
    removed = 0
    for q in questions:
        choice_svgs = [c["svg"] for c in q["choices"]]
        if len(set(choice_svgs)) == 4:
            clean_questions.append(q)
        else:
            removed += 1

    if removed:
        print(f"  Removed {removed} questions with duplicate choices")
        questions = clean_questions

    # Remove truly identical questions (same svg_question + same answer + same choices)
    seen_signatures = set()
    unique_questions = []
    dup_removed = 0
    for q in questions:
        sig = (q["svg_question"], q["answer"],
               tuple(c["svg"] for c in q["choices"]))
        if sig not in seen_signatures:
            seen_signatures.add(sig)
            unique_questions.append(q)
        else:
            dup_removed += 1

    if dup_removed:
        print(f"  Removed {dup_removed} truly duplicate questions")
        questions = unique_questions

    # Re-assign IDs
    for i, q in enumerate(questions, 1):
        q["id"] = i

    # Trim to exactly 600 (200 per difficulty)
    easy = [q for q in questions if q["difficulty"] == "Easy"][:200]
    medium = [q for q in questions if q["difficulty"] == "Medium"][:200]
    hard = [q for q in questions if q["difficulty"] == "Hard"][:200]
    questions = easy + medium + hard
    for i, q in enumerate(questions, 1):
        q["id"] = i

    print(f"  Final count: {len(questions)} "
          f"(E:{len(easy)}, M:{len(medium)}, H:{len(hard)})")

    # Write output
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(questions, f, indent=2, ensure_ascii=False)

    print(f"\nWritten to: {OUTPUT_PATH}")
    print(f"File size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
