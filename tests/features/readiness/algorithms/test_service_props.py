"""Property-based tests for readiness service-level algorithmic logic.

Tests trend carry-forward, point-impact ranking, and readiness level classification
using Hypothesis to validate universal properties across all valid inputs.
"""

from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from unittest.mock import MagicMock

from hypothesis import given, settings, assume
from hypothesis.strategies import (
    composite,
    dates,
    floats,
    integers,
    lists,
    sampled_from,
    text,
)

from app.features.content.repository import QuestionRepository, SubtopicRepository
from app.features.flashcards.repository import FlashcardRepository
from app.features.mastery.repository import MasteryRepository
from app.features.mock_exams.repository import MockExamRepository
from app.features.readiness.models import ReadinessScoreHistory
from app.features.readiness.repository import ReadinessRepository
from app.features.readiness.service import ReadinessService


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_service(
    readiness_repo: MagicMock | None = None,
    mastery_repo: MagicMock | None = None,
) -> ReadinessService:
    """Create a ReadinessService with mocked dependencies."""
    return ReadinessService(
        readiness_repo=readiness_repo or MagicMock(spec=ReadinessRepository),
        mastery_repo=mastery_repo or MagicMock(spec=MasteryRepository),
        flashcard_repo=MagicMock(spec=FlashcardRepository),
        mock_exam_repo=MagicMock(spec=MockExamRepository),
        content_repo=MagicMock(spec=SubtopicRepository),
        question_repo=MagicMock(spec=QuestionRepository),
    )


def _make_score_record(score: int, computed_at: datetime) -> MagicMock:
    """Create a mock ReadinessScoreHistory record."""
    obj = MagicMock(spec=ReadinessScoreHistory)
    obj.score = score
    obj.computed_at = computed_at
    return obj


def _make_mastery_row(subtopic_id: int, mastery_score: float) -> MagicMock:
    """Create a mock mastery row for point-impact testing."""
    obj = MagicMock()
    obj.subtopic_id = subtopic_id
    obj.mastery_score = mastery_score
    obj.retention_score = 0.8
    obj.total_attempts = 10
    return obj


# ---------------------------------------------------------------------------
# Strategies
# ---------------------------------------------------------------------------

valid_score = integers(min_value=0, max_value=100)

# Scores for sparse records within a 30-day window
sparse_day_offsets = lists(
    integers(min_value=0, max_value=29),
    min_size=0,
    max_size=15,
    unique=True,
)

valid_mastery_score = floats(
    min_value=0.0, max_value=1.0, allow_nan=False, allow_infinity=False
)


@composite
def score_records_within_window(draw):
    """Generate a list of (day_offset, score) pairs representing sparse score records
    within a 30-day window. day_offset 0 = start_date, day_offset 29 = today."""
    offsets = draw(sparse_day_offsets)
    records = []
    for offset in sorted(offsets):
        score = draw(valid_score)
        records.append((offset, score))
    return records


@composite
def mastery_rows_for_impact(draw):
    """Generate a list of mastery rows with varying mastery_scores.
    At least one row below target (0.8) for point-impact to have candidates."""
    n = draw(integers(min_value=1, max_value=20))
    rows = []
    for i in range(n):
        score = draw(valid_mastery_score)
        rows.append((i + 1, score))  # (subtopic_id, mastery_score)
    return rows


# ---------------------------------------------------------------------------
# Property 6: Trend carry-forward produces complete 30-day series
# Validates: Requirements 2.4
# ---------------------------------------------------------------------------


