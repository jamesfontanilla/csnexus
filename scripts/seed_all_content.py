"""Seed ALL content (verbal, numerical, analytical, clerical ability) into the database.

NON-DESTRUCTIVE: Only inserts new modules/topics/subtopics/lessons/questions.
Skips anything that already exists (matched by slug). Updates lesson content
for existing subtopics if the lesson.md file has changed.

Creates the full hierarchy:
  Module: "Verbal Ability" (per category)
    Topic: "Grammar and Correct Usage"
      Subtopics: subject-verb-agreement, verb-tenses, pronouns, prepositions,
                 conjunctions, modifiers, parallelism, articles,
                 active-and-passive-voice, direct-and-indirect-speech
    Topic: "Sentence Structure"
      Subtopics: basic-components-of-a-sentence, clauses,
                 types-of-sentences-by-purpose, types-of-sentences-by-structure
    Topic: "Vocabulary Development"
      Subtopics: synonyms, antonyms, analogies, context-clues, word-formation,
                 idioms-and-expressions, denotation-and-connotation,
                 formal-and-informal-language
    Topic: "Reading Comprehension"
      Subtopics: fundamentals-of-reading-comprehension, vocabulary-in-context,
                 analytical-comprehension, authors-purpose-and-tone,
                 organization-of-ideas
  Module: "Numerical Ability" (per category)
    Topic: "Basic Operations"
      Subtopics: fundamental-number-concepts, addition, subtraction,
                 multiplication, division, order-of-operations,
                 exponents-and-roots, estimation-and-mental-math,
                 operations-with-signed-numbers, word-problems
    Topic: "Percentages"
      Subtopics: fundamentals-of-percentages, basic-percentage-problems,
                 percentage-increase-and-decrease, discounts-markups-and-sales,
                 profit-loss-and-tax, percentage-applications,
                 percentage-mental-math-and-shortcuts, percentage-word-problems
    Topic: "Ratio, Proportion, and Average"
      Subtopics: introduction-to-ratios, types-of-ratios,
                 direct-and-inverse-proportions, ratio-word-problems,
                 proportion-word-problems, scale-and-map-problems,
                 introduction-to-average, finding-missing-values-in-averages,
                 average-word-problems, weighted-average
  Module: "Analytical Ability" (per category)
    Topic: "Abstract Reasoning"
      Subtopics: shape-patterns, figure-series, matrix-reasoning,
                 number-and-letter-patterns, odd-one-out, odd-one-out-problems,
                 spatial-relationships
    Topic: "Symbolic Logic"
      Subtopics: logical-statements, logical-operators, truth-and-validity,
                 conditional-reasoning, syllogisms
    Topic: "Word Analogy"
      Subtopics: synonym-and-antonym-analogies,
                 part-whole-and-classification-relationships,
                 cause-effect-and-progression-relationships,
                 function-and-purpose-relationships,
                 symbolic-characteristic-and-location-relationships,
                 language-meaning-and-context-relationships,
                 numerical-letter-and-abstract-analogies
  Module: "Clerical Ability" (per category)
    Topic: "Alphabetical Filing"
      Subtopics: basic-alphabetizing, business-and-office-filing,
                 chronological-filing, filing-rules, name-filing,
                 numerical-filing, prefix-and-special-name-handling
    Topic: "Spelling"
      Subtopics: common-spelling-errors, correct-spelling-recognition,
                 homophones, office-and-administrative-vocabulary,
                 word-recognition
    Topic: "Name and Number Comparison"
      Subtopics: name-comparison, number-comparison,
                 alphanumeric-comparison, error-detection,
                 speed-and-accuracy-drills
    Topic: "Coding and Decoding"
      Subtopics: code-conversion
    Topic: "Indexing and Record Organization"
      Subtopics: indexing-basics, record-classification, coding-systems,
                 filing-systems, record-retrieval

Usage:
    python scripts/seed_all_content.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sqlalchemy.orm import Session as SASession

from app.features.content.models import (
    Difficulty,
    Lesson,
    LessonStatus,
    LevelScope,
    Module,
    Question,
    QuestionType,
    Subtopic,
    Topic,
)
from app.features.users.models import Category
from app.infrastructure.database.session import SessionLocal, engine
from app.infrastructure.database.base import Base
from scripts.parse_lesson import parse_lesson_markdown


SEED_BASE = Path(__file__).resolve().parent.parent / "data" / "seed"

DIFFICULTY_MAP = {
    "Easy": Difficulty.EASY.value,
    "Medium": Difficulty.MEDIUM.value,
    "Hard": Difficulty.HARD.value,
}

# ---------------------------------------------------------------------------
# Content hierarchy configuration
# ---------------------------------------------------------------------------

# Each entry: (topic_slug, topic_title, subtopics_list)
# Each subtopic: (slug, title, order_index)

VERBAL_ABILITY_TOPICS: list[tuple[str, str, list[tuple[str, str, int]]]] = [
    ("grammar-and-correct-usage", "Grammar and Correct Usage", [
        ("subject-verb-agreement", "Subject-Verb Agreement", 1),
        ("verb-tenses", "Verb Tenses", 2),
        ("pronouns", "Pronouns", 3),
        ("prepositions", "Prepositions", 4),
        ("conjunctions", "Conjunctions", 5),
        ("modifiers", "Modifiers", 6),
        ("parallelism", "Parallelism", 7),
        ("articles", "Articles", 8),
        ("active-and-passive-voice", "Active and Passive Voice", 9),
        ("direct-and-indirect-speech", "Direct and Indirect Speech", 10),
    ]),
    ("sentence-structure", "Sentence Structure", [
        ("basic-components-of-a-sentence", "Basic Components of a Sentence", 1),
        ("clauses", "Clauses", 2),
        ("types-of-sentences-by-purpose", "Types of Sentences by Purpose", 3),
        ("types-of-sentences-by-structure", "Types of Sentences by Structure", 4),
    ]),
    ("vocabulary-development", "Vocabulary Development", [
        ("synonyms", "Synonyms", 1),
        ("antonyms", "Antonyms", 2),
        ("analogies", "Analogies", 3),
        ("context-clues", "Context Clues", 4),
        ("word-formation", "Word Formation", 5),
        ("idioms-and-expressions", "Idioms and Expressions", 6),
        ("denotation-and-connotation", "Denotation and Connotation", 7),
        ("formal-and-informal-language", "Formal and Informal Language", 8),
    ]),
    ("reading-comprehension", "Reading Comprehension", [
        ("fundamentals-of-reading-comprehension", "Fundamentals of Reading Comprehension", 1),
        ("vocabulary-in-context", "Vocabulary in Context", 2),
        ("analytical-comprehension", "Analytical Comprehension", 3),
        ("authors-purpose-and-tone", "Author's Purpose and Tone", 4),
        ("organization-of-ideas", "Organization of Ideas", 5),
    ]),
]

NUMERICAL_ABILITY_TOPICS: list[tuple[str, str, list[tuple[str, str, int]]]] = [
    ("basic-operations", "Basic Operations", [
        ("fundamental-number-concepts", "Fundamental Number Concepts", 1),
        ("addition", "Addition", 2),
        ("subtraction", "Subtraction", 3),
        ("multiplication", "Multiplication", 4),
        ("division", "Division", 5),
        ("order-of-operations", "Order of Operations", 6),
        ("exponents-and-roots", "Exponents and Roots", 7),
        ("estimation-and-mental-math", "Estimation and Mental Math", 8),
        ("operations-with-signed-numbers", "Operations with Signed Numbers", 9),
        ("word-problems", "Word Problems", 10),
    ]),
    ("percentages", "Percentages", [
        ("fundamentals-of-percentages", "Fundamentals of Percentages", 1),
        ("basic-percentage-problems", "Basic Percentage Problems", 2),
        ("percentage-increase-and-decrease", "Percentage Increase and Decrease", 3),
        ("discounts-markups-and-sales", "Discounts, Markups, and Sales", 4),
        ("profit-loss-and-tax", "Profit, Loss, and Tax", 5),
        ("percentage-applications", "Percentage Applications", 6),
        ("percentage-mental-math-and-shortcuts", "Percentage Mental Math and Shortcuts", 7),
        ("percentage-word-problems", "Percentage Word Problems", 8),
    ]),
    ("ratio-proportion-and-average", "Ratio, Proportion, and Average", [
        ("introduction-to-ratios", "Introduction to Ratios", 1),
        ("types-of-ratios", "Types of Ratios", 2),
        ("direct-and-inverse-proportions", "Direct and Inverse Proportions", 3),
        ("ratio-word-problems", "Ratio Word Problems", 4),
        ("proportion-word-problems", "Proportion Word Problems", 5),
        ("scale-and-map-problems", "Scale and Map Problems", 6),
        ("introduction-to-average", "Introduction to Average", 7),
        ("finding-missing-values-in-averages", "Finding Missing Values in Averages", 8),
        ("average-word-problems", "Average Word Problems", 9),
        ("weighted-average", "Weighted Average", 10),
    ]),
]

ANALYTICAL_ABILITY_TOPICS: list[tuple[str, str, list[tuple[str, str, int]]]] = [
    ("abstract-reasoning", "Abstract Reasoning", [
        ("shape-patterns", "Shape Patterns", 1),
        ("figure-series", "Figure Series", 2),
        ("matrix-reasoning", "Matrix Reasoning", 3),
        ("number-and-letter-patterns", "Number and Letter Patterns", 4),
        ("odd-one-out", "Odd One Out", 5),
        ("odd-one-out-problems", "Odd One Out Problems", 6),
        ("spatial-relationships", "Spatial Relationships", 7),
    ]),
    ("symbolic-logic", "Symbolic Logic", [
        ("logical-statements", "Logical Statements", 1),
        ("logical-operators", "Logical Operators", 2),
        ("truth-and-validity", "Truth and Validity", 3),
        ("conditional-reasoning", "Conditional Reasoning", 4),
        ("syllogisms", "Syllogisms", 5),
    ]),
    ("word-analogy", "Word Analogy", [
        ("synonym-and-antonym-analogies", "Synonym and Antonym Analogies", 1),
        ("part-whole-and-classification-relationships", "Part-Whole and Classification Relationships", 2),
        ("cause-effect-and-progression-relationships", "Cause-Effect and Progression Relationships", 3),
        ("function-and-purpose-relationships", "Function and Purpose Relationships", 4),
        ("symbolic-characteristic-and-location-relationships", "Symbolic, Characteristic, and Location Relationships", 5),
        ("language-meaning-and-context-relationships", "Language, Meaning, and Context Relationships", 6),
        ("numerical-letter-and-abstract-analogies", "Numerical, Letter, and Abstract Analogies", 7),
    ]),
]

CLERICAL_ABILITY_TOPICS: list[tuple[str, str, list[tuple[str, str, int]]]] = [
    ("alphabetical-filing", "Alphabetical Filing", [
        ("basic-alphabetizing", "Basic Alphabetizing", 1),
        ("business-and-office-filing", "Business and Office Filing", 2),
        ("chronological-filing", "Chronological Filing", 3),
        ("filing-rules", "Filing Rules", 4),
        ("name-filing", "Name Filing", 5),
        ("numerical-filing", "Numerical Filing", 6),
        ("prefix-and-special-name-handling", "Prefix and Special Name Handling", 7),
    ]),
    ("spelling", "Spelling", [
        ("common-spelling-errors", "Common Spelling Errors", 1),
        ("correct-spelling-recognition", "Correct Spelling Recognition", 2),
        ("homophones", "Homophones", 3),
        ("office-and-administrative-vocabulary", "Office and Administrative Vocabulary", 4),
        ("word-recognition", "Word Recognition", 5),
    ]),
    ("name-and-number-comparison", "Name and Number Comparison", [
        ("name-comparison", "Name Comparison", 1),
        ("number-comparison", "Number Comparison", 2),
        ("alphanumeric-comparison", "Alphanumeric Comparison", 3),
        ("error-detection", "Error Detection", 4),
        ("speed-and-accuracy-drills", "Speed and Accuracy Drills", 5),
    ]),
    ("coding-and-decoding", "Coding and Decoding", [
        ("code-conversion", "Code Conversion", 1),
    ]),
    ("indexing-and-record-organization", "Indexing and Record Organization", [
        ("indexing-basics", "Indexing Basics", 1),
        ("record-classification", "Record Classification", 2),
        ("coding-systems", "Coding Systems", 3),
        ("filing-systems", "Filing Systems", 4),
        ("record-retrieval", "Record Retrieval", 5),
    ]),
]

# Map topic slugs to their lesson/question directories
LESSON_DIRS = {
    "grammar-and-correct-usage": SEED_BASE / "lessons" / "verbal-ability" / "grammar",
    "sentence-structure": SEED_BASE / "lessons" / "verbal-ability" / "sentence-structure",
    "vocabulary-development": SEED_BASE / "lessons" / "verbal-ability" / "vocabulary-development",
    "reading-comprehension": SEED_BASE / "lessons" / "verbal-ability" / "reading-comprehension",
    "basic-operations": SEED_BASE / "lessons" / "numerical-ability" / "basic-operations",
    "percentages": SEED_BASE / "lessons" / "numerical-ability" / "percentages",
    "ratio-proportion-and-average": SEED_BASE / "lessons" / "numerical-ability" / "ratio-proportion-and-average",
    "abstract-reasoning": SEED_BASE / "lessons" / "analytical-ability" / "abstract-reasoning",
    "symbolic-logic": SEED_BASE / "lessons" / "analytical-ability" / "symbolic-logic",
    "word-analogy": SEED_BASE / "lessons" / "analytical-ability" / "word-analogy",
    "alphabetical-filing": SEED_BASE / "lessons" / "clerical-ability" / "alphabetical-filing",
    "spelling": SEED_BASE / "lessons" / "clerical-ability" / "spelling",
    "name-and-number-comparison": SEED_BASE / "lessons" / "clerical-ability" / "name-and-number-comparison",
    "coding-and-decoding": SEED_BASE / "lessons" / "clerical-ability" / "coding-and-decoding",
    "indexing-and-record-organization": SEED_BASE / "lessons" / "clerical-ability" / "indexing-and-record-organization",
}

QUESTION_DIRS = {
    "grammar-and-correct-usage": SEED_BASE / "questions" / "verbal-ability" / "grammar",
    "sentence-structure": SEED_BASE / "questions" / "verbal-ability" / "sentence-structure",
    "vocabulary-development": SEED_BASE / "questions" / "verbal-ability" / "vocabulary-development",
    "reading-comprehension": SEED_BASE / "questions" / "verbal-ability" / "reading-comprehension",
    "basic-operations": SEED_BASE / "questions" / "numerical-ability" / "basic-operations",
    "percentages": SEED_BASE / "questions" / "numerical-ability" / "percentages",
    "ratio-proportion-and-average": SEED_BASE / "questions" / "numerical-ability" / "ratio-proportion-and-average",
    "abstract-reasoning": SEED_BASE / "questions" / "analytical-ability" / "abstract-reasoning",
    "symbolic-logic": SEED_BASE / "questions" / "analytical-ability" / "symbolic-logic",
    "word-analogy": SEED_BASE / "questions" / "analytical-ability" / "word-analogy",
    "alphabetical-filing": SEED_BASE / "questions" / "clerical-ability" / "alphabetical-filing",
    "spelling": SEED_BASE / "questions" / "clerical-ability" / "spelling",
    "name-and-number-comparison": SEED_BASE / "questions" / "clerical-ability" / "name-and-number-comparison",
    "coding-and-decoding": SEED_BASE / "questions" / "clerical-ability" / "coding-and-decoding",
    "indexing-and-record-organization": SEED_BASE / "questions" / "clerical-ability" / "indexing-and-record-organization",
}


def get_or_create_module(
    session: SASession, slug: str, title: str, category: str, order_index: int
) -> Module:
    """Get existing module or create new one."""
    module = session.query(Module).filter(Module.slug == slug).first()
    if module:
        print(f"  [EXISTS] Module: {slug}")
        return module

    module = Module(
        category=category,
        slug=slug,
        title=title,
        order_index=order_index,
        is_published=True,
    )
    session.add(module)
    session.flush()
    print(f"  [CREATED] Module: {slug} (id={module.id})")
    return module


def get_or_create_topic(
    session: SASession, module_id: int, slug: str, title: str, order_index: int
) -> Topic:
    """Get existing topic or create new one."""
    topic = session.query(Topic).filter(
        Topic.module_id == module_id, Topic.slug == slug
    ).first()
    if topic:
        print(f"    [EXISTS] Topic: {slug}")
        return topic

    topic = Topic(
        module_id=module_id,
        slug=slug,
        title=title,
        order_index=order_index,
    )
    session.add(topic)
    session.flush()
    print(f"    [CREATED] Topic: {slug} (id={topic.id})")
    return topic


def seed_subtopic(
    session: SASession,
    topic: Topic,
    module: Module,
    slug: str,
    title: str,
    order_index: int,
    lesson_dir: Path,
    question_dir: Path,
) -> int:
    """Seed a single subtopic with its lesson and questions. Returns questions added."""
    # Check if subtopic already exists
    existing = session.query(Subtopic).filter(
        Subtopic.topic_id == topic.id, Subtopic.slug == slug
    ).first()

    if existing:
        subtopic = existing
        questions_added = 0

        # Update lesson content if the markdown file exists
        lesson = session.query(Lesson).filter(
            Lesson.subtopic_id == existing.id
        ).first()
        lesson_path = lesson_dir / slug / "lesson.md"
        if lesson_path.exists():
            md_text = lesson_path.read_text(encoding="utf-8")
            new_content = parse_lesson_markdown(md_text)
            if lesson:
                lesson.content_json = new_content
            else:
                # Lesson row missing — create it
                session.add(Lesson(
                    subtopic_id=existing.id,
                    content_json=new_content,
                    status=LessonStatus.PUBLISHED.value,
                ))

        # Seed questions that are not yet in the DB for this subtopic
        questions_path = question_dir / slug / "questions.json"
        if questions_path.exists():
            existing_count = session.query(Question).filter(
                Question.subtopic_id == existing.id
            ).count()
            if existing_count == 0:
                questions_raw = json.loads(questions_path.read_text(encoding="utf-8"))
                for q in questions_raw:
                    session.add(Question(
                        subtopic_id=existing.id,
                        topic_id=topic.id,
                        module_id=module.id,
                        category=module.category,
                        level_scope=LevelScope.SUBTOPIC.value,
                        stem=q["question"],
                        options=q["choices"],
                        correct_answer=q["answer"],
                        explanation=q["explanation"],
                        difficulty=DIFFICULTY_MAP.get(q["difficulty"], Difficulty.EASY.value),
                        qtype=QuestionType.MULTIPLE_CHOICE.value,
                        is_active=True,
                    ))
                questions_added = len(questions_raw)
                print(f"      [QUESTIONS ADDED] {slug} ({questions_added} questions)")
            else:
                print(f"      [EXISTS] {slug} ({existing_count} questions already present)")
        else:
            print(f"      [EXISTS] {slug} (no questions.json)")

        return questions_added

    # --- New subtopic ---
    subtopic = Subtopic(
        topic_id=topic.id,
        slug=slug,
        title=title,
        order_index=order_index,
    )
    session.add(subtopic)
    session.flush()

    # Load and create lesson
    lesson_path = lesson_dir / slug / "lesson.md"
    if lesson_path.exists():
        md_text = lesson_path.read_text(encoding="utf-8")
        lesson_content = parse_lesson_markdown(md_text)
        lesson = Lesson(
            subtopic_id=subtopic.id,
            content_json=lesson_content,
            status=LessonStatus.PUBLISHED.value,
        )
        session.add(lesson)
    else:
        print(f"      [WARN] No lesson.md for {slug}")

    # Load and create questions
    questions_path = question_dir / slug / "questions.json"
    questions_added = 0
    if questions_path.exists():
        questions_raw = json.loads(questions_path.read_text(encoding="utf-8"))
        for q in questions_raw:
            question = Question(
                subtopic_id=subtopic.id,
                topic_id=topic.id,
                module_id=module.id,
                category=module.category,
                level_scope=LevelScope.SUBTOPIC.value,
                stem=q["question"],
                options=q["choices"],
                correct_answer=q["answer"],
                explanation=q["explanation"],
                difficulty=DIFFICULTY_MAP.get(q["difficulty"], Difficulty.EASY.value),
                qtype=QuestionType.MULTIPLE_CHOICE.value,
                is_active=True,
            )
            session.add(question)
        questions_added = len(questions_raw)
    else:
        print(f"      [WARN] No questions.json for {slug}")

    print(f"      [CREATED] {slug} ({questions_added} questions)")
    return questions_added


def seed_topic_questions(
    session: SASession,
    topic: Topic,
    module: Module,
    question_dir: Path,
) -> int:
    """Seed topic-level questions from a questions.json at the topic directory root.

    These are used for 50-question topic quizzes (level_scope=TOPIC).
    Each question's 'subtopic' field is resolved to the DB subtopic_id.
    Returns the number of questions added.
    """
    topic_questions_path = question_dir / "questions.json"
    if not topic_questions_path.exists():
        return 0

    # Check if topic-level questions already exist for this topic
    existing_count = session.query(Question).filter(
        Question.topic_id == topic.id,
        Question.level_scope == LevelScope.TOPIC.value,
    ).count()
    if existing_count > 0:
        print(f"    [EXISTS] Topic questions for '{topic.slug}' ({existing_count} already present)")
        return 0

    # Build subtopic slug→id map for this topic
    subtopics = session.query(Subtopic).filter(Subtopic.topic_id == topic.id).all()
    subtopic_map: dict[str, int] = {}
    for st in subtopics:
        subtopic_map[st.slug] = st.id
        # Also map by title for fallback matching
        subtopic_map[st.title] = st.id

    questions_raw = json.loads(topic_questions_path.read_text(encoding="utf-8"))
    added = 0

    for q in questions_raw:
        # Resolve subtopic_id from the question's 'subtopic' field
        subtopic_name = q.get("subtopic", "")
        # Try slug-style match first (convert title to slug)
        slug_candidate = subtopic_name.lower().replace(" ", "-")
        subtopic_id = subtopic_map.get(slug_candidate) or subtopic_map.get(subtopic_name)

        if not subtopic_id:
            # Fallback: use the first subtopic in this topic
            if subtopics:
                subtopic_id = subtopics[0].id
            else:
                continue  # Skip if no subtopics exist

        session.add(Question(
            subtopic_id=subtopic_id,
            topic_id=topic.id,
            module_id=module.id,
            category=module.category,
            level_scope=LevelScope.TOPIC.value,
            stem=q["question"],
            options=q["choices"],
            correct_answer=q["answer"],
            explanation=q["explanation"],
            difficulty=DIFFICULTY_MAP.get(q["difficulty"], Difficulty.EASY.value),
            qtype=QuestionType.MULTIPLE_CHOICE.value,
            is_active=True,
        ))
        added += 1

    if added > 0:
        print(f"    [TOPIC QUESTIONS ADDED] '{topic.slug}' ({added} questions, level_scope=TOPIC)")

    return added


def main() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    total_questions = 0

    try:
        for cat_key, cat_value in [
            ("professional", Category.PROFESSIONAL.value),
            ("sub-professional", Category.SUB_PROFESSIONAL.value),
        ]:
            print(f"\n{'='*60}")
            print(f"Category: {cat_key}")
            print(f"{'='*60}")

            # --- Verbal Ability module ---
            va_module = get_or_create_module(
                session,
                slug=f"verbal-ability-{cat_key}",
                title="Verbal Ability",
                category=cat_value,
                order_index=10,
            )

            for topic_idx, (topic_slug, topic_title, subtopics) in enumerate(VERBAL_ABILITY_TOPICS, start=1):
                topic = get_or_create_topic(
                    session, va_module.id, topic_slug, topic_title,
                    order_index=topic_idx,
                )

                lesson_dir = LESSON_DIRS[topic_slug]
                question_dir = QUESTION_DIRS[topic_slug]

                for slug, title, order_idx in subtopics:
                    added = seed_subtopic(
                        session, topic, va_module,
                        slug, title, order_idx,
                        lesson_dir, question_dir,
                    )
                    total_questions += added

                # Seed topic-level questions (for 50-item topic quizzes)
                total_questions += seed_topic_questions(
                    session, topic, va_module, question_dir,
                )

            # --- Numerical Ability module ---
            na_module = get_or_create_module(
                session,
                slug=f"numerical-ability-{cat_key}",
                title="Numerical Ability",
                category=cat_value,
                order_index=20,
            )

            for topic_idx, (topic_slug, topic_title, subtopics) in enumerate(NUMERICAL_ABILITY_TOPICS, start=1):
                topic = get_or_create_topic(
                    session, na_module.id, topic_slug, topic_title,
                    order_index=topic_idx,
                )

                lesson_dir = LESSON_DIRS[topic_slug]
                question_dir = QUESTION_DIRS[topic_slug]

                for slug, title, order_idx in subtopics:
                    added = seed_subtopic(
                        session, topic, na_module,
                        slug, title, order_idx,
                        lesson_dir, question_dir,
                    )
                    total_questions += added

                # Seed topic-level questions (for 50-item topic quizzes)
                total_questions += seed_topic_questions(
                    session, topic, na_module, question_dir,
                )

            # --- Analytical Ability module ---
            aa_module = get_or_create_module(
                session,
                slug=f"analytical-ability-{cat_key}",
                title="Analytical Ability",
                category=cat_value,
                order_index=30,
            )

            for topic_idx, (topic_slug, topic_title, subtopics) in enumerate(ANALYTICAL_ABILITY_TOPICS, start=1):
                topic = get_or_create_topic(
                    session, aa_module.id, topic_slug, topic_title,
                    order_index=topic_idx,
                )

                lesson_dir = LESSON_DIRS[topic_slug]
                question_dir = QUESTION_DIRS[topic_slug]

                for slug, title, order_idx in subtopics:
                    added = seed_subtopic(
                        session, topic, aa_module,
                        slug, title, order_idx,
                        lesson_dir, question_dir,
                    )
                    total_questions += added

                # Seed topic-level questions (for 50-item topic quizzes)
                total_questions += seed_topic_questions(
                    session, topic, aa_module, question_dir,
                )

            # --- Clerical Ability module ---
            ca_module = get_or_create_module(
                session,
                slug=f"clerical-ability-{cat_key}",
                title="Clerical Ability",
                category=cat_value,
                order_index=40,
            )

            for topic_idx, (topic_slug, topic_title, subtopics) in enumerate(CLERICAL_ABILITY_TOPICS, start=1):
                topic = get_or_create_topic(
                    session, ca_module.id, topic_slug, topic_title,
                    order_index=topic_idx,
                )

                lesson_dir = LESSON_DIRS[topic_slug]
                question_dir = QUESTION_DIRS[topic_slug]

                for slug, title, order_idx in subtopics:
                    added = seed_subtopic(
                        session, topic, ca_module,
                        slug, title, order_idx,
                        lesson_dir, question_dir,
                    )
                    total_questions += added

                # Seed topic-level questions (for 50-item topic quizzes)
                total_questions += seed_topic_questions(
                    session, topic, ca_module, question_dir,
                )

        session.commit()
        print(f"\n{'='*60}")
        print(f"DONE. Total new questions added: {total_questions}")
        print(f"{'='*60}")

    except Exception as e:
        session.rollback()
        print(f"\nERROR: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
