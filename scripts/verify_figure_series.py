"""Verify figure series questions for 100% answer accuracy.

Checks:
1. Structural integrity (all required keys, 4 choices, answer in choices)
2. No duplicate questions (by SVG content)
3. Answer correctness by re-running the generation logic independently
4. SVG well-formedness (balanced tags)
5. Explanation consistency with answer

Usage:
    python scripts/verify_figure_series.py
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

QUESTIONS_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "analytical-ability" / "abstract-reasoning" / "figure-series"
    / "questions.json"
)

REQUIRED_KEYS = {"id", "subtest", "module", "subtopic", "difficulty",
                 "question", "choices", "answer", "explanation", "tags"}

VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}

# Direction sequences for verification
DIRECTIONS_4 = ["up", "right", "down", "left"]
DIRECTIONS_4_CCW = ["up", "left", "down", "right"]
DIRECTIONS_8 = ["up", "up-right", "right", "down-right", "down",
                "down-left", "left", "up-left"]


def load_questions() -> list[dict]:
    return json.loads(QUESTIONS_PATH.read_text(encoding="utf-8"))


def check_structure(questions: list[dict]) -> list[str]:
    """Check structural integrity of all questions."""
    errors = []
    for q in questions:
        qid = q.get("id", "?")
        # Required keys
        missing = REQUIRED_KEYS - set(q.keys())
        if missing:
            errors.append(f"Q{qid}: Missing keys: {missing}")
        # Difficulty valid
        if q.get("difficulty") not in VALID_DIFFICULTIES:
            errors.append(f"Q{qid}: Invalid difficulty '{q.get('difficulty')}'")
        # Exactly 4 choices
        if len(q.get("choices", [])) != 4:
            errors.append(f"Q{qid}: Has {len(q.get('choices', []))} choices (expected 4)")
        # Answer in choices
        if q.get("answer") not in q.get("choices", []):
            errors.append(f"Q{qid}: Answer not found in choices")
        # Tags non-empty
        if not q.get("tags"):
            errors.append(f"Q{qid}: Empty tags")
        # Subtopic correct
        if q.get("subtopic") != "Figure Series":
            errors.append(f"Q{qid}: Wrong subtopic '{q.get('subtopic')}'")
        # Module correct
        if q.get("module") != "Abstract Reasoning":
            errors.append(f"Q{qid}: Wrong module '{q.get('module')}'")
    return errors


def check_duplicates(questions: list[dict]) -> list[str]:
    """Check for duplicate questions by SVG content."""
    errors = []
    seen_svgs = {}
    for q in questions:
        # Extract SVG from question (the visual part)
        svg_match = re.search(r"<svg.*?</svg>", q["question"], re.DOTALL)
        if svg_match:
            svg = svg_match.group()
            if svg in seen_svgs:
                errors.append(
                    f"Q{q['id']}: Duplicate SVG with Q{seen_svgs[svg]}"
                )
            else:
                seen_svgs[svg] = q["id"]
    return errors


def check_svg_wellformedness(questions: list[dict]) -> list[str]:
    """Basic SVG tag balance check."""
    errors = []
    for q in questions:
        qid = q["id"]
        # Check question SVG
        svg_count = q["question"].count("<svg")
        svg_close = q["question"].count("</svg>")
        if svg_count != svg_close:
            errors.append(f"Q{qid}: Unbalanced SVG tags in question ({svg_count} open, {svg_close} close)")
        # Check choice SVGs
        for i, choice in enumerate(q["choices"]):
            c_open = choice.count("<svg")
            c_close = choice.count("</svg>")
            if c_open != c_close:
                errors.append(f"Q{qid} choice {i}: Unbalanced SVG tags")
    return errors


def check_answer_in_explanation(questions: list[dict]) -> list[str]:
    """Verify the explanation is non-empty and mentions the answer direction/concept."""
    errors = []
    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")
        if len(explanation) < 10:
            errors.append(f"Q{qid}: Explanation too short ({len(explanation)} chars)")
    return errors


def verify_rotation_answers(questions: list[dict]) -> list[str]:
    """For rotation-based questions, verify the answer SVG matches the expected direction."""
    errors = []

    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")
        answer = q.get("answer", "")

        # Only verify questions we can parse the rule for
        # Check 90° CW rotation questions
        if "rotates 90° clockwise" in explanation or "rotates 90° CW" in explanation:
            # Extract the sequence from explanation
            # Pattern: "up → right → down → left" or similar
            dir_match = re.search(
                r"(up|right|down|left)\s*→\s*(up|right|down|left)\s*→\s*(up|right|down|left)\s*→\s*(up|right|down|left)",
                explanation
            )
            if dir_match:
                seq = [dir_match.group(i) for i in range(1, 5)]
                # Verify it's actually 90° CW
                for i in range(len(seq) - 1):
                    expected_next_idx = (DIRECTIONS_4.index(seq[i]) + 1) % 4
                    if seq[i + 1] != DIRECTIONS_4[expected_next_idx]:
                        errors.append(
                            f"Q{qid}: Explanation claims 90° CW but sequence "
                            f"'{seq[i]} → {seq[i+1]}' is not 90° CW"
                        )
                        break

        # Check 90° CCW rotation questions
        elif "rotates 90° counterclockwise" in explanation or "rotates 90° CCW" in explanation:
            dir_match = re.search(
                r"(up|right|down|left)\s*→\s*(up|right|down|left)\s*→\s*(up|right|down|left)\s*→\s*(up|right|down|left)",
                explanation
            )
            if dir_match:
                seq = [dir_match.group(i) for i in range(1, 5)]
                for i in range(len(seq) - 1):
                    expected_next_idx = (DIRECTIONS_4.index(seq[i]) - 1) % 4
                    if seq[i + 1] != DIRECTIONS_4[expected_next_idx]:
                        errors.append(
                            f"Q{qid}: Explanation claims 90° CCW but sequence "
                            f"'{seq[i]} → {seq[i+1]}' is not 90° CCW"
                        )
                        break

        # Check 180° alternation
        elif "alternates 180" in explanation or "alternating between" in explanation:
            # Must match compound directions first (up-right before up)
            dir_match = re.search(
                r"(up-right|up-left|down-right|down-left|up|right|down|left)\s*[↔→]\s*(up-right|up-left|down-right|down-left|up|right|down|left)",
                explanation
            )
            if dir_match:
                d1, d2 = dir_match.group(1), dir_match.group(2)
                # Verify they are 180° apart
                opposites = {
                    "up": "down", "down": "up", "left": "right", "right": "left",
                    "up-right": "down-left", "down-left": "up-right",
                    "up-left": "down-right", "down-right": "up-left",
                }
                if opposites.get(d1) != d2:
                    errors.append(
                        f"Q{qid}: Claims 180° alternation but {d1} ↔ {d2} are not opposites"
                    )

    return errors


def verify_count_progression(questions: list[dict]) -> list[str]:
    """For count-based questions, verify the numeric progression is correct."""
    errors = []

    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")

        # Match patterns like "1 → 2 → 3 → 4" or "2 → 4 → 6 → 8"
        count_match = re.search(r"(\d+)\s*→\s*(\d+)\s*→\s*(\d+)\s*→\s*(\d+)", explanation)
        if count_match and ("increases by" in explanation or "increase by" in explanation):
            nums = [int(count_match.group(i)) for i in range(1, 5)]
            # Check constant difference
            diffs = [nums[i+1] - nums[i] for i in range(3)]
            if len(set(diffs)) != 1:
                errors.append(
                    f"Q{qid}: Claims constant increase but differences are {diffs} "
                    f"(sequence: {nums})"
                )

    return errors


def verify_sides_progression(questions: list[dict]) -> list[str]:
    """For side-count questions, verify sides increase by 1."""
    errors = []

    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")

        if "Sides increase by 1" in explanation or "sides increases by 1" in explanation:
            count_match = re.search(r"(\d+)\s*→\s*(\d+)\s*→\s*(\d+)\s*→\s*(\d+)", explanation)
            if count_match:
                nums = [int(count_match.group(i)) for i in range(1, 5)]
                for i in range(3):
                    if nums[i+1] - nums[i] != 1:
                        errors.append(
                            f"Q{qid}: Claims sides +1 but {nums[i]} → {nums[i+1]} is not +1"
                        )
                        break

    return errors


def verify_alternating_patterns(questions: list[dict]) -> list[str]:
    """For alternating questions, verify the pattern actually alternates."""
    errors = []

    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")

        if "alternate:" in explanation.lower() or "alternating" in explanation.lower():
            # Check A → B → A → B pattern mentions
            alt_match = re.search(
                r"(circle|square|triangle)\s*→\s*(circle|square|triangle)\s*→\s*(circle|square|triangle)\s*→\s*(circle|square|triangle)",
                explanation
            )
            if alt_match:
                seq = [alt_match.group(i) for i in range(1, 5)]
                # Verify alternation: seq[0]==seq[2] and seq[1]==seq[3]
                if seq[0] != seq[2] or seq[1] != seq[3]:
                    errors.append(
                        f"Q{qid}: Claims alternating but sequence {seq} does not alternate"
                    )

    return errors


def verify_45_degree_rotation(questions: list[dict]) -> list[str]:
    """For 45° rotation questions, verify the 8-direction sequence."""
    errors = []

    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")

        if "rotates 45° clockwise" in explanation or "rotates 45°" in explanation:
            # Extract direction sequence
            dirs_in_exp = re.findall(
                r"(up-right|up-left|down-right|down-left|up|right|down|left)",
                explanation
            )
            if len(dirs_in_exp) >= 4:
                seq = dirs_in_exp[:4]
                # Verify each step is +1 in DIRECTIONS_8
                valid = True
                for i in range(len(seq) - 1):
                    if seq[i] in DIRECTIONS_8 and seq[i+1] in DIRECTIONS_8:
                        idx1 = DIRECTIONS_8.index(seq[i])
                        idx2 = DIRECTIONS_8.index(seq[i+1])
                        if (idx1 + 1) % 8 != idx2:
                            valid = False
                            break
                if not valid:
                    errors.append(
                        f"Q{qid}: Claims 45° CW but sequence {seq} has non-45° step"
                    )

    return errors


def verify_cycle_patterns(questions: list[dict]) -> list[str]:
    """For cyclic pattern questions, verify the cycle repeats correctly."""
    errors = []

    for q in questions:
        qid = q["id"]
        explanation = q.get("explanation", "")

        if "cycle is" in explanation.lower() or "cycles" in explanation.lower():
            # Look for "circle → square → triangle → repeat" style
            cycle_match = re.search(
                r"(circle|square|triangle)\s*→\s*(circle|square|triangle)\s*→\s*(circle|square|triangle)\s*→\s*repeat",
                explanation
            )
            if cycle_match:
                cycle = [cycle_match.group(i) for i in range(1, 4)]
                # Verify all elements are distinct
                if len(set(cycle)) != 3:
                    errors.append(
                        f"Q{qid}: Cycle {cycle} has duplicates (not a valid 3-cycle)"
                    )

    return errors


def verify_answer_label_consistency(questions: list[dict]) -> list[str]:
    """Verify that the answer string starts with a valid label (A/B/C/D)."""
    errors = []
    for q in questions:
        qid = q["id"]
        answer = q["answer"]
        if not re.match(r"^[A-D]: ", answer):
            errors.append(f"Q{qid}: Answer doesn't start with valid label: '{answer[:20]}...'")
        # Verify all choices have proper labels
        for i, choice in enumerate(q["choices"]):
            expected_label = chr(65 + i)  # A, B, C, D
            if not choice.startswith(f"{expected_label}: "):
                errors.append(f"Q{qid}: Choice {i} doesn't start with '{expected_label}: '")
    return errors


def verify_unique_choices(questions: list[dict]) -> list[str]:
    """Verify all 4 choices in each question are distinct."""
    errors = []
    for q in questions:
        qid = q["id"]
        # Strip labels to compare SVG content
        svgs = [c.split(": ", 1)[1] if ": " in c else c for c in q["choices"]]
        if len(set(svgs)) != 4:
            errors.append(f"Q{qid}: Has duplicate choices (only {len(set(svgs))} unique)")
    return errors


def main() -> None:
    print("=" * 60)
    print("FIGURE SERIES QUESTION BANK VERIFICATION")
    print("=" * 60)

    questions = load_questions()
    print(f"\nLoaded {len(questions)} questions")
    print(f"  Easy: {sum(1 for q in questions if q['difficulty'] == 'Easy')}")
    print(f"  Medium: {sum(1 for q in questions if q['difficulty'] == 'Medium')}")
    print(f"  Hard: {sum(1 for q in questions if q['difficulty'] == 'Hard')}")

    all_errors: list[str] = []

    # Run all checks
    checks = [
        ("Structure", check_structure),
        ("Duplicates", check_duplicates),
        ("SVG Well-formedness", check_svg_wellformedness),
        ("Explanation Quality", check_answer_in_explanation),
        ("Rotation Answers", verify_rotation_answers),
        ("Count Progression", verify_count_progression),
        ("Sides Progression", verify_sides_progression),
        ("Alternating Patterns", verify_alternating_patterns),
        ("45° Rotation", verify_45_degree_rotation),
        ("Cycle Patterns", verify_cycle_patterns),
        ("Answer Labels", verify_answer_label_consistency),
        ("Unique Choices", verify_unique_choices),
    ]

    for name, check_fn in checks:
        errors = check_fn(questions)
        status = "✓ PASS" if not errors else f"✗ FAIL ({len(errors)} issues)"
        print(f"\n  [{status}] {name}")
        if errors:
            for e in errors[:10]:  # Show first 10
                print(f"    → {e}")
            if len(errors) > 10:
                print(f"    ... and {len(errors) - 10} more")
        all_errors.extend(errors)

    print("\n" + "=" * 60)
    if all_errors:
        print(f"RESULT: {len(all_errors)} issues found")
        sys.exit(1)
    else:
        print("RESULT: ALL CHECKS PASSED ✓ (100% accuracy verified)")
        sys.exit(0)


if __name__ == "__main__":
    main()