class TestTrendCarryForwardComplete30DaySeries:
    """Given any list of score records (sparse dates within 30 days),
    `get_trend()` always returns exactly 30 TrendPoints, scores carry forward
    from last known value, and dates form a continuous sequence.

    **Validates: Requirements 2.4**
    """

    @settings(max_examples=50)
    @given(
        score_records=score_records_within_window(),
        seed_score=integers(min_value=0, max_value=100) | sampled_from([None]),
    )
    def test_always_returns_exactly_30_points(
        self,
        score_records: list[tuple[int, int]],
        seed_score: int | None,
    ) -> None:
        """Trend always returns exactly 30 TrendPoints regardless of input sparsity."""
        readiness_repo = MagicMock(spec=ReadinessRepository)

        today = date.today()
        start_date = today - timedelta(days=29)

        # Build mock records from day offsets
        mock_records = []
        for offset, score in score_records:
            record_date = start_date + timedelta(days=offset)
            computed_at = datetime.combine(
                record_date, datetime.min.time()
            ).replace(tzinfo=timezone.utc)
            mock_records.append(_make_score_record(score, computed_at))

        readiness_repo.get_trend.return_value = mock_records
        readiness_repo.get_score_at_date.return_value = (
            _make_score_record(seed_score, datetime.now(timezone.utc))
            if seed_score is not None
            else None
        )

        service = _make_service(readiness_repo=readiness_repo)
        result = service.get_trend(user_id=1, days=30)

        assert len(result) == 30

    @settings(max_examples=50)
    @given(
        score_records=score_records_within_window(),
        seed_score=integers(min_value=0, max_value=100) | sampled_from([None]),
    )
    def test_dates_form_continuous_sequence(
        self,
        score_records: list[tuple[int, int]],
        seed_score: int | None,
    ) -> None:
        """Dates in the trend form a continuous daily sequence from start to today."""
        readiness_repo = MagicMock(spec=ReadinessRepository)

        today = date.today()
        start_date = today - timedelta(days=29)

        mock_records = []
        for offset, score in score_records:
            record_date = start_date + timedelta(days=offset)
            computed_at = datetime.combine(
                record_date, datetime.min.time()
            ).replace(tzinfo=timezone.utc)
            mock_records.append(_make_score_record(score, computed_at))

        readiness_repo.get_trend.return_value = mock_records
        readiness_repo.get_score_at_date.return_value = (
            _make_score_record(seed_score, datetime.now(timezone.utc))
            if seed_score is not None
            else None
        )

        service = _make_service(readiness_repo=readiness_repo)
        result = service.get_trend(user_id=1, days=30)

        # Check consecutive dates
        for i in range(len(result) - 1):
            current_date = date.fromisoformat(result[i].date)
            next_date = date.fromisoformat(result[i + 1].date)
            assert next_date - current_date == timedelta(days=1)

        # First date is start_date
        assert result[0].date == start_date.isoformat()
        # Last date is today
        assert result[-1].date == today.isoformat()

    @settings(max_examples=50)
    @given(
        score_records=score_records_within_window(),
        seed_score=integers(min_value=0, max_value=100) | sampled_from([None]),
    )
    def test_scores_carry_forward_from_last_known(
        self,
        score_records: list[tuple[int, int]],
        seed_score: int | None,
    ) -> None:
        """Scores carry forward: once a score is set, it persists until the next record."""
        readiness_repo = MagicMock(spec=ReadinessRepository)

        today = date.today()
        start_date = today - timedelta(days=29)

        mock_records = []
        for offset, score in score_records:
            record_date = start_date + timedelta(days=offset)
            computed_at = datetime.combine(
                record_date, datetime.min.time()
            ).replace(tzinfo=timezone.utc)
            mock_records.append(_make_score_record(score, computed_at))

        readiness_repo.get_trend.return_value = mock_records
        readiness_repo.get_score_at_date.return_value = (
            _make_score_record(seed_score, datetime.now(timezone.utc))
            if seed_score is not None
            else None
        )

        service = _make_service(readiness_repo=readiness_repo)
        result = service.get_trend(user_id=1, days=30)

        # Build expected score-by-date map
        score_by_offset: dict[int, int] = {
            offset: score for offset, score in score_records
        }

        # Verify carry-forward logic
        carry = seed_score if seed_score is not None else 0
        for i in range(30):
            if i in score_by_offset:
                carry = score_by_offset[i]
            assert result[i].score == carry

    @settings(max_examples=50)
    @given(score_records=score_records_within_window())
    def test_all_scores_are_valid_integers_0_100(
        self,
        score_records: list[tuple[int, int]],
    ) -> None:
        """All trend point scores are valid integers in [0, 100]."""
        readiness_repo = MagicMock(spec=ReadinessRepository)

        today = date.today()
        start_date = today - timedelta(days=29)

        mock_records = []
        for offset, score in score_records:
            record_date = start_date + timedelta(days=offset)
            computed_at = datetime.combine(
                record_date, datetime.min.time()
            ).replace(tzinfo=timezone.utc)
            mock_records.append(_make_score_record(score, computed_at))

        readiness_repo.get_trend.return_value = mock_records
        readiness_repo.get_score_at_date.return_value = None

        service = _make_service(readiness_repo=readiness_repo)
        result = service.get_trend(user_id=1, days=30)

        for point in result:
            assert isinstance(point.score, int)
            assert 0 <= point.score <= 100


