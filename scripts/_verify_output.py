import json
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "data" / "seed" / "questions" / "analytical-ability" / "abstract-reasoning" / "number-and-letter-patterns" / "questions.json"
data = json.loads(p.read_text(encoding="utf-8"))
print(f"Questions: {len(data)}")
print(f"First question ID: {data[0]['id']}")
print(f"Last question ID: {data[-1]['id']}")
easy = sum(1 for q in data if q["difficulty"] == "Easy")
medium = sum(1 for q in data if q["difficulty"] == "Medium")
hard = sum(1 for q in data if q["difficulty"] == "Hard")
print(f"Easy: {easy}, Medium: {medium}, Hard: {hard}")
print(f"Sample question: {data[0]['question'][:100]}")
