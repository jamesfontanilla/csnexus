"""
Complete the Clauses question bank to exactly 600 questions.
Loads existing questions from the supplement script output,
adds remaining Hard questions, and writes final JSON.
"""
import json, os, subprocess, sys

# Step 1: Run supplement to get current state
subprocess.run([sys.executable, "scripts/gen_clauses_supplement.py"],
               cwd=os.getcwd(), check=False)

# Step 2: Load whatever exists
path = os.path.join("data", "seed", "questions", "verbal-ability",
                    "sentence-structure", "clauses", "questions.json")
with open(path, "r", encoding="utf-8") as f:
    questions = json.load(f)

def count():
    e = sum(1 for q in questions if q["difficulty"] == "Easy")
    m = sum(1 for q in questions if q["difficulty"] == "Medium")
    h = sum(1 for q in questions if q["difficulty"] == "Hard")
    return e, m, h

print(f"Loaded: {len(questions)} (E={count()[0]}, M={count()[1]}, H={count()[2]})")