# ---------------------------------------------------------------------------
# Property 7: Point-impact ranking returns correct top-N subtopics
# Validates: Requirements 3.1
# ---------------------------------------------------------------------------


class TestPointImpactRankingTopN:
    """Given any set of mastery rows with varying mastery_scores, the top-impact
    list is sorted by point_impact descending, limited to 3, and only includes
    subtopics below the 0.8 target.

    **Validates: Requirements 3.1**
    """

    @settings(max_examples=50)
    @given(mastery_data=mastery_rows_for_impact())
    def test_only_subtopics_below_target_included(
        self,
        mastery_data: list[tuple[int, float]],
    ) -> None:
        """Only subtopics with mastery_score < 0.8 appear in top-impact list."""
        readiness_repo = MagicMock(spec=ReadinessRepository)
        mastery_repo = MagicMock(spec=MasteryRepository)
        content_repo = MagicMock(spec=SubtopicRepository)

        mastery_rows = [
            _make_mastery_row(subtopic_id, score)
            for subtopic_id, score in mastery_data
        ]
        mastery_repo.list_by_user.return_value = mastery_rows

        # Mock subtopic name lookup
        subtopic_mock = MagicMock()
        subtopic_mock.title = "Test Subtopic"
        content_repo.get.return_value = subtopic_mock

        service = _make_service(
            readiness_repo=readiness_repo,
            mastery_repo=mastery_repo,
        )
        service._content_repo = content_repo

        result = service._compute_top_impact_subtopics(user_id=1, top_n=3)

        # All returned subtopics must have mastery below target
        mastery_map = {sid: score for sid, score in mastery_data}
        for item in result:
            assert mastery_map[item.subtopic_id] < 0.8

    @settings(max_examples=50)
    @given(mastery_data=mastery_rows_for_impact())
    def test_limited_to_top_3(
        self,
        mastery_data: list[tuple[int, float]],
    ) -> None:
        """Result is limited to at most 3 subtopics."""
        readiness_repo = MagicMock(spec=ReadinessRepository)
        mastery_repo = MagicMock(spec=MasteryRepository)
        content_repo = MagicMock(spec=SubtopicRepository)

        mastery_rows = [
            _make_mastery_row(subtopic_id, score)
            for subtopic_id, score in mastery_data
        ]
        mastery_repo.list_by_user.return_value = mastery_rows

        subtopic_mock = MagicMock()
        subtopic_mock.title = "Test Subtopic"
        content_repo.get.return_value = subtopic_mock

        service = _make_service(
            readiness_repo=readiness_repo,
            mastery_repo=mastery_repo,
        )
        service._content_repo = content_repo

        result = service._compute_top_impact_subtopics(user_id=1, top_n=3)

        assert len(result) <= 3

    @settings(max_examples=50)
    @given(mastery_data=mastery_rows_for_impact())
    def test_sorted_by_point_impact_descending(
        self,
        mastery_data: list[tuple[int, float]],
    ) -> None:
        """Results are sorted by point_impact descending."""
        readiness_repo = MagicMock(spec=ReadinessRepository)
        mastery_repo = MagicMock(spec=MasteryRepository)
        content_repo = MagicMock(spec=SubtopicRepository)

        mastery_rows = [
            _make_mastery_row(subtopic_id, score)
            for subtopic_id, score in mastery_data
        ]
        mastery_repo.list_by_user.return_value = mastery_rows

        subtopic_mock = MagicMock()
        subtopic_mock.title = "Test Subtopic"
        content_repo.get.return_value = subtopic_mock

        service = _make_service(
            readiness_repo=readiness_repo,
            mastery_repo=mastery_repo,
        )
        service._content_repo = content_repo

        result = service._compute_top_impact_subtopics(user_id=1, top_n=3)

        # Verify descending order
        for i in range(len(result) - 1):
            assert result[i].point_impact >= result[i + 1].point_impact

    @settings(max_examples=50)
    @given(mastery_data=mastery_rows_for_impact())
    def test_top_n_are_highest_impact(
        self,
        mastery_data: list[tuple[int, float]],
    ) -> None:
        """The returned subtopics have the highest point_impact among all candidates."""
        readiness_repo = MagicMock(spec=ReadinessRepository)
        mastery_repo = MagicMock(spec=MasteryRepository)
        content_repo = MagicMock(spec=SubtopicRepository)

        mastery_rows = [
            _make_mastery_row(subtopic_id, score)
            for subtopic_id, score in mastery_data
        ]
        mastery_repo.list_by_user.return_value = mastery_rows

        subtopic_mock = MagicMock()
        subtopic_mock.title = "Test Subtopic"
        content_repo.get.return_value = subtopic_mock

        service = _make_service(
            readiness_repo=readiness_repo,
            mastery_repo=mastery_repo,
        )
        service._content_repo = content_repo

        result = service._compute_top_impact_subtopics(user_id=1, top_n=3)

        if not result:
            # All subtopics are >= 0.8, no candidates
            return

        # Compute expected impacts for all candidates below target
        target = 0.8
        total_subtopics = max(len(mastery_data), 1)
        all_impacts = []
        for subtopic_id, score in mastery_data:
            if score < target:
                gap = target - score
                impact = gap * (40.0 / total_subtopics)
                all_impacts.append(impact)

        all_impacts.sort(reverse=True)
        expected_top_impacts = all_impacts[:3]

        # Actual impacts returned should match expected
        actual_impacts = [item.point_impact for item in result]
        for actual, expected in zip(actual_impacts, expected_top_impacts):
            assert abs(actual - round(expected, 2)) < 0.01


