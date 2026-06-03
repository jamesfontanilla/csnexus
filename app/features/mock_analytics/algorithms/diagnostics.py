"""Pure diagnostic computation for post-mock exam analysis.

Computes subtopic-level breakdowns, highest-impact areas,
regression alerts, and difficulty performance from raw exam answers.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SubtopicDiagnostic:
    subtopic_id: int
    questions_attempted: int
    questions_correct: int
    points_lost: int
    avg_seconds_per_question: float
    accuracy_percentage: float


@dataclass(frozen=True)
class DiagnosticResult:
    total_score: float  # percentage correct, 1 decimal
    subtopic_breakdowns: list[SubtopicDiagnostic]
    highest_impact_areas: list[SubtopicDiagnostic]  # top 5 by points_lost
    regression_alerts: list[tuple[int, float]]  # (subtopic_id, decline_pct)
    difficulty_performance: dict[str, float]  # easy/medium/hard accuracy


def compute_diagnostic(
    answers: list[tuple[int, bool, int, float, str]],
    # (subtopic_id, is_correct, question_id, seconds, difficulty)
    historical_accuracy: dict[int, float],
    # subtopic_id -> historical avg accuracy (0-100 scale)
) -> DiagnosticResult:
    """Compute full diagnostic breakdown from exam answers. Pure function.

    Args:
        answers: List of answer tuples containing:
            - subtopic_id: which subtopic the question belongs to
            - is_correct: whether the user answered correctly
            - question_id: unique question identifier
            - seconds: time taken to answer in seconds
            - difficulty: "easy", "medium", or "hard"
        historical_accuracy: Dict mapping subtopic_id to the user's
            historical average accuracy percentage (0-100) for that subtopic.

    Returns:
        DiagnosticResult with total score, subtopic breakdowns,
        highest impact areas, regression alerts, and difficulty performance.
    """
    if not answers:
        return DiagnosticResult(
            total_score=0.0,
            subtopic_breakdowns=[],
            highest_impact_areas=[],
            regression_alerts=[],
            difficulty_performance={},
        )

    # Compute total score
    total_correct = sum(1 for _, is_correct, *_ in answers if is_correct)
    total_questions = len(answers)
    total_score = round(total_correct / total_questions * 100, 1)

    # Group answers by subtopic
    subtopic_breakdowns = _compute_subtopic_breakdowns(answers)

    # Highest impact areas: top 5 by points_lost descending
    highest_impact_areas = _compute_highest_impact_areas(subtopic_breakdowns)

    # Regression alerts: >15 percentage point decline vs historical
    regression_alerts = _compute_regression_alerts(
        subtopic_breakdowns, historical_accuracy
    )

    # Difficulty performance: per-level accuracy
    difficulty_performance = _compute_difficulty_performance(answers)

    return DiagnosticResult(
        total_score=total_score,
        subtopic_breakdowns=subtopic_breakdowns,
        highest_impact_areas=highest_impact_areas,
        regression_alerts=regression_alerts,
        difficulty_performance=difficulty_performance,
    )


def _compute_subtopic_breakdowns(
    answers: list[tuple[int, bool, int, float, str]],
) -> list[SubtopicDiagnostic]:
    """Compute per-subtopic diagnostic breakdowns.

    Time filtering: excludes answers with <2s or >600s when computing
    avg_seconds_per_question (outlier removal).
    """
    # Group by subtopic_id
    subtopic_data: dict[int, list[tuple[bool, float]]] = {}
    for subtopic_id, is_correct, _, seconds, _ in answers:
        if subtopic_id not in subtopic_data:
            subtopic_data[subtopic_id] = []
        subtopic_data[subtopic_id].append((is_correct, seconds))

    breakdowns: list[SubtopicDiagnostic] = []
    for subtopic_id, entries in subtopic_data.items():
        questions_attempted = len(entries)
        questions_correct = sum(1 for correct, _ in entries if correct)
        points_lost = questions_attempted - questions_correct

        # Time filtering: exclude <2s or >600s for avg calculation
        valid_times = [
            seconds for _, seconds in entries if 2.0 <= seconds <= 600.0
        ]
        avg_seconds = (
            sum(valid_times) / len(valid_times) if valid_times else 0.0
        )

        accuracy_percentage = round(
            questions_correct / questions_attempted * 100, 1
        )

        breakdowns.append(
            SubtopicDiagnostic(
                subtopic_id=subtopic_id,
                questions_attempted=questions_attempted,
                questions_correct=questions_correct,
                points_lost=points_lost,
                avg_seconds_per_question=round(avg_seconds, 1),
                accuracy_percentage=accuracy_percentage,
            )
        )

    return breakdowns


def _compute_highest_impact_areas(
    breakdowns: list[SubtopicDiagnostic],
) -> list[SubtopicDiagnostic]:
    """Return top 5 subtopics by points_lost descending.

    Only includes subtopics with points_lost > 0.
    If fewer than 5 have points_lost > 0, return only those.
    """
    with_loss = [b for b in breakdowns if b.points_lost > 0]
    sorted_by_loss = sorted(with_loss, key=lambda b: b.points_lost, reverse=True)
    return sorted_by_loss[:5]


def _compute_regression_alerts(
    breakdowns: list[SubtopicDiagnostic],
    historical_accuracy: dict[int, float],
) -> list[tuple[int, float]]:
    """Identify subtopics that declined >15 percentage points vs historical.

    Omits subtopics with no prior history (not in historical_accuracy dict).
    Returns list of (subtopic_id, decline_percentage_points).
    """
    alerts: list[tuple[int, float]] = []
    for breakdown in breakdowns:
        if breakdown.subtopic_id not in historical_accuracy:
            continue
        historical = historical_accuracy[breakdown.subtopic_id]
        decline = historical - breakdown.accuracy_percentage
        if decline > 15.0:
            alerts.append((breakdown.subtopic_id, round(decline, 1)))
    return alerts


def _compute_difficulty_performance(
    answers: list[tuple[int, bool, int, float, str]],
) -> dict[str, float]:
    """Compute percentage correct at each difficulty level.

    Returns a dict mapping difficulty ("easy", "medium", "hard") to
    the accuracy percentage (0-100, 1 decimal). Only includes levels
    that have at least one question.
    """
    difficulty_data: dict[str, list[bool]] = {}
    for _, is_correct, _, _, difficulty in answers:
        if difficulty not in difficulty_data:
            difficulty_data[difficulty] = []
        difficulty_data[difficulty].append(is_correct)

    performance: dict[str, float] = {}
    for level, results in difficulty_data.items():
        correct = sum(1 for r in results if r)
        total = len(results)
        performance[level] = round(correct / total * 100, 1)

    return performance
