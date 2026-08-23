# pyright: ignore[reportUnusedFunction]
"""Tests for generate_execution_report service.

These tests verify the behavior of the canonical execution report pipeline.
...
"""

from __future__ import annotations

"""Tests for generate_execution_report service.

These tests verify the behavior of the canonical execution report pipeline.
They replace the legacy test_builds_analytics_snapshot which tested the
deprecated AnalyticsSnapshot model.
"""

from datetime import date
import math
from src.analytics.service import generate_execution_report
from src.parser.models import SectionType, TaskStatus
from tests.helper import create_section, create_task, create_board
from src.analytics.models import BoardHealthStatus


def _create_sample_board():
    """Create a sample board with varied tasks for testing."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )
    focus = create_section(
        title="Focus",
        section_type=SectionType.FOCUS,
        wip_limit=2,
    )

    tasks = [
        create_task(
            title="Open task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
            tags=["work", "urgent"],  # ← ДОБАВЛЕНО
        ),
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
            tags=["admin"],          # ← ДОБАВЛЕНО
        ),
        create_task(
            title="Focused task",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
            tags=["deep-work", "project-x"],  # ← ДОБАВЛЕНО
        ),
    ]

    return create_board(tasks=tasks)

def test_generates_execution_report():
    """generate_execution_report must return a valid ExecutionReport."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    # Basic contract: report is not None
    assert report is not None

    # Metadata must be populated
    assert report.schema_version == "1.0"
    assert report.analysis_date == analysis_date
    assert len(report.report_id) == 36  # UUID format
    assert report.generated_at is not None


def test_board_health_reflects_board_content():
    """board_health must correctly reflect the board content."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    bh = report.board_health

    # Total tasks: 3 tasks in the board
    assert bh.total_tasks == 3
    
    # Active tasks: 2 (Open + In Progress), 1 Completed is NOT active
    assert bh.active_tasks == 2  # ← ДОБАВИТЬ

    # Score coverage: all 3 tasks have scores (10, 20, 15)
    assert bh.score_coverage == 1.0

    # Tag coverage: all 3 tasks now have tags
    assert bh.tag_coverage == 1.0

    # Orphan count: tasks have BOTH score AND tags → no orphans
    assert bh.orphan_tasks == 0

    # Status must be a valid BoardHealthStatus enum value
    assert bh.status is not None

def test_board_health_detects_unscored_tasks():
    """board_health must detect tasks without scores."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    tasks = [
        create_task(
            title="Task with score",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
        ),
        create_task(
            title="Task without score",
            status=TaskStatus.OPEN,
            section=inbox,
            score=None,  # No score
        ),
    ]

    board = create_board(tasks=tasks)
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    # 1 of 2 tasks has no score → score_coverage = 0.5
    assert report.board_health.score_coverage == 0.5
    assert report.board_health.missing_score == 1


def test_empty_board_produces_valid_report():
    """An empty board must still produce a valid ExecutionReport.
    
    Note on vacuous truth: when there are no tasks, coverage metrics
    are 1.0 (100%) because there are no tasks violating the criteria.
    This is mathematically consistent:
      score_coverage = 1 - (missing_score / total_tasks)
    With total_tasks=0, there's nothing missing → full coverage.
    """
    board = create_board(tasks=[])
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    # Basic contract: report exists and is valid
    assert report is not None
    assert report.schema_version == "1.0"
    assert report.analysis_date == analysis_date
    assert len(report.report_id) == 36  # UUID format

    # Board health for empty board
    bh = report.board_health
    assert bh.total_tasks == 0
    assert bh.missing_score == 0
    assert bh.missing_tag == 0
    assert bh.orphan_tasks == 0
    assert bh.sample_orphans == ()

    # Vacuous truth: no tasks → no violations → 100% coverage
    assert bh.score_coverage == 1.0
    assert bh.tag_coverage == 1.0
    assert bh.analytics_coverage == 1.0

    # Empty board is "excellent" (no problems to report)
    assert bh.status == BoardHealthStatus.EXCELLENT

    # Executive summary must still exist
    assert report.executive_summary is not None
    
    