# ---------------------------------------------------------------------------
# Property 8: Readiness level classification matches defined ranges
# Validates: Requirements 3.2
# ---------------------------------------------------------------------------


class TestReadinessLevelClassification:
    """For any score 0-100, `get_readiness_level(score)` returns exactly one of the
    four levels, and the classification matches: 0-39="Not Ready", 40-59="Getting There",
    60-79="Almost Ready", 80-100="Exam Ready".

    **Validates: Requirements 3.2**
    """

    VALID_LEVELS = {"Not Ready", "Getting There", "Almost Ready", "Exam Ready"}

    @settings(max_examples=50)
    @given(score=integers(min_value=0, max_value=100))
    def test_always_returns_exactly_one_valid_level(self, score: int) -> None:
        """For any valid score, exactly one of the four levels is returned."""
        service = _make_service()
        result = service.get_readiness_level(score)
        assert result in self.VALID_LEVELS

    @settings(max_examples=50)
    @given(score=integers(min_value=0, max_value=39))
    def test_not_ready_for_0_to_39(self, score: int) -> None:
        """Scores 0-39 classify as 'Not Ready'."""
        service = _make_service()
        assert service.get_readiness_level(score) == "Not Ready"

    @settings(max_examples=50)
    @given(score=integers(min_value=40, max_value=59))
    def test_getting_there_for_40_to_59(self, score: int) -> None:
        """Scores 40-59 classify as 'Getting There'."""
        service = _make_service()
        assert service.get_readiness_level(score) == "Getting There"

    @settings(max_examples=50)
    @given(score=integers(min_value=60, max_value=79))
    def test_almost_ready_for_60_to_79(self, score: int) -> None:
        """Scores 60-79 classify as 'Almost Ready'."""
        service = _make_service()
        assert service.get_readiness_level(score) == "Almost Ready"

    @settings(max_examples=50)
    @given(score=integers(min_value=80, max_value=100))
    def test_exam_ready_for_80_to_100(self, score: int) -> None:
        """Scores 80-100 classify as 'Exam Ready'."""
        service = _make_service()
        assert service.get_readiness_level(score) == "Exam Ready"

    @settings(max_examples=50)
    @given(score=integers(min_value=0, max_value=100))
    def test_boundaries_are_exhaustive_and_non_overlapping(self, score: int) -> None:
        """Every score maps to exactly one level — ranges are exhaustive and non-overlapping."""
        service = _make_service()
        result = service.get_readiness_level(score)

        # Check the result matches the expected range
        if score <= 39:
            assert result == "Not Ready"
        elif score <= 59:
            assert result == "Getting There"
        elif score <= 79:
            assert result == "Almost Ready"
        else:
            assert result == "Exam Ready"
