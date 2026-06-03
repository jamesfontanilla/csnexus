"""
Generate combined 1500-question bank for Name and Number Comparison topic.
500 Easy, 500 Medium, 500 Hard — sourced from all 5 subtopics (100 per subtopic per difficulty).

Subtopics:
- Name Comparison
- Number Comparison
- Alphanumeric Comparison
- Error Detection
- Speed and Accuracy Drills

Output: data/seed/questions/clerical-ability/name-and-number-comparison/questions.json
"""
import json
import os
import random
from collections import defaultdict

random.seed(2024)

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "seed", "questions", "clerical-ability", "name-and-number-comparison"
)

SUBTOPICS = [
    "name-comparison",
    "number-comparison",
    "alphanumeric-comparison",
    "error-detection",
    "speed-and-accuracy-drills",
]

DIFFICULTIES = ["Easy", "Medium", "Hard"]
PER_SUBTOPIC_PER_DIFFICULTY = 100  # 5 subtopics × 100 × 3 difficulties = 1500


def load_subtopic_questions(subtopic_dir: str) -> list[dict]:
    """Load questions from a subtopic's questions.json."""
    path = os.path.join(BASE_DIR, subtopic_dir, "questions.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def question_fingerprint(q: dict) -> str:
    """Create a unique fingerprint for a question (text + sorted choices)."""
    return q["question"] + "|" + "|".join(sorted(q["choices"]))


def sample_unique_questions(questions: list[dict], difficulty: str, count: int,
                            existing_fps: set) -> list[dict]:
    """Sample `count` unique questions of the given difficulty from the pool."""
    pool = [q for q in questions
            if q["difficulty"] == difficulty and question_fingerprint(q) not in existing_fps]
    if len(pool) < count:
        print(f"  WARNING: Only {len(pool)} unique {difficulty} questions available, needed {count}")
        sampled = pool
    else:
        sampled = random.sample(pool, count)
    # Add fingerprints to existing set
    for q in sampled:
        existing_fps.add(question_fingerprint(q))
    return sampled


def main():
    combined = []
    existing_fps = set()

    for subtopic_dir in SUBTOPICS:
        print(f"Processing: {subtopic_dir}")
        questions = load_subtopic_questions(subtopic_dir)

        for difficulty in DIFFICULTIES:
            sampled = sample_unique_questions(questions, difficulty,
                                             PER_SUBTOPIC_PER_DIFFICULTY, existing_fps)
            combined.extend(sampled)
            print(f"  {difficulty}: {len(sampled)} questions sampled")

    # Shuffle within each difficulty band then reassign IDs
    easy = [q for q in combined if q["difficulty"] == "Easy"]
    medium = [q for q in combined if q["difficulty"] == "Medium"]
    hard = [q for q in combined if q["difficulty"] == "Hard"]

    random.shuffle(easy)
    random.shuffle(medium)
    random.shuffle(hard)

    # Reassemble: Easy 1-500, Medium 501-1000, Hard 1001-1500
    final = []
    for idx, q in enumerate(easy + medium + hard, start=1):
        q_copy = dict(q)
        q_copy["id"] = idx
        q_copy["module"] = "Name and Number Comparison"
        final.append(q_copy)

    # Write output
    output_path = os.path.join(BASE_DIR, "questions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Wrote {len(final)} questions to {output_path}")
    print(f"  Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")

    # Quick duplicate check
    fps = defaultdict(list)
    for q in final:
        fps[question_fingerprint(q)].append(q["id"])
    true_dupes = sum(len(ids) - 1 for ids in fps.values() if len(ids) > 1)
    print(f"  True duplicates: {true_dupes}")


if __name__ == "__main__":
    main()