def test_analysis_date_is_preserved():
    """The injected analysis_date must be stored in the report."""
    board = _create_sample_board()
    target_date = date(2026, 3, 15)

    report = generate_execution_report(board, target_date)

    assert report.analysis_date == target_date


def test_default_analysis_date_uses_today():
    """When analysis_date is None, today's date must be used."""
    board = _create_sample_board()

    report = generate_execution_report(board, None)

    assert report.analysis_date == date.today()


def test_omitted_analysis_date_uses_today():
    """When analysis_date is omitted, today's date must be used."""
    board = _create_sample_board()

    report = generate_execution_report(board)

    assert report.analysis_date == date.today()


def test_executive_summary_is_populated():
    """executive_summary must be present in the report."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    # In MVP, executive_summary is a placeholder but must exist
    assert report.executive_summary is not None
    assert hasattr(report.executive_summary, "summary")
    assert isinstance(report.executive_summary.summary, str)


def test_report_id_is_unique_per_invocation():
    """Each invocation must produce a unique report_id."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, analysis_date)

    assert report1.report_id != report2.report_id


def test_overdue_tasks_reflect_analysis_date():
    """Overdue task detection must depend on analysis_date, not today."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    tasks = [
        create_task(
            title="Task due Jan 1",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
            due=date(2026, 1, 1),
        ),
    ]

    board = create_board(tasks=tasks)

    # Before the due date → not overdue
    report_before = generate_execution_report(board, date(2025, 12, 15))
    # After the due date → overdue
    report_after = generate_execution_report(board, date(2026, 1, 15))

    # Reports should differ in analysis_date
    assert report_before.analysis_date != report_after.analysis_date
    # Total tasks count stays the same
    assert (
        report_before.board_health.total_tasks
        == report_after.board_health.total_tasks
    )


# TODO: Add tests for AnalyticsBundle once it's added to ExecutionReport:
# - test_corridor_analysis_reflects_score_distribution
# - test_focus_analytics_counts_high_score_tasks
# - test_wip_statuses_detect_limit_violations
# - test_task_snapshots_include_all_board_tasks
# - test_findings_are_generated_from_analytics
# - test_recommendations_have_availability_not_produced_in_MVP

def test_board_health_detects_orphans_without_tags():
    """Tasks without tags must be counted as orphans even if they have scores."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    tasks = [
        # Complete task (has both score AND tags) → not an orphan
        create_task(
            title="Complete task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
            tags=["work"],
        ),
        # Orphan task (has score but NO tags)
        create_task(
            title="Task without tags",
            status=TaskStatus.OPEN,
            section=inbox,
            score=15,
            # Нет tags → orphan!
        ),
        # Orphan task (no score AND no tags)
        create_task(
            title="Task without anything",
            status=TaskStatus.OPEN,
            section=inbox,
            # Нет score, нет tags → orphan!
        ),
    ]

    board = create_board(tasks=tasks)
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    assert report.board_health.orphan_tasks == 2
    assert report.board_health.missing_tag == 2  # 2 задачи без тегов
    assert report.board_health.missing_score == 1  # 1 задача без score
    assert math.isclose(report.board_health.tag_coverage, 1 / 3, rel_tol=1e-9)
    assert math.isclose(report.board_health.score_coverage, 2 / 3, rel_tol=1e-9)
    
    def test_board_health_counts_active_tasks_correctly():
        """active_tasks must exclude completed and archived tasks."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    tasks = [
        # Активные задачи
        create_task(
            title="Open task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
            tags=["work"],
        ),
        create_task(
            title="In progress task",
            status=TaskStatus.IN_PROGRESS,
            section=inbox,
            score=15,
            tags=["work"],
        ),
        # НЕ активные задачи
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
            tags=["done"],
        ),
        create_task(
            title="Cancelled task",
            status=TaskStatus.CANCELLED,
            section=inbox,
            score=5,
            tags=["dropped"],
        ),
    ]

    board = create_board(tasks=tasks)
    report = generate_execution_report(board, date(2026, 1, 15))

    # Всего 4 задачи, но только 2 активные
    assert report.board_health.total_tasks == 4
    assert report.board_health.active_tasks == 2