"""
Generate combined 1500-question bank for Indexing and Record Organization topic.
500 Easy, 500 Medium, 500 Hard — sourced from all 5 subtopics (100 per subtopic per difficulty).

Subtopics:
- Indexing Basics
- Record Classification
- Coding Systems
- Filing Systems
- Record Retrieval

Output: data/seed/questions/clerical-ability/indexing-and-record-organization/questions.json
"""
import json
import os
import random

random.seed(2024)

BASE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data", "seed", "questions", "clerical-ability", "indexing-and-record-organization"
)

SUBTOPICS = [
    "indexing-basics",
    "record-classification",
    "coding-systems",
    "filing-systems",
    "record-retrieval",
]

DIFFICULTIES = ["Easy", "Medium", "Hard"]
PER_SUBTOPIC_PER_DIFFICULTY = 100  # 5 subtopics × 100 × 3 difficulties = 1500


def load_subtopic_questions(subtopic_dir: str) -> list[dict]:
    """Load questions from a subtopic's questions.json."""
    path = os.path.join(BASE_DIR, subtopic_dir, "questions.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def sample_questions(questions: list[dict], difficulty: str, count: int) -> list[dict]:
    """Sample `count` questions of the given difficulty from the pool."""
    pool = [q for q in questions if q["difficulty"] == difficulty]
    if len(pool) < count:
        print(f"  WARNING: Only {len(pool)} {difficulty} questions available, needed {count}")
        return pool
    return random.sample(pool, count)


def main():
    combined = []

    for subtopic_dir in SUBTOPICS:
        print(f"Processing: {subtopic_dir}")
        questions = load_subtopic_questions(subtopic_dir)

        for difficulty in DIFFICULTIES:
            sampled = sample_questions(questions, difficulty, PER_SUBTOPIC_PER_DIFFICULTY)
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
        q_copy["module"] = "Indexing and Record Organization"
        final.append(q_copy)

    # Write output
    output_path = os.path.join(BASE_DIR, "questions.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Wrote {len(final)} questions to {output_path}")
    print(f"  Easy: {len(easy)}, Medium: {len(medium)}, Hard: {len(hard)}")


if __name__ == "__main__":
    main()
