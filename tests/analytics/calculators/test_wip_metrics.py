"""Tests for calculate_wip_metrics."""

import math

from src.analytics.calculators.wip_metrics import calculate_wip_metrics
from src.parser.models import (
    Board,
    Section,
    SectionType,
    Task,
    TaskStatus,
)


def _make_section(
    title: str,
    section_type: SectionType = SectionType.EXECUTION,
    wip_limit: int | None = None,
) -> Section:
    return Section(
        title=title,
        raw_title=f"## {title}",
        type=section_type,
        wip_limit=wip_limit,
    )


def _make_task(
    title: str,
    section: Section,
    status: TaskStatus = TaskStatus.OPEN,
    archived: bool = False,
) -> Task:
    return Task(
        title=title,
        status=status,
        section=section,
        archived=archived,
    )


class TestCalculateWipMetrics:
    """Tests for calculate_wip_metrics function."""

    def test_empty_board(self):
        """Empty board returns empty list."""
        board = Board(tasks=[])
        assert calculate_wip_metrics(board) == []

    def test_sections_without_wip_limit_are_ignored(self):
        """Sections without wip_limit are not included in results."""
        section = _make_section("Backlog")
        task = _make_task("Task 1", section)
        board = Board(tasks=[task])

        result = calculate_wip_metrics(board)
        assert result == []

    def test_section_with_wip_limit_and_no_tasks(self):
        """Section with WIP limit but no active tasks."""
        section = _make_section("In Progress", wip_limit=3)
        board = Board(tasks=[])

        # Need at least one task in the section for it to appear in board.sections
        # But if there are no tasks, board.sections is empty
        # So we add a completed task to register the section
        completed_task = _make_task(
            "Done task", section, status=TaskStatus.COMPLETED
        )
        board = Board(tasks=[completed_task])

        result = calculate_wip_metrics(board)
        assert len(result) == 1
        assert result[0].section_name == "In Progress"
        assert result[0].active_tasks == 0
        assert result[0].wip_limit == 3
        assert result[0].remaining_capacity == 3
        assert result[0].utilization == 0.0
        assert result[0].is_near_limit is False
        assert result[0].is_over_limit is False

    def test_section_within_wip_limit(self):
        """Section with active tasks within WIP limit."""
        section = _make_section("Dev", wip_limit=5)
        tasks = [
            _make_task("Task 1", section, TaskStatus.OPEN),
            _make_task("Task 2", section, TaskStatus.IN_PROGRESS),
            _make_task("Task 3", section, TaskStatus.OPEN),
        ]
        board = Board(tasks=tasks)

        result = calculate_wip_metrics(board)
        assert len(result) == 1

        wip = result[0]
        assert wip.section_name == "Dev"
        assert wip.active_tasks == 3
        assert wip.wip_limit == 5
        assert wip.remaining_capacity == 2
        assert math.isclose(wip.utilization, 0.6)
        assert wip.is_near_limit is False
        assert wip.is_over_limit is False

    def test_section_near_wip_limit(self):
        """Section at 80% or above is marked as near_limit."""
        section = _make_section("Dev", wip_limit=5)
        tasks = [
            _make_task(f"Task {i}", section, TaskStatus.IN_PROGRESS)
            for i in range(4)  # 4/5 = 80%
        ]
        board = Board(tasks=tasks)

        result = calculate_wip_metrics(board)
        wip = result[0]

        assert wip.active_tasks == 4
        assert math.isclose(wip.utilization, 0.8)
        assert wip.is_near_limit is True
        assert wip.is_over_limit is False

    def test_section_over_wip_limit(self):
        """Section exceeding WIP limit is marked as over_limit."""
        section = _make_section("Dev", wip_limit=3)
        tasks = [
            _make_task(f"Task {i}", section, TaskStatus.OPEN)
            for i in range(5)
        ]
        board = Board(tasks=tasks)

        result = calculate_wip_metrics(board)
        wip = result[0]

        assert wip.active_tasks == 5
        assert wip.wip_limit == 3
        assert wip.remaining_capacity == 0
        assert math.isclose(wip.utilization, 5 / 3)
        assert wip.is_near_limit is True
        assert wip.is_over_limit is True

    def test_archived_tasks_are_ignored(self):
        """Archived tasks do not count towards WIP."""
        section = _make_section("Dev", wip_limit=3)
        tasks = [
            _make_task("Active", section, TaskStatus.OPEN),
            _make_task("Archived", section, TaskStatus.OPEN, archived=True),
        ]
        board = Board(tasks=tasks)

        result = calculate_wip_metrics(board)
        wip = result[0]

        assert wip.active_tasks == 1

    def test_non_active_statuses_are_ignored(self):
        """Only OPEN and IN_PROGRESS count as active for WIP."""
        section = _make_section("Dev", wip_limit=5)
        tasks = [
            _make_task("Open", section, TaskStatus.OPEN),
            _make_task("In Progress", section, TaskStatus.IN_PROGRESS),
            _make_task("Completed", section, TaskStatus.COMPLETED),
            _make_task("Cancelled", section, TaskStatus.CANCELLED),
            _make_task("Delegated", section, TaskStatus.DELEGATED),
            _make_task("Scheduled", section, TaskStatus.SCHEDULED),
            _make_task("Paused", section, TaskStatus.PAUSED),
        ]
        board = Board(tasks=tasks)

        result = calculate_wip_metrics(board)
        wip = result[0]

        assert wip.active_tasks == 2  # Only OPEN + IN_PROGRESS

    def test_multiple_sections(self):
        """Multiple sections with WIP limits are calculated independently."""
        dev = _make_section("Dev", wip_limit=3)
        review = _make_section("Review", wip_limit=2)
        backlog = _make_section("Backlog")  # No WIP limit

        tasks = [
            _make_task("Dev 1", dev, TaskStatus.OPEN),
            _make_task("Dev 2", dev, TaskStatus.IN_PROGRESS),
            _make_task("Review 1", review, TaskStatus.OPEN),
            _make_task("Backlog 1", backlog, TaskStatus.OPEN),
        ]
        board = Board(tasks=tasks)

        result = calculate_wip_metrics(board)

        # Backlog has no wip_limit, so only Dev and Review
        assert len(result) == 2

        by_name = {w.section_name: w for w in result}

        assert by_name["Dev"].active_tasks == 2
        assert by_name["Dev"].wip_limit == 3
        assert by_name["Dev"].is_over_limit is False

        assert by_name["Review"].active_tasks == 1
        assert by_name["Review"].wip_limit == 2
        assert by_name["Review"].is_over_limit is False

    def test_zero_wip_limit(self):
        """Section with wip_limit=0 handles division by zero."""
        section = _make_section("Blocked", wip_limit=0)
        task = _make_task("Task", section, TaskStatus.OPEN)
        board = Board(tasks=[task])

        result = calculate_wip_metrics(board)
        wip = result[0]

        assert wip.active_tasks == 1
        assert wip.wip_limit == 0
        assert wip.utilization == 0.0  # Guard against division by zero
        assert wip.is_over_limit is True  # 1 > 0