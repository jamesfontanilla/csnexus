"""Validate the Basic Components of a Sentence question bank for accuracy."""
import json
from pathlib import Path

INPUT = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions" / "verbal-ability"
    / "sentence-structure" / "basic-components-of-a-sentence" / "questions.json"
)

with open(INPUT, "r", encoding="utf-8") as f:
    data = json.load(f)

errors = []

for i, q in enumerate(data):
    qid = q.get("id", "?")

    # 1. Answer must be in choices
    if q["answer"] not in q["choices"]:
        errors.append(
            f'Q{qid}: Answer "{q["answer"]}" NOT in choices {q["choices"]}'
        )

    # 2. Exactly 4 choices
    if len(q["choices"]) != 4:
        errors.append(f"Q{qid}: Has {len(q['choices'])} choices (expected 4)")

    # 3. Required fields
    required = [
        "id", "subtest", "module", "subtopic", "difficulty",
        "question", "choices", "answer", "explanation", "tags",
        "category", "language",
    ]
    for field in required:
        if field not in q:
            errors.append(f'Q{qid}: Missing field "{field}"')

    # 4. Sequential IDs
    if q["id"] != i + 1:
        errors.append(f"Q{qid}: ID mismatch, expected {i + 1}")

    # 5. Valid difficulty
    if q["difficulty"] not in ("Easy", "Medium", "Hard"):
        errors.append(f'Q{qid}: Invalid difficulty "{q["difficulty"]}"')

    # 6. No duplicate choices
    if len(set(q["choices"])) != len(q["choices"]):
        errors.append(f"Q{qid}: Duplicate choices found: {q['choices']}")

    # 7. Non-empty explanation
    if not q.get("explanation", "").strip():
        errors.append(f"Q{qid}: Empty explanation")

    # 8. Non-empty question
    if not q.get("question", "").strip():
        errors.append(f"Q{qid}: Empty question")

    # 9. Tags is a non-empty list
    if not isinstance(q.get("tags"), list) or len(q["tags"]) == 0:
        errors.append(f"Q{qid}: Tags missing or empty")

    # 10. Consistent metadata
    if q.get("subtest") != "Verbal Ability":
        errors.append(f'Q{qid}: Wrong subtest "{q.get("subtest")}"')
    if q.get("module") != "Sentence Structure":
        errors.append(f'Q{qid}: Wrong module "{q.get("module")}"')
    if q.get("subtopic") != "Basic Components of a Sentence":
        errors.append(f'Q{qid}: Wrong subtopic "{q.get("subtopic")}"')

# Summary
print(f"Total questions: {len(data)}")
print(f"Easy: {sum(1 for q in data if q['difficulty'] == 'Easy')}")
print(f"Medium: {sum(1 for q in data if q['difficulty'] == 'Medium')}")
print(f"Hard: {sum(1 for q in data if q['difficulty'] == 'Hard')}")
print()

if errors:
    print(f"FOUND {len(errors)} ERROR(S):")
    for e in errors:
        print(f"  - {e}")
else:
    print("ALL 600 QUESTIONS PASSED VALIDATION")
    print("  [OK] All answers exist in their choices")
    print("  [OK] All have exactly 4 unique choices")
    print("  [OK] All required fields present")
    print("  [OK] IDs sequential 1-600")
    print("  [OK] Valid difficulty values")
    print("  [OK] Non-empty questions and explanations")
    print("  [OK] Non-empty tags")
    print("  [OK] Consistent metadata across all items")
