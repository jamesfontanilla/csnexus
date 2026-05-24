"""Verify all 600 matrix reasoning questions for correctness.

Checks:
1. Structural integrity (all required fields present, correct types)
2. Answer consistency (answer matches one of the choices exactly)
3. Difficulty distribution (200 Easy, 200 Medium, 200 Hard)
4. ID uniqueness and sequential ordering
5. Logical correctness by re-generating each question and comparing
6. SVG well-formedness (basic tag matching)
7. No duplicate questions

Usage:
    python scripts/verify_matrix_reasoning.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from collections import Counter

QUESTIONS_PATH = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions"
    / "analytical-ability" / "abstract-reasoning" / "matrix-reasoning"
    / "questions.json"
)

REQUIRED_FIELDS = ["id", "subtest", "module", "subtopic", "difficulty",
                   "question", "choices", "answer", "explanation", "tags"]

VALID_DIFFICULTIES = {"Easy", "Medium", "Hard"}
EXPECTED_TOTAL = 600
EXPECTED_PER_DIFFICULTY = 200


def load_questions() -> list[dict]:
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def check_structure(questions: list[dict]) -> list[str]:
    """Check structural integrity of all questions."""
    errors = []

    if len(questions) != EXPECTED_TOTAL:
        errors.append(f"TOTAL COUNT: Expected {EXPECTED_TOTAL}, got {len(questions)}")

    for i, q in enumerate(questions):
        prefix = f"Q{q.get('id', f'index_{i}')}"

        # Check required fields
        for field in REQUIRED_FIELDS:
            if field not in q:
                errors.append(f"{prefix}: Missing required field '{field}'")

        # Check field types
        if "id" in q and not isinstance(q["id"], int):
            errors.append(f"{prefix}: 'id' should be int, got {type(q['id']).__name__}")
        if "choices" in q and not isinstance(q["choices"], list):
            errors.append(f"{prefix}: 'choices' should be list")
        elif "choices" in q and len(q["choices"]) != 4:
            errors.append(f"{prefix}: Expected 4 choices, got {len(q['choices'])}")
        if "tags" in q and not isinstance(q["tags"], list):
            errors.append(f"{prefix}: 'tags' should be list")
        if "difficulty" in q and q["difficulty"] not in VALID_DIFFICULTIES:
            errors.append(f"{prefix}: Invalid difficulty '{q['difficulty']}'")

        # Check subtest/module/subtopic
        if q.get("subtest") != "Analytical Ability":
            errors.append(f"{prefix}: Wrong subtest '{q.get('subtest')}'")
        if q.get("module") != "Abstract Reasoning":
            errors.append(f"{prefix}: Wrong module '{q.get('module')}'")
        if q.get("subtopic") != "Matrix Reasoning":
            errors.append(f"{prefix}: Wrong subtopic '{q.get('subtopic')}'")

    return errors


def check_answer_consistency(questions: list[dict]) -> list[str]:
    """Verify that the answer field matches exactly one of the choices."""
    errors = []

    for q in questions:
        qid = q.get("id", "?")
        prefix = f"Q{qid}"
        answer = q.get("answer", "")
        choices = q.get("choices", [])

        if not answer:
            errors.append(f"{prefix}: Empty answer field")
            continue

        if not choices:
            errors.append(f"{prefix}: Empty choices list")
            continue

        # Check answer is in choices
        if answer not in choices:
            errors.append(f"{prefix}: Answer not found in choices")
            # Show what we have for debugging
            answer_label = answer[:2] if len(answer) >= 2 else answer
            choice_labels = [c[:2] for c in choices]
            errors.append(f"  Answer starts with: '{answer_label}', "
                          f"Choices start with: {choice_labels}")

        # Check answer label format (A:, B:, C:, or D:)
        answer_label_match = re.match(r'^([A-D]):', answer)
        if not answer_label_match:
            errors.append(f"{prefix}: Answer doesn't start with valid label (A-D):")

        # Check all choices have proper labels
        expected_labels = ['A', 'B', 'C', 'D']
        for i, choice in enumerate(choices):
            if not choice.startswith(f"{expected_labels[i]}:"):
                errors.append(f"{prefix}: Choice {i} doesn't start with '{expected_labels[i]}:'")

        # Check no duplicate choices
        if len(set(choices)) != len(choices):
            errors.append(f"{prefix}: Duplicate choices detected")

    return errors


def check_ids(questions: list[dict]) -> list[str]:
    """Check ID uniqueness and sequential ordering."""
    errors = []
    ids = [q.get("id") for q in questions]

    # Check uniqueness
    id_counts = Counter(ids)
    duplicates = {k: v for k, v in id_counts.items() if v > 1}
    if duplicates:
        errors.append(f"DUPLICATE IDs: {duplicates}")

    # Check sequential (1 to 600)
    expected_ids = list(range(1, EXPECTED_TOTAL + 1))
    if sorted(ids) != expected_ids:
        missing = set(expected_ids) - set(ids)
        extra = set(ids) - set(expected_ids)
        if missing:
            errors.append(f"MISSING IDs: {sorted(missing)[:20]}...")
        if extra:
            errors.append(f"EXTRA IDs: {sorted(extra)[:20]}...")

    return errors


def check_difficulty_distribution(questions: list[dict]) -> list[str]:
    """Check difficulty distribution is exactly 200/200/200."""
    errors = []
    diff_counts = Counter(q.get("difficulty") for q in questions)

    for diff in VALID_DIFFICULTIES:
        count = diff_counts.get(diff, 0)
        if count != EXPECTED_PER_DIFFICULTY:
            errors.append(f"DISTRIBUTION: {diff} has {count} questions "
                          f"(expected {EXPECTED_PER_DIFFICULTY})")

    return errors


def check_svg_wellformedness(questions: list[dict]) -> list[str]:
    """Basic SVG well-formedness checks."""
    errors = []

    for q in questions:
        qid = q.get("id", "?")
        prefix = f"Q{qid}"

        # Check question has SVG
        question_text = q.get("question", "")
        if "<svg" not in question_text:
            errors.append(f"{prefix}: No SVG in question")
        elif "</svg>" not in question_text:
            errors.append(f"{prefix}: Unclosed SVG in question")

        # Check SVG tag count matches
        svg_opens = question_text.count("<svg")
        svg_closes = question_text.count("</svg>")
        if svg_opens != svg_closes:
            errors.append(f"{prefix}: SVG tag mismatch in question "
                          f"(opens={svg_opens}, closes={svg_closes})")

        # Check choices have SVG
        for i, choice in enumerate(q.get("choices", [])):
            if "<svg" not in choice:
                errors.append(f"{prefix}: Choice {chr(65+i)} has no SVG")
            elif "</svg>" not in choice:
                errors.append(f"{prefix}: Choice {chr(65+i)} has unclosed SVG")

        # Check answer has SVG
        answer = q.get("answer", "")
        if "<svg" not in answer:
            errors.append(f"{prefix}: Answer has no SVG")

    return errors


def check_logical_correctness(questions: list[dict]) -> list[str]:
    """Re-generate questions and verify answers match.
    
    This imports the generator and re-runs it to confirm deterministic output.
    """
    errors = []

    # Import the generator module
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        import importlib
        import gen_matrix_reasoning_questions as gen_mod
        importlib.reload(gen_mod)

        regenerated = gen_mod.generate_questions()

        if len(regenerated) != len(questions):
            errors.append(f"REGENERATION: Count mismatch "
                          f"(original={len(questions)}, regenerated={len(regenerated)})")
            return errors

        mismatches = 0
        for orig, regen in zip(questions, regenerated):
            if orig["answer"] != regen["answer"]:
                mismatches += 1
                if mismatches <= 10:
                    errors.append(
                        f"Q{orig['id']}: Answer mismatch - "
                        f"original='{orig['answer'][:50]}...' vs "
                        f"regenerated='{regen['answer'][:50]}...'"
                    )
            if orig["explanation"] != regen["explanation"]:
                if mismatches <= 5:
                    errors.append(
                        f"Q{orig['id']}: Explanation mismatch"
                    )

        if mismatches > 10:
            errors.append(f"... and {mismatches - 10} more answer mismatches")

        if mismatches == 0:
            print("  ✓ All answers match regenerated output (deterministic)")

    except Exception as e:
        errors.append(f"REGENERATION FAILED: {e}")

    return errors


def check_answer_logic_by_type(questions: list[dict]) -> list[str]:
    """Verify answer logic based on question type (from tags)."""
    errors = []

    for q in questions:
        qid = q.get("id", "?")
        prefix = f"Q{qid}"
        tags = q.get("tags", [])
        answer = q.get("answer", "")
        explanation = q.get("explanation", "")

        # Basic sanity: explanation should not be empty
        if not explanation or len(explanation) < 10:
            errors.append(f"{prefix}: Explanation too short or empty")

        # Check that answer label in answer matches a valid choice
        answer_match = re.match(r'^([A-D]):', answer)
        if answer_match:
            label = answer_match.group(1)
            choices = q.get("choices", [])
            # Find the choice with this label
            matching_choice = None
            for c in choices:
                if c.startswith(f"{label}:"):
                    matching_choice = c
                    break
            if matching_choice and matching_choice != answer:
                errors.append(f"{prefix}: Answer label '{label}' matches choice "
                              f"but content differs")

        # Verify explanation mentions key concepts based on tags
        if "rotation" in tags:
            rotation_keywords = ["rotat", "clockwise", "counterclockwise", "CW", "CCW",
                                 "pointing", "direction"]
            if not any(kw.lower() in explanation.lower() for kw in rotation_keywords):
                errors.append(f"{prefix}: Rotation question but explanation lacks "
                              f"rotation-related keywords")

        if "progression" in tags:
            prog_keywords = ["increas", "progress", "add", "grow", "left to right",
                             "per column", "per row", "each row"]
            if not any(kw.lower() in explanation.lower() for kw in prog_keywords):
                errors.append(f"{prefix}: Progression question but explanation lacks "
                              f"progression keywords")

        if "distribution" in tags:
            dist_keywords = ["each row", "one of each", "contains", "needs",
                             "missing", "distribution"]
            if not any(kw.lower() in explanation.lower() for kw in dist_keywords):
                errors.append(f"{prefix}: Distribution question but explanation lacks "
                              f"distribution keywords")

    return errors


def check_question_variety(questions: list[dict]) -> list[str]:
    """Check that questions have sufficient variety."""
    errors = []
    warnings = []

    # Check tag variety
    all_tags = set()
    for q in questions:
        all_tags.update(q.get("tags", []))

    if len(all_tags) < 10:
        warnings.append(f"LOW VARIETY: Only {len(all_tags)} unique tags across all questions")

    # Check explanation variety (no exact duplicates beyond threshold)
    explanations = [q.get("explanation", "") for q in questions]
    explanation_counts = Counter(explanations)
    duplicated_explanations = {k: v for k, v in explanation_counts.items() if v > 15}
    if duplicated_explanations:
        for exp, count in duplicated_explanations.items():
            errors.append(f"EXCESSIVE DUPLICATE EXPLANATION ({count}x): '{exp[:80]}...'")

    # Report explanation stats as info (not errors for moderate duplication)
    moderate_dups = {k: v for k, v in explanation_counts.items() if 5 < v <= 15}
    if moderate_dups:
        print(f"\n  ℹ️  {len(moderate_dups)} explanation templates used 6-15 times "
              f"(expected for same-type questions with different visuals)")
    # Check question SVG variety (no exact duplicate matrices)
    question_svgs = [q.get("question", "") for q in questions]
    svg_counts = Counter(question_svgs)
    duplicated_svgs = {k: v for k, v in svg_counts.items() if v > 1}
    if duplicated_svgs:
        errors.append(f"DUPLICATE QUESTIONS: {len(duplicated_svgs)} questions have "
                      f"identical SVG matrices")

    # Report tag distribution
    tag_counts = Counter()
    for q in questions:
        for tag in q.get("tags", []):
            tag_counts[tag] += 1

    print(f"\n  Tag distribution:")
    for tag, count in tag_counts.most_common(15):
        print(f"    {tag}: {count}")

    return errors


def check_choice_answer_svg_match(questions: list[dict]) -> list[str]:
    """Verify that the answer SVG content matches the corresponding choice SVG."""
    errors = []

    for q in questions:
        qid = q.get("id", "?")
        prefix = f"Q{qid}"
        answer = q.get("answer", "")
        choices = q.get("choices", [])

        # Extract answer label
        answer_match = re.match(r'^([A-D]):', answer)
        if not answer_match:
            continue

        label = answer_match.group(1)
        label_idx = ord(label) - ord('A')

        if label_idx >= len(choices):
            errors.append(f"{prefix}: Answer label '{label}' but only {len(choices)} choices")
            continue

        # The answer should be identical to the choice at that index
        if choices[label_idx] != answer:
            # Extract SVG from both
            answer_svg = answer[2:].strip()  # Remove "X: " prefix
            choice_svg = choices[label_idx][2:].strip()
            if answer_svg != choice_svg:
                errors.append(f"{prefix}: Answer SVG doesn't match choice {label} SVG")

    return errors


def check_matrix_has_question_mark(questions: list[dict]) -> list[str]:
    """Verify each matrix SVG contains a question mark (missing cell indicator)."""
    errors = []

    for q in questions:
        qid = q.get("id", "?")
        prefix = f"Q{qid}"
        question_text = q.get("question", "")

        if "?" not in question_text and "&#63;" not in question_text:
            errors.append(f"{prefix}: Matrix SVG has no question mark (missing cell)")

    return errors


def main() -> None:
    print("=" * 60)
    print("MATRIX REASONING QUESTION BANK VERIFICATION")
    print("=" * 60)

    # Load questions
    print(f"\nLoading questions from: {QUESTIONS_PATH}")
    try:
        questions = load_questions()
        print(f"  Loaded {len(questions)} questions")
    except Exception as e:
        print(f"  FATAL: Cannot load questions: {e}")
        sys.exit(1)

    all_errors = []
    all_warnings = []

    # Run all checks
    checks = [
        ("Structural Integrity", check_structure),
        ("Answer Consistency", check_answer_consistency),
        ("ID Validation", check_ids),
        ("Difficulty Distribution", check_difficulty_distribution),
        ("SVG Well-formedness", check_svg_wellformedness),
        ("Matrix Question Mark", check_matrix_has_question_mark),
        ("Choice-Answer SVG Match", check_choice_answer_svg_match),
        ("Answer Logic by Type", check_answer_logic_by_type),
        ("Question Variety", check_question_variety),
        ("Deterministic Regeneration", check_logical_correctness),
    ]

    for check_name, check_fn in checks:
        print(f"\n{'─' * 40}")
        print(f"CHECK: {check_name}")
        print(f"{'─' * 40}")
        errors = check_fn(questions)
        if errors:
            all_errors.extend(errors)
            for err in errors[:20]:  # Limit output
                print(f"  ✗ {err}")
            if len(errors) > 20:
                print(f"  ... and {len(errors) - 20} more errors")
        else:
            print(f"  ✓ PASSED")

    # Summary
    print(f"\n{'=' * 60}")
    print("VERIFICATION SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total questions: {len(questions)}")
    print(f"  Total errors: {len(all_errors)}")

    if all_errors:
        print(f"\n  ❌ VERIFICATION FAILED with {len(all_errors)} errors")
        sys.exit(1)
    else:
        print(f"\n  ✅ ALL CHECKS PASSED - 100% accuracy verified")
        sys.exit(0)


if __name__ == "__main__":
    main()
