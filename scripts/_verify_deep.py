"""Deep verification of flagged questions and random sampling."""
import json
import random
from pathlib import Path

FILE = (
    Path(__file__).resolve().parent.parent
    / "data" / "seed" / "questions" / "verbal-ability"
    / "sentence-structure" / "types-of-sentences-by-structure" / "questions.json"
)

with open(FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

# Check flagged IDs manually
flagged = [242, 244, 246, 266, 274, 301, 348, 350, 373, 377, 439, 506, 508, 543, 546, 556, 570, 572, 592]

print("=== FLAGGED QUESTIONS - MANUAL REVIEW ===\n")
for qid in flagged:
    q = data[qid - 1]
    print(f"Q{q['id']} ({q['difficulty']}):")
    print(f"  Q: {q['question'][:120]}")
    print(f"  A: {q['answer']}")
    print(f"  E: {q['explanation'][:120]}")
    print()

# Check specific problematic patterns
print("\n=== CHECKING Q207 (noted self-correction in explanation) ===")
q207 = data[206]
print(f"Q{q207['id']}: {q207['question'][:100]}")
print(f"  Answer: {q207['answer']}")
print(f"  Explanation: {q207['explanation']}")
print()

print("\n=== CHECKING Q226 (noted self-correction in explanation) ===")
q226 = data[225]
print(f"Q{q226['id']}: {q226['question'][:100]}")
print(f"  Answer: {q226['answer']}")
print(f"  Explanation: {q226['explanation']}")
print()

print("\n=== CHECKING Q249 (correlative conjunction classification) ===")
q249 = data[248]
print(f"Q{q249['id']}: {q249['question'][:100]}")
print(f"  Answer: {q249['answer']}")
print(f"  Explanation: {q249['explanation']}")
print()

# Random sample of 20 for spot-check
print("\n=== RANDOM SAMPLE (20 questions) ===\n")
random.seed(42)
sample = random.sample(data, 20)
for q in sample:
    print(f"Q{q['id']} ({q['difficulty']}): {q['question'][:90]}")
    print(f"  -> {q['answer']}")
    print()
