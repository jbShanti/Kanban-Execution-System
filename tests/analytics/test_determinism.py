"""Determinism tests for analytics snapshot and report.

These tests verify that identical inputs produce identical outputs,
ensuring that the analytics pipeline is fully deterministic.
"""

from datetime import date, datetime, timezone

from src.analytics.service import (
    build_analytics_snapshot,
    generate_analytics_report,
)
from src.analytics.report_builder import build_analytics_report
from src.parser.models import (
    SectionType,
    TaskStatus,
)
from tests.helper import create_section, create_task, create_board


def test_snapshot_determinism():
    """Test that identical board and analysis_date produce identical snapshots."""
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
        ),
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
        ),
        create_task(
            title="Focused task",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
        ),
    ]

    board = create_board(tasks=tasks)
    analysis_date = date(2026, 1, 15)

    snapshot1 = build_analytics_snapshot(board, analysis_date)
    snapshot2 = build_analytics_snapshot(board, analysis_date)

    # Compare all relevant fields
    assert snapshot1.summary.total_tasks == snapshot2.summary.total_tasks
    assert snapshot1.summary.active_tasks == snapshot2.summary.active_tasks
    assert snapshot1.summary.completed_tasks == snapshot2.summary.completed_tasks
    assert snapshot1.summary.total_score == snapshot2.summary.total_score
    assert snapshot1.summary.overdue_tasks == snapshot2.summary.overdue_tasks
    assert snapshot1.summary.scored_tasks == snapshot2.summary.scored_tasks
    assert snapshot1.summary.unscored_tasks == snapshot2.summary.unscored_tasks
    assert snapshot1.summary.by_status == snapshot2.summary.by_status
    assert snapshot1.summary.sections.keys() == snapshot2.summary.sections.keys()

    for section_name in snapshot1.summary.sections:
        s1 = snapshot1.summary.sections[section_name]
        s2 = snapshot2.summary.sections[section_name]
        assert s1.total_tasks == s2.total_tasks
        assert s1.active_tasks == s2.active_tasks
        assert s1.completed_tasks == s2.completed_tasks
        assert s1.total_score == s2.total_score

    assert snapshot1.board.total_tasks == snapshot2.board.total_tasks
    assert snapshot1.board.active_tasks == snapshot2.board.active_tasks
    assert snapshot1.board.completed_tasks == snapshot2.board.completed_tasks
    assert snapshot1.board.total_score == snapshot2.board.total_score

    assert snapshot1.sections.keys() == snapshot2.sections.keys()
    for section_name in snapshot1.sections:
        m1 = snapshot1.sections[section_name]
        m2 = snapshot2.sections[section_name]
        assert m1.total_tasks == m2.total_tasks
        assert m1.active_tasks == m2.active_tasks
        assert m1.total_score == m2.total_score

    assert snapshot1.board_health.total_tasks == snapshot2.board_health.total_tasks
    assert snapshot1.board_health.score_coverage == snapshot2.board_health.score_coverage
    assert snapshot1.board_health.tag_coverage == snapshot2.board_health.tag_coverage
    assert snapshot1.board_health.analytics_coverage == snapshot2.board_health.analytics_coverage
    assert snapshot1.board_health.status == snapshot2.board_health.status


def test_report_determinism():
    """Test that identical snapshot and generated_at produce identical reports."""
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
        ),
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
        ),
        create_task(
            title="Focused task",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
        ),
    ]

    board = create_board(tasks=tasks)
    analysis_date = date(2026, 1, 15)
    generated_at = datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

    snapshot1 = build_analytics_snapshot(board, analysis_date)
    snapshot2 = build_analytics_snapshot(board, analysis_date)

    report1 = build_analytics_report(snapshot1, generated_at)
    report2 = build_analytics_report(snapshot2, generated_at)

    assert report1.global_score == report2.global_score
    assert report1.total_tasks == report2.total_tasks
    assert report1.scored_tasks == report2.scored_tasks
    assert report1.high_value_tasks == report2.high_value_tasks
    assert report1.high_value_percentage == report2.high_value_percentage
    assert report1.focus_tasks == report2.focus_tasks
    assert report1.focus_percentage == report2.focus_percentage
    assert report1.generated_at == report2.generated_at
    assert report1.generated_at == generated_at
    assert report1.board_health == report2.board_health

    assert len(report1.corridors) == len(report2.corridors)
    for c1, c2 in zip(report1.corridors, report2.corridors):
        assert c1.name == c2.name
        assert c1.task_count == c2.task_count
        assert c1.total_score == c2.total_score
        assert c1.average_score == c2.average_score
        assert c1.percentage == c2.percentage
        assert c1.score_share_percentage == c2.score_share_percentage


def test_generate_analytics_report_determinism():
    """Test that the full pipeline is deterministic."""
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
        ),
        create_task(
            title="Completed task",
            status=TaskStatus.COMPLETED,
            section=inbox,
            score=20,
        ),
        create_task(
            title="Focused task",
            status=TaskStatus.IN_PROGRESS,
            section=focus,
            score=15,
        ),
    ]

    board = create_board(tasks=tasks)
    analysis_date = date(2026, 1, 15)
    generated_at = datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)

    report1 = generate_analytics_report(board, analysis_date, generated_at)
    report2 = generate_analytics_report(board, analysis_date, generated_at)

    assert report1.global_score == report2.global_score
    assert report1.total_tasks == report2.total_tasks
    assert report1.scored_tasks == report2.scored_tasks
    assert report1.generated_at == report2.generated_at
    assert report1.generated_at == generated_at
    assert report1.board_health == report2.board_health


def test_different_analysis_dates_produce_different_results():
    """Test that different analysis dates produce different results (when relevant)."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    tasks = [
        create_task(
            title="Overdue task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
            due=date(2026, 1, 1),
        ),
        create_task(
            title="Future task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=20,
            due=date(2026, 12, 31),
        ),
    ]

    board = create_board(tasks=tasks)

    # Analysis date before the overdue task's due date
    snapshot1 = build_analytics_snapshot(board, date(2025, 12, 15))
    # Analysis date after the overdue task's due date
    snapshot2 = build_analytics_snapshot(board, date(2026, 1, 15))

    # The overdue count should differ
    assert snapshot1.summary.overdue_tasks != snapshot2.summary.overdue_tasks
    assert snapshot1.summary.overdue_tasks == 0
    assert snapshot2.summary.overdue_tasks == 1


def test_different_generated_at_produces_different_report_timestamp():
    """Test that different generated_at values produce different report timestamps."""
    inbox = create_section(
        title="Inbox",
        section_type=SectionType.INBOX,
    )

    tasks = [
        create_task(
            title="Task",
            status=TaskStatus.OPEN,
            section=inbox,
            score=10,
        ),
    ]

    board = create_board(tasks=tasks)
    analysis_date = date(2026, 1, 15)

    snapshot = build_analytics_snapshot(board, analysis_date)

    generated_at1 = datetime(2026, 1, 15, 10, 0, 0, tzinfo=timezone.utc)
    generated_at2 = datetime(2026, 1, 15, 11, 0, 0, tzinfo=timezone.utc)

    report1 = build_analytics_report(snapshot, generated_at1)
    report2 = build_analytics_report(snapshot, generated_at2)

    # The generated_at should differ
    assert report1.generated_at != report2.generated_at
    assert report1.generated_at == generated_at1
    assert report2.generated_at == generated_at2

    # But the rest of the report should be identical
    assert report1.global_score == report2.global_score
    assert report1.total_tasks == report2.total_tasks
    assert report1.corridors == report2.corridors