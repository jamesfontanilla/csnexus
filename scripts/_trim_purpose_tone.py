"""Trim to exactly 600 questions (200 per difficulty) and re-number IDs 1-600."""
import json

PATH = r"data/seed/questions/verbal-ability/reading-comprehension/authors-purpose-and-tone/questions.json"

with open(PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

easy = [q for q in data if q["difficulty"] == "Easy"][:200]
medium = [q for q in data if q["difficulty"] == "Medium"][:200]
hard = [q for q in data if q["difficulty"] == "Hard"][:200]

final = easy + medium + hard

for i, q in enumerate(final, start=1):
    q["id"] = i

with open(PATH, "w", encoding="utf-8") as f:
    json.dump(final, f, indent=2, ensure_ascii=False)

print(f"Done: {len(final)} questions")
print(f"  Easy:   {len(easy)} (IDs 1-200)")
print(f"  Medium: {len(medium)} (IDs 201-400)")
print(f"  Hard:   {len(hard)} (IDs 401-600)")
