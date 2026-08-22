"""Determinism tests for ExecutionReport.

These tests verify that identical inputs produce identical analytical outputs,
ensuring that the analytics pipeline is fully deterministic.

Note: Metadata fields like `report_id` and `generated_at` are intentionally
excluded from determinism checks as they are report instance identifiers,
not analytical content (per EXECUTION_REPORT_ARCHITECTURE.md Section 7.4).
"""

from datetime import date

from src.analytics.service import generate_execution_report
from src.parser.models import SectionType, TaskStatus
from tests.helper import create_section, create_task, create_board


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

    return create_board(tasks=tasks)


def test_execution_report_determinism():
    """Identical board + identical analysis_date → identical analytical content.

    The `report_id` and `generated_at` fields are intentionally NOT compared
    because they are per-instance metadata (UUID + timestamp), not analytics.
    """
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, analysis_date)

    # --- Metadata differs (expected) ---
    assert report1.report_id != report2.report_id, (
        "Each report must get a unique UUID"
    )

    # --- Analytical content must be identical ---
    assert report1.analysis_date == report2.analysis_date
    assert report1.schema_version == report2.schema_version
    assert report1.board_health == report2.board_health
    assert report1.executive_summary == report2.executive_summary


def test_board_health_deep_determinism():
    """All fields of board_health must be deterministic."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, analysis_date)

    bh1 = report1.board_health
    bh2 = report2.board_health

    assert bh1.total_tasks == bh2.total_tasks
    assert bh1.score_coverage == bh2.score_coverage
    assert bh1.tag_coverage == bh2.tag_coverage
    assert bh1.analytics_coverage == bh2.analytics_coverage
    assert bh1.missing_score == bh2.missing_score
    assert bh1.missing_tag == bh2.missing_tag
    assert bh1.orphan_tasks == bh2.orphan_tasks
    assert bh1.sample_orphans == bh2.sample_orphans
    assert bh1.status == bh2.status


def test_executive_summary_determinism():
    """ExecutiveSummary must be deterministic."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, analysis_date)

    assert report1.executive_summary == report2.executive_summary
    assert report1.executive_summary.summary == report2.executive_summary.summary


def test_analysis_date_is_preserved():
    """The injected analysis_date must be stored in the report as-is."""
    board = _create_sample_board()
    analysis_date = date(2026, 3, 15)

    report = generate_execution_report(board, analysis_date)

    assert report.analysis_date == analysis_date
    assert report.analysis_date == date(2026, 3, 15)


def test_default_analysis_date_uses_today():
    """When analysis_date is None, today's date must be used."""
    board = _create_sample_board()

    report = generate_execution_report(board, None)

    assert report.analysis_date == date.today()


def test_no_analysis_date_argument_uses_today():
    """When analysis_date is omitted, today's date must be used."""
    board = _create_sample_board()

    report = generate_execution_report(board)

    assert report.analysis_date == date.today()


def test_report_id_is_unique_per_call():
    """Each call to generate_execution_report must produce a unique report_id."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, analysis_date)
    report3 = generate_execution_report(board, analysis_date)

    ids = {report1.report_id, report2.report_id, report3.report_id}
    assert len(ids) == 3, "All three report_ids must be unique"

    # UUID format check
    for report in (report1, report2, report3):
        assert len(report.report_id) == 36
        assert report.report_id.count("-") == 4


def test_schema_version_is_stable():
    """schema_version must be consistent across all reports."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report1 = generate_execution_report(board, analysis_date)
    report2 = generate_execution_report(board, date(2026, 2, 20))

    assert report1.schema_version == "1.0"
    assert report2.schema_version == "1.0"


def test_different_analysis_dates_affect_report():
    """Different analysis_dates must produce distinguishable reports.

    The same board analyzed on different dates should yield reports with
    different `analysis_date` fields. Board health may also differ if
    time-dependent calculations are involved (e.g., overdue tasks).
    """
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

    report_before = generate_execution_report(board, date(2025, 12, 15))
    report_after = generate_execution_report(board, date(2026, 1, 15))

    # analysis_date must differ
    assert report_before.analysis_date != report_after.analysis_date

    # total_tasks must be the same (same board)
    assert (
        report_before.board_health.total_tasks
        == report_after.board_health.total_tasks
    )


def test_generated_at_is_set():
    """generated_at must be a valid datetime."""
    from datetime import datetime

    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    assert isinstance(report.generated_at, datetime)
    # generated_at should be close to now
    assert (datetime.now() - report.generated_at).total_seconds() < 5


def test_report_is_frozen():
    """ExecutionReport must be immutable (frozen dataclass)."""
    import pytest
    from dataclasses import FrozenInstanceError

    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    # Using setattr bypasses Pylance static analysis,
    # but still triggers FrozenInstanceError at runtime.
    with pytest.raises(FrozenInstanceError):
        setattr(report, "analysis_date", date(2099, 1, 1))


def test_report_is_hashable():
    """Frozen dataclasses must be hashable (usable in sets/dicts)."""
    board = _create_sample_board()
    analysis_date = date(2026, 1, 15)

    report = generate_execution_report(board, analysis_date)

    # Should not raise
    hash(report)

    # Should be usable in a set
    report_set = {report}
    assert report in report_set