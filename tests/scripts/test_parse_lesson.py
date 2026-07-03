from __future__ import annotations

from scripts.parse_lesson import parse_lesson_markdown


SAMPLE_LESSON = """# Fractions and Ratios

## Explanations
### Introduction
Fractions compare parts to a whole.

> [!TIP]
> Think of a fraction like a slice of pizza.

### Why Topic Is Tested
Fractions appear in speed, proportion, and comparison questions.

### Common Mistakes
> [!WARNING]
> Mixing numerator and denominator roles.

### Learning Objectives
- Identify numerator and denominator
- Simplify fractions
- Convert between fractions and ratios

## Ratio Moves
### Overview
Ratios are comparison tools.

### Core Principle
$$a:b = a/b$$

### Visualization
```mermaid
graph TD
  A[Whole] --> B[Part]
```

### Common Mistakes
> [!WARNING]
> Do not cross-multiply too early.

### Worked Mini Example
```python
ratio = 2 / 5
```

### Quick Check
Question: What is 1/2 of 8?
Answer: 4

### Key Insight
Ratios compare quantities with the same units.

## Worked Examples
### Example 1
1. Identify the total.
2. Divide evenly.

| A | B |
|---|---|
| 1 | 2 |

### Example 2
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10"></svg>
```

## Exam Strategies
### Time Management
- Estimate first.
- Skip and return.

### Shortcut & Elimination Techniques
- Cancel common factors.

## Memory Aids
### Mnemonics
- "Part over whole"

## Practice & Review
### Guided Practice
```quiz
Question: What is 3/4 of 8?
Answer: 6
```

## Key Takeaways
- Fractions compare parts.
- Ratios compare quantities.

## Summary
Fractions and ratios are related forms of comparison.

## Final Challenge
### Mixed Practice Set
Question: Which is larger, 2/3 or 3/5?
Answer: 2/3

## Bonus Notes
Some extra note.
"""


def _find_section(sections: list[dict[str, object]], title: str) -> dict[str, object]:
    for section in sections:
        if section.get("title") == title:
            return section
    raise AssertionError(f"Section not found: {title}")


def test_parse_lesson_builds_semantic_sections_and_blocks() -> None:
    result = parse_lesson_markdown(SAMPLE_LESSON, category="math")

    assert result["metadata"]["title"] == "Fractions and Ratios"
    assert result["summary"].startswith("Fractions compare parts")
    assert result["metadata"]["screen_count"] == result["screen_plan"]["screen_count"]
    assert result["screen_plan"]["screens"][0]["kind"] == "cover"
    assert any(screen["kind"] == "concept" for screen in result["screen_plan"]["screens"])
    assert any(screen["kind"] == "practice" for screen in result["screen_plan"]["screens"])
    assert any(screen["kind"] == "summary" for screen in result["screen_plan"]["screens"])

    sections = result["sections"]
    assert [section["kind"] for section in sections[:3]] == [
        "explanations",
        "micro_concept",
        "worked_examples",
    ]

    explanations = _find_section(sections, "Explanations")
    explanation_titles = [subsection["title"] for subsection in explanations.get("subsections", [])]
    assert "Introduction" in explanation_titles
    assert "Learning Objectives" in explanation_titles

    ratio_moves = _find_section(sections, "Ratio Moves")
    subsection_map = {subsection["title"]: subsection for subsection in ratio_moves.get("subsections", [])}
    assert "Core Principle" in subsection_map
    assert "Visualization" in subsection_map
    assert "Worked Mini Example" in subsection_map
    assert "Quick Check" in subsection_map

    core_principle_types = [block["type"] for block in subsection_map["Core Principle"]["blocks"]]
    visualization_types = [block["type"] for block in subsection_map["Visualization"]["blocks"]]
    worked_example_types = [block["type"] for block in subsection_map["Worked Mini Example"]["blocks"]]
    quick_check_types = [block["type"] for block in subsection_map["Quick Check"]["blocks"]]
    assert "formula" in core_principle_types
    assert "code" in visualization_types
    assert "code" in worked_example_types
    assert "check_understanding" in quick_check_types

    worked_examples = _find_section(sections, "Worked Examples")
    example_types = [subsection["kind"] for subsection in worked_examples.get("subsections", [])]
    assert "generic_worked_example" in example_types or "generic_subsection" in example_types

    assert result["practice_problems"]
    assert result["metadata"]["has_practice_problems"] is True
    assert result["memory_aids"]
    assert result["exam_strategies"]


def test_parse_lesson_keeps_unknown_sections_without_crashing() -> None:
    result = parse_lesson_markdown(SAMPLE_LESSON)

    bonus = _find_section(result["sections"], "Bonus Notes")
    assert bonus["kind"] == "generic_section"
    assert bonus["blocks"]
    assert result["worked_examples"]
    assert result["key_takeaways"]
